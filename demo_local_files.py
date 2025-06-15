#!/usr/bin/env python3
"""
Demo script to test the local file functionality of the Gradio interface.
"""

import os
from gradio_app import load_screenplay_with_typewriter, load_images_with_typewriter_effect, load_images_from_local, load_videos_sequentially, load_video_from_local, AVAILABLE_VIDEOS

def demo_local_functionality():
    print("🎬 Tell Me Your Story - Local File Demo")
    print("=" * 50)
    
    # Test screenplay loading
    print("\n📝 Testing screenplay loading...")
    test_prompt = "A brave knight embarks on a quest to save the kingdom from an ancient evil."
    print("Note: The typewriter effect will be demonstrated in the Gradio interface.")
    
    # Get the final result from the generator
    result_generator = load_screenplay_with_typewriter(test_prompt)
    final_result = None
    for result in result_generator:
        final_result = result
    
    if final_result:
        screenplay_content, screenplay_status = final_result
        print(f"Status: {screenplay_status}")
        if screenplay_content:
            print(f"Screenplay preview: {screenplay_content[:200]}...")
    
    # Test image loading
    print("\n🖼️ Testing image loading...")
    print("Note: The progressive image typewriter effect will be demonstrated in the Gradio interface.")
    
    # Get the final result from the generator (using legacy function for demo)
    image_paths, image_status = load_images_from_local()
    print(f"Status: {image_status}")
    if image_paths:
        print(f"Found {len(image_paths)} images:")
        for i, path in enumerate(image_paths):
            file_size = os.path.getsize(path) / (1024 * 1024)  # MB
            print(f"  {i+1}. {path} ({file_size:.1f} MB)")
    
    print("For typewriter effect testing, run: python test_image_typewriter.py")
    
    # Test video loading
    print("\n🎥 Testing video loading...")
    print("Note: The sequential video playback will be demonstrated in the Gradio interface.")
    
    # Check available videos
    existing_videos = [v for v in AVAILABLE_VIDEOS if os.path.exists(v)]
    print(f"📹 Found {len(existing_videos)} videos for sequential playback:")
    for i, video_path in enumerate(existing_videos):
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        print(f"  {i+1}. {os.path.basename(video_path)} ({file_size:.1f} MB)")
    
    if not existing_videos:
        print("❌ No videos found for sequential playback!")
    else:
        print(f"✅ Sequential playback will show {len(existing_videos)} videos one by one")
    
    print("For sequential video testing, run: python test_sequential_videos.py")
    
    print("\n✅ Demo completed! The Gradio interface should work with these files.")
    print("\nTo start the Gradio interface, run:")
    print("  python run_gradio.py")
    print("  or")
    print("  python gradio_app.py")

if __name__ == "__main__":
    demo_local_functionality() 