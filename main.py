import argparse

import generateScreenplay
import processScreenplay
import generateScenesImages

screenplay_file_path = "./outputs/screenplay.txt"
together_api_key = ""


story_prompt_1 = """
    A lady is walking towards a bus stop and is running late. She sees the bus approaching and starts running. 
    Seeing her run, the bus driver applies brakes and the bus makes a screeching noise.
    A kid nearby gets scared of the screeching noise and starts to cry.
    The kids mother gets extremely angry because of this.
    She starts doing salsa dance to relieve her of her stress.
    """

story_prompt_2 = """
A chef is cooking food in a busy kitchen. The owner of the restaurant walk in. He is in a good mood. 
The owner says that he is giving everyone a 50% bonus on tips that day.
Everyone becomes happy. They start clapping. The chef also starts singing an opera song.
"""

story_prompt_3 = """
A cat and dog are going to the market. Then the cat buys a banana. The dog buys a blueberry muffin. 
They both thank the shopkeper. Then they head back home.
"""

story_prompt_4 = """
There are two guys working out in the gym. First one says he's tired. The second one says he is hungry.
The first guy goes to the swimming pool to cool off and says he feels better now.
The second guy orders a banana shake and says it is very refreshing.
"""

screenplay_prompt = """
    Take the story provided below and generate a screenplay for it. The output should be a JSON object only. The screenplay should be in the format of a play.
    Follow the instructions below for generating the screenplay. Every scene must have at least one character and at least one dialogue.

    The output should be in the following JSON format:
    {
        "title": "Title of the play",
        "characters": ["Character 1", "Character 2", "Character 3"],
        "scenes": [
            {
                "scene_number": 1,
                "scene_characters": ["Character 1", "Character 2"]
                "scene_setting": "Description of the scene setting with details like where the scene is taking place, who is present, what time of the day it is etc.",
                "dialogue": [
                    {
                        "character_name": "name of the character speaking the dialog",
                        "dialog": "what the character says"
                    }
                    {
                        "character_name": "name of the character speaking the dialog",
                        "dialog": "what the character says"
                    }
                    {
                        "character_name": "name of the character speaking the dialog",
                        "dialog": "what the character says"
                    }
            }
            {
                "scene_number": 2,
                "scene_characters": ["Character 1", "Character 2"]
                "scene_setting": "Description of the scene setting with details like where the scene is taking place, who is present, what time of the day it is etc.",
                "dialogue": [
                    {
                        "character_name": "name of the character speaking the dialog",
                        "dialog": "what the character says"
                    }
                    {
                        "character_name": "name of the character speaking the dialog",
                        "dialog": "what the character says"
                    }
                    {
                        "character_name": "name of the character speaking the dialog",
                        "dialog": "what the character says"
                    }
            }
        ]
        Do not include any other text in the output. It should only be a valid JSON object. No other text should be present in the output.


    """


def main():
    print ("Generating the screenplay for the story prompt")
    screenplay = generateScreenplay.generate_screenplay(story_prompt_4, screenplay_prompt, together_api_key)
    print ("Screenplay received successfully")
    print (screenplay[45:100], "\n\n")
    
    screenplay_string = str(screenplay)
    start_index = screenplay_string.find('{')

    if start_index != -1:
        substring = screenplay_string[start_index:]
    else:
        substring = screenplay_string

    screenplay = substring


    print ("Storing the screenplay in a file")
    with open(screenplay_file_path, "w") as f:
        f.write(screenplay)
    print ("Screenplay stored in a file successfully\n\n")

    print ("Generating the scenes for the screenplay")
    scenes = processScreenplay.get_scenes_from_screenplay(screenplay_file_path)
    print ("Scenes generated successfully\n\n") 
    
    i = 0
    prompts = []

    for scene in scenes:
        print ("Generating the prompt for scene", i )
        prompts.append (processScreenplay.create_scene_prompt(scene))
        print (prompts[i], "\n\n")
        i += 1

    i = 0
    images = []
    
    for prompt in prompts:
        print ("Generating the image for the scene", i)
        images.append (generateScenesImages.generate_scene_image(prompt))
        print ("Image generated successfully") 
        print (images[i])
        i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--api_key", type=str, default=None)
    args = parser.parse_args()

    together_api_key = args.api_key
   
    main()