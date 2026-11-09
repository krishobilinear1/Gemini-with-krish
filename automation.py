import os, json, random, datetime
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, TextClip

HOOKS = [
    ("SAVDHAN! Ye App Chupke Se Paisa Chura Raha Hai", "SAVDHAN!"),
    ("Ye Fraud 99% Logo Ko Nahi Pata", "99% KO NAHI PATA"),
    ("Police Bhi Hairaan! Naya Scam Aa Gaya", "POLICE HAIRAAN"),
    ("New Launch Ne Sabko Hila Diya!", "NEW LAUNCH!"),
    ("Ye Link Khola To Bank Khali!", "LINK MAT KHOLNA"),
    ("Aadhaar Walo Ke Liye Sabse Bada Khatra!", "AADHAAR KHATRA"),
    ("WhatsApp Pe Ye Msg Aaye To Delete Karo", "DELETE KARO!"),
    ("Bank Wala Call Aaye To Ye Mat Bolna", "BANK FRAUD"),
    ("AI Ne Ye Kaand Kar Diya!", "AI KAAND!"),
    ("Ye Trick Sirf Hacker Jante Hain", "HACKER TRICK"),
    ("Raat Ko Sote Time Ye Ho Raha Hai!", "RAAT KA SCAM"),
    ("UPI Se Paisa Bhejte Ho? To Ye Dekho", "UPI FRAUD!"),
    ("Instagram Pe Ye Ladki Asli Nahi Hai!", "FAKE ID!"),
    ("Free Recharge Ke Chakkar Me Lakhon Gaye", "FREE KA DHOKHA"),
    ("Ye Naya AI Phone Sabka Baap Nikla!", "AI PHONE!"),
    ("OTP Kisi Ko Mat Dena, Warna Ye Hoga", "OTP SCAM"),
    ("Ye 1 Setting ON Kar Lo, Hacker Nahi Ghus Payega", "SETTING ON KARO"),
    ("Play Store Se Ye App Abhi Delete Karo!", "DELETE NOW!"),
    ("Ye Video Dekh Ke Dimaag Hil Jayega", "DIMAAG HIL JAYEGA"),
    ("Job Ke Naam Pe Itna Bada Fraud!", "JOB FRAUD"),
    ("WiFi Se Ye Kaam Kiya To Paisa Gaya", "WIFI KHATRA"),
    ("Ye Company Raat-o-Raat Crorepati Kaise Bani?", "SECRET REVEAL"),
    ("Tumhara Phone Hack Hai? Ye 3 Sign Check Karo", "HACK CHECK"),
    ("Ye Naya Feature Aate Hi Sab Pagal Ho Gaye", "NEW FEATURE!"),
    ("Loan App Walo Ka Asli Sach Aa Gaya", "LOAN APP EXPOSED"),
    ("Ye Photo Bheji To Fas Gaye!", "PHOTO FRAUD"),
    ("Google Pe Ye Cheez Kabhi Search Mat Karna", "GOOGLE SECRET"),
    ("Ye Baccha 16 Saal Me Hacker Kaise Ban Gaya?", "16 SAAL KA HACKER"),
    ("Kya Tumhara Data Dark Web Pe Bik Raha Hai?", "DATA LEAK!"),
    ("Is Video Ke Baad Tum Kabhi Fraud Me Nahi Fasoge", "FULL SAFE"),
]

MID_HOOKS = [
    "Ruko ruko, sabse khatarnak wala to abhi baaki hai!",
    "Ye wala sun ke tumhare hosh ud jayenge!",
    "Teesra wala to sabse zyada khatarnak hai, usko miss mat karna!",
    "Aage jo bataunga na, wo 99 percent logo ko nahi pata!",
    "Video ko skip mat karna, aakhri wala point tumhara paisa bachayega!",
]

OUTROS = [
    "Aur haan, aise hi video ke liye Subscribe kar lo, kyunki kal wala video isse bhi zyada khatarnak hoga!",
    "Ek Subscribe to banta hai yaar! Bell icon dabana mat bhoolna, warna agla scam tumko pata bhi nahi chalega!",
    "Video ko us dost ko bhejo jo har link pe click kar deta hai! Aur Subscribe karke hi jaana!",
    "Comment me batao, tumhare saath kabhi aisa hua hai? Subscribe karke hi jaana, warna YouTube ye video phir nahi dikhayega!",
]

def make_bg(thumb_text, filename="bg.png"):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), (10, 10, 30))
    d = ImageDraw.Draw(img)
    # gradient jaisa feel
    for y in range(H):
        r = int(10 + y*0.02)
        g = int(10 + y*0.01)
        b = int(30 + y*0.03)
        d.line([(0, y), (W, y)], fill=(min(r,60), min(g,40), min(b,90)))
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 110)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
    # thumb text - bada peela
    words = thumb_text.split()
    y = 700
    for w in words:
        bbox = d.textbbox((0,0), w, font=font_big)
        tw = bbox[2]-bbox[0]
        d.text(((W-tw)//2, y), w, fill=(255, 220, 0), font=font_big, stroke_width=4, stroke_fill=(0,0,0))
        y += 140
    d.text((W//2-180, y+40), "RUKO! POORA DEKHO!", fill=(255,255,255), font=font_small)
    img.save(filename)
    return filename

def main():
    day = datetime.datetime.now().day
    hook_title, thumb_text = HOOKS[(day-1) % 30]
    mid = random.choice(MID_HOOKS)
    outro = random.choice(OUTROS)

    script = f"""Ruko! Ruko! Ruko! Video ko skip mat karna!
{hook_title}!
Haan bhai, tumne bilkul sahi suna! Abhi abhi jo khabar aayi hai na, usko sunkar mera to dimaag hi hil gaya!
Dekho, aaj kal log itne smart ho gaye hain, unko lagta hai unke saath kabhi fraud nahi ho sakta. Par jo naya tarika aaya hai na, usme to padhe-likhe log bhi fas rahe hain!
Socho, tum aaram se baithe ho, chai pee rahe ho, aur achanak ek message aata hai. Bas, ek click... aur khel khatam!
{mid}
Pehli cheez - Anjaan link pe kabhi click mat karna, chahe wo tumhare dost ke naam se hi kyun na aaya ho!
Dusri cheez - OTP! Bhai OTP to apni jaan se bhi zyada sambhal ke rakhna! Bank wala kabhi OTP nahi maangta, jo maange samajh jao fraud hai!
Aur teesri aur sabse important cheez - Agar koi tumko darake bole ki tumhara account band ho jayega, tumhara paisa atak jayega, to samajh jao, wahi fraud hai! Darna mat, seedha call kaat dena!
Bhai, ye video sirf tumhare liye nahi hai, ye tumhare mummy-papa, dost, sabke liye hai! Isliye isko share zaroor karna!
{outro}
"""
    script = script.strip()
    print(f"HOOK: {hook_title}")
    tts = gTTS(text=script, lang='hi', slow=False)
    tts.save("voice.mp3")

    # VIDEO BANAO - short.mp4
    bg = make_bg(thumb_text)
    audio = AudioFileClip("voice.mp3")
    duration = audio.duration
    print(f"Audio duration: {duration}")

    # Background image clip + zoom feel ke liye thoda bada karke
    clip = ImageClip(bg).set_duration(duration).set_audio(audio)
    # Text overlay - upar hook
    try:
        txt = TextClip(hook_title, fontsize=60, color='white', bg_color='black', font='DejaVu-Sans-Bold', method='caption', size=(1000, None))
        txt = txt.set_position(('center', 200)).set_duration(duration)
        final = CompositeVideoClip([clip, txt], size=(1080,1920))
    except Exception as e:
        print(f"TextClip fail, only bg: {e}")
        final = clip

    final.write_videofile("short.mp4", fps=24, codec="libx264", audio_codec="aac", threads=2, logger=None)
    print("VIDEO DONE: short.mp4")

    info = {
        "title": f"{hook_title} | #Shorts",
        "description": f"{hook_title}\n\nAaj ki is video me maine bataya hai naya fraud, cyber attack aur new launch ke baare me. Poora video dekho warna pachtaoge!\n\n3 Point Yaad Rakhna:\n1. Anjaan Link Mat Kholo\n2. OTP Kabhi Mat Do\n3. Darane Wale Call Se Bacho\n\nYe video sirf awareness ke liye hai.",
        "tags": ["shorts", "cyber security", "fraud", "tech news", "hindi", "viral shorts"],
        "thumb_text": thumb_text,
        "script": script,
        "hook": hook_title
    }
    with open("upload_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print("DONE!")

if __name__ == "__main__":
    main()
