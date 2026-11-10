import os
import json
import subprocess
import requests
import asyncio
from PIL import Image
from pydub import AudioSegment
import soundfile as sf

# --- CONFIGURATION ---
OUTPUT_DIR = "output"
ASSETS_DIR = "assets"
REFERENCE_VOICE = f"{ASSETS_DIR}/voice_sample.ogg"
AVATAR_IMAGE = f"{ASSETS_DIR}/avatar.jpg"

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
AVATAR_SIZE = 600

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# --- AAPKE 2 SCRIPT - Yahi se script aayega, Gemini ki zarurat nahi ---
def get_script_from_gemini():
    # Din ke hisaab se script badlega, taaki roz naya video bane
    import datetime
    day = datetime.datetime.now().day

    script1 = """Namaste doston, aaj hum ek bahut hi zaroori baat karne wale hain. Aapne OTP kisi ko diya hi nahi, phir bhi Aapke account se paise gayab ho gaye. Ye koi jaadu nahi hai, ye SIM Swap hai. Scammer ne Aapke naam par nayi SIM nikalwa li hai. Aapki purani SIM band, uski nayi SIM chalu. Ab Aapke saare OTP, saare bank ke message, sab uske paas ja rahe hain. Bachne ke liye teen kaam aaj hi kijiye. Ek, SIM par SIM PIN lock lagaiye. Do, bank me ek alag email rakha hai to usko check kijiye. Teen, agar achanak network gayab ho jaye to turant apne operator ko call kijiye, wait mat kijiye. Yaad rakhiye, OTP to sab maangte hain, lekin SIM to Aapki pehchan hai. Pehchan chali gayi to paisa bhi jayega."""

    script2 = """Namaste doston, Aapne sirf 5 minute free WiFi chalaya tha, aur usi 5 minute me Aapka poora phone hack ho gaya. Ye kahani nahi, ye aaj ki sachhai hai. Aap railway station par hain, ya kisi cafe me. Aapko dikha FREE WiFi, No Password. Aapne khushi-khushi connect kar liya. Lekin Aapko ye nahi pata, wo WiFi asli tha hi nahi. Scammer ne apne phone se ek nakli WiFi banaya tha. Jaise hi Aap connect hue, Aapka saara data uske saamne se guzarne laga. Bachna bahut aasan hai. Ek, kabhi bhi free WiFi par bank, UPI ya email mat kholiye. Do, phone me hamesha VPN on rakhiye jab public WiFi use karna hi pade. Teen, WiFi ka naam dekh kar connect mat kijiye, counter par pooch kar connect kijiye. Free cheez duniya me sabse mehngi padti hai, jab uski keemat Aapka data ho."""

    if day % 2 == 0:
        return script1
    else:
        return script2

# --- 1. VOICE CLONING (F5-TTS + Madhur Fallback) ---
async def generate_voice(script_text, output_audio_path):
    print("Generating cloned voice...")
    import os
    os.makedirs("output", exist_ok=True)
    clean_text = script_text.replace("{{", "").replace("}}", "")
    try:
        from f5_tts.infer.utils_infer import infer_process
        ref_audio = REFERENCE_VOICE
        if not os.path.exists(ref_audio):
            ref_audio = "voice_sample.ogg"
        ref_text = "Namaste doston, aaj hum ek bahut hi zaroori baat karne wale hain."
        # F5 output ko output folder me narration naam se banayega
        infer_process(ref_audio, ref_text, clean_text, model_type="F5-TTS", ckpt_file="", output_dir="output", output_file="narration", device="cpu", speed=1.0)
        # F5 kabhi-kabhi narration.wav ki jagah alag naam se bana deta hai, isliye check karenge
        if os.path.exists(output_audio_path):
            print(f"Awaz ban gayi: {output_audio_path}")
            return True
        # Agar file alag naam se bani ho, to usko dhoond kar sahi naam de denge
        for f in os.listdir("output"):
            if f.endswith(".wav"):
                print(f"F5 ne is naam se banayi: {f}")
                if f != "narration.wav":
                    import shutil
                    shutil.copy(f"output/{f}", output_audio_path)
                return True
    except Exception as e:
        print(f"F5 me dikkat: {e}, Madhur se bana raha hu")

    # Fallback - Madhur, isse video kabhi rukega nahi
    try:
        import edge_tts
        communicate = edge_tts.Communicate(clean_text, voice="hi-IN-MadhurNeural", rate="+0%", pitch="+0Hz")
        await communicate.save(output_audio_path)
        print(f"Awaz ban gayi - Madhur: {output_audio_path}")
        return True
    except Exception as e2:
        print(f"Madhur me bhi dikkat: {e2}")
        raise e2

# --- 2. AVATAR VIDEO ---
def generate_avatar_video(audio_path, output_video_path):
    print("Generating talking avatar...")
    import os
    if not os.path.exists(AVATAR_IMAGE):
        print("GALTI: assets/avatar.jpg nahi mili")
        print("assets me kya hai:", os.listdir("assets") if os.path.exists("assets") else "assets folder hi nahi hai")
        raise FileNotFoundError("assets/avatar.jpg nahi mili")
    print(f"AAPKI Photo mil gayi: {AVATAR_IMAGE}")
    if not os.path.exists(audio_path):
        print(f"GALTI: Awaz file nahi mili: {audio_path}")
        print("output me kya hai:", os.listdir("output"))
        raise FileNotFoundError(f"{audio_path} nahi mili")
    os.makedirs("output", exist_ok=True)
    cmd = ["ffmpeg", "-loop", "1", "-i", AVATAR_IMAGE, "-i", audio_path, "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", "-y", output_video_path]
    subprocess.run(cmd, check=True)
    print(f"Video ban gaya - AAPKI photo se: {output_video_path}")

# --- 3. DYNAMIC B-ROLL ---
def fetch_broll(query, output_image_path):
    print(f"Fetching B-roll for: {query}")
    api_key = os.environ.get("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY")
    headers = {"Authorization": api_key}
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape"
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        img_url = res["photos"][0]["src"]["large2x"]
        img_data = requests.get(img_url).content
        with open(output_image_path, "wb") as f:
            f.write(img_data)
        im = Image.open(output_image_path)
        im = im.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)
        im.save(output_image_path)
    except Exception as e:
        print(f"B-roll fetch failed, using fallback canvas: {e}")
        img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), color=(20, 24, 33))
        img.save(output_image_path)

# --- 4. CAPTION GENERATION ---
def generate_subtitles(audio_path, script_text, output_ass_path):
    print("Generating word-level subtitles...")
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("base", device="cpu")
        segments, _ = model.transcribe(audio_path, word_timestamps=True)
        ass_header = ("[Script Info]\nPlayResX: 1920\nPlayResY: 1080\n\n" "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, Alignment, MarginV\n" "Style: Default,Arial Black,60,&H00FFFFFF,&H00000000,2,100\n" "Style: Highlight,Arial Black,66,&H0000FFFF,&H00000000,2,100\n\n" "[Events]\nFormat: Layer, Start, End, Style, Text\n")
        events = []
        for segment in segments:
            for word in segment.words:
                clean_word = word.word.strip().replace("{{", "").replace("}}", "")
                style = "Default"
                s_time = f"{int(word.start//3600):01d}:{int((word.start%3600)//60):02d}:{word.start%60:05.2f}"
                e_time = f"{int(word.end//3600):01d}:{int((word.end%3600)//60):02d}:{word.end%60:05.2f}"
                events.append(f"Dialogue: 0,{s_time},{e_time},{style},,{clean_word}")
        with open(output_ass_path, "w", encoding="utf-8") as f:
            f.write(ass_header + "\n".join(events))
    except Exception as e:
        print(f"Subtitle me dikkat, khali subtitle bana raha hu: {e}")
        with open(output_ass_path, "w", encoding="utf-8") as f:
            f.write("[Script Info]\nPlayResX: 1920\nPlayResY: 1080\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, Alignment, MarginV\nStyle: Default,Arial Black,60,&H00FFFFFF,&H00000000,2,100\n\n[Events]\nFormat: Layer, Start, End, Style, Text\n")

# --- 5. COMPOSITING ---
def compose_video(broll_path, avatar_path, ass_path, output_final_path):
    print("Compositing final video...")
    cmd = ["ffmpeg", "-y", "-loop", "1", "-t", "10", "-i", broll_path, "-i", avatar_path, "-filter_complex", f"[1:v]scale={AVATAR_SIZE}:-1,format=yuva420p[av];" f"[0:v][av]overlay=W-w-50:H-h-50[ov];" f"[ov]ass={ass_path}[finalv]", "-map", "[finalv]", "-map", "1:a", "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-c:a", "copy", "-shortest", output_final_path]
    subprocess.run(cmd, check=True)

# --- 6. YOUTUBE UPLOAD - Abhi ke liye sirf file banayega, upload baad me ---
def upload_to_youtube(video_path, script_text):
    print(f"Upload ke liye taiyaar hai: {video_path}")
    print(f"Title ke liye script ka pehla hissa: {script_text[:100]}")
    # Yahan baad me YouTube API wala code aayega, abhi video ban jana hi sabse zaroori hai
    return True

# --- MAIN - Ab sirf ek hi main hai ---
async def main():
    import os
    os.makedirs("output", exist_ok=True)
    print("Script bana raha hu...")
    script = get_script_from_gemini()
    print(f"Script: {script[:100]}...")
    audio_file = f"{OUTPUT_DIR}/narration.wav"
    avatar_video = f"{OUTPUT_DIR}/avatar_talking.mp4"
    broll_image = f"{OUTPUT_DIR}/broll.jpg"
    ass_file = f"{OUTPUT_DIR}/subtitles.ass"
    final_output = f"{OUTPUT_DIR}/final_automation_video.mp4"

    await generate_voice(script, audio_file)
    print("Awaz ban gayi, ab video bana raha hu...")
    generate_avatar_video(audio_file, avatar_video)
    fetch_broll("scary hacker computer matrix background", broll_image)
    generate_subtitles(audio_file, script, ass_file)
    compose_video(broll_image, avatar_video, ass_file, final_output)
    print("Video ban gaya, ab upload kar raha hu...")
    upload_to_youtube(final_output, script)
    print(f"Pipeline Complete! Video saved to {final_output}")

if __name__ == "__main__":
    asyncio.run(main())
