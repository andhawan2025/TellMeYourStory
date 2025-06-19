import argparse
import json
import re
import os

import generateScreenplay
import processScreenplay
import generateScenesImagesFlux
import generateVideoFal
import generateAudioElevenLabs

screenplay_file_path = "./outputs/screenplays/screenplay.txt"
screenplay_data_file_path = "./outputs/screenplays/screenplay_data.json"
prompts_file_path = "./prompts/prompts.json"
image_file_path = "./outputs/fluxImages"

together_api_key = ""  # text to screenplay
openai_api_key = "" # screenplay to images
elevenlabs_api_key = "" # text to audio
fal_api_key = "" # images to video

def check_file_exists(file_path):
    """
    Check if a file exists and is not empty.
    
    Args:
        file_path (str): Path to the file to check
        
    Returns:
        bool: True if file exists and is not empty, False otherwise
    """
    return os.path.exists(file_path) and os.path.getsize(file_path) > 0

def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, create it if it doesn't.
    
    Args:
        directory_path (str): Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def parse_xml_screenplay_to_dict(xml_content):
    """
    Parse XML screenplay content into a Python dictionary using regular expressions.
    
    Args:
        xml_content (str): XML content as string
        
    Returns:
        dict: Parsed screenplay as dictionary
    """
    try:
        # Clean the XML content by removing any leading text before <screenplay>
        start_tag = xml_content.find('<screenplay>')
        end_tag = xml_content.rfind('</screenplay>')
        
        if start_tag == -1 or end_tag == -1:
            raise ValueError("Could not find <screenplay> tags in the content")
        
        # Extract only the XML part
        xml_part = xml_content[start_tag:end_tag + len('</screenplay>')]
        
        # Initialize the dictionary structure
        screenplay_dict = {
            "title": "",
            "characters": [],
            "scenes": []
        }
        
        # Parse title using regex
        title_match = re.search(r'<title>(.*?)</title>', xml_part, re.DOTALL)
        if title_match:
            screenplay_dict["title"] = title_match.group(1).strip()
        
        # Parse characters using regex
        characters_match = re.search(r'<characters>(.*?)</characters>', xml_part, re.DOTALL)
        if characters_match:
            characters_content = characters_match.group(1)
            # Find all character blocks
            character_blocks = re.findall(r'<character>(.*?)</character>', characters_content, re.DOTALL)
            
            for character_block in character_blocks:
                character = {}
                
                # Extract character_number
                char_num_match = re.search(r'<character_number>(.*?)</character_number>', character_block)
                if char_num_match:
                    character["character_number"] = int(char_num_match.group(1).strip())
                
                # Extract character_name
                char_name_match = re.search(r'<character_name>(.*?)</character_name>', character_block)
                if char_name_match:
                    character["character_name"] = char_name_match.group(1).strip()
                
                # Extract character_gender
                char_gender_match = re.search(r'<character_gender>(.*?)</character_gender>', character_block)
                if char_gender_match:
                    character["character_gender"] = char_gender_match.group(1).strip()
                
                # Extract character_agegroup
                char_age_match = re.search(r'<character_agegroup>(.*?)</character_agegroup>', character_block)
                if char_age_match:
                    character["character_agegroup"] = char_age_match.group(1).strip()
                
                screenplay_dict["characters"].append(character)
        
        # Parse scenes using regex
        scenes_match = re.search(r'<scenes>(.*?)</scenes>', xml_part, re.DOTALL)
        if scenes_match:
            scenes_content = scenes_match.group(1)
            # Find all scene blocks
            scene_blocks = re.findall(r'<scene>(.*?)</scene>', scenes_content, re.DOTALL)
            
            for scene_block in scene_blocks:
                scene = {}
                
                # Extract scene_number
                scene_num_match = re.search(r'<scene_number>(.*?)</scene_number>', scene_block)
                if scene_num_match:
                    scene["scene_number"] = int(scene_num_match.group(1).strip())
                
                # Extract scene_characters
                scene_chars_match = re.search(r'<scene_characters>(.*?)</scene_characters>', scene_block, re.DOTALL)
                if scene_chars_match:
                    scene["scene_characters"] = []
                    char_nums = re.findall(r'<character_number>(.*?)</character_number>', scene_chars_match.group(1))
                    for char_num in char_nums:
                        scene["scene_characters"].append(int(char_num.strip()))
                
                # Extract scene_setting
                scene_setting_match = re.search(r'<scene_setting>(.*?)</scene_setting>', scene_block, re.DOTALL)
                if scene_setting_match:
                    scene["scene_setting"] = scene_setting_match.group(1).strip()
                
                # Extract dialogue
                dialogue_match = re.search(r'<dialogue>(.*?)</dialogue>', scene_block, re.DOTALL)
                if dialogue_match:
                    scene["dialogue"] = []
                    dialogue_content = dialogue_match.group(1)
                    # Find all dialogue_entry blocks
                    dialogue_entries = re.findall(r'<dialogue_entry>(.*?)</dialogue_entry>', dialogue_content, re.DOTALL)
                    
                    for dialogue_entry_block in dialogue_entries:
                        dialogue_entry = {}
                        
                        # Extract character_number from dialogue
                        dialog_char_match = re.search(r'<character_number>(.*?)</character_number>', dialogue_entry_block)
                        if dialog_char_match:
                            dialogue_entry["character_number"] = dialog_char_match.group(1).strip()
                        
                        # Extract dialog
                        dialog_match = re.search(r'<dialog>(.*?)</dialog>', dialogue_entry_block, re.DOTALL)
                        if dialog_match:
                            dialogue_entry["dialog"] = dialog_match.group(1).strip()
                        
                        scene["dialogue"].append(dialogue_entry)
                
                screenplay_dict["scenes"].append(scene)
        
        return screenplay_dict
        
    except Exception as e:
        print(f"Error parsing XML screenplay: {e}")
        return None

def clean_screenplay_content(content):
    """
    Clean the screenplay content by removing any extra text and repetitive instructions.
    
    Args:
        content (str): Raw screenplay content
        
    Returns:
        str: Cleaned XML content
    """
    # Find the start and end of the actual screenplay XML
    start_tag = content.find('<screenplay>')
    end_tag = content.rfind('</screenplay>')
    
    if start_tag == -1 or end_tag == -1:
        return content
    
    # Extract only the XML part
    xml_part = content[start_tag:end_tag + len('</screenplay>')]
    
    return xml_part

def main():
    # Ensure output directories exist
    ensure_directory_exists("./outputs/screenplays")
    ensure_directory_exists("./outputs/fluxImages")
    ensure_directory_exists("./outputs/falVideos")
    ensure_directory_exists("./outputs/elevenlabsAudio")

    # Step 1: Get user input.
    # user input is read from the story_number variable

    # Step 2: Generate the screenplay.
    if args.reset or not check_file_exists(screenplay_file_path):
        print ("Generating the screenplay for story ", args.story_number)
        story_prompt = generateScreenplay.get_story_prompt(args.story_number)
        screenplay_prompt = generateScreenplay.get_screenplay_prompt()
        screenplay = generateScreenplay.generate_screenplay(story_prompt, screenplay_prompt, together_api_key)
        print ("Screenplay generated successfully.")
        
        # Clean and store the screenplay
        cleaned_screenplay = clean_screenplay_content(str(screenplay))
        with open(screenplay_file_path, "w") as f:
            f.write(cleaned_screenplay)
        print ("Screenplay stored successfully\n")
    else:
        print ("Screenplay file already exists, skipping generation.")

    # Step 3: Load the screenplay and parse XML to dictionary
    if args.reset or not check_file_exists(screenplay_data_file_path):
        print ("Loading the screenplay and parsing XML to dictionary")
        with open(screenplay_file_path, "r") as f:
            screenplay_content = f.read()
        
        screenplay_data = parse_xml_screenplay_to_dict(screenplay_content)
        
        if screenplay_data is None:
            print("Failed to parse screenplay XML. Exiting.")
            return
        
        # save screenplay_data to a json file
        with open(screenplay_data_file_path, "w") as f:
            json.dump(screenplay_data, f, indent=4)
        print ("Screenplay data saved successfully")
    else:
        print ("Loading existing screenplay data from JSON")
        with open(screenplay_data_file_path, "r") as f:
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
        print (i, ":\n", image_prompts[i], "\n")
        i += 1
    print ("Image prompts generated successfully")
    
    # Step 5(a): Generate the images for the scenes: Open AI
    #print ("Generating images for the scenes using Open AI")
    #i = 0
    #for prompt in image_prompts:
    #    image_paths.append ("./outputs/openAIImages/image" + str(i) + ".png")
    #    images.append (generateSceneImagesOpenAI.generate_scene_image_gpt41mini (prompt, image_paths[i], openai_api_key))
    #    print ("Image ", i, " generated and saved to ", image_paths[i])
    #    i += 1
    #print ("Images generated and downloaded successfully.")

    # Step 5(b): Generate the images for the scenes: Flux
    print ("Generating images for the scenes using Flux")
    i = 0
    images = []
    image_paths = []
    for prompt in image_prompts:
        image_path = "./outputs/fluxImages/image" + str(i) + ".webp"
        image_paths.append(image_path)
        
        if args.reset or not check_file_exists(image_path):
            images.append(generateScenesImagesFlux.generate_and_download_flux_scene_image(prompt, i))
            print ("Image ", i, " generated and saved to ", image_paths[i])
        else:
            print ("Image ", i, " already exists, skipping generation.")
        i += 1
    print ("Images processing completed.\n")

    # Step 6: Generate the video prompts for the scenes
    print ("Generating video prompts for the scenes")
    i = 0
    video_prompts = []
    for scene in scenes:
        video_prompts.append (processScreenplay.create_video_prompt(scene, characters_list))
        print ( i, ":\n", video_prompts[i], "\n")
        i += 1
    print ("Video prompts generated successfully\n")

    # Step 7: Generate the videos and audio files for each scenes and overlay the audio on the video
    print ("Generating videos for the scenes")
    i = 0
    videos = []
    for scene in scenes:
        video_path = "./outputs/falVideos/video" + str(i) + ".mp4"
        
        if args.reset or not check_file_exists(video_path):
            videos.append(generateVideoFal.generate_fal_video_from_image(video_prompts[i], image_paths[i], fal_api_key, video_path))
            print (i, ": ", videos[i])
        else:
            print ("Video ", i, " already exists, skipping generation.")
        i += 1
    
    
    print ("Videos processing completed.")

    # Step 8: Generate the audio for the scenes
    print ("Generating audio for all the scenes")
    audio_output_dir = "./outputs/elevenlabsAudio"
    
    # Check if audio files exist (this is a simplified check - you might want to check for specific audio files)
    if args.reset or not os.path.exists(audio_output_dir) or len(os.listdir(audio_output_dir)) == 0:
        generateAudioElevenLabs.generate_audio_from_screenplay(elevenlabs_api_key, screenplay_data_file_path)
        print ("Audio generated and saved successfully.")
    else:
        print ("Audio files already exist, skipping generation.")


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