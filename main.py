import argparse

import generateScreenplay
import processScreenplay
import generateSceneImagesOpenAI
import getPrompts
import generateVideoFal

screenplay_file_path = "./outputs/screenplay.txt"
prompts_file_path = "./prompts/prompts.json"
together_api_key = ""  # text to screenplay
openai_api_key = "" # screenplay to images
fal_api_key = "" # images to video

def main():
    # Step 1: Get user input.

    # Step 2: Generate the screenplay.
    print ("Generating the screenplay for story ", args.story_number)
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

    # Step 3: Generate the scenes for the screenplay
    print ("Generating the scenes for the screenplay")
    scenes = processScreenplay.get_scenes_from_screenplay(screenplay_file_path)
    print (len(scenes), "scenes generated successfully")
    
    # Step 4: Generate the image prompts for the scenes
    print ("Generating image prompts")
    i = 0
    image_prompts = []
    for scene in scenes:
        image_prompts.append (processScreenplay.create_scene_prompt(scene))
        #print (i, ":\n", image_prompts[i])
        i += 1
    print ("Image prompts generated successfully")
    
    # Step 5: Generate the images for the scenes
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

    # Step 6: Generate the video prompts for the scenes
    print ("Generating video prompts for the scenes")
    i = 0
    video_prompts = []
    for scene in scenes:
        video_prompts.append (processScreenplay.create_video_prompt(scene))
        print ("\n\n", i, ":\n", video_prompts[i], "\n\n")
        i += 1
    print ("Video prompts generated successfully")

    # Step 7: Generate the videos for the scenes
    print ("Generating videos for the scenes")
    i = 0
    videos = []
    for scene in scenes:
        videos.append (generateVideoFal.generate_fal_video_from_image(video_prompts[i], image_paths[i], fal_api_key, "./outputs/falVideos/video" + str(i) + ".mp4"))
        print (i, ": ", videos[i])
        i += 1
    print ("Videos generated and downloaded successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--_together_api_key", type=str, default=None)
    parser.add_argument("-o", "--openai_api_key", type=str, default=None)
    parser.add_argument("-f", "--fal_api_key", type=str, default=None)
    parser.add_argument("-s", "--story_number", type=int, default=None)
    args = parser.parse_args()

    together_api_key = args._together_api_key
    openai_api_key = args.openai_api_key
    fal_api_key = args.fal_api_key

    main()