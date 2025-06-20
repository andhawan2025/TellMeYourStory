import gradio_client
import os
import shutil
import openai
from openai import OpenAI
from urllib.parse import urlparse, unquote

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

def download_flux_scene_image(image_url, output_file_path):
    """
    Download a Flux scene image to a specific file path.
    
    Args:
        image_url: URL or path to the source image
        output_file_path: Full path where the image should be saved
        
    Returns:
        str: Path to the downloaded image file
    """
    # Handle different types of image_url
    if isinstance(image_url, tuple) and len(image_url) > 0:
        file_path = image_url[0]
    elif isinstance(image_url, list) and len(image_url) > 0:
        file_path = image_url[0]
    else:
        file_path = image_url
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)

    src_path = file_url_to_path(file_path)
    shutil.copy(src_path, output_file_path)

    return output_file_path


def file_url_to_path(file_url):
    # If it's already a Windows path, return as is
    if ':\\' in file_url:
        return file_url
    
    path = urlparse(file_url).path
    # Remove leading slash for Windows paths
    if path.startswith('/'):
        path = path[1:]
    return unquote(path.replace('/', '\\'))

def generate_and_download_flux_scene_image(scene_prompt, output_file_path):
    """
    Generate a Flux scene image and download it to a specific path.
    
    Args:
        scene_prompt: The prompt to generate the image from
        output_file_path: Full path where the image should be saved
        
    Returns:
        str: Path to the downloaded image file
    """
    result = generate_fluxscene_image(scene_prompt)
    
    # result is a tuple, not a string, so we need to handle it properly
    if isinstance(result, tuple) and len(result) > 0:
        image_url = result[0]  # Get the first element of the tuple
    else:
        image_url = result  # Fallback if it's not a tuple
    
    image_path = download_flux_scene_image(image_url, output_file_path)
    return image_path