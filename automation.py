# automation.py - Awaz ke saath - Final Version
import os, json, random, datetime, asyncio, subprocess

# --- SETTINGS ---
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

# --- AWAZ WALA PART ---
async def make_voice(script, audio_file):
    # Hindi Ladka ki Awaz - hi-IN-SwaraNeural = Ladka jaisi saaf awaz
    # Speed 1.20x ke liye rate +20%
    import edge_tts
    communicate = edge_tts.Communicate(
        script,
        voice="hi-IN-MadhurNeural",  # Ladka ki awaz
        rate="+20%",  # Ye hi 1.20x Speed hai
        pitch="+0Hz"
    )
    await communicate.save(audio_file)
    print(f"Awaz ban gayi: {audio_file}")

def main():
    topic = get_new_topic()
    script = make_script(topic)
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    audio_file = f"{OUTPUT_FOLDER}/voice_{today}.mp3"
    
    print(f"Topic: {topic}")
    print(f"Script: {script}")
    
    # Awaz banao
    asyncio.run(make_voice(script, audio_file))
    
    # Description
    description = f"""{topic}\n\n{script}\n\n#AI #Tech #CyberSecurity #News\n\n---\nAI Generated Video | Avatar Video"""
    with open(f"{OUTPUT_FOLDER}/description_{today}.txt", "w", encoding="utf-8") as f:
        f.write(description)
    print("Ho gaya! Awaz + Script + Description ready hai.")
    print("Ab bas Avatar Photo + Is Awaz ko Wav2Lip me daalo, Lip Sync ban jayega.")

if __name__ == "__main__":
    main()
