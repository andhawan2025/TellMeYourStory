#!/usr/bin/env python3
"""
Test script to verify the sequential video playback functionality.
"""

import time
import os
from gradio_app import load_videos_sequentially, AVAILABLE_VIDEOS

def test_sequential_video_loading():
    print("🎬 Testing Sequential Video Playback")
    print("=" * 40)
    
    # Check which videos exist
    existing_videos = [v for v in AVAILABLE_VIDEOS if os.path.exists(v)]
    print(f"📹 Available videos: {len(existing_videos)}")
    for i, video in enumerate(existing_videos):
        size_mb = os.path.getsize(video) / (1024 * 1024)
        print(f"  {i+1}. {os.path.basename(video)} ({size_mb:.1f} MB)")
    
    if not existing_videos:
        print("❌ No videos found to test!")
        return
    
    print(f"\n🎥 Testing sequential playback of {len(existing_videos)} videos...")
    print("⏱️  Starting timer...")
    
    start_time = time.time()
    update_count = 0
    video_changes = 0
    current_video = None
    
    # Run the sequential video playback and track changes
    for video_path, status in load_videos_sequentially():
        update_count += 1
        current_time = time.time() - start_time
        
        # Detect when video changes
        if video_path != current_video and video_path is not None:
            video_changes += 1
            current_video = video_path
            video_name = os.path.basename(video_path) if video_path else "None"
            print(f"🎬 {current_time:.1f}s - Video #{video_changes} started: {video_name}")
        
        # Show status updates
        if "Loading" in status or "✅" in status:
            print(f"📺 {current_time:.1f}s - Update #{update_count} - {status}")
    
    total_time = time.time() - start_time
    
    print(f"\n📊 Results:")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Total updates: {update_count}")
    print(f"   Video changes: {video_changes}")
    print(f"   Expected videos: {len(existing_videos)}")
    print(f"   Average time per video: {total_time / max(1, video_changes):.2f} seconds")
    
    if video_changes == len(existing_videos):
        print("✅ All expected videos were played!")
    else:
        print(f"⚠️  Expected {len(existing_videos)} videos, but played {video_changes}")
    
    if total_time <= (len(existing_videos) * 6):  # Rough estimate: ~6 seconds per video
        print("✅ Sequential video timing is reasonable!")
    else:
        print("⚠️  Sequential video timing might be too slow")

if __name__ == "__main__":
    test_sequential_video_loading() 