#!/usr/bin/env python3
"""
Test script to verify the typewriter effect timing.
"""

import time
from gradio_app import load_screenplay_with_typewriter

def test_typewriter_timing():
    print("🎬 Testing Typewriter Effect Timing")
    print("=" * 40)
    
    test_prompt = "A brave knight embarks on a quest to save the kingdom from an ancient evil."
    
    print(f"📝 Testing with prompt: '{test_prompt}'")
    print("⏱️  Starting timer...")
    
    start_time = time.time()
    update_count = 0
    
    # Run the typewriter effect and count updates
    for screenplay_content, status in load_screenplay_with_typewriter(test_prompt):
        update_count += 1
        current_time = time.time() - start_time
        
        # Show progress every few updates to avoid spam
        if update_count % 10 == 0 or "✅" in status:
            progress = len(screenplay_content) if screenplay_content else 0
            print(f"⏱️  {current_time:.1f}s - Update #{update_count} - {progress} chars - {status}")
    
    total_time = time.time() - start_time
    
    print(f"\n📊 Results:")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Total updates: {update_count}")
    print(f"   Target time: 8.0 seconds")
    print(f"   Time difference: {abs(total_time - 8.0):.2f} seconds")
    
    if total_time <= 8.5:  # Allow small margin for processing
        print("✅ Typewriter timing is within acceptable range!")
    else:
        print("⚠️  Typewriter timing might be too slow")

if __name__ == "__main__":
    test_typewriter_timing() 