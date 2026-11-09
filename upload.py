import json, os, random
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

with open("upload_info.json", encoding="utf-8") as f:
    info = json.load(f)

# --- FIX: Token me agar Enter / Space aa gaya ho to saaf karo ---
raw_token = os.environ["YOUTUBE_TOKEN_JSON"].strip()
try:
    token_data = json.loads(raw_token, strict=False)
except:
    # Double escaping fix
    token_data = json.loads(raw_token.encode().decode('unicode_escape'), strict=False)

print(f"Token loaded OK for: {token_data.get('client_id','')[:20]}...")

creds = Credentials.from_authorized_user_info(token_data, scopes=["https://www.googleapis.com/auth/youtube.upload"])
youtube = build("youtube", "v3", credentials=creds)

# --- SEO DESCRIPTION BUILDER ---
base_desc = info["description"]

seo_hashtags = "\n\n#CyberSecurity #CyberAttack #FraudAlert #OnlineFraud #HackingNews #TechNews #NewLaunch #AIScam #DigitalIndia #StaySafeOnline #ViralShorts #Trending #HindiTech #KrishTech"

seo_footer = "\n\n⚠️ Aise hi naye Fraud, Hacking News aur New Launch ke liye Subscribe karo - Gemini-with-krish\n\nDisclaimer: Ye video sirf jaankari aur awareness ke liye hai."

full_description = base_desc + seo_footer + seo_hashtags

# --- SEO TAGS ---
extra_tags = ["cyber security", "fraud alert", "online fraud", "hacking news", "tech news hindi", "new launch", "cyber attack", "ai scam", "stay safe online", "digital fraud"]
all_tags = list(dict.fromkeys(info.get("tags", []) + extra_tags))[:30]

# --- HOOK WALE TITLE KO AUR STRONG KARO ---
title = info["title"][:100]

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": title,
            "description": full_description,
            "tags": all_tags,
            "categoryId": "28",
            "defaultLanguage": "hi",
        },
        "status": {"privacyStatus": "unlisted", "selfDeclaredMadeForKids": False}
    },
    media_body=MediaFileUpload("short.mp4", chunksize=-1, resumable=True)
)
res = request.execute()
print(f"UPLOADED! Video ID: {res['id']}")

youtube.thumbnails().set(videoId=res['id'], media_body=MediaFileUpload("thumbnail.jpg")).execute()
print("Thumbnail lag gaya!")
