import os, random, json, asyncio, datetime
from PIL import Image, ImageDraw
import edge_tts

# --- 1. CYBER SECURITY TOPICS - Roz Naya Fraud + Solution ---
TOPICS = [
    "OTP Fraud: OTP maangne wala call aaye to kya kare",
    "UPI Fraud: QR code scan karne se paisa kaise kat jata hai",
    "KYC Fraud: Bank se bolke account band hone wala SMS",
    "Job Fraud: Ghar baithe job ke naam pe paise maangna",
    "Lottery Fraud: Aap jeet gaye 25 Lakh wala SMS",
    "WhatsApp Hack: OTP share karne se WhatsApp hack kaise hota hai",
    "Link Fraud: Parcel delivery wala fake link",
    "Customer Care Fraud: Google se fake number nikalna",
    "Investment Fraud: Double paisa wala Telegram group",
    "Aadhaar Fraud: Aadhaar OTP se SIM kaise nikal lete hai",
    "Screen Sharing Fraud: AnyDesk download karane wala scam",
    "Electricity Bill Fraud: Bijli katne wala SMS",
    "Facebook Hack: Friend ke naam se paisa maangna",
    "ATM Fraud: ATM me card phasne wala fraud",
    "WiFi Fraud: Free WiFi se data kaise chori hota hai",
    "PAN Card Fraud: PAN se loan kaise le lete hai",
    "Instagram Fraud: Blue tick ke naam pe paise maangna",
    "Loan App Fraud: 5000 ka loan 50000 kaise ban jata hai",
    "Video Call Fraud: Nude video call blackmail se kaise bache",
    "QR Code Fraud: Dukaan pe QR badal dena",
    "Sim Swap Fraud: SIM band hona = bada khatra",
    "Fake Police Call: Digital Arrest wala naya fraud",
    "OLX Fraud: Army wala buyer ban ke thagna",
    "Captcha Fraud: Work from home typing job wala fraud",
    "Fake SBI Call: Account verify karne wala call",
    "UPI Collect Request Fraud: Paise aane ki jagah katna",
    "Play Store Fraud: Nakli app se bank khali",
    "YouTube Earning Fraud: Paise deke subscriber badhana",
    "Ransomware: Phone lock hone pe kya kare",
    "Password Hack: Ek hi password sab jagah rakhna",
]

# Aaj ka topic - date se choose hoga taaki repeat na ho
today = datetime.date.today()
topic = TOPICS[today.toordinal() % len(TOPICS)]
print(f"Today Topic: {topic}")

# --- 2. VIRAL SCRIPT - Cyber Awareness 50-60 Sec ---
def get_viral_script(topic):
    try:
        from google import genai
        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        prompt = f"""
        You are a Cyber Security Awareness Shorts writer for India.
        Topic: {topic}
        Write a 55 second Hindi script in Hinglish, simple language for common people.
        Structure:
        1. Start with RUKO! Ye naya fraud chal raha hai...
        2. Ek chhota sa example batao ki fraud kaise hota hai - 15 sec
        3. Phir 3 clear solution / bachne ke tarike batao - 30 sec
        4. End me bolo: Agar aisa call aaye to turant 1930 pe call karo, aur video share karo taaki sab bach sake.
        Keep tone serious but helpful, not scary. No fake promises.
        Only give script, no extra text. 130-150 words max.
        """
        res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return res.text.strip()
    except Exception as e:
        print(f"Gemini fail, backup: {e}")
        return f"RUKO! Ye naya fraud chal raha hai - {topic}. Isme chor aapko dara ke ya lalach deke OTP ya link bhejta hai. Yaad rakho, pehla - Bank kabhi OTP nahi maangta. Dusra - Kisi bhi anjaan link pe click mat karo. Teesra - Koi QR scan karne se paisa nahi aata, paisa kat ta hai. Agar aisa call aaye to turant 1930 pe call karo. Ye video apne parivaar ko bhej do taaki wo bach sake. Follow karo Fixzology ko roz naye fraud se bachne ke liye."

script_text = get_viral_script(topic)
print(script_text)

# --- 3. VOICEOVER - Ladke ki awaaz, thodi slow taaki samajh aaye ---
async def make_voice():
    communicate = edge_tts.Communicate(script_text, "hi-IN-MadhurNeural", rate="+5%")
    await communicate.save("voice.mp3")
asyncio.run(make_voice())

# --- 4. VIDEO BANANA ---
from moviepy import AudioFileClip, TextClip, CompositeVideoClip, ColorClip
import textwrap

audio = AudioFileClip("voice.mp3")
duration = max(50, min(62, audio.duration + 1))
print(f"Video Duration: {duration} sec")

# Background - Dark Red/Black Cyber Theme
bg = ColorClip(size=(1080, 1920), color=(15, 0, 0), duration=duration)

title_clip = TextClip(
    font="DejaVu-Sans-Bold",
    text="RUKO! YE NAYA FRAUD HAI! ⚠️",
    font_size=80, color="yellow",
    size=(950, None), method="caption"
).with_position(("center", 180)).with_duration(duration)

topic_clip = TextClip(
    font="DejaVu-Sans",
    text="\n".join(textwrap.wrap(topic, width=28)),
    font_size=58, color="white",
    size=(900, None), method="caption"
).with_position(("center", 750)).with_duration(duration)

cta_clip = TextClip(
    font="DejaVu-Sans-Bold",
    text="1930 PE CALL KARO\nShare Karo - Sabko Bachao 👇\nFollow @ Fixzology",
    font_size=62, color="white",
    size=(900, None), method="caption", bg_color="red"
).with_position(("center", 1480)).with_duration(duration)

final = CompositeVideoClip([bg, title_clip, topic_clip, cta_clip])
final = final.with_audio(audio)
final.write_videofile("short.mp4", fps=24, codec="libx264", audio_codec="aac")

# --- 5. THUMBNAIL ---
img = Image.new("RGB", (1080, 1920), (180, 0, 0))
d = ImageDraw.Draw(img)
d.text((80, 600), "CYBER\nFRAUD!", fill=(255,255,255))
d.text((80, 1000), "BACH KE\nRAHO!", fill=(255,255,0))
d.text((80, 1400), "1930 PE CALL KARO", fill=(255,255,255))
img.save("thumbnail.jpg")

# --- 6. UPLOAD INFO SAVE KARNA ---
title = f"Ye Naya Fraud Chal Raha Hai! 😱 {topic} | Bachne Ka Tarika | Fixzology"
description = f"""{title}

{script_text}

⚠️ Agar aapke saath fraud ho jaye to turant:
1. 1930 (National Cyber Helpline) pe call karo
2. cybercrime.gov.in pe complaint karo
3. Bank ko turant inform karo

Ye video apne Mummy-Papa aur Dosto ko zaroor bhejo, taaki wo is fraud se bach sake!

Roz naya Fraud + Solution ke liye Follow karo!

#CyberSecurity #OnlineFraud #Fixzology #CyberCrime #FraudAlert #1930 #Awareness
"""
with open("upload_info.json", "w", encoding="utf-8") as f:
    json.dump({"title": title, "description": description, "topic": topic, "tags": ["cyber security", "online fraud", "fraud se kaise bache", "cyber awareness hindi", "1930 helpline", "upi fraud", "otp fraud", "fixzology"]}, f, ensure_ascii=False)

print("DONE! Video ban gaya - short.mp4")
