import gradio_client
import os
import shutil
import ast
from urllib.parse import urlparse, unquote

local_outputs_dir = r"C:\Users\andha\OneDrive\Documents\GitHub\TellMeYourStory\outputs\fluxImages"

client = gradio_client.Client("black-forest-labs/Flux.1-schnell")

def generate_scene_image(scene_prompt):
    

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

def download_scene_image (image_url):
    safe_str = image_url.replace("\\", "\\\\")
    my_tuple = ast.literal_eval(safe_str)
    file_path = my_tuple[0]
    number = my_tuple[1]
        
    file_url_to_path (file_path)
    os.makedirs(local_outputs_dir, exist_ok=True)

    src_path = file_url_to_path(file_path)
    dst_path = os.path.join(local_outputs_dir, os.path.basename(src_path))
    shutil.copy(src_path, dst_path)
    print(f"Copied to {dst_path}")


def file_url_to_path(file_url):
    path = urlparse(file_url).path
    # Remove leading slash for Windows paths
    if path.startswith('/'):
        path = path[1:]
    return unquote(path.replace('/', '\\'))




