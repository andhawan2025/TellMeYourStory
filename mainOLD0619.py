import argparse
import json
import re
import os

import generateScreenplay
import processScreenplay
import generateScenesImagesFlux
import generateVideoFal
import generateAudioElevenLabs
import videoAudioOverlay
import utils

PROMPTS_SOURCE_DIRECTORY = "./prompts/"


SCREENPLAY_OUTPUT_DIR = "./outputs/screenplays/"
IMAGES_OUTPUT_DIR = "./outputs/images/"
VIDEOS_OUTPUT_DIR = "./outputs/videos/"
AUDIO_OUTPUT_DIR = "./outputs/audios/"
COMBINED_OUTPUT_DIR = "./outputs/combined/"

PROMPTS_FILE_NAME = "prompts.json"
SCREENPLAY_TXT_FILENAME = "screenplay.txt"
SCREENPLAY_JSON_FILENAME = "screenplay.json"
COMBINED_VIDEO_FILENAME = "combined_video_final.mp4"

together_api_key = ""  # text to screenplay
openai_api_key = "" # screenplay to images
elevenlabs_api_key = "" # text to audio
fal_api_key = "" # images to video

screenplay = None
scenes = []
character_list = []

def main():
    # Ensure output directories exist
    utils.ensure_directory_exists(PROMPTS_SOURCE_DIRECTORY)
    utils.ensure_directory_exists(SCREENPLAY_OUTPUT_DIR)
    utils.ensure_directory_exists(IMAGES_OUTPUT_DIR)
    utils.ensure_directory_exists(VIDEOS_OUTPUT_DIR)
    utils.ensure_directory_exists(AUDIO_OUTPUT_DIR)
    utils.ensure_directory_exists(COMBINED_OUTPUT_DIR)

    # Step 1: Get user input.
    # User input is read from the story_number variable
    story_number = args.story_number

    # Step 2: Generate the screenplay.
    if args.reset or not utils.check_file_exists(SCREENPLAY_OUTPUT_DIR + SCREENPLAY_TXT_FILENAME):
        print ("Generating the screenplay for story ", story_number)
        story_prompt = generateScreenplay.get_story_prompt(story_number)
        screenplay_prompt = generateScreenplay.get_screenplay_prompt()
        screenplay = generateScreenplay.generate_screenplay(story_prompt, screenplay_prompt, together_api_key)
        print ("Screenplay generated successfully.")
        
        # Clean and store the screenplay
        cleaned_screenplay = utils.clean_screenplay_content(str(screenplay))
        with open(SCREENPLAY_OUTPUT_DIR + SCREENPLAY_TXT_FILENAME, "w") as f:
            f.write(cleaned_screenplay)
        print ("Screenplay stored successfully\n")
    else:
        print ("Screenplay file already exists, skipping generation.")

    # Step 3: Load the screenplay and parse XML to dictionary
    if args.reset or not utils.check_file_exists(SCREENPLAY_OUTPUT_DIR + SCREENPLAY_JSON_FILENAME):
        print ("Loading the screenplay and parsing XML to dictionary")
        with open(SCREENPLAY_OUTPUT_DIR + SCREENPLAY_TXT_FILENAME, "r") as f:
            screenplay_content = f.read()
        
        screenplay_data = utils.parse_xml_screenplay_to_dict(screenplay_content)
        
        if screenplay_data is None:
            print("Failed to parse screenplay XML. Exiting.")
            return
        
        # save screenplay_data to a json file
        with open(SCREENPLAY_OUTPUT_DIR + SCREENPLAY_JSON_FILENAME, "w") as f:
            json.dump(screenplay_data, f, indent=4)
        print ("Screenplay data saved successfully")
    else:
        print ("Loading existing screenplay data from JSON")
        with open(SCREENPLAY_OUTPUT_DIR + SCREENPLAY_JSON_FILENAME, "r") as f:
            screenplay_data = json.load(f)
    
    characters_list = screenplay_data.get("characters", [])
    scenes = screenplay_data.get("scenes", [])
    
    print (len(scenes), "scenes loaded successfully")
    print (len(characters_list), "characters loaded successfully")
    print ("Characters:", [char["character_name"] for char in characters_list], "\n")
    
    
    # Step 4: Generate the image prompts for the scenes
    print ("Generating image prompts")
    i = 0
    image_prompts = []
    for scene in scenes:
        image_prompts.append (processScreenplay.create_scene_prompt(scene, characters_list))
        i += 1
    print ("Image prompts generated successfully")
    
    
  

    # Step 5: Generate the images for the scenes: Flux
    print ("Generating images for the scenes using Flux")
    i = 0
    images = []
    image_paths = []
    for prompt in image_prompts:
        image_path = IMAGES_OUTPUT_DIR + "image" + str(i) + ".webp"
        image_paths.append(image_path)
        
        if args.reset or not utils.check_file_exists(image_path):
            images.append(generateScenesImagesFlux.generate_and_download_flux_scene_image(prompt, image_path))
            print ("Image ", i, " generated and saved to ", image_paths[i])
        else:
            print ("Image ", i, " already exists, skipping generation.")
        i += 1
    print ("Images processing completed.\n")

    # Step 6: Generate the audio for the scenes
    print ("Generating audio for all the scenes")
    
    audio_files = []
    
    # Check if audio files exist (this is a simplified check - you might want to check for specific audio files)
    if args.reset or not os.path.exists(AUDIO_OUTPUT_DIR) or len(os.listdir(AUDIO_OUTPUT_DIR)) == 0:
        for scene in scenes:
            audio_files.append(generateAudioElevenLabs.generate_audio_for_scene_dialogues(elevenlabs_api_key, scene, AUDIO_OUTPUT_DIR, character_list))
        print ("Audio generated and saved successfully.")
    else:
        print ("Audio files already exist, skipping generation.")
        # Initialize audio_files with existing files
        for i in range(len(scenes)):
            scene_audio_files = []
            # Look for audio files for this scene
            scene_audio_dir = AUDIO_OUTPUT_DIR
            if os.path.exists(scene_audio_dir):
                for file in os.listdir(scene_audio_dir):
                    if file.startswith(f"scene{i+1}_") and file.endswith(".mp3"):
                        scene_audio_files.append(os.path.join(scene_audio_dir, file))
                # Sort by dialogue number
                scene_audio_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
            audio_files.append(scene_audio_files)
    
    # Step 7: Generate the video prompts for the scenes
    print ("Generating video prompts for the scenes")
    i = 0
    video_prompts = []
    for scene in scenes:
        video_prompts.append (processScreenplay.create_video_prompt(scene, characters_list))
        print ( i, ":\n", video_prompts[i], "\n")
        i += 1
    print ("Video prompts generated successfully\n")

    
    #Step 7: Generate the videos files for each scene
    print ("Generating videos for the scenes")
    i = 0
    videos = []
    for scene in scenes:
        video_path = VIDEOS_OUTPUT_DIR + "video" + str(i) + ".mp4"
        
        if args.reset or not utils.check_file_exists(video_path):
            videos.append(generateVideoFal.generate_fal_video_from_image(video_prompts[i], image_paths[i], fal_api_key, video_path))
            print (i, ": ", videos[i])
        else:
            print ("Video ", i, " already exists, skipping generation.")
        i += 1
    print ("Videos processing completed.")
    
    
    #Step 8: Overlay the audio on the video
    print ("Overlaying the audio on the video")
    
    # List to store the paths of videos with audio overlay
    videos_with_audio = []
    
    for i, scene in enumerate(scenes):
        video_path = VIDEOS_OUTPUT_DIR + "video" + str(i) + ".mp4"
        scene_audio_files = audio_files[i] if i < len(audio_files) else []
        
        if scene_audio_files:
            output_file_name = f"combined_video{i}.mp4"
            output_file_path = COMBINED_OUTPUT_DIR
            
            print(f"Overlaying audio on video {i} with {len(scene_audio_files)} audio files")
            
            # Check if combined video already exists
            combined_video_path = os.path.join(output_file_path, output_file_name)
            if args.reset or not utils.check_file_exists(combined_video_path):
                try:
                    videoAudioOverlay.overlay_audio_on_video(
                        video_path, 
                        scene_audio_files, 
                        output_file_path, 
                        output_file_name, 
                        start_time=0
                    )
                    print(f"Video {i} with audio overlay saved to {combined_video_path}")
                except Exception as e:
                    print(f"Error overlaying audio on video {i}: {e}")
                    # If overlay fails, use the original video path
                    combined_video_path = video_path
            else:
                print(f"Combined video {i} already exists, skipping overlay.")
            
            videos_with_audio.append(combined_video_path)
        else:
            print(f"No audio files found for scene {i}, using original video")
            videos_with_audio.append(video_path)
    
    print(f"Audio overlay completed. {len(videos_with_audio)} videos processed.")
    print("Videos with audio overlay:", videos_with_audio)
    
    #Step 9: Combine the videos into a single video
    print ("Combining the videos into a single video")
    videoAudioOverlay.combineVideos(videos_with_audio, COMBINED_OUTPUT_DIR, COMBINED_VIDEO_FILENAME)
    print ("Videos combined successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--_together_api_key", type=str, default=None)
    parser.add_argument("-o", "--openai_api_key", type=str, default=None)
    parser.add_argument("-f", "--fal_api_key", type=str, default=None)
    parser.add_argument("-e", "--elevenlabs_api_key", type=str, default=None)
    parser.add_argument("-s", "--story_number", type=int, default=None)
    parser.add_argument("-r", "--reset", action="store_true", help="Reset and regenerate all files")
    args = parser.parse_args()

    together_api_key = args._together_api_key
    openai_api_key = args.openai_api_key
    fal_api_key = args.fal_api_key
    elevenlabs_api_key = args.elevenlabs_api_key

    main()