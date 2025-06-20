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

PROMPTS_FILE_NAME = "storyPrompts.txt"
SCREENPLAY_PROMPT_FILE_NAME = "ScreenplayPrompt.txt"
SCREENPLAY_TXT_FILENAME = "screenplay.txt"
SCREENPLAY_JSON_FILENAME = "screenplay.json"
COMBINED_VIDEO_FILENAME = "combined_video_final.mp4"

together_api_key = ""  # text to screenplay
openai_api_key = "" # screenplay to images
elevenlabs_api_key = "" # text to audio
fal_api_key = "" # images to video

screenplay = None
scenes = []
characters_list = []

def setup_directories():
    """Step 0: Ensure all output directories exist"""
    utils.ensure_directory_exists(PROMPTS_SOURCE_DIRECTORY)
    utils.ensure_directory_exists(SCREENPLAY_OUTPUT_DIR)
    utils.ensure_directory_exists(IMAGES_OUTPUT_DIR)
    utils.ensure_directory_exists(VIDEOS_OUTPUT_DIR)
    utils.ensure_directory_exists(AUDIO_OUTPUT_DIR)
    utils.ensure_directory_exists(COMBINED_OUTPUT_DIR)

def generate_screenplay_step(story_number, story_prompt_path, screenplay_prompt_path, screenplay_output_path):
    print(story_prompt_path)
    print(screenplay_prompt_path)
    """Step 1: Generate the screenplay"""
    if args.reset or not utils.check_file_exists(screenplay_output_path):
        print("Generating the screenplay for story", story_number)
        story_prompt = generateScreenplay.get_story_prompt(story_number, story_prompt_path)
        screenplay_prompt = generateScreenplay.get_screenplay_prompt(screenplay_prompt_path)
        screenplay = generateScreenplay.generate_screenplay(story_prompt, screenplay_prompt, together_api_key)
        print("Screenplay generated successfully.")
        
        # Clean and store the screenplay
        cleaned_screenplay = utils.clean_screenplay_content(str(screenplay))
        with open(screenplay_output_path, "w") as f:
            f.write(cleaned_screenplay)
        print("Screenplay stored successfully\n")
    else:
        print("Screenplay file already exists, skipping generation.")

def parse_screenplay_step(screenplay_output_path_txt, screenplay_output_path_json):
    """
    Step 2: Load and parse the screenplay XML to dictionary.
    Read XML from TXT file and store it in JSON file.
    """
    if args.reset or not utils.check_file_exists(screenplay_output_path_json):
        print("Loading the screenplay and parsing XML to dictionary")
        with open(screenplay_output_path_txt, "r") as f:
            screenplay_content = f.read()
        
        screenplay_data = utils.parse_xml_screenplay_to_dict(screenplay_content)
        
        if screenplay_data is None:
            print("Failed to parse screenplay XML. Exiting.")
            return None
        
        # save screenplay_data to a json file
        with open(screenplay_output_path_json, "w") as f:
            json.dump(screenplay_data, f, indent=4)
        print("Screenplay data saved successfully")
    else:
        print("Loading existing screenplay data from JSON")
        with open(screenplay_output_path_json, "r") as f:
            screenplay_data = json.load(f)
    
    return screenplay_data

def generate_image_prompts_step(scenes, characters_list):
    """Step 3: Generate image prompts for the scenes"""
    print("Generating image prompts")
    image_prompts = []
    for scene in scenes:
        image_prompts.append(processScreenplay.create_scene_prompt(scene, characters_list))
    print("Image prompts generated successfully")
    return image_prompts

def generate_images_step(image_prompts):
    """Step 4: Generate images for the scenes using Flux"""
    print("Generating images for the scenes using Flux")
    images = []
    image_paths = []
    for i, prompt in enumerate(image_prompts):
        image_path = IMAGES_OUTPUT_DIR + "image" + str(i) + ".webp"
        image_paths.append(image_path)
        
        if args.reset or not utils.check_file_exists(image_path):
            images.append(generateScenesImagesFlux.generate_and_download_flux_scene_image(prompt, image_path))
            print("Image", i, "generated and saved to", image_paths[i])
        else:
            print("Image", i, "already exists, skipping generation.")
    print("Images processing completed.\n")
    return image_paths

def generate_audio_step(scenes, character_list):
    """Step 5: Generate audio for all the scenes"""
    print("Generating audio for all the scenes")
    print(character_list)
    
    audio_files = []
    
    # Check if audio files exist (this is a simplified check - you might want to check for specific audio files)
    if args.reset or not os.path.exists(AUDIO_OUTPUT_DIR) or len(os.listdir(AUDIO_OUTPUT_DIR)) == 0:
        for scene in scenes:
            audio_files.append(generateAudioElevenLabs.generate_audio_for_scene_dialogues(elevenlabs_api_key, scene, AUDIO_OUTPUT_DIR, character_list))
        print("Audio generated and saved successfully.")
    else:
        print("Audio files already exist, skipping generation.")
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
    
    return audio_files

def generate_video_prompts_step(scenes, characters_list):
    """Step 6: Generate video prompts for the scenes"""
    print("Generating video prompts for the scenes")
    video_prompts = []
    for i, scene in enumerate(scenes):
        video_prompts.append(processScreenplay.create_video_prompt(scene, characters_list))
    print("Video prompts generated successfully\n")
    return video_prompts

def generate_videos_step(scenes, video_prompts, image_paths):
    """Step 7: Generate videos for each scene"""
    print("Generating videos for the scenes")
    videos = []
    for i, scene in enumerate(scenes):
        video_path = VIDEOS_OUTPUT_DIR + "video" + str(i) + ".mp4"
        
        if args.reset or not utils.check_file_exists(video_path):
            videos.append(generateVideoFal.generate_fal_video_from_image(video_prompts[i], image_paths[i], fal_api_key, video_path))
            print(i, ":", videos[i])
        else:
            print("Video", i, "already exists, skipping generation.")
    print("Videos processing completed.")
    return videos

def overlay_audio_step(scenes, audio_files):
    """Step 8: Overlay audio on videos"""
    print("Overlaying the audio on the video")
    
    # List to store the paths of videos with audio overlay
    videos_with_audio = []
    
    for i, scene in enumerate(scenes):
        video_path = VIDEOS_OUTPUT_DIR + "video" + str(i) + ".mp4"
        scene_audio_files = audio_files[i] if i < len(audio_files) else []
        
        if scene_audio_files:
            output_file_name = f"combined_video{i}.mp4"
            output_file_path = COMBINED_OUTPUT_DIR
            
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
    return videos_with_audio

def combine_videos_step(videos_with_audio):
    """Step 9: Combine all videos into a single video"""
    print("Combining the videos into a single video")
    
    combined_video_path = os.path.join(COMBINED_OUTPUT_DIR, COMBINED_VIDEO_FILENAME)
    
    if args.reset or not utils.check_file_exists(combined_video_path):
        videoAudioOverlay.combineVideos(videos_with_audio, COMBINED_OUTPUT_DIR, COMBINED_VIDEO_FILENAME)
        print("Videos combined successfully")
    else:
        print("Combined video already exists, skipping combination.")

def main():
    # Step 0: Setup directories
    setup_directories()
    
    # Step 1: Get user input and generate screenplay
    story_number = args.story_number
    story_prompt_path = PROMPTS_SOURCE_DIRECTORY + PROMPTS_FILE_NAME
    screenplay_prompt_path = PROMPTS_SOURCE_DIRECTORY + SCREENPLAY_PROMPT_FILE_NAME
    screenplay_output_path = SCREENPLAY_OUTPUT_DIR + SCREENPLAY_TXT_FILENAME
    screenplay_output_path_json = SCREENPLAY_OUTPUT_DIR + SCREENPLAY_JSON_FILENAME

    generate_screenplay_step(story_number, story_prompt_path, screenplay_prompt_path, screenplay_output_path)
    
    # Step 2: Parse screenplay
    screenplay_data = parse_screenplay_step(screenplay_output_path, screenplay_output_path_json)
    if screenplay_data is None:
        return
    
    characters_list = screenplay_data.get("characters", [])
    scenes = screenplay_data.get("scenes", [])
    
    #print(len(scenes), "scenes loaded successfully")
    #print(len(characters_list), "characters loaded successfully")
    #print("Characters:", characters_list, "\n")
    
    # Step 3: Generate image prompts
    image_prompts = generate_image_prompts_step(scenes, characters_list)
    
    # Step 4: Generate images
    image_paths = generate_images_step(image_prompts)
    
    # Step 5: Generate audio
    audio_files = generate_audio_step(scenes, characters_list)
    
    # Step 6: Generate video prompts
    video_prompts = generate_video_prompts_step(scenes, characters_list)
    
    # Step 7: Generate videos
    videos = generate_videos_step(scenes, video_prompts, image_paths)
    
    # Step 8: Overlay audio on videos
    videos_with_audio = overlay_audio_step(scenes, audio_files)
    
    # Step 9: Combine all videos
    combine_videos_step(videos_with_audio)

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