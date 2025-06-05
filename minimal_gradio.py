import argparse
import gradio as gr
import tempfile
import requests
import time
import json

import generateScreenplay
import processScreenplay
import generateScenesImagesFlux
import getPrompts
import generateVideoLeonardo
import playVideos

screenplay_file_path = "./outputs/screenplay.txt"
prompts_file_path = "./prompts/prompts.json"
videos_directory = "./outputs/leonardoVideos"
together_api_key = ""
openai_api_key = ""
leonardo_api_key = ""

LEONARDO_API_KEY = ""

def main(story_prompt):
    #Generate screenplay from story prompt
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

    #Store screenplay at a predefined path
    #with open(screenplay_file_path, "w") as f:
    #    f.write(substring)
    #print ("Screenplay stored successfully")

    #Generate scenes from screenplay
    #scenes = processScreenplay.get_scenes_from_screenplay(screenplay_file_path)
    
    #Generate image prompts for each scene
    #i = 0
    #image_prompts = []
    #for scene in scenes:
    #    image_prompts.append (processScreenplay.create_scene_prompt(scene))
    #    i += 1

    #Generate and downlpad images for each scene
    #i = 0
    #images = []
    #image_paths = []
    #for prompt in image_prompts:
    #    image_paths.append ("./outputs/openAIImages/image" + str(i) + ".png")
    #    images.append (generateScenesImages.generate_and_download_openai_scene_images (prompt, image_paths[i], openai_api_key))
    #    print (image_paths[i])
    #    i += 1
    #    break
    
    #Generate video prompts for each scene
    #i = 0
    #video_prompts = []
    #for scene in scenes:
    #    video_prompts.append (processScreenplay.create_video_prompt(scene))
    #    i += 1
    
    #Generate and download videos for each scene
    #i = 0
    #videos = []
    #video_paths = []
    #for prompt in video_prompts:
    #    video_paths.append ("./outputs/leonardoVideos/video" + str(i) + ".mp4")
    #    videos.append (generateVideoLeonardo.generate_video_leonardo(image_paths[i], prompt, video_paths[i]))
    
    #Play videos
    #playVideos.play_videos(videos_directory)
    print (story_prompt)
    return "./outputs/leonardoVideos/video0.mp4"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--_together_api_key", type=str, default=None)
    parser.add_argument("-o", "--openai_api_key", type=str, default=None)
    parser.add_argument("-l", "--leonardo_api_key", type=str, default=None)
    parser.add_argument("-s", "--story_number", type=int, default=None)
    args = parser.parse_args()

    together_api_key = args._together_api_key
    openai_api_key = args.openai_api_key
    leonardo_api_key = args.leonardo_api_key

    iface = gr.Interface(
        fn=main,  # or the function you want to expose
        inputs=gr.Textbox(label="Story Prompt"),  # specify your inputs here
        outputs=gr.PlayableVideo(label="Generated Video"), # specify your outputs here
        title="Tell Me Your Story",
        description="Only a dummy video is generated for now."
    )

    main("test")
    iface.launch()