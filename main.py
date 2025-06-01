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
    #print ("Generating the screenplay for the story prompt", args.story_number)
    #story_prompt = getPrompts.get_story_prompt(args.story_number)
    #screenplay_prompt = getPrompts.get_screenplay_prompt()
    #screenplay = generateScreenplay.generate_screenplay(story_prompt, screenplay_prompt, together_api_key)
    
    #Ensure any leading text in LLM response is removed.
    #screenplay_json_string = str(screenplay)
    #start_index = screenplay_json_string.find('{')

    #if start_index != -1:
    #    substring = screenplay_json_string[start_index:]
    #else:
    #    substring = screenplay_json_string

    #substring = screenplay_json_string

    
    #print ("Storing the screenplay in a file")
    #with open(screenplay_file_path, "w") as f:
    #    f.write(substring)
    #print ("Screenplay stored in a file successfully\n\n")

    print ("Generating the scenes for the screenplay")
    scenes = processScreenplay.get_scenes_from_screenplay(screenplay_file_path)
    print ("Scenes generated successfully")
    print(len(scenes))
    
    #i = 0
    #prompts = []
    #print ("Generating prompts")
    
    #for scene in scenes:
    #    print ("Generating prompt for scene", i )
    #    prompts.append (processScreenplay.create_scene_prompt(scene))
    #    print (prompts[i], "\n\n")
    #    i += 1

    #print (prompts[2])

    #i = 0
    #images = []
    
    #for prompt in prompts:
        #print ("Generating the image for the scene", i)
        #images.append (generateScenesImages.generate_scene_image(prompt))
        #print (images[i])
        #print ("Image for scene", i, "generated successfully")
        #print ("Downloading the image for scene", i)
        #generateScenesImages.download_scene_image(images[i])
        #print ("Image for scene", i, "downloaded successfully")
        #i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--_together_api_key", type=str, default=None)
    #parser.add_argument("-r", "--runway_api_key", type=str, default=None)
    parser.add_argument("-s", "--story_number", type=int, default=None)
    args = parser.parse_args()

    together_api_key = args._together_api_key
    #runway_api_key = args.runway_api_key

    main()