import os
import json
import asyncio
import edge_tts
import google.generativeai as genai
from moviepy import ImageClip, AudioFileClip

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# 1. Gemini AI को टेक नीश के लिए सेट करना
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0falsh")

prompt = """
तुम भारत के शीर्ष टेक और AI क्रिएटर हो। 
किसी एक अनोखे, उपयोगी और नए AI टूल या फ्यूचर टेक फैक्ट पर 40-45 सेकंड की YouTube Shorts स्क्रिप्ट लिखो।
शुरुआत में एक जबरदस्त हुक होना चाहिए।
केवल शुद्ध JSON आउटपुट दो:
{
  "title": "आकर्षक टेक टाइटल #shorts #aitools #tech",
  "description": "इस वीडियो में एक अनोखे AI टूल के बारे में बताया गया है। #ai #tech #shorts",
  "tags": ["AI Tools", "Technology", "Free AI", "Tech Shorts"],
  "script": "वॉइसओवर के लिए सरल और ऊर्जावान हिंदी स्क्रिप्ट।"
}
"""
response = model.generate_content(prompt)
clean_text = response.text.replace("```json", "").replace("```", "").strip()
data = json.loads(clean_text)

# 2. प्राकृतिक हिंदी आवाज़ तैयार करना (Edge-TTS)
async def make_audio():
    comm = edge_tts.Communicate(data["script"], voice="hi-IN-MadhurNeural")
    await comm.save("voice.mp3")

asyncio.run(make_audio())

# 3. इमेज और आवाज़ जोड़कर वीडियो तैयार करना
audio = AudioFileClip("voice.mp3")
video = ImageClip("avatar.png").set_duration(audio.duration).set_audio(audio)
video.write_videofile("shorts.mp4", fps=24, codec="libx264", audio_codec="aac")

# 4. YouTube पर अपलोड (Science & Technology कैटेगरी)
creds = Credentials.from_authorized_user_info(json.loads(os.environ.get("YOUTUBE_TOKEN_JSON")))
youtube = build("youtube", "v3", credentials=creds)

body = {
    "snippet": {
        "title": data["title"][:100],
        "description": data["description"],
        "tags": data["tags"],
        "categoryId": "28"  # 28 = Science & Technology
    },
    "status": {"privacyStatus": "unlisted"}
}

media = MediaFileUpload("shorts.mp4", mimetype="video/mp4", resumable=True)
youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
print("टेक शॉर्ट्स सफलतापूर्वक अपलोड हो गया!")
