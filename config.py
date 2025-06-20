# API Keys Configuration
# Load API keys from environment variables for better security

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Together AI API key for text-to-screenplay generation
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")

# OpenAI API key for image generation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ElevenLabs API key for text-to-speech
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# Fal AI API key for image-to-video generation
FAL_API_KEY = os.getenv("FAL_API_KEY", "")

# Flask secret key (change this in production)
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "your-secret-key-here-change-this-in-production") 