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
    elif os.path.exists("avatar.jpg"):
        # bg nahi hai to avatar hi thumbnail bana do
        from PIL import Image
        img = Image.open("avatar.jpg")
        img = img.convert("RGB")
        img.save("thumbnail.jpg", "JPEG")
        print("Thumbnail ban gaya avatar.jpg se")
    else:
        print("bg.png bhi nahi mila, thumbnail skip")

with open("upload_info.json", encoding="utf-8") as f:
    info = json.load(f)

token_info = json.loads(os.environ["YOUTUBE_TOKEN_JSON"])
creds = Credentials.from_authorized_user_info(token_info)
youtube = build("youtube", "v3", credentials=creds)

# VIDEO KA SAHI NAAM LO - automation.py se jo bana hai
video_file = info.get("video", "short.mp4")
print(f"Uploading {video_file}...")

# Agar videos/ folder wali file hai to usko short.mp4 bana do, ya wahi upload karo
if not os.path.exists(video_file):
    print(f"{video_file} nahi mila, short.mp4 dhoondh raha hu")
    video_file = "short.mp4"

req = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": info["title"],
            "description": info["description"],
            "tags": info.get("tags", ["AI", "Tech", "CyberSecurity", "Hindi"]),
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public",
            "madeForKids": False,
            "selfDeclaredMadeForKids": False
        }
    },
    media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
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
