import os
import google.generativeai as genai
import requests
import asyncio
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from edge_tts import Communicate

# Force the output to the main folder
output_filename = "output_video.mp4"

# Use the Secret from GitHub
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

async def make_video():
    print("Robot is starting...")
    try:
        # Simple test script
        resp = model.generate_content("Write three very short motivational quotes about success.")
        quotes = resp.text.split('\n')
        quotes = [q for q in quotes if len(q) > 5][:3]

        clips = []
        for i, quote in enumerate(quotes):
            print(f"Processing part {i}...")
            # 1. Audio
            audio_file = f"audio_{i}.mp3"
            await Communicate(quote, "en-US-ChristopherNeural").save(audio_file)
            
            # 2. Image
            img_file = f"img_{i}.jpg"
            img_url = f"https://image.pollinations.ai/prompt/3d%20animation%20productivity%20{i}?width=1280&height=720&nologo=true"
            img_data = requests.get(img_url).content
            with open(img_file, 'wb') as f:
                f.write(img_data)
            
            # 3. Create Clip
            a_clip = AudioFileClip(audio_file)
            i_clip = ImageClip(img_file).set_duration(a_clip.duration).set_fps(24)
            clips.append(i_clip.set_audio(a_clip))

        print("Finalizing video...")
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
        print("SUCCESS: Video created!")
        
    except Exception as e:
        print(f"FATAL ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(make_video())
            
