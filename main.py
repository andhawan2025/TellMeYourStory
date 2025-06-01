import argparse

import generateScreenplay
import processScreenplay
import generateScenesImages
import getPrompts

screenplay_file_path = "./outputs/screenplay.txt"
prompts_file_path = "./prompts/prompts.json"
together_api_key = ""
runway_api_key = ""
RUNWAY_API_URL = "https://api.runwayml.com/v1/generate"

def main():
    print ("Generating the screenplay for story", args.story_number)
    story_prompt = getPrompts.get_story_prompt(args.story_number)
    screenplay_prompt = getPrompts.get_screenplay_prompt()
    screenplay = generateScreenplay.generate_screenplay(story_prompt, screenplay_prompt, together_api_key)
    
    #Ensure any leading text in LLM response is removed.
    screenplay_json_string = str(screenplay)
    start_index = screenplay_json_string.find('{')
    if start_index != -1:
        substring = screenplay_json_string[start_index:]
    else:
        substring = screenplay_json_string

    with open(screenplay_file_path, "w") as f:
        f.write(substring)
    print ("Screenplay stored successfully")

    print ("Generating the scenes for the screenplay")
    scenes = processScreenplay.get_scenes_from_screenplay(screenplay_file_path)
    print (len(scenes), "scenes generated successfully")
    
    print ("Generating prompts")
    i = 0
    prompts = []
    for scene in scenes:
        prompts.append (processScreenplay.create_scene_prompt(scene))
        i += 1
    print ("Prompts generated successfully")
    
    print ("Generating the images for the scenes")
    i = 0
    images = []
    image_paths = []
    for prompt in prompts:
        images.append (generateScenesImages.generate_scene_image(prompt))
        image_paths.append(generateScenesImages.download_scene_image(images[i], i))
        i += 1
    print ("Images generated and downloaded successfully.")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--_together_api_key", type=str, default=None)
    #parser.add_argument("-r", "--runway_api_key", type=str, default=None)
    parser.add_argument("-s", "--story_number", type=int, default=None)
    args = parser.parse_args()

    together_api_key = args._together_api_key
    #runway_api_key = args.runway_api_key

    main()