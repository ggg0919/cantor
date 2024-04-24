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
    
    
def split_task(args):
    keywords = ["N/A", "Not required", "Not needed", "None", "No", "List the objects to be identified or counted in the image", "Specify the text or information to be extracted from the image", "Pose any specific questions you have about the image that require deeper visual analysis"]
    cnt = 0
    
    with open(args.decision_path, 'r') as file:
        decision = json.load(file)

    prompt = decision["decision"]
    if not prompt.endswith('\n'):
        prompt += '\n'  
    decision["decision"] = prompt

    filter_mathches = []
    matches = re.findall(r'ChartSense Expert\*{0,2}:\*{0,2}\s*(.*?)\n', prompt) 
    if matches:
        for i in range(len(matches)):
            if not any(keyword in matches[i] for keyword in keywords):
                filter_mathches.append(f"ChartSense Expert: " + matches[i])
                
    matches = re.findall(r'VisionIQ Analyst\*{0,2}:\*{0,2}\s*(.*?)\n', prompt) 
    if matches:
        for i in range(len(matches)):
            if not any(keyword in matches[i] for keyword in keywords):
                filter_mathches.append(f"VisionIQ Analyst: " + matches[i])

    matches = re.findall(r'TextIntel Extractor\*{0,2}:\*{0,2}\s*(.*?)\n', prompt) 
    if matches:
        for i in range(len(matches)):
            if not any(keyword in matches[i] for keyword in keywords):
                filter_mathches.append(f"TextIntel Extractor: " + matches[i])

    matches = re.findall(r'ObjectQuant Locator\*{0,2}:\*{0,2}\s*(.*?)\n', prompt) 
    if matches:
        for i in range(len(matches)):
            if not any(keyword in matches[i] for keyword in keywords):
                filter_mathches.append(f"ObjectQuant Locator: " + matches[i])
        
    print(filter_mathches)
    if filter_mathches:
        decision["task"] = filter_mathches
    
    with open(args.decision_path, 'w') as json_file:
        json.dump(decision, json_file , indent=4)

    print(f"task_num:{len(decision["task"])}")






