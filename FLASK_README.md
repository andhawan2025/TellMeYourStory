# Tell Me Your Story - Flask Web Application

A Flask web application that transforms user stories into AI-generated videos using the same pipeline as the original command-line tool.

## Features

- **User-friendly Web Interface**: Beautiful UI based on the React design from `pages.tsx`
- **Real-time Progress Tracking**: Live updates during video generation
- **Story Input**: Users can input their own stories (up to 30 sentences)
- **Complete Video Pipeline**: 
  - Story → Screenplay generation
  - Scene image generation
  - Audio generation for dialogues
  - Video generation from images
  - Audio overlay on videos
  - Final video combination
- **Video Playback**: Built-in video player for generated videos
- **Download Functionality**: Users can download their generated videos

## Setup Instructions

### 1. Install Dependencies

```bash
# Install Flask dependencies
pip install -r requirements_flask.txt

# Install video generation dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.py` and add your API keys:

```python
# Together AI API key for text-to-screenplay generation
TOGETHER_API_KEY = "your-together-ai-key"

# OpenAI API key for image generation
OPENAI_API_KEY = "your-openai-key"

# ElevenLabs API key for text-to-speech
ELEVENLABS_API_KEY = "your-elevenlabs-key"

# Fal AI API key for image-to-video generation
FAL_API_KEY = "your-fal-ai-key"

# Flask secret key (change this in production)
FLASK_SECRET_KEY = "your-secret-key-here"
```

### 3. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Landing Page**: Visit the homepage to learn about the application
2. **Story Input**: Click "Start Creating" to enter your story
3. **Story Submission**: Write your story (max 30 sentences) and submit
4. **Video Generation**: Watch real-time progress as your video is generated
5. **Video Playback**: View and download your generated video

## File Structure

```
├── app.py                 # Main Flask application
├── config.py             # API key configuration
├── requirements_flask.txt # Flask dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── landing.html      # Landing page
│   ├── story.html        # Story input page
│   ├── generating_video.html # Progress page
│   └── video.html        # Video playback page
├── static/               # Static files (CSS, JS, images)
└── outputs/              # Generated content
    ├── screenplays/      # Generated screenplays
    ├── images/          # Generated scene images
    ├── videos/          # Generated scene videos
    ├── audios/          # Generated audio files
    └── combined/        # Final combined videos
```

## API Endpoints

- `GET /` - Landing page
- `GET/POST /story` - Story input page
- `GET /generating-video` - Video generation progress page
- `GET/POST /video` - Video playback page
- `GET /serve-video` - Serve video file
- `GET /download-video` - Download video file
- `GET /progress` - Get generation progress (JSON)
- `POST /reset` - Reset session and start over

## Technical Details

### Video Generation Pipeline

The application follows the same 9-step pipeline as the original tool:

1. **Generate Screenplay**: Convert user story to structured screenplay
2. **Parse Screenplay**: Extract scenes and characters from XML
3. **Generate Image Prompts**: Create prompts for scene images
4. **Generate Images**: Create scene images using Flux
5. **Generate Audio**: Create audio for dialogues using ElevenLabs
6. **Generate Video Prompts**: Create prompts for video generation
7. **Generate Videos**: Create videos from images using Fal AI
8. **Overlay Audio**: Combine audio with videos
9. **Combine Videos**: Merge all scenes into final video

### Session Management

- Each video generation gets a unique session ID
- Progress is tracked globally and associated with session ID
- Generated files are saved with session ID to avoid conflicts
- Session data is cleared when user starts over

### Error Handling

- Comprehensive error handling in each pipeline step
- Error messages are displayed to users
- Failed generations can be retried by starting over

## Production Deployment

For production deployment:

1. Change the Flask secret key in `config.py`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up proper file storage for generated videos
4. Implement user authentication if needed
5. Add rate limiting and file cleanup

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all API keys are correctly set in `config.py`
2. **File Permissions**: Ensure the application has write permissions to the `outputs/` directory
3. **Memory Issues**: Video generation can be memory-intensive; ensure sufficient RAM
4. **Timeout Issues**: Some API calls may take time; the progress tracking handles this

### Debug Mode

Run with debug mode for detailed error messages:

```bash
export FLASK_ENV=development
python app.py
```

## License

This project uses the same license as the original Tell Me Your Story application. 