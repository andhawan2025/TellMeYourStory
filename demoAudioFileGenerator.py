import os
import json
import random
import argparse
import subprocess
from elevenlabs import ElevenLabs
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

elevenlabs_api_key = ""

DIALOGUE_1 = "Hello and welcome to 'Tell Me Your Story' everyone. Tell me your story is all about letting anyone generate a complete video from story ideas they have. Anyone can be  content creator, thanks to this App. It's extremely simple - just enter a story prompt and Abracadabra, see your movie come to life in 3 easy steps. So let's see how it works."
DIALOGUE_2 = "We start with writing a story. I'll write a simple story about a cat and a dog going to the market and purchasing their favorite things. Here's the prompt. And that's all I need to do. Now let me put AI to work for creating these few sentences into an actual full length video."
DIALOGUE_3 = "The story is now being processed. It takes a while. There are several steps that go on behind the scenes. First, the prompt is taken and a screenplay is generated from it. I'm using Meta's Llama 3.8 to take the story and generate a screenplay. The screenplay consists of all characters in the story,  breakdown of the story into scene and the dialogues for each scene. Then, an image is created for each scene. The image has the characters and the dialogues for each scene. I'm using Flux.1 Schnell model for images. An image prompt is created and fed into the Flux model for this. Next, I use elevenlabs' text to speech convertor to get individual audio files for each dialog. I assign each character a voice ID based on their gender and age, and ensure their voice remains consistent across different scenes. Finally, I use Google's Veo to generate a video from the images and overlay the audio files on the video. The combined file is presented as the final video to the user of this app."
DIALOGUE_4 = "Here's the final video. Let's play it."
DIALOGUE_5 = "You can also see the generatd screenplay here. As mentioned before, the screenplay consists of all characters, scenes and dialogues. This story was broken down into 5 scenes. The details of all five scenes have been captured in this JSON file."
DIALOGUE_6 = "Now, each scene has one image generated for it. You can see those images here. These are the five images that were used to generate the final video you guys just saw."
DIALOGUE_7 ="So that's it folks. This was a proof of concept for Tell Me Your Story. There is more to come in the future, with much better scene continuity, character consistency, emotions and sounds effects in the videos. Hope you enjoyed it."

OUTPUT_AUDIO_DIRECTORY = "./outputs/demo/"

OUTPUT_AUDIO_FILE_1 = OUTPUT_AUDIO_DIRECTORY + "dialogue_1.mp3"
OUTPUT_AUDIO_FILE_2 = OUTPUT_AUDIO_DIRECTORY + "dialogue_2.mp3"
OUTPUT_AUDIO_FILE_3 = OUTPUT_AUDIO_DIRECTORY + "dialogue_3.mp3"
OUTPUT_AUDIO_FILE_4 = OUTPUT_AUDIO_DIRECTORY + "dialogue_4.mp3"
OUTPUT_AUDIO_FILE_SCENE = OUTPUT_AUDIO_DIRECTORY + "dialogue_scene.mp3"
OUTPUT_AUDIO_FILE_5 = OUTPUT_AUDIO_DIRECTORY + "dialogue_5.mp3"
OUTPUT_AUDIO_FILE_6 = OUTPUT_AUDIO_DIRECTORY + "dialogue_6.mp3"
OUTPUT_AUDIO_FILE_7 = OUTPUT_AUDIO_DIRECTORY + "dialogue_7.mp3"

DIALOGUE_1_OFFSET = 3
DIALOGUE_2_OFFSET = 29
DIALOGUE_3_OFFSET = 50
DIALOGUE_4_OFFSET = 119
DIALOGUE_SCENE_OFFSET = 127
DIALOGUE_5_OFFSET = 160
DIALOGUE_6_OFFSET = 182
DIALOGUE_7_OFFSET = 192

INPUT_VIDEO_FILE = "./outputs/demo/demo_video.mp4"
OUTPUT_VIDEO_FILE = "./outputs/demo/demo_video_with_audio.mp4"

def generate_audio_for_scene_dialogues(elevenlabs_api_key, input_dialogue, output_file):

    # Set the API key
    elevenlabs = ElevenLabs(api_key=elevenlabs_api_key)
    
    voice_id = "TxGEqnHWrfWFTfGW9XjX"

    # Generate audio using ElevenLabs API
    audio = elevenlabs.text_to_speech.convert(
        text=input_dialogue,
        voice_id=voice_id,
        output_format="mp3_44100_128"
    )
        
    # Convert generator to bytes
    audio_bytes = b''.join(audio)
        
    # Save the audio file
    with open(output_file, "wb") as f:
        f.write(audio_bytes)
    
    print(f"Generated audio for {output_file}")

def overlay_audio_on_video():
    # Load the video file
    video = VideoFileClip(INPUT_VIDEO_FILE)
    
    # Get the original audio from the video
    #original_audio = video.audio
    
    # Extract the specific portion of original audio (2:02 to 2:30 = 122 to 150 seconds)
    # and position it at offset 122 seconds
    #extracted_audio = original_audio.subclipped(122, 150).with_start(122)
    
    # Load the audio files and set their start times
    audio_1 = AudioFileClip(OUTPUT_AUDIO_FILE_1).with_start(DIALOGUE_1_OFFSET)
    audio_2 = AudioFileClip(OUTPUT_AUDIO_FILE_2).with_start(DIALOGUE_2_OFFSET)
    audio_3 = AudioFileClip(OUTPUT_AUDIO_FILE_3).with_start(DIALOGUE_3_OFFSET)
    audio_4 = AudioFileClip(OUTPUT_AUDIO_FILE_4).with_start(DIALOGUE_4_OFFSET)
    audio_scene = AudioFileClip(OUTPUT_AUDIO_FILE_SCENE).with_start(DIALOGUE_SCENE_OFFSET)
    audio_5 = AudioFileClip(OUTPUT_AUDIO_FILE_5).with_start(DIALOGUE_5_OFFSET)
    audio_6 = AudioFileClip(OUTPUT_AUDIO_FILE_6).with_start(DIALOGUE_6_OFFSET)
    audio_7 = AudioFileClip(OUTPUT_AUDIO_FILE_7).with_start(DIALOGUE_7_OFFSET)
    
    # Combine all dialogue audio clips and the extracted audio into a composite
    dialogue_audio = CompositeAudioClip([audio_1, audio_2, audio_3, audio_4, audio_scene, audio_5, audio_6, audio_7])
    
    # Combine original audio with dialogue audio
    # The dialogue audio will overlay on top of the original audio
    #combined_audio = CompositeAudioClip([original_audio, dialogue_audio])

    # Overlay the combined audio on the video
    video = video.with_audio(dialogue_audio)

    # Export the video
    video.write_videofile(OUTPUT_VIDEO_FILE, codec="libx264", audio_codec="aac")
    
    # Close the video file to free up resources
    video.close()

def extract_audio_segment():
    """Extract audio from demo_video.mp4 from seconds 122 to 150 and save as dialogue_scene.mp3"""
    print("Extracting audio segment from demo video...")
    
    # Load the video file
    video = VideoFileClip(INPUT_VIDEO_FILE)
    
    # Get the original audio from the video
    original_audio = video.audio
    
    # Extract the specific portion of original audio (2:02 to 2:30 = 122 to 150 seconds)
    extracted_audio = original_audio.subclipped(122, 150)
    
    # Save the extracted audio as MP3
    output_file = "./outputs/demo/dialogue_scene.mp3"
    extracted_audio.write_audiofile(output_file)
    
    # Close the video file to free up resources
    video.close()
    
    print(f"Audio segment extracted and saved to {output_file}")

def main():
    print("Starting Audio File Generation")
    #generate_audio_for_scene_dialogues(elevenlabs_api_key, DIALOGUE_1, OUTPUT_AUDIO_FILE_1)
    #generate_audio_for_scene_dialogues(elevenlabs_api_key, DIALOGUE_2, OUTPUT_AUDIO_FILE_2)
    #generate_audio_for_scene_dialogues(elevenlabs_api_key, DIALOGUE_3, OUTPUT_AUDIO_FILE_3)
    #generate_audio_for_scene_dialogues(elevenlabs_api_key, DIALOGUE_4, OUTPUT_AUDIO_FILE_4)
    #generate_audio_for_scene_dialogues(elevenlabs_api_key, DIALOGUE_5, OUTPUT_AUDIO_FILE_5)
    #generate_audio_for_scene_dialogues(elevenlabs_api_key, DIALOGUE_6, OUTPUT_AUDIO_FILE_6)
    #generate_audio_for_scene_dialogues(elevenlabs_api_key, DIALOGUE_7, OUTPUT_AUDIO_FILE_7)
    print("Finished Audio File Generation")

    print("Starting Audio Video Overlay")
    overlay_audio_on_video()
    print("Finished Audio Video Overlay")
    
    # Extract audio segment
    #extract_audio_segment()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--elevenlabs_api_key', type=str, default=None)
    args = parser.parse_args()
    
    elevenlabs_api_key = args.elevenlabs_api_key
    
    main()