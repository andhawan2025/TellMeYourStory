import openai
from openai import OpenAI
import base64
import requests



def generate_scene_image_gpt41mini (scene_prompt, file_path, openai_api_key):
    # Call OpenAI API to generate image
    openai.api_key = openai_api_key
    
    client = OpenAI(api_key=openai_api_key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=scene_prompt,
        tools=[{"type": "image_generation",}],
    )

    # Save the image to a file
    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]
    
    if image_data:
        image_base64 = image_data[0]
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image_base64))

    print(f"Image downloaded and saved to {file_path}")

    return file_path



def generate_scene_image_dalle2 (scene_prompt, file_path, openai_api_key):
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


def generate_scene_image_gptimage1 (scene_prompt, file_path, openai_api_key):
    # Call OpenAI API to generate image
    openai.api_key = openai_api_key
    
    client = OpenAI(api_key=openai_api_key)

    response = client.images.generate(
        model="gpt-image-1",
        prompt=scene_prompt
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    # Save the image to a file
    with open(file_path, "wb") as f:
           f.write(image_bytes)

    print(f"Image downloaded and saved to {file_path}")

    return file_path
