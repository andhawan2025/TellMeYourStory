LTX_VIDEO_PATH = "./LTX-Video/inference.py"

system_prompt = """
You are a video generator application. The user will give you a prompt. You are supposed to generate a video based on the prompt.
Follow the below instructions:
1. The video should be only 7 seconds long.
2. The video should identify the characters in the prompt.
3. The video should be an animation with a cartoon style.
4. The video should be funny. The characters should be humorous.
"""

user_prompt_1 = """
A lady is running after a bus as she is about to miss it.
The bus driver sees her and applies brakes to stop the bus for her.
The brakes make a screeching noise.
A kid nearby gets scared of the screeching noise and starts to cry
The kids mother gets angry and starts dancing salsa to relieve herself of the stress.
"""

def main():
    print (system_prompt)
    print (user_prompt_1)
    # LTX_Video.inference.main()

main ()