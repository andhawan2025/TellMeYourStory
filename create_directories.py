#!/usr/bin/env python3
"""
Script to create all required output directories for the TellMeYourStory Flask app.
"""

import os
import utils

def create_all_directories():
    """Create all required output directories"""
    
    # Define all the directories that need to be created
    directories = [
        "./prompts/",
        "./outputs/",
        "./outputs/screenplays/",
        "./outputs/images/",
        "./outputs/videos/",
        "./outputs/audios/",
        "./outputs/combined/"
    ]
    
    print("Creating required directories...")
    
    for directory in directories:
        try:
            utils.ensure_directory_exists(directory)
            print(f"✓ Created/verified directory: {directory}")
        except Exception as e:
            print(f"✗ Error creating directory {directory}: {e}")
    
    print("\nAll directories have been created successfully!")
    
    # List the created directories
    print("\nCreated directories:")
    for directory in directories:
        if os.path.exists(directory):
            print(f"  {directory}")
        else:
            print(f"  {directory} (FAILED TO CREATE)")

if __name__ == "__main__":
    create_all_directories() 