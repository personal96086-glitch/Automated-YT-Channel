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
    # 1. Get Topic and Script
    prompt = "Pick a trending productivity topic and write a motivational script. Break it into 20-second segments. Format: Segment 1: [text] Segment 2: [text]..."
    response = model.generate_content(prompt)
    segments = response.text.split("Segment")
    
    clips = []
    
    # 2. Process each segment (for the first 5 segments to start)
    for i, text in enumerate(segments[1:6]):
        # Generate Audio
        audio_file = f"voice_{i}.mp3"
        communicate = Communicate(text, "en-US-ChristopherNeural")
        await communicate.save(audio_file)
        
        # Generate Image Prompt & Image
        img_prompt_resp = model.generate_content(f"Write a 3D animation image prompt for: {text}")
        img_url = f"https://image.pollinations.ai/prompt/{img_prompt_resp.text.replace(' ', '%20')}?width=1280&height=720&nologo=true"
        
        img_data = requests.get(img_url).content
        with open(f"image_{i}.jpg", 'wb') as f:
            f.write(img_data)
            
        # Create Video Clip
        audio_clip = AudioFileClip(audio_file)
        img_clip = ImageClip(f"image_{i}.jpg").set_duration(audio_clip.duration).set_fps(24)
        clips.append(img_clip.set_audio(audio_clip))

    # 3. Join clips and export at 720p
    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile("output_video.mp4", fps=24, bitrate="2000k")

if __name__ == "__main__":
    asyncio.run(generate_video())
      
