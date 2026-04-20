import os
import google.generativeai as genai
import requests
import asyncio
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from edge_tts import Communicate

# Setup Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def generate_video():
    try:
        # 1. Get Script
        prompt = "Write a 1-minute motivational script about consistency. Break it into 3 short paragraphs."
        response = model.generate_content(prompt)
        segments = response.text.split('\n\n')
        
        clips = []
        # 2. Process first 3 segments
        for i, text in enumerate(segments[:3]):
            if len(text.strip()) < 5: continue
            
            # Voice
            audio_file = f"v_{i}.mp3"
            await Communicate(text, "en-US-ChristopherNeural").save(audio_file)
            
            # Image
            img_url = f"https://image.pollinations.ai/prompt/3d%20animation%20style%20productivity%20scene%20{i}?width=1280&height=720&nologo=true"
            with open(f"i_{i}.jpg", 'wb') as f:
                f.write(requests.get(img_url).content)
                
            # Create Clip
            a_clip = AudioFileClip(audio_file)
            i_clip = ImageClip(f"i_{i}.jpg").set_duration(a_clip.duration).set_fps(24)
            clips.append(i_clip.set_audio(a_clip))

        # 3. Export
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile("output_video.mp4", fps=24, codec="libx264")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(generate_video())
  
