import os
import json
import re
import uuid
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from werkzeug.utils import secure_filename
import generateScreenplay
import processScreenplay
import generateScenesImagesFlux
import generateVideoFal
import generateAudioElevenLabs
import videoAudioOverlay
import utils

# Import configuration
try:
    from config import (
        TOGETHER_API_KEY, 
        OPENAI_API_KEY, 
        ELEVENLABS_API_KEY, 
        FAL_API_KEY, 
        FLASK_SECRET_KEY
    )
except ImportError:
    # Fallback if config.py doesn't exist
    TOGETHER_API_KEY = ""
    OPENAI_API_KEY = ""
    ELEVENLABS_API_KEY = ""
    FAL_API_KEY = ""
    FLASK_SECRET_KEY = "your-secret-key-here"

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# Configuration
PROMPTS_SOURCE_DIRECTORY = "./prompts/"
SCREENPLAY_OUTPUT_DIR = "./outputs/screenplays/"
IMAGES_OUTPUT_DIR = "./outputs/images/"
VIDEOS_OUTPUT_DIR = "./outputs/videos/"
AUDIO_OUTPUT_DIR = "./outputs/audios/"
COMBINED_OUTPUT_DIR = "./outputs/combined/"

PROMPTS_FILE_NAME = "storyPrompts.txt"
SCREENPLAY_PROMPT_FILE_NAME = "ScreenplayPrompt.txt"
SCREENPLAY_TXT_FILENAME = "screenplay.txt"
SCREENPLAY_JSON_FILENAME = "screenplay.json"
COMBINED_VIDEO_FILENAME = "combined_video_final.mp4"

# Global variables for tracking generation progress
generation_progress = {}
generation_status = {}
generation_results = {}  # Store results like video paths

def setup_directories():
    """Ensure all output directories exist"""
    utils.ensure_directory_exists(PROMPTS_SOURCE_DIRECTORY)
    utils.ensure_directory_exists(SCREENPLAY_OUTPUT_DIR)
    utils.ensure_directory_exists(IMAGES_OUTPUT_DIR)
    utils.ensure_directory_exists(VIDEOS_OUTPUT_DIR)
    utils.ensure_directory_exists(AUDIO_OUTPUT_DIR)
    utils.ensure_directory_exists(COMBINED_OUTPUT_DIR)

def count_sentences(text):
    """Count sentences in text"""
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def generate_screenplay_step(story_text, session_id):
    """Step 1: Generate the screenplay from user story"""
    print(f"Generating screenplay for session {session_id}")
    generation_progress[session_id] = 10
    
    screenplay_output_path = SCREENPLAY_OUTPUT_DIR + SCREENPLAY_TXT_FILENAME
    
    # Ensure the directory exists before trying to write the file
    utils.ensure_directory_exists(SCREENPLAY_OUTPUT_DIR)
    
    # Check if screenplay already exists
    if os.path.exists(screenplay_output_path):
        print(f"Screenplay already exists, skipping generation")
        generation_progress[session_id] = 20
        return screenplay_output_path
    
    screenplay_prompt_path = PROMPTS_SOURCE_DIRECTORY + SCREENPLAY_PROMPT_FILE_NAME
    
    # Get the screenplay prompt template
    screenplay_prompt = generateScreenplay.get_screenplay_prompt(screenplay_prompt_path)
    
    # Use the story text directly instead of trying to parse it as JSON
    story_prompt = story_text
    
    # Generate the screenplay
    screenplay = generateScreenplay.generate_screenplay(story_prompt, screenplay_prompt, TOGETHER_API_KEY)
    
    # Clean and store the screenplay
    cleaned_screenplay = utils.clean_screenplay_content(str(screenplay))
    with open(screenplay_output_path, "w") as f:
        f.write(cleaned_screenplay)
    
    generation_progress[session_id] = 20
    return screenplay_output_path

def parse_screenplay_step(screenplay_output_path, session_id):
    """Step 2: Parse the screenplay XML to dictionary"""
    print(f"Parsing screenplay for session {session_id}")
    generation_progress[session_id] = 30
    
    screenplay_output_path_json = SCREENPLAY_OUTPUT_DIR + SCREENPLAY_JSON_FILENAME
    
    # Ensure the directory exists before trying to write the file
    utils.ensure_directory_exists(SCREENPLAY_OUTPUT_DIR)
    
    # Check if parsed screenplay already exists
    if os.path.exists(screenplay_output_path_json):
        print(f"Parsed screenplay already exists, loading from file")
        with open(screenplay_output_path_json, "r") as f:
            screenplay_data = json.load(f)
        generation_progress[session_id] = 40
        return screenplay_data
    
    with open(screenplay_output_path, "r") as f:
        screenplay_content = f.read()
    
    screenplay_data = utils.parse_xml_screenplay_to_dict(screenplay_content)
    
    if screenplay_data is None:
        generation_status[session_id] = "Failed to parse screenplay XML"
        return None
    
    # Save screenplay_data to JSON file
    with open(screenplay_output_path_json, "w") as f:
        json.dump(screenplay_data, f, indent=4)
    
    generation_progress[session_id] = 40
    return screenplay_data

def generate_image_prompts_step(scenes, characters_list, session_id):
    """Step 3: Generate image prompts for the scenes"""
    print(f"Generating image prompts for session {session_id}")
    generation_progress[session_id] = 50
    
    image_prompts = []
    for scene in scenes:
        image_prompts.append(processScreenplay.create_scene_prompt(scene, characters_list))
    
    generation_progress[session_id] = 60
    return image_prompts

def generate_images_step(image_prompts, session_id):
    """Step 4: Generate images for the scenes using Flux"""
    print(f"Generating images for session {session_id}")
    generation_progress[session_id] = 70
    
    # Ensure the directory exists before trying to write files
    utils.ensure_directory_exists(IMAGES_OUTPUT_DIR)
    
    images = []
    image_paths = []
    for i, prompt in enumerate(image_prompts):
        image_path = IMAGES_OUTPUT_DIR + f"image{i}.webp"
        image_paths.append(image_path)
        
        # Check if image already exists
        if os.path.exists(image_path):
            print(f"Image {i} already exists, skipping generation")
            images.append(image_path)
        else:
            images.append(generateScenesImagesFlux.generate_and_download_flux_scene_image(prompt, image_path))
            print(f"Image {i} generated and saved to {image_paths[i]}")
    
    generation_progress[session_id] = 80
    return image_paths

def generate_audio_step(scenes, character_list, session_id):
    """Step 5: Generate audio for all the scenes"""
    print(f"Generating audio for session {session_id}")
    generation_progress[session_id] = 85
    
    # Ensure the directory exists before trying to write files
    utils.ensure_directory_exists(AUDIO_OUTPUT_DIR)
    
    audio_files = []
    for scene in scenes:
        # Check if audio files already exist for this scene
        scene_audio_files = []
        scene_number = scene.get('scene_number', len(audio_files) + 1)
        
        # Look for existing audio files for this scene
        for dialogue in scene.get('dialogue', []):
            dialogue_number = dialogue.get('dialogue_number', 1)
            audio_file_path = os.path.join(AUDIO_OUTPUT_DIR, f"scene{scene_number}_{dialogue_number}.mp3")
            
            if os.path.exists(audio_file_path):
                scene_audio_files.append(audio_file_path)
                print(f"Audio file already exists: {audio_file_path}")
            else:
                # Generate missing audio file
                generated_audio = generateAudioElevenLabs.generate_audio_for_scene_dialogues(
                    ELEVENLABS_API_KEY, scene, AUDIO_OUTPUT_DIR, character_list
                )
                scene_audio_files.extend(generated_audio)
                break  # Break after generating all audio for this scene
        
        audio_files.append(scene_audio_files)
    
    generation_progress[session_id] = 90
    return audio_files

def generate_video_prompts_step(scenes, characters_list, session_id):
    """Step 6: Generate video prompts for the scenes"""
    print(f"Generating video prompts for session {session_id}")
    
    video_prompts = []
    for i, scene in enumerate(scenes):
        video_prompts.append(processScreenplay.create_video_prompt(scene, characters_list))
    
    return video_prompts

def generate_videos_step(scenes, video_prompts, image_paths, session_id):
    """Step 7: Generate videos for each scene"""
    print(f"Generating videos for session {session_id}")
    generation_progress[session_id] = 92
    
    # Ensure the directory exists before trying to write files
    utils.ensure_directory_exists(VIDEOS_OUTPUT_DIR)
    
    videos = []
    for i, scene in enumerate(scenes):
        video_path = VIDEOS_OUTPUT_DIR + f"video{i}.mp4"
        
        # Check if video already exists
        if os.path.exists(video_path):
            print(f"Video {i} already exists, skipping generation")
            videos.append(video_path)
        else:
            videos.append(generateVideoFal.generate_fal_video_from_image(
                video_prompts[i], image_paths[i], FAL_API_KEY, video_path
            ))
            print(f"Video {i}: {videos[i]}")
    
    generation_progress[session_id] = 95
    return videos

def overlay_audio_step(scenes, audio_files, session_id):
    """Step 8: Overlay audio on videos"""
    print(f"Overlaying audio for session {session_id}")
    generation_progress[session_id] = 97
    
    # Ensure the directory exists before trying to write files
    utils.ensure_directory_exists(COMBINED_OUTPUT_DIR)
    
    videos_with_audio = []
    for i, scene in enumerate(scenes):
        video_path = VIDEOS_OUTPUT_DIR + f"video{i}.mp4"
        scene_audio_files = audio_files[i] if i < len(audio_files) else []
        
        if scene_audio_files:
            output_file_name = f"combined_video{i}.mp4"
            output_file_path = COMBINED_OUTPUT_DIR
            combined_video_path = os.path.join(output_file_path, output_file_name)
            
            # Check if combined video already exists
            if os.path.exists(combined_video_path):
                print(f"Combined video {i} already exists, skipping overlay")
                videos_with_audio.append(combined_video_path)
            else:
                videoAudioOverlay.overlay_audio_on_video(
                    video_path, 
                    scene_audio_files, 
                    output_file_path, 
                    output_file_name, 
                    start_time=0
                )
                videos_with_audio.append(combined_video_path)
        else:
            videos_with_audio.append(video_path)
    
    generation_progress[session_id] = 98
    return videos_with_audio

def combine_videos_step(videos_with_audio, session_id):
    """Step 9: Combine all videos into a single video"""
    print(f"Combining videos for session {session_id}")
    generation_progress[session_id] = 99
    
    # Ensure the directory exists before trying to write files
    utils.ensure_directory_exists(COMBINED_OUTPUT_DIR)
    
    combined_video_path = os.path.join(COMBINED_OUTPUT_DIR, COMBINED_VIDEO_FILENAME)
    
    # Check if final combined video already exists
    if os.path.exists(combined_video_path):
        print(f"Final combined video already exists, skipping combination")
        generation_progress[session_id] = 100
        generation_status[session_id] = "completed"
        return combined_video_path
    
    videoAudioOverlay.combineVideos(videos_with_audio, COMBINED_OUTPUT_DIR, COMBINED_VIDEO_FILENAME)
    
    generation_progress[session_id] = 100
    generation_status[session_id] = "completed"
    return combined_video_path

def check_existing_files(session_id):
    """Check if all files already exist for a session"""
    # Check screenplay files
    screenplay_txt = SCREENPLAY_OUTPUT_DIR + SCREENPLAY_TXT_FILENAME
    screenplay_json = SCREENPLAY_OUTPUT_DIR + SCREENPLAY_JSON_FILENAME
    
    if not (os.path.exists(screenplay_txt) and os.path.exists(screenplay_json)):
        return False
    
    # Load screenplay data to check scenes
    with open(screenplay_json, "r") as f:
        screenplay_data = json.load(f)
    
    scenes = screenplay_data.get("scenes", [])
    if not scenes:
        return False
    
    # Check images
    for i in range(len(scenes)):
        image_path = IMAGES_OUTPUT_DIR + f"image{i}.webp"
        if not os.path.exists(image_path):
            return False
    
    # Check videos
    for i in range(len(scenes)):
        video_path = VIDEOS_OUTPUT_DIR + f"video{i}.mp4"
        if not os.path.exists(video_path):
            return False
    
    # Check final combined video
    final_video_path = os.path.join(COMBINED_OUTPUT_DIR, COMBINED_VIDEO_FILENAME)
    if not os.path.exists(final_video_path):
        return False
    
    return True

def generate_video_pipeline(story_text, session_id, force_regenerate=False):
    """Main pipeline to generate video from story"""
    # Check if all files already exist for this session (unless force regenerate is enabled)
    if not force_regenerate and check_existing_files(session_id):
        print(f"All files already exist, skipping generation")
        generation_progress[session_id] = 100
        generation_status[session_id] = "completed"
        final_video_path = os.path.join(COMBINED_OUTPUT_DIR, COMBINED_VIDEO_FILENAME)
        generation_results[session_id] = final_video_path
        return
    
    # Step 1: Generate screenplay
    screenplay_path = generate_screenplay_step(story_text, session_id)
    if not screenplay_path:
        return
    
    # Step 2: Parse screenplay
    screenplay_data = parse_screenplay_step(screenplay_path, session_id)
    if not screenplay_data:
        return
    
    characters_list = screenplay_data.get("characters", [])
    scenes = screenplay_data.get("scenes", [])
    
    # Step 3: Generate image prompts
    image_prompts = generate_image_prompts_step(scenes, characters_list, session_id)
    if not image_prompts:
        return
    
    # Step 4: Generate images
    image_paths = generate_images_step(image_prompts, session_id)
    if not image_paths:
        return
    
    # Step 5: Generate audio
    audio_files = generate_audio_step(scenes, characters_list, session_id)
    if not audio_files:
        return
    
    # Step 6: Generate video prompts
    video_prompts = generate_video_prompts_step(scenes, characters_list, session_id)
    if not video_prompts:
        return
    
    # Step 7: Generate videos
    videos = generate_videos_step(scenes, video_prompts, image_paths, session_id)
    if not videos:
        return
    
    # Step 8: Overlay audio on videos
    videos_with_audio = overlay_audio_step(scenes, audio_files, session_id)
    if not videos_with_audio:
        return
    
    # Step 9: Combine all videos
    final_video_path = combine_videos_step(videos_with_audio, session_id)
    if final_video_path:
        generation_results[session_id] = final_video_path
        # Note: session['video_generated'] will be set by the frontend when it detects completion

# Flask Routes
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/story', methods=['GET', 'POST'])
def story():
    if request.method == 'POST':
        story_text = request.form.get('story', '').strip()
        force_regenerate = request.form.get('force_regenerate', 'false').lower() == 'true'
        
        if not story_text:
            flash('Please enter a story', 'error')
            return render_template('story.html', story='', sentence_count=0)
        
        # Count sentences
        sentence_count = count_sentences(story_text)
        
        if sentence_count > 30:
            flash('Story must be 30 sentences or less', 'error')
            return render_template('story.html', story=story_text, sentence_count=sentence_count)
        
        # Store story in session
        session['story'] = story_text
        session['sentence_count'] = sentence_count
        
        # Generate unique session ID for this video generation
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        
        # Initialize progress tracking
        generation_progress[session_id] = 0
        generation_status[session_id] = 'starting'
        
        # If force regenerate is enabled, clear any existing files
        if force_regenerate:
            session['force_regenerate'] = True
            print(f"Force regeneration enabled for session {session_id}")
        
        # Start video generation in background thread
        thread = threading.Thread(target=generate_video_pipeline, args=(story_text, session_id, force_regenerate))
        thread.daemon = True
        thread.start()
        
        return redirect(url_for('generating_video'))
    
    return render_template('story.html', story='', sentence_count=0)

@app.route('/force-regenerate', methods=['POST'])
def force_regenerate():
    """Force regeneration of video for current session"""
    if 'session_id' not in session:
        return redirect(url_for('story'))
    
    session_id = session['session_id']
    story_text = session.get('story', '')
    
    if not story_text:
        flash('No story found in session', 'error')
        return redirect(url_for('story'))
    
    # Clear existing progress and results
    if session_id in generation_progress:
        del generation_progress[session_id]
    if session_id in generation_status:
        del generation_status[session_id]
    if session_id in generation_results:
        del generation_results[session_id]
    
    # Set force regenerate flag
    session['force_regenerate'] = True
    
    # Initialize progress tracking
    generation_progress[session_id] = 0
    generation_status[session_id] = 'starting'
    
    # Start video generation in background thread
    thread = threading.Thread(target=generate_video_pipeline, args=(story_text, session_id, True))
    thread.daemon = True
    thread.start()
    
    flash('Video regeneration started', 'success')
    return redirect(url_for('generating_video'))

@app.route('/generating-video')
def generating_video():
    if 'session_id' not in session:
        return redirect(url_for('story'))
    
    session_id = session['session_id']
    progress = generation_progress.get(session_id, 0)
    status = generation_status.get(session_id, 'starting')
    
    return render_template('generating_video.html', progress=progress, status=status)

@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == 'POST':
        # This is called by the JavaScript to mark video as generated
        session['video_generated'] = True
        return jsonify({'status': 'success'})
    
    if not session.get('video_generated', False):
        return redirect(url_for('story'))
    
    video_path = generation_results.get(session['session_id'], '')
    return render_template('video.html', video_path=video_path)

@app.route('/serve-video')
def serve_video():
    if not session.get('video_generated', False):
        return redirect(url_for('story'))
    
    video_path = generation_results.get(session['session_id'], '')
    if not video_path or not os.path.exists(video_path):
        flash('Video file not found', 'error')
        return redirect(url_for('video'))
    
    return send_file(video_path, mimetype='video/mp4')

@app.route('/download-video')
def download_video():
    if not session.get('video_generated', False):
        return redirect(url_for('story'))
    
    video_path = generation_results.get(session['session_id'], '')
    if not video_path or not os.path.exists(video_path):
        flash('Video file not found', 'error')
        return redirect(url_for('video'))
    
    return send_file(video_path, as_attachment=True, download_name='your_story_video.mp4')

@app.route('/progress')
def get_progress():
    if 'session_id' not in session:
        return jsonify({'progress': 0, 'status': 'no_session'})
    
    session_id = session['session_id']
    progress = generation_progress.get(session_id, 0)
    status = generation_status.get(session_id, 'starting')
    
    # If generation is complete, set the session flag
    if progress >= 100 and status == 'completed':
        session['video_generated'] = True
    
    return jsonify({'progress': progress, 'status': status})

@app.route('/reset', methods=['POST'])
def reset():
    # Clear session data
    session.clear()
    
    # Clear progress tracking for this session
    if 'session_id' in session:
        session_id = session['session_id']
        if session_id in generation_progress:
            del generation_progress[session_id]
        if session_id in generation_status:
            del generation_status[session_id]
    
    return redirect(url_for('landing'))

if __name__ == '__main__':
    setup_directories()
    app.run(debug=True, host='0.0.0.0', port=5000)