# suppress warnings
import warnings

warnings.filterwarnings("ignore")

# import libraries
import requests
from together import Together

def generate_screenplay(story_prompt, screenplay_prompt, together_api_key):
    
    # Get Client for your LLMs
    print ("Creating client for Together API")
    client = Together(api_key=together_api_key)

    print ("Now generating chatbot prompt")
    chatbot_prompt = story_prompt + " \n " + screenplay_prompt

    print ("Calling the LLM to get the screenplay")
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
        messages=[{"role": "user", "content": chatbot_prompt}],
    )

    print ("Screenplay generated successfully. Returning the screenplay")
    return response.choices[0].message.content



