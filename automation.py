import os
import json
import subprocess
import requests
from PIL import Image
from pydub import AudioSegment
from faster_whisper import WhisperModel
import soundfile as sf
from f5_tts.infer.utils_infer import infer_process, load_model, load_vocoder

# --- CONFIGURATION ---
OUTPUT_DIR = "output"
ASSETS_DIR = "assets"
REFERENCE_VOICE = f"{ASSETS_DIR}/voice_sample.ogg" # Your GitHub voice clone
AVATAR_IMAGE = f"{ASSETS_DIR}/avatar.png"          # Your single photo avatar

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
AVATAR_SIZE = 600

TOPICS_SCRIPTS = {
    "Cyber Fraud Alert": {
        "text": "Alert! {{ONLINE SCAMMERS}} are using voice cloning. Never share your {{OTP}} or PIN.",
        "visual_query": "scary hacker computer matrix background"
    }
}

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# --- 1. VOICE CLONING (F5-TTS) ---
def generate_voice(script_text, output_audio_path):
    print("Generating cloned voice...")
    # Clean text for synthesis
    clean_text = script_text.replace("{{", "").replace("}}", "")
    temp_raw = output_audio_path.replace(".wav", "_raw.wav")
    
    async def generate_voice(script, audio_file):
    print("Generating cloned voice...")
    try:
        # F5-TTS - AAPKI ASLI AWAZ wala kaam
        from f5_tts.infer.utils_infer import infer_process, load_model, load_vocoder

        # Aapki awaz ka sample - ye file repo me honi chahiye
        ref_audio = "voice_sample.ogg"
        ref_text = "Namaste doston, aaj hum ek bahut hi zaroori baat karne wale hain."

        # F5 ka sahi tarika - load_model ko alag se bulane ki zarurat nahi hai
        # infer_process khud hi model load kar lega
        infer_process(
            ref_audio,
            ref_text,
            script,
            model_type="F5-TTS",
            ckpt_file="",  # Khali rakhenge, to ye apne aap official model download kar lega
            output_dir=".",
            output_file=audio_file,
            device="cpu",
            speed=1.0,
        )
        print(f"Awaz ban gayi - AAPKI AWAZ: {audio_file}")
        return True

    except Exception as e:
        print(f"F5 me dikkat, Madhur se bana raha hu: {e}")
        # Fallback - Agar F5 fail bhi hua, to video rukega nahi
        import edge_tts
        communicate = edge_tts.Communicate(script, voice="hi-IN-MadhurNeural", rate="+0%", pitch="+0Hz")
        await communicate.save(audio_file)
        print(f"Awaz ban gayi - Madhur: {audio_file}")
        return True # Switch to cuda if available
    vocoder = load_vocoder(device="cpu")
    
    wav, sr, _ = infer_process(
        ref_audio=REFERENCE_VOICE,
        ref_text="This is a reference text.", # Adjust as needed
        gen_text=clean_text,
        model=model,
        vocoder=vocoder,
        speed=1.2, # Fast paced news style
        device="cpu"
    )
    sf.write(temp_raw, wav, sr)
    
    # Process audio for punchy broadcast sound
    audio = AudioSegment.from_wav(temp_raw)
    compressed = audio.compress_dynamic_range(threshold=-16.0, ratio=3.0)
    compressed.export(output_audio_path, format="wav")
    os.remove(temp_raw)

# --- 2. LIP SYNC (MuseTalk/LivePortrait placeholder) ---
def generate_avatar_video(audio_path, output_video_path):
    print("Generating talking avatar...")
    # In real pipeline, call MuseTalk or LivePortrait CLI here
    # Mocking video generation using image and audio loop for demonstration
    cmd = [
        "ffmpeg", "-loop", "1", "-i", AVATAR_IMAGE,
        "-i", audio_path, "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
        "-shortest", "-y", output_video_path
    ]
    subprocess.run(cmd, check=True)

# --- 3. DYNAMIC B-ROLL (Pexels API) ---
def fetch_broll(query, output_image_path):
    print(f"Fetching B-roll for: {query}")
    api_key = "YOUR_PEXELS_API_KEY" # Replace with user's key
    headers = {"Authorization": api_key}
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape"
    
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        img_url = res["photos"][0]["src"]["large2x"]
        img_data = requests.get(img_url).content
        with open(output_image_path, "wb") as f:
            f.write(img_data)
        
        # Resize to 1080p
        im = Image.open(output_image_path)
        im = im.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)
        im.save(output_image_path)
    except Exception as e:
        print(f"B-roll fetch failed, using fallback canvas: {e}")
        img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), color=(20, 24, 33))
        img.save(output_image_path)

# --- 4. CAPTION GENERATION (Whisper) ---
def generate_subtitles(audio_path, script_text, output_ass_path):
    print("Generating word-level subtitles...")
    model = WhisperModel("base", device="cpu")
    segments, _ = model.transcribe(audio_path, word_timestamps=True)
    
    ass_header = (
        "[Script Info]\nPlayResX: 1920\nPlayResY: 1080\n\n"
        "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, Alignment, MarginV\n"
        "Style: Default,Arial Black,60,&H00FFFFFF,&H00000000,2,100\n"
        "Style: Highlight,Arial Black,66,&H0000FFFF,&H00000000,2,100\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Text\n"
    )
    
    events = []
    for segment in segments:
        for word in segment.words:
            clean_word = word.word.strip().replace("{{", "").replace("}}", "")
            is_highlight = "{{" in word.word or "}}" in word.word
            style = "Highlight" if is_highlight else "Default"
            
            s_time = f"{int(word.start//3600):01d}:{int((word.start%3600)//60):02d}:{word.start%60:05.2f}"
            e_time = f"{int(word.end//3600):01d}:{int((word.end%3600)//60):02d}:{word.end%60:05.2f}"
            
            events.append(f"Dialogue: 0,{s_time},{e_time},{style},,{clean_word}")
            
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(events))

# --- 5. COMPOSITING (FFmpeg) ---
def compose_video(broll_path, avatar_path, ass_path, output_final_path):
    print("Compositing final video...")
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", "10", "-i", broll_path, # B-roll loop
        "-i", avatar_path,                         # Talking avatar
        "-filter_complex",
        f"[1:v]scale={AVATAR_SIZE}:-1,format=yuva420p[av];"
        f"[0:v][av]overlay=W-w-50:H-h-50[ov];"      # Overlay at bottom right
        f"[ov]ass={ass_path}[finalv]",             # Burn subtitles
        "-map", "[finalv]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "copy", "-shortest", output_final_path
    ]
    subprocess.run(cmd, check=True)

# --- MAIN EXECUTION ---
def main():
    topic = "Cyber Fraud Alert"
    data = TOPICS_SCRIPTS[topic]
    script = data["text"]
    query = data["visual_query"]
    
    audio_file = f"{OUTPUT_DIR}/narration.wav"
    avatar_video = f"{OUTPUT_DIR}/avatar_talking.mp4"
    broll_image = f"{OUTPUT_DIR}/broll.jpg"
    ass_file = f"{OUTPUT_DIR}/subtitles.ass"
    final_output = f"{OUTPUT_DIR}/final_automation_video.mp4"
    
    generate_voice(script, audio_file)
    generate_avatar_video(audio_file, avatar_video)
    fetch_broll(query, broll_image)
    generate_subtitles(audio_file, script, ass_file)
    compose_video(broll_image, avatar_video, ass_file, final_output)
    
    print(f"Pipeline Complete! Video saved to {final_output}")

if __name__ == "__main__":
    main()
