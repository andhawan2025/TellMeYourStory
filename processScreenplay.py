import json

def get_scenes_from_screenplay(screnplayFilePath):
    screenplay_json = []

    with open(screnplayFilePath, 'r', encoding='utf-8') as file:
        screenplay_json = json.load(file)
    
    scenes = screenplay_json.get("scenes", [])
    return scenes

def extract_all_characters(play_json):
    """
    Extracts all unique characters from the play JSON object, including the top-level characters
    and characters appearing in each scene.

    Args:
        play_json (dict): The JSON object representing the play.

    Returns:
        list: A list of all unique character names.
    """
    characters = set()

    # Add characters from the top-level "characters" key
    top_level_characters = play_json.get("characters", [])
    characters.update(top_level_characters)

    # Add characters from each scene's "scene_characters"
    scenes = play_json.get("scenes", [])
    for scene in scenes:
        scene_characters = scene.get("scene_characters", [])
        characters.update(scene_characters)

    return list(characters)


def create_scene_prompt(scene):
    """
    Given a scene JSON object, create a prompt to generate an image description.

    Args:
    scene (dict): A dictionary with keys 'scene_number', 'scene_characters', 'scene_setting', 'dialogue'.

    Returns:
    str: Formatted prompt string.
    """
    scene_characters = scene.get("scene_characters", [])
    characters = ", ".join(scene.get("scene_characters", []))
    setting = scene.get("scene_setting", "No setting description provided.")
    dialogues = scene.get("dialogue", [])

    prompt = (
        f"Generate an image for a scene that is described next. Proivde a high-resolution, hyperrealistic, highly detailed image, with cinematic lighting, ultra-sharp focus and 8K resolution."
        f"The imgage should be a single image that captures the entire scene. The image should fit in a 1024x1024 canvas. "
        f"The dialogues that are present in the scene should be included in the image. "
        f"There are {len(scene_characters)} characters in the scene, as follows: {characters}. "
        f"Scene setting: {setting}. "
    )
    
    for entry in dialogues:
        character_name = entry.get("character_name")
        dialog = entry.get("dialog")
        new_str = " Then, " + character_name + " says " + dialog + ". "
        prompt += new_str
    
    return prompt    

def create_video_prompt(scene):
    """
    Given a scene JSON object, create a prompt to generate a video prompt to go along with the image for video generation.

    Args:
    scene (dict): A dictionary with keys 'scene_number', 'scene_characters', 'scene_setting', 'dialogue'.

    Returns:
    str: Formatted prompt string.
    """
    scene_characters = scene.get("scene_characters", [])
    characters = ", ".join(scene.get("scene_characters", []))
    setting = scene.get("scene_setting", "No setting description provided.")
    dialogues = scene.get("dialogue", [])

    prompt = (
        f"Generate a video for a scene that is described next and presented in the image alongwith the dialogues. "
        f"The dialogues should appear as callouts in the video. "
        f"There are {len(scene_characters)} characters in the scene, as follows: {characters}. "
        f"Scene setting: {setting}. "
    )
    
    for entry in dialogues:
        character_name = entry.get("character_name")
        dialog = entry.get("dialog")
        new_str = " Then, " + character_name + " says " + dialog + ". "
        prompt += new_str
    
    return prompt