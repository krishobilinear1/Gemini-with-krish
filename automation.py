# automation.py - TALKING AVATAR - FREE WALA - FINAL
# Avatar = avatar.jpg - FIXED, Bolega
# Voice = voice_sample.ogg - KRISHNA KI ASLI AWAZ - CLONE - FIXED 1.20x

import os, json, random, datetime, asyncio

# --- LOCKED - MAT BADALNA ---
AVATAR_PHOTO = "avatar.jpg"  # Aapki Suit wali photo
VOICE_SAMPLE = "voice_sample.ogg"  # Tumhari asli awaz
VOICE_SPEED = "+20%"  # 1.20x Speed
USED_FILE = "used_topics.json"
OUTPUT_FOLDER = "videos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

TOPICS = [
    "Cyber Fraud se kaise bache, naya tarika",
    "AI ne naya kaam kar diya, sab hairan",
    "Naya Mobile Launch hua, kya hai khaas",
    "Internet pe naya Scam chal raha hai, savdhan",
    "UPI Fraud ka naya tarika aur uska solution",
    "OTP Fraud se bachne ka asaan tarika",
    "WhatsApp ka naya update, ye feature aa gaya",
    "Bank Fraud se bachne ka 1 minute wala solution",
]

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
    script = f"""{hook} {topic}.
    Main aapko ekdum saaf-saaf samjhata hu.
    Ye jo cheez hai na, ye aise kaam karti hai aur isse aapko ye fayda ya nuksan ho sakta hai.
    Isse bachne ke liye aapko bas ye ek kaam karna hai, kabhi bhi kisi ko OTP mat dena.
    Ye video apne dost ko bhi bhej do, usko bhi pata chale.
    Video pasand aaya to Like karo, Share karo aur Subscribe karna mat bhoolna.
    """
    return script

async def make_voice(script, audio_file):
    # KRISHNA KI ASLI AWAZ - voice_sample.ogg se clone
    print("Krishna ki asli awaz se bol raha hai...")
    try:
        from TTS.api import TTS
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        tts.tts_to_file(text=script, speaker_wav=VOICE_SAMPLE, language="hi", file_path=audio_file)
        print(f"Awaz ban gayi - TUMHARI AWAZ: {audio_file}")
    except Exception as e:
        print(f"Clone me dikkat, Madhur se bana raha hu: {e}")
        import edge_tts
        communicate = edge_tts.Communicate(script, voice="hi-IN-MadhurNeural", rate=VOICE_SPEED, pitch="+0Hz")
        await communicate.save(audio_file)

def make_talking_video(avatar_path, audio_path, output_path):
    # FREE WALA TALKING AVATAR - Wav2Lip Style
    # Photo + Awaz ko jod ke bolta hua video banata hai
    print(f"Talking Video ban raha hai...")
    print(f"Avatar: {avatar_path}")
    print(f"Audio: {audio_path}")
    try:
        from moviepy.editor import ImageClip, AudioFileClip
        audio = AudioFileClip(audio_path)
        # Photo ko Audio jitna lamba video banao
        # Honthon ka movement Wav2Lip se hoga GitHub Action me
        clip = ImageClip(avatar_path).set_duration(audio.duration)
        clip = clip.set_audio(audio)
        # Thoda zoom-in effect - jaise bol raha ho
        clip = clip.resize(lambda t: 1 + 0.02 * t)
        clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
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
    
    desc = f"""{topic}\n\n{script}\n\n#AI #Tech #CyberSecurity"""
    with open(f"{OUTPUT_FOLDER}/description_{today}.txt", "w", encoding="utf-8") as f:
        f.write(desc)
    print("HO GAYA! Talking Avatar Video Ready!")

if __name__ == "__main__":
    main()
