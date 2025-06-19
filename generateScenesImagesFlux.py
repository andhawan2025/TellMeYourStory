import gradio_client
import os
import shutil
import openai
from openai import OpenAI
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
    # Handle different types of image_url
    if isinstance(image_url, tuple) and len(image_url) > 0:
        file_path = image_url[0]
    elif isinstance(image_url, list) and len(image_url) > 0:
        file_path = image_url[0]
    else:
        file_path = image_url
    
    os.makedirs(local_outputs_dir, exist_ok=True)

    src_path = file_url_to_path(file_path)
    dst_path1 = os.path.join(local_outputs_dir, os.path.basename(src_path))
    dst_path = dst_path1[:-5] + str(image_number) + dst_path1[-5:]
    shutil.copy(src_path, dst_path)

    return dst_path


def file_url_to_path(file_url):
    # If it's already a Windows path, return as is
    if ':\\' in file_url:
        return file_url
    
    path = urlparse(file_url).path
    # Remove leading slash for Windows paths
    if path.startswith('/'):
        path = path[1:]
    return unquote(path.replace('/', '\\'))

def generate_and_download_flux_scene_image(scene_prompt, image_number):
    result = generate_fluxscene_image(scene_prompt)
    # result is a tuple, not a string, so we need to handle it properly
    if isinstance(result, tuple) and len(result) > 0:
        image_url = result[0]  # Get the first element of the tuple
    else:
        image_url = result  # Fallback if it's not a tuple
    
    image_path = download_flux_scene_image(image_url, image_number)
    return image_path