#!/usr/bin/env python3
"""
Test script to verify the image typewriter effect timing.
"""

import time
from gradio_app import load_images_with_typewriter_effect

def test_image_typewriter_timing():
    print("🖼️ Testing Image Typewriter Effect Timing")
    print("=" * 45)
    
    print("📸 Testing progressive image loading...")
    print("⏱️  Starting timer...")
    
    start_time = time.time()
    update_count = 0
    image_count = 0
    last_image_count = 0
    
    # Run the image typewriter effect and count updates
    for images, status in load_images_with_typewriter_effect():
        update_count += 1
        current_time = time.time() - start_time
        current_image_count = len(images)
        
        # Detect when a new image is added
        if current_image_count > last_image_count:
            image_count = current_image_count
            print(f"🖼️  {current_time:.1f}s - Image #{image_count} completed!")
            last_image_count = current_image_count
        
        # Show progress every few updates to avoid spam
        if update_count % 10 == 0 or "✅" in status:
            print(f"⏱️  {current_time:.1f}s - Update #{update_count} - {len(images)} images - {status}")
    
    total_time = time.time() - start_time
    
    print(f"\n📊 Results:")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Total updates: {update_count}")
    print(f"   Images loaded: {image_count}")
    print(f"   Expected time: ~15.0 seconds (3 images × 5 seconds each)")
    print(f"   Time difference: {abs(total_time - 15.0):.2f} seconds")
    print(f"   Average time per image: {total_time / max(1, image_count):.2f} seconds")
    
    if total_time <= 17.0:  # Allow margin for processing (15s + 2s buffer)
        print("✅ Image typewriter timing is within acceptable range!")
    else:
        print("⚠️  Image typewriter timing might be too slow")
    
    if image_count == 3:
        print("✅ All expected images were loaded!")
    else:
        print(f"⚠️  Expected 3 images, but loaded {image_count}")

if __name__ == "__main__":
    test_image_typewriter_timing() 