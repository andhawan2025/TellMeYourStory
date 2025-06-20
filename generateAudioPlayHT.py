import requests
import os
import json
import random

PLAYHT_API_KEY = "ak-aed6fbc348524361a4b97c27dec2d980"
#PLAYHT_USER_ID = "ak-aed6fbc348524361a4b97c27dec2d980"
PLAYHT_USER_ID = "lBdguWJw2XMv3xZ8itKEfd1WV1y1"

def generate_audio_playht(text, voice, playht_api_key, output_file_path):
    url = "https://api.play.ai/api/v1/tts"

    payload = {
        "model": "PlayDialog",
        "text": text,
        "voice": voice,
        "voice2": voice,
        "outputFormat": "mp3",
        "speed": 1,
        "sampleRate": 44100,
        "seed": None,
        "temperature": None,
    }

    # Use the correct authentication headers as required by PlayHT API
    headers = {
        "AUTHORIZATION": PLAYHT_API_KEY,
        "X-API-KEY": PLAYHT_API_KEY,
        "X-USER-ID": PLAYHT_USER_ID,
        "Content-Type": "application/json"
    }

    print(f"Making request to: {url}")

    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response body: {response.text[:500]}...")
    
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Save the audio content to file
    with open(output_file_path, "wb") as f:
        f.write(response.content)
    
    print(f"Audio saved to: {output_file_path}")
    return output_file_path

# Voice assignments for different character types
VOICE_ASSIGNMENTS = {
    "male": {
        "baby": ["s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"],
        "kid": ["s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"],
        "adult": ["s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"],
        "old": ["s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"]
    },
    "female": {
        "baby": ["s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"],
        "kid": ["s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"],
        "adult": ["s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"],
        "old": ["s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"]
    }
}

def assign_voice_to_character(character_info):
    """Assign a voice ID based on character gender and age"""
    # If character_info is provided, use it; otherwise default to male adult
    if character_info and "gender" in character_info and "age_group" in character_info:
        gender = character_info["gender"].lower()
        age_group = character_info["age_group"].lower()
    else:
        # Fallback to gender detection and default to adult
        gender = "male"
        age_group = "adult"
    
    # Get available voices for this gender and age group
    available_voices = VOICE_ASSIGNMENTS[gender][age_group]
    
    # Return a random voice from the available options
    return random.choice(available_voices)

def generate_audio_for_scene_dialogues(playht_api_key, scene, output_audio_directory, character_list):
    """
    Generate audio files for all dialogues in a scene using PlayHT
    
    Args:
        playht_api_key (str): PlayHT API key
        scene (dict): Scene data containing dialogues
        output_audio_directory (str): Directory to save audio files
        character_list (list): List of character information
    
    Returns:
        list: List of audio file paths generated for this scene
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_audio_directory, exist_ok=True)
    
    scene_number = scene.get("scene_number", 0)
    print(f"Generating audio for Scene {scene_number}")
    
    # List to store file paths for this scene
    audio_file_paths = []
    
    # Generate audio for each dialogue in the scene
    for i, dialogue in enumerate(scene.get("dialogue", [])):
        char_num = str(dialogue.get("character_number", i))
        
        # Get character info from character_list
        character_info = None
        character_name = f"Character_{char_num}"
        
        # Find character in character_list
        for char in character_list:
            if str(char.get("character_number")) == str(char_num):
                character_name = char.get("character_name", f"Character_{char_num}")
                character_info = {
                    "gender": char.get("character_gender", "male").lower(),
                    "age_group": char.get("character_agegroup", "adult").lower()
                }
                break
        
        if not character_info:
            # Fallback to default character info
            character_info = {
                "gender": "male",  # Default gender
                "age_group": "adult"  # Default age group
            }
            
        dialog_text = dialogue.get("dialog", "")
        
        if not dialog_text.strip():
            print(f"  Skipping empty dialogue for {character_name}")
            continue
        
        # Assign voice based on character info
        voice_id = assign_voice_to_character(character_info)
        
        # Generate filename for this dialogue
        filename = f"scene{scene_number}_{i+1}.mp3"
        file_path = os.path.join(output_audio_directory, filename)
        
        print(f"  Generating audio for {character_name} (voice: {voice_id}): '{dialog_text[:50]}...'")
        
        # Generate audio using PlayHT API
        result = generate_audio_playht(dialog_text, voice_id, playht_api_key, file_path)
        
        if result:
            audio_file_paths.append(result)
            print(f"  Audio saved to {result}")
        else:
            print(f"  Error generating audio for {character_name}")
            # Continue with next dialogue even if one fails
            continue
    
    print(f"Generated {len(audio_file_paths)} audio files for Scene {scene_number}")
    return audio_file_paths

def process_screenplay_and_generate_audio(screenplay_file_path, output_audio_directory):
    """
    Read screenplay JSON file and generate audio for all dialogues in all scenes
    
    Args:
        screenplay_file_path (str): Path to the screenplay JSON file
        output_audio_directory (str): Directory to save all audio files
    
    Returns:
        dict: Dictionary containing all generated audio files organized by scene
    """
    print(f"Reading screenplay from: {screenplay_file_path}")
    
    # Read the screenplay JSON file
    with open(screenplay_file_path, 'r', encoding='utf-8') as f:
        screenplay_data = json.load(f)
    
    # Extract characters and scenes
    characters = screenplay_data.get("characters", [])
    scenes = screenplay_data.get("scenes", [])
    
    print(f"Found {len(characters)} characters and {len(scenes)} scenes")
    print("Characters:", [char["character_name"] for char in characters])
    
    # Create output directory
    os.makedirs(output_audio_directory, exist_ok=True)
    
    # Dictionary to store all generated audio files
    all_audio_files = {}
    
    # Process each scene
    for scene in scenes:
        scene_number = scene.get("scene_number", 0)
        print(f"\n{'='*50}")
        print(f"Processing Scene {scene_number}")
        print(f"Setting: {scene.get('scene_setting', 'No setting')}")
        print(f"Characters: {scene.get('scene_characters', [])}")
        print(f"Dialogues: {len(scene.get('dialogue', []))}")
        print(f"{'='*50}")
        
        # Generate audio for this scene
        scene_audio_files = generate_audio_for_scene_dialogues(
            PLAYHT_API_KEY, 
            scene, 
            output_audio_directory, 
            characters
        )
        
        all_audio_files[f"scene_{scene_number}"] = scene_audio_files
    
    print(f"\n{'='*50}")
    print("AUDIO GENERATION COMPLETE")
    print(f"{'='*50}")
    
    # Summary
    total_files = sum(len(files) for files in all_audio_files.values())
    print(f"Total audio files generated: {total_files}")
    
    for scene_key, files in all_audio_files.items():
        print(f"{scene_key}: {len(files)} files")
    
    return all_audio_files

def main():
    print("PlayHT Audio Generation Module")
    
    # Define file paths
    screenplay_file = "./outputs/screenplays/screenplay.json"
    output_directory = "./outputs/audios/"
    
    # Process the screenplay and generate audio
    result = process_screenplay_and_generate_audio(screenplay_file, output_directory)
    
    if result:
        print("\nAudio generation completed successfully!")
        print(f"Check the output directory: {output_directory}")
    else:
        print("\nAudio generation failed!")

if __name__ == "__main__":
    main()
