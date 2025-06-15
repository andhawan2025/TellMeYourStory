#!/usr/bin/env python3
"""
Run the Tell Me Your Story Gradio application.
"""

import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gradio_app import create_gradio_interface

def main():
    print("🎬 Starting Tell Me Your Story Application...")
    print("📋 Local file-based version - no API keys required!")
    print("📁 Make sure you have the following files:")
    print("   - Screenplay files in ./outputs/ (screenplay*.txt)")
    print("   - Image files in ./outputs/openAIImages/ (image0.png, image1.png, image2.png)")
    print("   - Video file in ./outputs/falVideos/ (video0.mp4)")
    print()
    
    app = create_gradio_interface()
    
    try:
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=True,
            show_error=True
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    main() 