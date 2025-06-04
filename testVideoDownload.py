import requests
import time

# 1. Define your image paths and prompts
image_paths = [
    "./outputs/openAIImages/image0.webpp",
    "./outputs/openAIImages/image1.webpp",
    "./outputs/openAIImages/image2.webpp"
]
prompts = [
]

RUNWAY_API_KEY = ""
API_URL = "https://api.runwayml.com/v1/gen2/video"  # Adjust if needed
HEADERS = {
    "Authorization": f"Bearer {RUNWAY_API_KEY}"
}

def upload_image(image_path):
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post("https://api.runwayml.com/v1/uploads", headers=HEADERS, files=files)
        response.raise_for_status()
        return response.json()["url"]

def generate_video(image_url, prompt):
    payload = {
        "image": image_url,
        "prompt": prompt
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["id"]

def poll_for_video(video_id):
    status_url = f"{API_URL}/{video_id}"
    while True:
        response = requests.get(status_url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "succeeded":
            return data["output"]["video_url"]
        elif data.get("status") == "failed":
            raise Exception("Video generation failed")
        time.sleep(5)

def download_video(video_url, filename):
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

# 3. Main loop for 3 videos
for idx, (img_path, prompt) in enumerate(zip(image_paths, prompts), 1):
    print(f"Processing video {idx}...")
    image_url = upload_image(img_path)
    video_id = generate_video(image_url, prompt)
    print(f"Submitted job {video_id}, waiting for completion...")
    video_url = poll_for_video(video_id)
    print(f"Video ready: {video_url}")
    local_filename = f"runway_video_{idx}.mp4"
    download_video(video_url, local_filename)
    print(f"Downloaded to {local_filename}\n")

print("All videos downloaded.")

def main():
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--runway_api_key", type=str, default=None)
    args = parser.parse_args()

    RUNWAY_API_KEY = args.runway_api_key
    main()