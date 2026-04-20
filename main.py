import os
import google.generativeai as genai
import requests
import asyncio
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from edge_tts import Communicate

# Use absolute path to avoid "File Not Found" errors
current_dir = os.getcwd()
output_path = os.path.join(current_dir, "output_video.mp4")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

async def make_video():
    print("Starting video creation...")
    try:
        resp = model.generate_content("Write 3 short motivational sentences.")
        lines = resp.text.split('.')
        
        clips = []
        for i, line in enumerate(lines[:3]):
            if len(line.strip()) < 5: continue
            
            audio_file = os.path.join(current_dir, f"{i}.mp3")
            img_file = os.path.join(current_dir, f"{i}.jpg")
            
            await Communicate(line, "en-US-ChristopherNeural").save(audio_file)
            
            img_url = f"https://image.pollinations.ai/prompt/3d%20render%20productivity%20{i}?width=1280&height=720&nologo=true"
            with open(img_file, 'wb') as f:
                f.write(requests.get(img_url).content)
            
            audio = AudioFileClip(audio_file)
            img = ImageClip(img_file).set_duration(audio.duration).set_fps(24)
            clips.append(img.set_audio(audio))
            
        final = concatenate_videoclips(clips, method="compose")
        # EXPLICIT PATH SAVING
        final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        print(f"Video saved successfully at {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(make_video())
    
