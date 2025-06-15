import argparse

import requests
import time

leonardo_api_key = ""
image_path = "./outputs/openAIImages/image10.png"
video_path = "./outputs/leonardoVideos/video0.mp4"
prompt = "Generate a video for a scene that is described next and presented in the image alongwith the dialogues. The dialogues should appear as callouts in the video. There are 2 characters in the scene, as follows: Lady, Bus Driver. Scene setting: A busy street with a bus stop, a bus approaching, and a kid playing nearby..  Then, Lady says Oh no, I'm running late!.  Then, Bus Driver applies brakes and the bus goes (makes sound) Screech"

leonardo_ai_imageupload_url = "https://cloud.leonardo.ai/api/rest/v1/uploads"
leonardo_ai_video_gen_url = "https://cloud.leonardo.ai/api/rest/v1/generate/video"
leonardo_ai_video_poll_url = "https://cloud.leonardo.ai/api/rest/v1/generate/video/"

def generate_video_leonardo(image_path, prompt, video_path, leonardo_api_key):
    
    headers = {"Authorization": f"Bearer {leonardo_api_key}"}
    
    #Upload the image
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(leonardo_ai_imageupload_url, headers=headers, files=files)
        response.raise_for_status()
        image_data = response.json()
        # Adjust the key below based on actual API response
        image_url = image_data["uploadUrl"]

    print("Image uploaded:", image_url)

    video_gen_payload = {
        "image_url": image_url,  # or "image_id" if the API uses IDs
        "prompt": prompt,
        # Add other parameters as required by the API
    }

    headers = {
        "Authorization": f"Bearer {leonardo_api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(leonardo_ai_video_gen_url, headers=headers, json=video_gen_payload)
    response.raise_for_status()
    video_job = response.json()
    video_job_id = video_job["id"]  # Adjust key as per API docs

    print("Video generation job started:", video_job_id)

    #Poll for video completion
    while True:
        poll_response = requests.get(leonardo_ai_video_poll_url + video_job_id, headers=headers)
        poll_response.raise_for_status()
        status_data = poll_response.json()
        if status_data.get("status") == "COMPLETED":
            video_url = status_data["video_url"]  # Adjust key as per API docs
            break
        elif status_data.get("status") == "FAILED":
            raise Exception("Video generation failed")
        print("Waiting for video to complete...")
        time.sleep(5)

    print("Video ready:", video_url)

    # Download the video
    video_data = requests.get(video_url).content
    with open(video_path, "wb") as f:
        f.write(video_data)

    print("Video downloaded as generated_video.mp4")

def main():
    generate_video_leonardo(image_path, prompt, video_path, leonardo_api_key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--leonardo_api_key", type=str, default=None)
    args = parser.parse_args()

    leonardo_api_key = args.leonardo_api_key

    main()