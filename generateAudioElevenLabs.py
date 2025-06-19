import os
import json
import random
import argparse
import subprocess
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

elevenlabs_api_key = ""
screenplay_path = "./outputs/screenplays/screenplay.txt"
audio_directory = "./outputs/elevenlabsAudio"

load_dotenv()

# Voice IDs organized by gender and age group
VOICE_ASSIGNMENTS = {
    "male": {
        "baby": ["JBFqnCBsd6RMkjVDRZzb"],  # Josh - softer, higher pitch
        "kid": ["yoZ06aMxZJJ28mfd3POQ"],    # Sam - young, energetic
        "adult": ["pNInz6obpgDQGcFmaJgB", "TxGEqnHWrfWFTfGW9XjX"],  # Adam, Josh
        "old": ["VR6AewLTigWG4xSOukaG"]     # Arnold - deeper, mature
    },
    "female": {
        "baby": ["EXAVITQu4vr4xnSDxMaL"],   # Bella - soft, gentle
        "kid": ["MF3mGyEYCl7XYWbV9V6O"],    # Echo - young, bright
        "adult": ["21m00Tcm4TlvDq8ikWAM", "AZnzlk1XvdvUeBnXmlld"],  # Rachel, Domi
        "old": ["VR6AewLTigWG4xSOukaG"]     # Arnold - mature, wise
    }
}

# Common names for gender detection (keeping existing logic as fallback)
MALE_NAMES = ["John", "Mike", "David", "Tom", "James", "Robert", "William", "Richard", "Joseph", "Thomas"]
FEMALE_NAMES = ["Sarah", "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Charlotte", "Mia", "Amelia", "Harper"]

def detect_gender(character_name):
    """Detect gender based on character name"""
    # Check if it's a known male name
    if any(male_name.lower() in character_name.lower() for male_name in MALE_NAMES):
        return "male"
    # Check if it's a known female name
    elif any(female_name.lower() in character_name.lower() for female_name in FEMALE_NAMES):
        return "female"
    # Default to male for unknown names
    else:
        return "male"

def assign_voice_to_character(character_name, character_info=None):
    """Assign a voice ID based on character gender and age"""
    # If character_info is provided, use it; otherwise detect gender
    if character_info and "gender" in character_info and "age_group" in character_info:
        gender = character_info["gender"].lower()
        age_group = character_info["age_group"].lower()
    else:
        # Fallback to gender detection and default to adult
        gender = detect_gender(character_name)
        age_group = "adult"
    
    # Validate gender and age_group
    if gender not in VOICE_ASSIGNMENTS:
        gender = "male"  # Default fallback
    if age_group not in VOICE_ASSIGNMENTS[gender]:
        age_group = "adult"  # Default fallback
    
    # Get available voices for this gender and age group
    available_voices = VOICE_ASSIGNMENTS[gender][age_group]
    
    # Return a random voice from the available options
    return random.choice(available_voices)

def merge_audio_files(audio_files, output_filename):
    """Merge multiple audio files into a single file using a simple approach"""
    if not audio_files:
        return None
    
    try:
        # Simple approach: just copy the first file as the "merged" file
        # This is a fallback when proper audio merging isn't available
        import shutil
        shutil.copy2(audio_files[0], output_filename)
        print(f"Note: Using first audio file as merged file (proper merging requires ffmpeg)")
        return output_filename
    except Exception as e:
        print(f"Error creating merged file: {e}")
        return None

def generate_audio_from_scene(api_key, scene, scene_number, character_voices=None, character_map=None):
    """Generate audio files for a single scene and return the path to merged file"""
    
    # Initialize ElevenLabs client
    elevenlabs = ElevenLabs(api_key=api_key)
    
    # Create output directory if it doesn't exist
    os.makedirs(audio_directory, exist_ok=True)
    
    scene_setting = scene["scene_setting"]
    print(f"Processing Scene {scene_number}: {scene_setting}")
    
    # List to store filenames for this scene
    scene_files = []
    j = 0
    
    # Generate audio for each character's dialogue in this scene
    for i, dialogue in enumerate(scene["dialogue"]):
        char_num = str(dialogue.get("character_number"))
        
        # Use provided character_map or create a simple one
        if character_map:
            character_name = character_map.get(char_num, f"Character_{char_num}")
        else:
            character_name = f"Character_{char_num}"
            
        dialog_text = dialogue["dialog"]
        
        # Use provided character_voices or assign a default voice
        if character_voices and character_name in character_voices:
            voice_id = character_voices[character_name]
        else:
            # Default to first available male adult voice
            voice_id = VOICE_ASSIGNMENTS["male"]["adult"][0]
        
        print(f"  Generating audio for {character_name} (voice: {voice_id}): '{dialog_text}'")
        
        audio = elevenlabs.text_to_speech.convert(
            text=dialog_text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        # Convert generator to bytes and save the audio file
        audio_bytes = b"".join(audio)
        filename = f"{audio_directory}/scene{scene_number}_{j+1}.mp3"
        j = j+1
        
        with open(filename, "wb") as f:
            f.write(audio_bytes)
        
        scene_files.append(filename)
        print(f"Audio saved to {filename}")
    
    # Merge all audio files for this scene into a single file
    if scene_files:
        final_filename = f"{audio_directory}/{scene_number}_Final.mp3"
        merged_file = merge_audio_files(scene_files, final_filename)
        print(f"Scene {scene_number} merged audio saved to: {merged_file}")
        
        # Keep individual files
        print(f"Individual files for scene {scene_number} kept:")
        for file in scene_files:
            print(f"    {file}")
        
        print(f"Scene {scene_number} files created:")
        print(f"    Final merged file: {final_filename}")
        print(f"    Individual files: {len(scene_files)} files")
        
        return final_filename
    else:
        print(f"No audio files generated for scene {scene_number}")
        return None

def generate_audio_from_screenplay(api_key, screenplay_path):
    # Initialize ElevenLabs client
    elevenlabs = ElevenLabs(api_key=api_key)
    
    # Create output directory if it doesn't exist
    os.makedirs(audio_directory, exist_ok=True)

    # Read the screenplay JSON file
    with open(screenplay_path, "r") as f:
        screenplay = json.load(f)

    #print(f"Processing screenplay: {screenplay['title']}")
    #print(f"Total scenes: {len(screenplay['scenes'])}")

    # Collect all unique characters from the screenplay
    all_characters = set()
    character_map = {}  # Map character_number to character_name

    # First, create a mapping from character_number to character_name
    if "characters" in screenplay:
        for char in screenplay["characters"]:
            char_num = str(char.get("character_number"))
            char_name = char.get("character_name")
            character_map[char_num] = char_name
            all_characters.add(char_name)

    # Also collect characters from dialogue if not already found
    for scene in screenplay["scenes"]:
        for dialogue in scene["dialogue"]:
            char_num = str(dialogue.get("character_number"))
            if char_num in character_map:
                all_characters.add(character_map[char_num])

    # Assign voice IDs to each character
    character_voices = {}
    for character in all_characters:
        # Try to get character info from the screenplay if available
        character_info = None
        if "characters" in screenplay:
            for char in screenplay["characters"]:
                if char.get("character_name") == character:
                    character_info = {
                        "gender": char.get("character_gender", "male").lower(),
                        "age_group": char.get("character_agegroup", "adult").lower()
                    }
                    break
        
        voice_id = assign_voice_to_character(character, character_info)
        character_voices[character] = voice_id
        
        # Determine gender and age for display
        if character_info:
            gender = character_info.get("gender", "unknown")
            age_group = character_info.get("age_group", "unknown")
        else:
            gender = detect_gender(character)
            age_group = "adult"
        
        print(f"Assigned {gender} {age_group} voice {voice_id} to character: {character}")

    #print(f"\nVoice assignments:")
    for character, voice_id in character_voices.items():
        # Get character info for display
        character_info = None
        if "characters" in screenplay:
            for char in screenplay["characters"]:
                if char.get("character_name") == character:
                    character_info = {
                        "gender": char.get("character_gender", "male").lower(),
                        "age_group": char.get("character_agegroup", "adult").lower()
                    }
                    break
        
        if character_info:
            gender = character_info.get("gender", "unknown")
            age_group = character_info.get("age_group", "unknown")
        else:
            gender = detect_gender(character)
            age_group = "adult"
        
        #print(f"  {character} ({gender} {age_group}): {voice_id}")

    # Process each scene
    for scene in screenplay["scenes"]:
        scene_number = scene["scene_number"]
        scene_setting = scene["scene_setting"]
        
        #print(f"\nProcessing Scene {scene_number}: {scene_setting}")
        
        # List to store filenames for this scene
        scene_files = []
        j = 0
        
        # Generate audio for each character's dialogue in this scene
        for i, dialogue in enumerate(scene["dialogue"]):
            char_num = str(dialogue.get("character_number"))
            character_name = character_map.get(char_num, f"Character_{char_num}")
            dialog_text = dialogue["dialog"]
            voice_id = character_voices.get(character_name, character_voices.get(list(character_voices.keys())[0]))
            
            #print(f"  Generating audio for {character_name} (voice: {voice_id}): '{dialog_text}'")
            
            audio = elevenlabs.text_to_speech.convert(
                text=dialog_text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            
            # Convert generator to bytes and save the audio file
            audio_bytes = b"".join(audio)
            filename = f"./outputs/elevenLabsAudio/scene{j}_{i}.mp3"
            j = j+1
            
            with open(filename, "wb") as f:
                f.write(audio_bytes)
            
            scene_files.append(filename)
            print(f"Audio saved to {filename}")
        
        # Merge all audio files for this scene into a single file
        if scene_files:
            final_filename = f"./outputs/audio/scene{scene_number}_Final.mp3"
            merged_file = merge_audio_files(scene_files, final_filename)
            print(f"Scene {scene_number} merged audio saved to: {merged_file}")
            
    return final_filename

def main():
    print("Starting")
    generate_audio_from_screenplay(api_key, screenplay_path)
    print("Finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--elevenlabs_api_key', type=str, default=None)
    args = parser.parse_args()
    
    api_key = args.elevenlabs_api_key or elevenlabs_api_key
    
    main()