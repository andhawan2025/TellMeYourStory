import os
import json
import random
import argparse
import subprocess
from elevenlabs import ElevenLabs

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

def generate_audio_for_scene_dialogues(elevenlabs_api_key, scene, output_audio_directory, character_list):

    # Set the API key
    elevenlabs = ElevenLabs(api_key=elevenlabs_api_key)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_audio_directory, exist_ok=True)
    
    scene_number = scene.get("scene_number", 0)
    print(f"Generating audio for Scene {scene_number}")
    
    # List to store file paths for this scene
    audio_file_paths = []
    
    print(character_list)

    # Generate audio for each dialogue in the scene
    for i, dialogue in enumerate(scene.get("dialogue", [])):
        char_num = str(dialogue.get("character_number", i))
        print(f"Character number for dialogue {i}: {char_num}")
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
                print(f"Character info: {character_name}: {character_info}")
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
        
        # Assign voice based on character info using the assign_voice_to_character function
        voice_id = assign_voice_to_character(character_info)
        
        # Generate filename for this dialogue
        filename = f"scene{scene_number}_{i+1}.mp3"
        file_path = os.path.join(output_audio_directory, filename)
        
        print(f"  Generating audio for {character_name} (voice: {voice_id}): '{dialog_text[:50]}...'")
        
        # Generate audio using ElevenLabs API
        audio = elevenlabs.text_to_speech.convert(
            text=dialog_text,
            voice_id=voice_id,
            #model="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        # Convert generator to bytes
        audio_bytes = b''.join(audio)
        
        # Save the audio file
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        
        audio_file_paths.append(file_path)
        print(f"  Audio saved to {file_path}")

    print(f"Generated {len(audio_file_paths)} audio files for Scene {scene_number}")
    return audio_file_paths

def main():
    print("Starting")
    #generate_audio_from_screenplay(api_key, screenplay_path)
    print("Finished")

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-e', '--elevenlabs_api_key', type=str, default=None)
    #parser.add_argument('-s', '--screenplay_path', type=str, default=None)
    #args = parser.parse_args()
    
    #api_key = args.elevenlabs_api_key or elevenlabs_api_key
    #screenplay_path = args.screenplay_path

    main()