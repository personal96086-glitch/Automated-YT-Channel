name: Generate Weekly Video
on:
  schedule:
    - cron: '0 0 * * 1'
  workflow_dispatch: 

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'

      # THIS PART WAS MISSING: It installs the video engine
      - name: Install FFmpeg
        uses: FedericoCarboni/setup-ffmpeg@v3

      - name: Install dependencies
        run: |
          pip install google-generativeai moviepy==1.0.3 edge-tts requests imageio-ffmpeg

      - name: Run Script
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python main.py

      - name: Upload Video
        uses: actions/upload-artifact@v4
        with:
          name: youtube-video
          path: output_video.mp4
