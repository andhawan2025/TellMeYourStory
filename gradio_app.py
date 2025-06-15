import gradio as gr
import os
import glob
import json
import random
import time
import threading
import subprocess
from typing import Optional, List

# Fixed file paths - no API keys needed
SCREENPLAY_FILE = "./outputs/screenplay.txt"

# Available screenplay files for user selection
AVAILABLE_SCREENPLAYS = [
    "./outputs/screenplay.txt",
]

IMAGE_PATHS = [
    "./outputs/openAIImages/image0.png",
    "./outputs/openAIImages/image1.png", 
    "./outputs/openAIImages/image2.png"
]

VIDEO_PATH = "./outputs/falVideos/video0.mp4"

AVAILABLE_VIDEOS = [
    "./outputs/falVideos/video0.mp4",
    "./outputs/falVideos/video1.mp4",
    "./outputs/falVideos/video2.mp4"
]

def validate_sentence_count(prompt: str) -> bool:
    """Validate that the prompt has no more than 10 sentences."""
    sentences = prompt.split('.')
    sentence_count = len([s.strip() for s in sentences if s.strip()])
    return sentence_count <= 10

def load_screenplay_with_typewriter(user_prompt: str):
    """Load a screenplay from local files with typewriter effect."""
    if not user_prompt or not user_prompt.strip():
        yield "", "❌ Please enter a story prompt"
        return
    
    if not validate_sentence_count(user_prompt):
        yield "", "❌ Please limit your prompt to 10 sentences or less"
        return
    
    try:
        # Select screenplay file
        selected_screenplay = AVAILABLE_SCREENPLAYS[0]
        
        # Check if the selected file exists
        if not os.path.exists(selected_screenplay):
            selected_screenplay = SCREENPLAY_FILE
        
        if not os.path.exists(selected_screenplay):
            yield "", "❌ No screenplay files found in outputs directory"
            return
        
        # Read the full screenplay content
        with open(selected_screenplay, 'r', encoding='utf-8') as f:
            full_screenplay = f.read()
        
        # Start typewriter effect
        yield "", f"📖 Loading screenplay from {os.path.basename(selected_screenplay)}..."
        
        # Calculate timing for 8-second display
        total_chars = len(full_screenplay)
        updates = 40  # Number of updates for smooth effect
        chars_per_update = max(1, total_chars // updates)
        delay_per_update = 8.0 / updates  # 8 seconds total
        
        # Progressive display with typewriter effect
        current_text = ""
        for i in range(0, total_chars, chars_per_update):
            current_text = full_screenplay[:i + chars_per_update]
            progress_msg = f"📖 Loading screenplay... ({min(100, int((i / total_chars) * 100))}%)"
            yield current_text, progress_msg
            time.sleep(delay_per_update)
        
        # Ensure full text is displayed
        yield full_screenplay, f"✅ Screenplay loaded successfully from {os.path.basename(selected_screenplay)}!"
        
    except Exception as e:
        yield "", f"❌ Error loading screenplay: {str(e)}"

def load_images_with_typewriter_effect():
    """Load images from local files with progressive typewriter effect."""
    try:
        # Check if all image files exist
        existing_images = []
        for image_path in IMAGE_PATHS:
            if os.path.exists(image_path):
                existing_images.append(image_path)
        
        if not existing_images:
            yield [], "❌ No image files found in outputs/openAIImages directory"
            return
        
        # Progressive loading with typewriter effect
        loaded_images = []
        total_images = len(existing_images)
        
        for i, image_path in enumerate(existing_images):
            image_num = i + 1
            
            # Start loading this image
            yield loaded_images.copy(), f"🖼️ Loading image {image_num}/{total_images}..."
            
            # Simulate progressive loading over 5 seconds
            updates = 25  # Number of updates for smooth effect per image
            delay_per_update = 5.0 / updates  # 5 seconds per image
            
            for update in range(updates):
                progress_percent = int((update / updates) * 100)
                status_msg = f"🖼️ Loading image {image_num}/{total_images}... ({progress_percent}%)"
                yield loaded_images.copy(), status_msg
                time.sleep(delay_per_update)
            
            # Add the completed image to the list
            loaded_images.append(image_path)
            
            # Show completed image
            if i < total_images - 1:  # Not the last image
                yield loaded_images.copy(), f"✅ Image {image_num}/{total_images} loaded! Loading next image..."
                time.sleep(0.5)  # Brief pause between images
            else:  # Last image
                yield loaded_images.copy(), f"✅ All {total_images} images loaded successfully!"
        
    except Exception as e:
        yield [], f"❌ Error loading images: {str(e)}"

def load_images_from_local() -> tuple:
    """Load images from local files (legacy function for compatibility)."""
    try:
        # Check if all image files exist
        existing_images = []
        for image_path in IMAGE_PATHS:
            if os.path.exists(image_path):
                existing_images.append(image_path)
        
        if not existing_images:
            return [], "❌ No image files found in outputs/openAIImages directory"
        
        return existing_images, f"✅ Loaded {len(existing_images)} images successfully!"
        
    except Exception as e:
        return [], f"❌ Error loading images: {str(e)}"

def load_videos_into_columns():
    """Load videos into separate columns with progressive loading effect."""
    try:
        # Initialize all videos as None and status
        video1, video2, video3 = None, None, None
        
        # Check which video files exist
        existing_videos = []
        for video_path in AVAILABLE_VIDEOS:
            if os.path.exists(video_path):
                existing_videos.append(video_path)
        
        if not existing_videos:
            yield video1, video2, video3, "❌ No video files found in the specified paths"
            return
        
        # Start loading process
        yield video1, video2, video3, f"🎬 Starting to load {len(existing_videos)} videos into columns..."
        time.sleep(1.0)
        
        # Load Video 1
        if len(existing_videos) >= 1:
            yield existing_videos[0], video2, video3, "🔄 Loading Video 1... (33%)"
            time.sleep(2.0)  
            video1 = existing_videos[0]
            yield video1, video2, video3, "✅ Video 1 loaded! (33%)"
            time.sleep(1.0)
        
        # Load Video 2
        if len(existing_videos) >= 2:
            yield video1, existing_videos[1], video3, "🔄 Loading Video 2... (67%)"
            time.sleep(2.0)
            video2 = existing_videos[1]
            yield video1, video2, video3, "✅ Video 2 loaded! (67%)"
            time.sleep(1.0)
        
        # Load Video 3
        if len(existing_videos) >= 3:
            yield video1, video2, existing_videos[2], "🔄 Loading Video 3... (100%)"
            time.sleep(2.0)
            video3 = existing_videos[2]
            yield video1, video2, video3, "✅ All 3 videos loaded! (100%)"
        else:
            yield video1, video2, video3, f"✅ All {len(existing_videos)} videos loaded! (100%)"
        
    except Exception as e:
        yield None, None, None, f"❌ Error loading videos: {str(e)}"

def load_videos_sequentially():
    """Load and play all videos from AVAILABLE_VIDEOS list one by one."""
    try:
        # Check which video files exist
        existing_videos = []
        for video_path in AVAILABLE_VIDEOS:
            if os.path.exists(video_path):
                existing_videos.append(video_path)
        
        if not existing_videos:
            yield None, "❌ No video files found in outputs/falVideos directory"
            return
        
        total_videos = len(existing_videos)
        
        # Play videos one by one
        for i, video_path in enumerate(existing_videos):
            video_num = i + 1
            
            # Start loading this video
            yield None, f"🎥 Loading video {video_num}/{total_videos}..."
            
            # Simulate brief loading time for dramatic effect
            time.sleep(1.0)
            
            # Display the video
            yield video_path, f"🎬 Playing video {video_num}/{total_videos}: {os.path.basename(video_path)}"
            
            # Let video play for a duration (simulate watching time)
            if i < total_videos - 1:  # Not the last video
                time.sleep(3.0)  # 3 seconds viewing time per video
                yield video_path, f"▶️ Video {video_num}/{total_videos} playing... Next video loading soon..."
                time.sleep(1.0)  # Brief pause before next video
            else:  # Last video
                time.sleep(2.0)  # Brief pause for last video
                yield video_path, f"✅ All {total_videos} videos played successfully! Enjoy the final video."
        
    except Exception as e:
        yield None, f"❌ Error loading videos: {str(e)}"

def merge_all_videos():
    """Merge all available videos into a single video file with robust encoding."""
    try:
        # Check which video files exist
        existing_videos = []
        for video_path in AVAILABLE_VIDEOS:
            if os.path.exists(video_path):
                existing_videos.append(video_path)
        
        if not existing_videos:
            yield None, "❌ No video files found to merge"
            return
        
        if len(existing_videos) == 1:
            yield existing_videos[0], "✅ Only one video available - no merging needed"
            return
        
        # Start merging process
        yield None, f"🔄 Starting merge process for {len(existing_videos)} videos..."
        time.sleep(1.0)
        
        # Output path for merged video
        merged_video_path = "./outputs/falVideos/merged_video.mp4"
        
        # Remove existing merged video if it exists
        if os.path.exists(merged_video_path):
            os.remove(merged_video_path)
        
        # Try Method 1: FFmpeg with re-encoding for compatibility
        try:
            yield None, "🔄 Method 1: Creating video list file..."
            
            # Create a temporary file list for ffmpeg
            filelist_path = "./outputs/falVideos/video_list.txt"
            with open(filelist_path, 'w') as f:
                for video in existing_videos:
                    # Use forward slashes and absolute path
                    abs_path = os.path.abspath(video).replace('\\', '/')
                    f.write(f"file '{abs_path}'\n")
            
            yield None, "🔄 Method 1: Merging with re-encoding..."
            
            # More robust ffmpeg command with re-encoding
            ffmpeg_cmd = [
                'ffmpeg', '-f', 'concat', '-safe', '0', 
                '-i', filelist_path,
                '-c:v', 'libx264',  # Re-encode video
                '-c:a', 'aac',      # Re-encode audio
                '-r', '30',         # Set frame rate
                '-pix_fmt', 'yuv420p',  # Set pixel format
                '-y', merged_video_path
            ]
            
            # Run ffmpeg command
            result = subprocess.run(ffmpeg_cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=120)
            
            # Clean up temporary file
            if os.path.exists(filelist_path):
                os.remove(filelist_path)
            
            if result.returncode == 0 and os.path.exists(merged_video_path):
                yield merged_video_path, f"✅ Successfully merged {len(existing_videos)} videos with re-encoding!"
                return
            else:
                yield None, f"⚠️ Method 1 failed, trying alternative approach..."
                time.sleep(1.0)
                
        except subprocess.TimeoutExpired:
            yield None, "⚠️ Method 1 timed out, trying alternative approach..."
        except FileNotFoundError:
            yield None, "⚠️ FFmpeg not found, trying alternative approach..."
        
        # Try Method 2: Simple concatenation without re-encoding
        try:
            yield None, "🔄 Method 2: Simple concatenation..."
            
            # Create file list again
            filelist_path = "./outputs/falVideos/video_list.txt"
            with open(filelist_path, 'w') as f:
                for video in existing_videos:
                    abs_path = os.path.abspath(video).replace('\\', '/')
                    f.write(f"file '{abs_path}'\n")
            
            # Simple copy command
            ffmpeg_cmd = [
                'ffmpeg', '-f', 'concat', '-safe', '0', 
                '-i', filelist_path, '-c', 'copy', 
                '-y', merged_video_path
            ]
            
            result = subprocess.run(ffmpeg_cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=60)
            
            if os.path.exists(filelist_path):
                os.remove(filelist_path)
            
            if result.returncode == 0 and os.path.exists(merged_video_path):
                yield merged_video_path, f"✅ Successfully merged {len(existing_videos)} videos with simple concatenation!"
                return
            else:
                yield None, f"⚠️ Method 2 also failed, trying Python-based approach..."
                time.sleep(1.0)
                
        except Exception as e:
            yield None, f"⚠️ Method 2 failed: {str(e)}, trying Python approach..."
        
        # Try Method 3: Python-based merging using existing combineVideos logic
        try:
            yield None, "🔄 Method 3: Python-based video merging..."
            
            # Import moviepy for video processing
            try:
                from moviepy.editor import VideoFileClip, concatenate_videoclips
                
                yield None, "🔄 Loading video clips..."
                clips = []
                for video_path in existing_videos:
                    clip = VideoFileClip(video_path)
                    clips.append(clip)
                
                yield None, "🔄 Concatenating clips..."
                final_clip = concatenate_videoclips(clips)
                
                yield None, "🔄 Writing merged video..."
                final_clip.write_videofile(merged_video_path, logger=None)
                
                # Clean up clips
                for clip in clips:
                    clip.close()
                final_clip.close()
                
                if os.path.exists(merged_video_path):
                    yield merged_video_path, f"✅ Successfully merged {len(existing_videos)} videos using MoviePy!"
                    return
                    
            except ImportError:
                yield None, "⚠️ MoviePy not available, using simple fallback..."
            
        except Exception as e:
            yield None, f"⚠️ Python method failed: {str(e)}, using fallback..."
        
        # Fallback: Create a simple merged video using first video
        yield None, "🔄 Fallback: Using first video as merged result..."
        import shutil
        shutil.copy2(existing_videos[0], merged_video_path)
        yield merged_video_path, f"⚠️ Created merged video using first video (merging failed - check video compatibility)"
            
    except Exception as e:
        yield None, f"❌ Error merging videos: {str(e)}"

def load_video_from_local() -> tuple:
    """Load single video from local files (legacy function for compatibility)."""
    try:
        # Check if the video file exists
        if not os.path.exists(VIDEO_PATH):
            return None, f"❌ Video file not found at {VIDEO_PATH}"
        
        return VIDEO_PATH, "✅ Video loaded successfully!"
        
    except Exception as e:
        return None, f"❌ Error loading video: {str(e)}"

def create_gradio_interface():
    """Create and configure the Gradio interface."""
    
    with gr.Blocks(title="Tell Me Your Story", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 🎬 Tell Me Your Story")
        gr.Markdown("Transform your story ideas into visual narratives with pre-generated screenplays, images, and videos!")
                
        # Frame 1: Story Input and Screenplay Loading
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📝 Frame 1: Your Story")
                user_prompt = gr.Textbox(
                    label="Enter your story prompt (max 10 sentences)",
                    value="In the first scene, there is a girl sitting on a bench in a gym wearing a pink gym outfit and she says she is tired. In the second scene, she is in another area of the gym wearing the same clothes and she just dropped a weight and drops it on her foot. The weight is next to her foot and she is looking at it and says OUCH. In the third scene, the girl is still standing next to the weight wearing the same outfit but now she's looking up towards a good looking man that tells her do you need help.",
                    lines=5,
                    max_lines=10
                )
                load_screenplay_btn = gr.Button("📖 Generate Screenplay", variant="primary")
                screenplay_status = gr.Textbox(label="Status", interactive=False)
        
        # Frame 2: Screenplay Display and Image Loading
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📖 Frame 2: Loaded Screenplay")
                screenplay_display = gr.Textbox(
                    label="Screenplay",
                    lines=10,
                    max_lines=15,
                    interactive=False
                )
                load_images_btn = gr.Button("🖼️ Generate Images", variant="primary")
                images_status = gr.Textbox(label="Status", interactive=False)
        
        # Frame 3: Image Display and Video Loading
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 🖼️ Frame 3: Scene Images")
                image_gallery = gr.Gallery(
                    label="Scene Images",
                    columns=3,
                    rows=1,
                    height="auto"
                )
                load_video_btn = gr.Button("🎥 Generate Videos", variant="primary")
                video_status = gr.Textbox(label="Status", interactive=False)
        
        # Frame 4: Video Display (3 columns)
        with gr.Row():
            gr.Markdown("## 🎥 Frame 4: Generated Videos")
        
        with gr.Row():
            with gr.Column(scale=1):
                video_display_1 = gr.Video(
                    label="Video 1",
                    height=300
                )
            with gr.Column(scale=1):
                video_display_2 = gr.Video(
                    label="Video 2", 
                    height=300
                )
            with gr.Column(scale=1):
                video_display_3 = gr.Video(
                    label="Video 3",
                    height=300
                )
        
        with gr.Row():
            merge_videos_btn = gr.Button("🔗 Merge All Videos", variant="secondary", size="lg")
        
        # Frame 5: Merged Video Display
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 🎞️ Frame 5: Merged Video")
                merged_video_display = gr.Video(
                    label="Merged Video",
                    height=400
                )
                merged_video_status = gr.Textbox(label="Merge Status", interactive=False)
        
        # Event handlers
        load_screenplay_btn.click(
            fn=load_screenplay_with_typewriter,
            inputs=[user_prompt],
            outputs=[screenplay_display, screenplay_status],
            show_progress=False
        )
        
        load_images_btn.click(
            fn=load_images_with_typewriter_effect,
            inputs=[],
            outputs=[image_gallery, images_status],
            show_progress=False
        )
        
        load_video_btn.click(
            fn=load_videos_into_columns,
            inputs=[],
            outputs=[video_display_1, video_display_2, video_display_3, video_status],
            show_progress=False
        )
        
        merge_videos_btn.click(
            fn=merge_all_videos,
            inputs=[],
            outputs=[merged_video_display, merged_video_status],
            show_progress=False
        )
        
        # Instructions
        with gr.Row():
            gr.Markdown("""
            ## 📋 Instructions:
            1. **Frame 1**: Enter your story prompt (max 5 sentences) and click "📖 Load Screenplay" to load a screenplay with typewriter effect
            2. **Frame 2**: Watch the screenplay load with typewriter animation (8 seconds), then click "🖼️ Load Images" 
            3. **Frame 3**: Watch images load progressively (5 seconds each, 15 seconds total), then click "🎥 Generate Videos"
            4. **Frame 4**: Watch videos load into 3 separate columns (similar to images), then click "🔗 Merge All Videos" to combine them
            5. **Frame 5**: View the merged video that combines all individual videos into one seamless film!
            
            **Note**: All content is loaded from local files in the `outputs/` directory. No API keys required!
            
            **Features**:
            - ✨ **Screenplay Typewriter Effect**: Loads progressively over 8 seconds for dramatic effect
            - 🖼️ **Progressive Image Loading**: Each image loads over 5 seconds with progress tracking
            - 🎬 **Column Video Display**: Videos load into 3 separate columns for side-by-side viewing
            - 🔗 **Video Merging**: Combines all videos into a single merged video file
            - 📁 **Local Files**: All content from existing files
            - 🎯 **Real-time Progress**: Percentage and status updates for all loading phases
            
            **Available Files**:
            - Screenplays: `outputs/screenplay*.txt`
            - Images: `outputs/openAIImages/image0.png`, `image1.png`, `image2.png`
            - Videos: `outputs/falVideos/video0.mp4`, `video1.mp4`, `video2.mp4` (displayed in 3 columns)
            - Merged: `outputs/falVideos/merged_video.mp4` (created after merging)
            """)
    
    return app

if __name__ == "__main__":
    # Create and launch the Gradio interface
    app = create_gradio_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    ) 