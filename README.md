---
title: Tell Me Your Story
emoji: 📚
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# Tell Me Your Story

Transform your stories into stunning videos with AI! This interactive web application allows users to:

1. **Share Your Story** - Write your story, idea, or script in up to 30 sentences
2. **Customize Characters** - Upload avatars and define personality traits for your characters  
3. **Generate Video** - Watch as AI creates a personalized video from your story

## Features

- Beautiful, responsive landing page
- Interactive story input with sentence counting
- Character customization with trait selection
- Simulated video generation with progress tracking
- Mobile-friendly design using Tailwind CSS

## How to Use

1. Click "Start Creating" to begin
2. Write your story in the text area (max 30 sentences)
3. Customize your characters by selecting personality traits
4. Click "Generate Video" to create your personalized video

Built with HTML, JavaScript, and Tailwind CSS for a seamless user experience.

# Quickstart
1. Give a prompt
2. Generate screenplay
3. Generate scenes
4. Generate image prompt and get image for each scene
5. Generate video prompt, text prompt and get video for each scene
6. Generate audio for each scene
7. Overlay audio for each scene on the scene 
8. Merge all videos into one
9. Play the video back to the user

# Running the application
python minimal.py -k <TOGETHER_APIKEY>
                  -o <OPEN_AI_APIKEY>
                  -l <LEONARDO_AI_APIKEY>
                  -s <STORY_NUMBER>