import requests

# Replace with your actual API key



def generate_video(text_prompt, image_path, api_key, api_url):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    with open(image_path, "rb") as img_file:
        files = {
            "image": img_file
        }
    data = {
        "prompt": text_prompt,
        # Add other parameters as needed, e.g., "num_frames": 16
    }
    response = requests.post(API_URL, headers=headers, data=data, files=files)

    # Check the response
    if response.status_code == 200:
        # The response may contain a URL to the generated video
        result = response.json()
        print("Video URL:", result.get("video_url"))
    else:
        print("Error:", response.status_code, response.text)

    return result

def download_video(video_response, output_video_path):
    with open(output_video_path, "wb") as f:
        f.write(video_response.content)
    print(f"Video saved as {output_video_path}")