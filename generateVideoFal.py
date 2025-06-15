import fal_client
import base64
import os
import argparse
import requests
from typing import Optional

fal_model = "fal-ai/veo2/image-to-video"
fal_api_key = ""

prompt1 = "Generate a video for a scene that is described next and presented in the image alongwith the dialogues. The video should fit in a 1024x1024 canvas. The video should be no longer than 5 secondsThe dialogues should appear as callouts in the video. There are 1 characters in the scene, as follows: Girl. Scene setting: A girl is sitting on a bench in a gym, wearing a pink gym outfit, looking tired..  Then, Girl says I'm so tired.."
prompt2 = "Generate a video for a scene that is described next and presented in the image alongwith the dialogues. The video should fit in a 1024x1024 canvas. The video should be no longer than 5 secondsThe dialogues should appear as callouts in the video. There are 1 characters in the scene, as follows: Girl. Scene setting: The girl is now standing next to a weight in another area of the gym, still wearing the same pink gym outfit, holding a weight. She drops the weight and says OUCH.  Then, Girl says OUCH."
prompt3 = "Generate a video for a scene that is described next and presented in the image alongwith the dialogues. The video should fit in a 1024x1024 canvas. The video should be no longer than 5 secondsThe dialogues should appear as callouts in the video. There are 2 characters in the scene, as follows: Girl, Good Looking Man. Scene setting: The girl is still standing next to the weight, looking up at a good looking man who has approached her..  Then, Good Looking Man says Do you need help?.  Then, Girl says Yes I think I do."

image_path1 = "./outputs/openAIImages/image0.png"
image_path2 = "./outputs/openAIImages/image1.png"
image_path3 = "./outputs/openAIImages/image2.png"

def on_queue_update(update):
    """Callback function to handle queue updates and display logs"""
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

def upload_image_to_fal(image_path: str, fal_api_key: str) -> str:
    
    # Set API key
    os.environ['FAL_KEY'] = fal_api_key
    
    print(f"Uploading image: {image_path}")
    
    # Upload image to FAL storage - returns URL string directly
    uploaded_url = fal_client.upload_file(image_path)
        
    print(f"Image uploaded successfully: {uploaded_url}")
    return uploaded_url
        
def encode_image_to_base64(image_path: str) -> str:
    """Convert a local image file to base64 encoding"""
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_image}"
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    except Exception as e:
        raise Exception(f"Error encoding image: {str(e)}")

def download_video(video_url: str, local_filepath: str):
    print(f"Downloading video from: {video_url}")
    print(f"Saving to: {local_filepath}")
        
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(local_filepath), exist_ok=True)
        
    # Download the video
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
     
    # Save to local file
    with open(local_filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    print(f"Video downloaded successfully to: {local_filepath}")
    return True

def generate_fal_video_from_image (prompt: str, image_input: str, fal_api_key: str, video_store_path: str):
    # Generates and downloads a video from an image using FAL AI. Returns the path of the downloaded video.

    # Set API key
    os.environ['FAL_KEY'] = fal_api_key
    
    # Upload image to FAL storage instead of using base64
    #print ("Uploading image to FAL storage: ", image_input)
    #print(f"Processing local image: {image_input}")
    image_url = upload_image_to_fal(image_input, fal_api_key)
        
    print("Starting video generation...")
    
    # Generate video using FAL AI
    result = fal_client.subscribe(
        fal_model,
        arguments={
            "prompt": prompt,
            "image_url": image_url,
            "duration": '5s',
            "fps": 24
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
        
    print("\nVideo generation completed!")
    print(f"Video URL: {result.get('video', {}).get('url', 'No URL found')}")

    # Download the generated video
    video_url = result.get('video', {}).get('url')
    if video_url:
        download_video(video_url, video_store_path)
    print("Video downloaded successfully and stored at", video_store_path)
        
    return result

def main():
    
    #result = generate_fal_video_from_image(
    #    prompt=prompt1,
    #    image_input=image_path1,
    #    fal_api_key=fal_api_key,
    #    video_store_path="./outputs/falVideos/video0.mp4"
    #)

    #result = generate_fal_video_from_image(
    #    prompt=prompt2,
    #    image_input=image_path2,
    #    fal_api_key=fal_api_key,
    #    video_store_path="./outputs/falVideos/video1.mp4"
    #)

    result = generate_fal_video_from_image(
        prompt=prompt3,
        image_input=image_path3,
        fal_api_key=fal_api_key,
       video_store_path="./outputs/falVideos/video2.mp4"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fal_api_key", type=str, default=None)
    
    args = parser.parse_args()
    fal_api_key = args.fal_api_key
    
    main()