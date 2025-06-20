import argparse
import json
import xml.etree.ElementTree as ET
import re

import generateScreenplay
import processScreenplay
import generateScenesImagesFlux
import generateVideoFal
import generateAudioElevenLabs

screenplay_file_path = "./outputs/screenplays/screenplay.txt"
prompts_file_path = "./prompts/prompts.json"
image_file_path = "./outputs/fluxImages"

together_api_key = ""  # text to screenplay
openai_api_key = "" # screenplay to images
elevenlabs_api_key = "" # text to audio
fal_api_key = "" # images to video

def parse_xml_screenplay_to_dict(xml_content):
    """
    Parse XML screenplay content into a Python dictionary.
    
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
        
        # Parse XML
        root = ET.fromstring(xml_part)
        
        # Initialize the dictionary structure
        screenplay_dict = {
            "title": "",
            "characters": [],
            "scenes": []
        }
        
        # Parse title
        title_elem = root.find('title')
        if title_elem is not None:
            screenplay_dict["title"] = title_elem.text.strip()
        
        # Parse characters
        characters_elem = root.find('characters')
        if characters_elem is not None:
            for character_elem in characters_elem.findall('character'):
                character = {}
                for child in character_elem:
                    if child.tag == 'character_number':
                        character[child.tag] = int(child.text.strip())
                    else:
                        character[child.tag] = child.text.strip()
                screenplay_dict["characters"].append(character)
        
        # Parse scenes
        scenes_elem = root.find('scenes')
        if scenes_elem is not None:
            for scene_elem in scenes_elem.findall('scene'):
                scene = {}
                
                # Parse scene number
                scene_number_elem = scene_elem.find('scene_number')
                if scene_number_elem is not None:
                    scene["scene_number"] = int(scene_number_elem.text.strip())
                
                # Parse scene characters
                scene_characters_elem = scene_elem.find('scene_characters')
                if scene_characters_elem is not None:
                    scene["scene_characters"] = []
                    for char_num_elem in scene_characters_elem.findall('character_number'):
                        scene["scene_characters"].append(int(char_num_elem.text.strip()))
                
                # Parse scene setting
                scene_setting_elem = scene_elem.find('scene_setting')
                if scene_setting_elem is not None:
                    scene["scene_setting"] = scene_setting_elem.text.strip()
                
                # Parse dialogue
                dialogue_elem = scene_elem.find('dialogue')
                if dialogue_elem is not None:
                    scene["dialogue"] = []
                    for dialogue_entry_elem in dialogue_elem.findall('dialogue_entry'):
                        dialogue_entry = {}
                        for child in dialogue_entry_elem:
                            if child.tag == 'character_number':
                                dialogue_entry[child.tag] = child.text.strip()
                            else:
                                dialogue_entry[child.tag] = child.text.strip()
                        scene["dialogue"].append(dialogue_entry)
                
                screenplay_dict["scenes"].append(scene)
        
        return screenplay_dict
        
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return None
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
    # Step 1: Get user input.
    # user input is read from the story_number variable

    # Step 2: Generate the screenplay.
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

    # Step 3: Load the screenplay and parse XML to dictionary
    print ("Loading the screenplay and parsing XML to dictionary")
    with open(screenplay_file_path, "r") as f:
        screenplay_content = f.read()
    
    screenplay_data = parse_xml_screenplay_to_dict(screenplay_content)
    
    if screenplay_data is None:
        print("Failed to parse screenplay XML. Exiting.")
        return
    
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
        image_paths.append ("./outputs/fluxImages/image" + str(i) + ".webp")
        images.append (generateScenesImagesFlux.generate_and_download_flux_scene_image(prompt, i))
        print ("Image ", i, " generated and saved to ", image_paths[i])
        i += 1
    print ("Images generated and downloaded successfully.\n")

    # Step 6: Generate the video prompts for the scenes
    print ("Generating video prompts for the scenes")
    i = 0
    video_prompts = []
    for scene in scenes:
        video_prompts.append (processScreenplay.create_video_prompt(scene, characters_list))
        print ( i, ":\n", video_prompts[i], "\n")
        i += 1
    print ("Video prompts generated successfully\n")

    # Step 7: Generate the videos for the scenes
    #print ("Generating videos for the scenes")
    #i = 0
    #videos = []
    #for scene in scenes:
    #    videos.append (generateVideoFal.generate_fal_video_from_image(video_prompts[i], image_paths[i], fal_api_key, "./outputs/falVideos/video" + str(i) + ".mp4"))
    #    print (i, ": ", videos[i])
    #    i += 1
    #print ("Videos generated and downloaded successfully.")

    # Step 8: Generate the audio for the scenes
    print ("Generating audio for all the scenes")
    generateAudioElevenLabs.generate_audio_from_screenplay(elevenlabs_api_key, screenplay_file_path)
    print ("Audio generated and saved successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--_together_api_key", type=str, default=None)
    parser.add_argument("-o", "--openai_api_key", type=str, default=None)
    parser.add_argument("-f", "--fal_api_key", type=str, default=None)
    parser.add_argument("-e", "--elevenlabs_api_key", type=str, default=None)
    parser.add_argument("-s", "--story_number", type=int, default=None)
    args = parser.parse_args()

    together_api_key = args._together_api_key
    openai_api_key = args.openai_api_key
    fal_api_key = args.fal_api_key
    elevenlabs_api_key = args.elevenlabs_api_key

    main()