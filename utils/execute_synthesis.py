import pathlib
import textwrap
import os
import PIL.Image
import json
import argparse
import google.generativeai as genai

# Used to securely store your API key
# from google.colab import userdata
from datasets import load_dataset
from IPython.display import display
from IPython.display import Markdown
from .prompt import prompt_template

def execute_synthesis(args):
    with open(args.decision_path, 'r') as file:
        decision = json.load(file)
    image = PIL.Image.open(args.image_path)
    genai.configure(api_key = args.api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
    
    supplementary_information = decision["supplementary_information"]
    
    query = decision["query"]
    base_prompt = prompt_template["execute_synthesis_prompt"]
    prompt =  f"{base_prompt}\nPlease answer the following case:\n Question:{query}\nSupplementary information:{supplementary_information}"

    response = model.generate_content([prompt, image], stream=True, 
                                    safety_settings={'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                    'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                    'HARM_CATEGORY_HARASSMENT': 'block_none',
                                    'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
    try:
        response.resolve()
    except:
        print(response.prompt_feedback) 
    else:
        try:
            print("\n\nExecute_Synthesis:")
            print(response.text)
            decision["response"] = response.text
        except:
            decision["response"] = " "

    with open(args.decision_path, 'w') as json_file:
        json.dump(decision, json_file , indent=4)