import os, json, shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# bg.png ko hi thumbnail bana do - automation.py ko chhedna nahi hai
if not os.path.exists("thumbnail.jpg"):
    if os.path.exists("bg.png"):
        # bg.png ko thumbnail.jpg me copy karo
        from PIL import Image
        img = Image.open("bg.png")
        img = img.convert("RGB")
        img.save("thumbnail.jpg", "JPEG")
        print("Thumbnail ban gaya bg.png se")
    else:
        print("bg.png bhi nahi mila, thumbnail skip")

with open("upload_info.json", encoding="utf-8") as f:
    info = json.load(f)

token_info = json.loads(os.environ["YOUTUBE_TOKEN_JSON"])
creds = Credentials.from_authorized_user_info(token_info)
youtube = build("youtube", "v3", credentials=creds)

print("Uploading short.mp4...")
req = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": info["title"],
            "description": info["description"],
            "tags": info["tags"],
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public",
            "madeForKids": False,
            "selfDeclaredMadeForKids": False
        }
    },
    media_body=MediaFileUpload("short.mp4", chunksize=-1, resumable=True)
)
res = req.execute()
video_id = res["id"]
print(f"UPLOADED! Video ID: {video_id}")

# Thumbnail lagao - agar hai to
if os.path.exists("thumbnail.jpg"):
    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload("thumbnail.jpg")
        ).execute()
        print("Thumbnail lag gaya!")
    except Exception as e:
        print(f"Thumbnail fail, par video upload ho gaya: {e}")
else:
    print("Thumbnail nahi mila, video bina thumbnail ke upload hua")

print("DONE! ALL FINISHED")
