import pathlib
import textwrap
import os
import PIL.Image
import json
import argparse
import google.generativeai as genai

# Used to securely store your API key
# from google.colab import userdata

from IPython.display import display
from IPython.display import Markdown
from .prompt import prompt_template
import re


def decision_generation(args):
    with open(args.decision_path, 'r') as file:
        decision = json.load(file)
    image = PIL.Image.open(args.image_path)
    genai.configure(api_key = args.api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
    base_prompt = prompt_template['decision_prompt']
    prompt = f"{base_prompt}\nPlease refer to the prompts and examples above to help me solve the following problem:\nQuestion: {args.query}\n"
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
            print("Decision_Generation:")
            print(response.text)
            decision["query"] = args.query
            decision["decision"] = response.text
        except:
            decision["decision"] = " "
    with open(args.decision_path, 'w') as json_file:
        json.dump(decision, json_file , indent=4)



