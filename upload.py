import json, os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

with open("upload_info.json", encoding="utf-8") as f:
    info = json.load(f)

# --- FIX: Token me agar Enter / Space aa gaya ho to saaf karo ---
raw_token = os.environ["YOUTUBE_TOKEN_JSON"].strip()
# Agar token me asli newline hai to usko hata do
try:
    token_data = json.loads(raw_token, strict=False)
except:
    # Double escaping fix
    token_data = json.loads(raw_token.encode().decode('unicode_escape'), strict=False)

print(f"Token loaded OK for: {token_data.get('client_id','')[:20]}...")

creds = Credentials.from_authorized_user_info(token_data, scopes=["https://www.googleapis.com/auth/youtube.upload"])
youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": info["title"][:100],
            "description": info["description"],
            "tags": info["tags"],
            "categoryId": "27",
            "defaultLanguage": "hi",
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    },
    media_body=MediaFileUpload("short.mp4", chunksize=-1, resumable=True)
)
res = request.execute()
print(f"UPLOADED! Video ID: {res['id']}")

youtube.thumbnails().set(videoId=res['id'], media_body=MediaFileUpload("thumbnail.jpg")).execute()
print("Thumbnail lag gaya!")
