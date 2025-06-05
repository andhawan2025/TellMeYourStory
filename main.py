import argparse

import generateScreenplay
import processScreenplay
import generateSceneImagesOpenAI
import getPrompts

screenplay_file_path = "./outputs/screenplay.txt"
prompts_file_path = "./prompts/prompts.json"
together_api_key = ""
openai_api_key = ""

def main():
    print ("Generating the screenplay for story", args.story_number)
    story_prompt = getPrompts.get_story_prompt(args.story_number)
    screenplay_prompt = getPrompts.get_screenplay_prompt()
    screenplay = generateScreenplay.generate_screenplay(story_prompt, screenplay_prompt, together_api_key)
    print ("Screenplay generated successfully.")
    
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
    
    print ("Generating image prompts")
    i = 0
    image_prompts = []
    for scene in scenes:
        image_prompts.append (processScreenplay.create_scene_prompt(scene))
        i += 1
    print ("Image prompts generated successfully")
    
    print ("Generating the images for the scenes")
    i = 0
    images = []
    image_paths = []
    for prompt in image_prompts:
        image_paths.append ("./outputs/openAIImages/image" + str(i) + ".png")
        images.append (generateSceneImagesOpenAI.generate_scene_image_gpt41mini (prompt, image_paths[i], openai_api_key))
        print ("Image ", i, " generated and saved to ", image_paths[i])
        i += 1
    print ("Images generated and downloaded successfully.")

    #print ("Generating video prompts for the scenes")
    #i = 0
    #video_prompts = []
    #for scene in scenes:
    #    video_prompts.append (processScreenplay.create_video_prompt(scene))
    #    print ("\n\n", i, ":\n", video_prompts[i], "\n\n")
    #    i += 1
    #print ("Video prompts generated successfully")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--_together_api_key", type=str, default=None)
    parser.add_argument("-o", "--openai_api_key", type=str, default=None)
    #parser.add_argument("-r", "--runway_api_key", type=str, default=None)
    parser.add_argument("-s", "--story_number", type=int, default=None)
    args = parser.parse_args()

    together_api_key = args._together_api_key
    openai_api_key = args.openai_api_key

    main()