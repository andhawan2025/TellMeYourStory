import json

story_prompt_path = "./prompts/storyPrompts.txt"
screenplay_prompt_path = "./prompts/screenplayPrompt.txt"

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

def main():
    story = get_story_prompt (2)
    print(story)
    screenplay = get_screenplay_prompt()
    print(screenplay)

if __name__ == "__main__":
    main()
