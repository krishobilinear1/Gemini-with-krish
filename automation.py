# automation.py - TALKING AVATAR - FINAL
# Avatar = avatar.jpg - FIXED
# Voice = voice_sample.ogg - AAPKI ASLI AWAZ - CLONE - FIXED 1.20x

import os, json, random, datetime, asyncio

# --- ANTIALIAS FIX ---
try:
    import PIL.Image
    if not hasattr(PIL.Image, 'ANTIALIAS'):
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
except:
    pass

# --- LOCKED - MAT BADALNA ---
AVATAR_PHOTO = "avatar.jpg"  # Aapki Suit wali photo
VOICE_SAMPLE = "voice_sample.ogg"  # Aapki asli awaz
VOICE_SPEED = "+20%"  # 1.20x Speed - LOCKED
USED_FILE = "used_topics.json"
OUTPUT_FOLDER = "videos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- TOPICS + HAR TOPIC KA APNA POORA SCRIPT ---
TOPICS_SCRIPTS = {
    "AI Voice Clone se 50000 ka Fraud - Naya Scam | Latest News": """Rukiye! Aapke papa ka phone aaya, bola beta 50000 bhej de, accident ho gaya hai. Awaz bilkul papa jaisi thi, lekin wo papa the hi nahi.
Ye hai AI Voice Clone Scam. Chor aapki Instagram reel se 10 second ki awaz utha kar, AI se poori awaz bana lete hain.
Isse bachne ke liye, apne parivar me ek Secret Code Word bana lijiye. Jaise - Papa ko boliye, agar asli emergency hai to 'Neela Tota' bolna. Code word nahi bola, to paisa nahi bhejna.""",

    "WhatsApp pe Job Offer wala Naya Scam - Telegram Task Fraud | Latest": """Ek message aaya - Ghar baithe 5000 roz kamao, bas YouTube ko like karna hai. Pehle din 500 rupaye bhi aa gaye. Dusre din bola, 10000 lagao, 20000 milenge. Bas yahi pe khel khatam.
Ye hai Task Fraud. Pehle chhota paisa dekar lalach dete hain, phir bada paisa lekar gayab ho jate hain.
Yaad rakhiye, paise kamane ke liye paise lagane wali koi bhi job 100% fraud hai.""",

    "QR Code Scan karte hi Bank Khali - Naya UPI Scam": """Dukaan wale ne bola, paisa wapas karna hai, ye QR code scan kijiye. Aapne scan kiya, PIN dala, aur aapke 20000 gayab.
Ek baat hamesha yaad rakhiye, paisa lene ke liye kabhi PIN nahi dalna hota. PIN sirf paisa bhejne ke liye hota hai.
Koi bhi bole QR scan karo, PIN dalo, paisa aayega, to samajh jaiye wo chor hai.""",

    "Google pe Pehla Number wala Fake Customer Care - Naya Fraud": """Google pe customer care number search kiya, pehle wale number pe call kiya, usne bola AnyDesk app download karo. Aapne kiya, aur phone ka poora control uske paas chala gaya.
Google pe pehla dikhne wala number hamesha sahi nahi hota. Chor paise dekar apna number upar laate hain.
Customer care number hamesha company ki official website se lijiye.""",

    "Aapki SIM Band ho Jayegi - TRAI Fraud Call | Latest News": """Call aaya, bola main TRAI se bol raha hu, aapki SIM 2 ghante me band ho jayegi, 1 dabaiye. Aapne dabaya, aur aapka OTP chala gaya.
TRAI, Bank, Police kabhi aise call nahi karte. SIM band karne ki dhamki dene wala 100% chor hai. Call kaat dijiye.""",

    "Aadhaar se Loan Le Liya - KYC Fraud | Cyber Security": """Aapko call aaya, bola main bank se bol raha hu, aapki KYC band ho jayegi, ek link pe click kijiye. Aapne click kiya, aur aapke naam pe 2 lakh ka loan le liya gaya.
Bank kabhi WhatsApp pe link nahi bhejta. KYC karna hai to seedha bank ki official app ya branch me jaiye.""",

    "Play Store se Fake Loan App - Photo Morphing Blackmail": """Loan app se 2000 liye, 7 din me 5000 mangne lage. Mana kiya to aapki photo ko ganda bana kar, aapke saare contacts ko bhej diya.
Ye Loan App Scam hai. Ye app aapka poora contact aur gallery chura leti hai.
Kabhi bhi anjaan loan app download mat kijiye.""",

    "WiFi se Aapka Password Chori - Public WiFi Hack | Cyber Security": """Railway station pe Free WiFi se aapne bank khola. 10 minute baad aapke account se paisa gayab. Kyunki wo Free WiFi hacker ka tha.
Free WiFi pe kabhi bank, UPI, ya Gmail mat kholiye. Zaroori ho to apne Mobile Data se hi bank chalaiye.""",

    "Aapke Beta ka Video Viral kar dunga - Sextortion Scam": """Video call pe ek ladki aayi, 2 minute baat hui, phir bola 50000 de, nahi to aapka video viral kar dunga.
Ye Sextortion hai. Dar kar paisa mat dijiye. Paisa dene se wo aur mangenge.
Turant call kaat kar, us number ko Block kijiye aur 1930 pe call karke report kijiye.""",

    "Instagram pe Blue Tick wali Ladki ka Fraud - Crypto Scam": """Instagram pe ek ladki ne message kiya, meri crypto se roz 10000 ki kamai hoti hai, aap bhi lagao. Aapne 5000 lagaye, app me 15000 dikhne laga. Jab nikalne gaye, to app ne bola aur 20000 tax do.
Ye app hi nakli tha. Number screen pe badh raha tha, lekin paisa kabhi tha hi nahi.""",

    "Cyber Fraud se kaise bache, naya tarika": """Cyber Fraud ab purane tarike se nahi, naye AI wale tarike se ho raha hai. Chor ab aapko bank wala banke nahi, aapke dost wala banke call karte hain.
Isse bachne ke liye ek hi niyam hai - Koi bhi OTP, PIN, ya link mange, to call kaat dijiye, aur khud official number pe call kijiye.""",

    "AI ne naya kaam kar diya, sab hairan": """AI ne naya kaam kar diya hai, ab AI aapki awaz, aapka chehra, sab copy kar sakta hai.
Isliye ab kisi bhi video ya voice call pe poora bharosa mat kijiye. Agar koi paisa mange, to secret code poochiye.""",

    "Naya Mobile Launch hua, kya hai khaas": """Naya Mobile Launch hua hai, lekin khareedne se pehle ek cheez dekhiye - kya usme aapko sach me naya feature mil raha hai, ya sirf naam naya hai.
Camera ke megapixel pe mat jaiye, processor aur battery dekhiye.""",

    "Internet pe naya Scam chal raha hai, savdhan": """Internet pe naya Scam chal raha hai, savdhan rahiye. Ab chor aapko lottery, job, aur loan ke naam pe nahi, aapke bachhe ke school ke naam pe call kar rahe hain.
Bolte hain aapke bachhe ka accident ho gaya, paisa bhejo. Ghabraye nahi, pehle school me call karke confirm kijiye.""",

    "UPI Fraud ka naya tarika aur uska solution": """UPI Fraud ka naya tarika aa gaya hai - Chor aapko paisa bhejne ke liye bolenge, aap PIN dalenge, aur paisa kat jayega.
Yaad rakhiye, UPI me paisa lene ke liye PIN kabhi nahi dalna hota.""",

    "OTP Fraud se bachne ka asaan tarika": """OTP Fraud se bachne ka asaan tarika sirf ek hai - OTP kisi ko mat batana.
Bank, Police, Aapka beta, koi bhi OTP mange, to mat dijiye. OTP ka matlab hai - One Time Password, ye sirf aapka hai.""",

    "WhatsApp ka naya update, ye feature aa gaya": """WhatsApp ka naya update aa gaya hai, ab aap apni chat ko lock kar sakte hain, aur kisi ko pata bhi nahi chalega.
Iske liye chat pe lamba dabaiye, Lock Chat ka option aayega.""",

    "Bank Fraud se bachne ka 1 minute wala solution": """Bank Fraud se bachne ka 1 minute wala solution suniye - Apne bank me jaa kar, International Transaction band kar dijiye, aur ek chhota sa limit laga dijiye, jaise 5000.
Agar kabhi fraud bhi hua, to bada nuksan nahi hoga.""",
}

TOPICS = list(TOPICS_SCRIPTS.keys())

def get_new_topic():
    if os.path.exists(USED_FILE):
        with open(USED_FILE, "r") as f:
            used = json.load(f)
    else:
        used = []
    fresh = [t for t in TOPICS if t not in used]
    if not fresh:
        used = []
        fresh = TOPICS
    topic = random.choice(fresh)
    used.append(topic)
    with open(USED_FILE, "w") as f:
        json.dump(used, f)
    return topic

def make_script(topic):
    hooks = [
        "Dekho bhai! Ye cheez aapko pata honi chahiye,",
        "Ruko ruko! Ye video mat chhodna,",
        "Dekho bhai, ye bahut important hai,",
    ]
    hook = random.choice(hooks)
    body = TOPICS_SCRIPTS.get(topic, topic)
    script = f"""{hook} {body}
    Ye video apne dost ko bhi bhej dijiye, usko bhi pata chale.
    Video pasand aaya to Like karo, Share karo aur Subscribe karna mat bhoolna.
    """
    return script

async def make_voice(script, audio_file):
    # AAPKI ASLI AWAZ - voice_sample.ogg se clone
    print("Aapki asli awaz se bol raha hu...")
    try:
        from TTS.api import TTS
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        tts.tts_to_file(text=script, speaker_wav=VOICE_SAMPLE, language="hi", file_path=audio_file)
        print(f"Awaz ban gayi - AAPKI AWAZ: {audio_file}")
    except Exception as e:
        print(f"Clone me dikkat, Madhur se bana raha hu: {e}")
        import edge_tts
        communicate = edge_tts.Communicate(script, voice="hi-IN-MadhurNeural", rate=VOICE_SPEED, pitch="+0Hz")
        await communicate.save(audio_file)

def make_talking_video(avatar_path, audio_path, output_path):
    # FREE WALA TALKING AVATAR
    print(f"Talking Video ban raha hai...")
    print(f"Avatar: {avatar_path}")
    print(f"Audio: {audio_path}")
    try:
        from moviepy.editor import ImageClip, AudioFileClip
        audio = AudioFileClip(audio_path)
        clip = ImageClip(avatar_path).set_duration(audio.duration)
        clip = clip.set_audio(audio)
        # FIX: Zoom wali resize line hatayi - wahi video faad rahi thi
        clip = clip.resize((720, 1280))
        # FIX: pix_fmt yuv420p - Isi se lines wali galti aati thi
        clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"])
        print(f"Talking Video Ready: {output_path}")
        return True
    except Exception as e:
        print(f"Video banane me dikkat: {e}")
        return False

def main():
    topic = get_new_topic()
    script = make_script(topic)
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    audio_file = f"{OUTPUT_FOLDER}/voice_{today}.mp3"
    video_file = f"{OUTPUT_FOLDER}/talking_{today}.mp4"
    
    print(f"Avatar: {AVATAR_PHOTO} - FIXED BOLEGA")
    print(f"Topic: {topic}")
    
    asyncio.run(make_voice(script, audio_file))
    make_talking_video(AVATAR_PHOTO, audio_file, video_file)
    
    desc = f"""{topic}

{script}

---
Cyber Security Hindi | Latest News | Fraud Se Bacho

#AI #Tech #CyberSecurity #Hindi #FraudSeBacho #LatestNews #News #UPIFraud #OnlineScam #CyberFraud"""
    with open(f"{OUTPUT_FOLDER}/description_{today}.txt", "w", encoding="utf-8") as f:
        f.write(desc)
    # UPLOAD KE LIYE - upload_info.json banana jaruri hai - TAGS KE SAATH
    with open("upload_info.json", "w", encoding="utf-8") as f:
        json.dump({
            "title": topic,
            "description": desc,
            "video": video_file,
            "tags": ["AI", "Tech", "CyberSecurity", "Hindi", "FraudSeBacho", "LatestNews", "News", "UPIFraud", "OnlineScam"],
            "privacyStatus": "private",
            "categoryId": "27"
        }, f, ensure_ascii=False, indent=2)
    print("HO GAYA! Talking Avatar Video Ready!")

if __name__ == "__main__":
    main()
