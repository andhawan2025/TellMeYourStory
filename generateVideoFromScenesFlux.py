import requests

def generate_flux_video(api_key, prompt, image_path):
    url = "https://api.flux-ai.io/v1/video/generate"  # Hypothetical endpoint

    # Open the image file
    files = {
        'image': open(image_path, 'rb')
    }

    # Payload
    data = {
        'prompt': prompt,
        'model': 'video_pro_5s_v1.6',  # Example model, choose depending on what Flux offers
        'duration': 5,                 # In seconds, depending on model
        'guidance_scale': 7.5,         # Prompt adherence, standard
    }

    # Headers with API key
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    # POST request
    response = requests.post(url, headers=headers, files=files, data=data)

    # Check response
    if response.status_code == 200:
        result = response.json()
        video_url = result.get('video_url')
        print(f"Video generated successfully: {video_url}")
        return video_url
    else:
        print(f"Failed to generate video: {response.text}")
        return None

# Usage
api_key = "your_flux_api_key_here"
prompt = "A futuristic city with flying cars at sunset"
image_path = "path_to_your_image.jpg"

video_url = generate_flux_video(api_key, prompt, image_path)