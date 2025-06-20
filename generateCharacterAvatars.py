import os
import json
import openai
import google.generativeai as genai
import requests

# === CONFIG ===
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
SCREENPLAY_PATH = "./outputs_s3/screenplays/screenplay.json"
AVATAR_DIR = "./outputs_s3/avatars"
SCENE_DIR = "./outputs_s3/scenes"
os.makedirs(AVATAR_DIR, exist_ok=True)
os.makedirs(SCENE_DIR, exist_ok=True)

# === FUNCTIONS ===
def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def generate_avatar_prompt(character):
    
    prompt = f"""
    Generate a detailed visual description of a character avatar:
    Name: {character["name"]}
    Age: {character["age"]}
    Gender: {character["gender"]}
    """
    return gemini.generate_content(prompt).text.strip()

def generate_image_from_prompt(prompt, output_path):
    genai.configure(api_key=GEMINI_API_KEY)
    gemini = genai.GenerativeModel("gemini-pro")
        
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response["data"][0]["url"]
    image_data = requests.get(image_url).content
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path

def generate_scene_prompt(scene, characters, avatar_descriptions):
    character_lines = []
    for d in scene["dialogue"]:
        name = next(c["name"] for c in characters if str(c["character_number"]) == d["character_number"])
        character_lines.append(f"{name}: \"{d['dialog']}\"")
    
    scene_prompt = f"""
    Create a detailed image description for the following scene.
    Setting: {scene['scene_setting']}
    Dialogue:\n{chr(10).join(character_lines)}

    Character appearances:
    {chr(10).join(avatar_descriptions)}

    Use this as a prompt for an AI to generate a full scene image.
    """
    return gemini.generate_content(scene_prompt).text.strip()

def generate_character_avatars(characters):
    for char in characters:
        print(f"Generating avatar for: {char['name']}")
        avatar_prompt = generate_avatar_prompt(char)
        avatar_path = os.path.join(AVATAR_DIR, f"{char['name'].replace(' ', '_')}.png")
        avatar_paths[char["character_number"]] = generate_image_from_prompt(avatar_prompt, avatar_path)

# === MAIN ===
data = read_json(SCREENPLAY_PATH)
characters = data["characters"]
scenes = data["scenes"]
avatar_prompts = {}
avatar_paths = {}

# Step 1: Generate avatars
for char in characters:
    print(f"Generating avatar for: {char['name']}")
    avatar_prompt = generate_avatar_prompt(char)
    avatar_prompts[char["character_number"]] = avatar_prompt
    avatar_path = os.path.join(AVATAR_DIR, f"{char['name'].replace(' ', '_')}.png")
    avatar_paths[char["character_number"]] = generate_image_from_prompt(avatar_prompt, avatar_path)

# Step 2: Generate scenes
for scene in scenes:
    print(f"\nGenerating scene {scene['scene_number']}")
    scene_char_nums = scene["scene_characters"]
    relevant_prompts = [avatar_prompts[num] for num in scene_char_nums]
    scene_image_prompt = generate_scene_prompt(scene, characters, relevant_prompts)
    scene_path = os.path.join(SCENE_DIR, f"scene_{scene['scene_number']}.png")
    generate_image_from_prompt(scene_image_prompt, scene_path)
    print(f"Scene image saved to {scene_path}")
