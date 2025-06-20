# suppress warnings
import warnings

warnings.filterwarnings("ignore")

#llm_model = "meta-llama/Meta-Llama-3-8B-Instruct-Lite"
#llm_model="meta-llama/Llama-3.3-70B-Instruct-Turbo"
llm_model="meta-llama/Llama-3-8b-chat-hf"

# import libraries
import json
import together
story_prompt_path = "./prompts/storyPrompts.txt"
screenplay_prompt_path = "./prompts/screenplayPromptTest.txt"


def generate_screenplay(story_prompt, screenplay_prompt, together_api_key):
    
    # Set the API key
    together.api_key = together_api_key

    chatbot_prompt = screenplay_prompt.format(story_prompt=story_prompt)

    response = together.Complete.create(
        prompt=chatbot_prompt,
        model=llm_model,
        max_tokens=2048,
        temperature=0
    )

    return response['output']['choices'][0]['text']

#Get the story prompt from story ID story_number from the storyPrompts.txt file.
def get_story_prompt(story_number):
    with open(story_prompt_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    stories = json.loads(content)
    
    story_prompt = "No story prompt found"

    for story in stories["stories"]:
        if int(story['story_id']) == story_number:
            story_prompt = story['story_prompt']
            break
        
    return story_prompt

def get_screenplay_prompt():
    with open(screenplay_prompt_path, "r", encoding="utf-8") as f:
        screenplay_prompt = f.read().strip()
    
    return screenplay_prompt