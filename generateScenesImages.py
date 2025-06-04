import gradio_client
import os
import shutil
import openai
import requests
from urllib.parse import urlparse, unquote

local_outputs_dir = r"C:\Users\andha\OneDrive\Documents\GitHub\TellMeYourStory\outputs\fluxImages"

client = gradio_client.Client("black-forest-labs/Flux.1-schnell")

def generate_fluxscene_image(scene_prompt):
    

    result = client.predict (
        prompt = scene_prompt,
        seed = 0,
        randomize_seed = True,
        width=1024,
        height=1024,
        num_inference_steps=4,
        api_name = "/infer"
    )

    return result

def download_flux_scene_image (image_url, image_number):
    file_path = image_url[0]
          
    file_url_to_path (file_path)
    os.makedirs(local_outputs_dir, exist_ok=True)

    src_path = file_url_to_path(file_path)
    dst_path1 = os.path.join(local_outputs_dir, os.path.basename(src_path))
    dst_path = dst_path1[:-5] + str(image_number) + dst_path1[-5:]
    shutil.copy(src_path, dst_path)

    return dst_path


def file_url_to_path(file_url):
    path = urlparse(file_url).path
    # Remove leading slash for Windows paths
    if path.startswith('/'):
        path = path[1:]
    return unquote(path.replace('/', '\\'))

def generate_and_download_openai_scene_images(scene_prompt, file_path, openai_api_key):
    # Call OpenAI API to generate image
    openai.api_key = openai_api_key
    response = openai.Image.create(
        #model='dall-e-2',
        prompt=scene_prompt,
        n=1,
        size='1024x1024'
    )

    # Extract image URL
    image_url = response['data'][0]['url']
    print(f"Image URL: {image_url}")

    # Download the image
    img_data = requests.get(image_url).content
    with open(file_path, 'wb') as handler:
        handler.write(img_data)
    
    print(f"Image downloaded and saved to {file_path}")

    return file_path
