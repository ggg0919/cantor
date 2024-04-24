import pathlib
import textwrap
import os
import PIL.Image
import json
import argparse
import google.generativeai as genai
import re
# Used to securely store your API key
# from google.colab import userdata

from IPython.display import display
from IPython.display import Markdown

def execute_modularization(args):
    with open(args.decision_path, 'r') as file:
        decision = json.load(file)
    image = PIL.Image.open(args.image_path)
    genai.configure(api_key = args.api_key)
    
    model = genai.GenerativeModel('gemini-pro-vision')
    # 定义提示语
    decision["sub-answers"] =[]
    prompts = decision["sub-tasks"]
    print("\n\nExecute_Modularization:")
    for prompt in prompts:
        print(prompt)
        response = model.generate_content([prompt, image], 
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
                print(response.text)
                decision["sub-answers"].append(response.text) 
            except:
                decision["sub-answers"].append(" ") 
    with open(args.decision_path, 'w') as json_file:
        json.dump(decision, json_file , indent=4)

def summary(args):
    with open(args.decision_path, 'r') as file:
        decision = json.load(file)
    
    matches = re.findall(r'Answer\*{0,2}:{0,1}\*{0,2}\s*(.*?)\s*\*{0,2}Modules{0,1}\'s{0,1} [tT]asks{0,1}\*{0,2}:', decision["decision"], re.DOTALL)  #Image Understanding Module + Image Understanding Agent
    matches2 = re.findall(r'Rationale\*{0,2}:\*{0,2}\s*(.*?)\n\*{0,2}Modules{0,1}\'s{0,1} [tT]asks{0,1}\*{0,2}:', decision["decision"], re.DOTALL)
    
    if matches: 
        supplementary_information = ' '.join(matches)
    else:
        if matches2:
            supplementary_information = ' '.join(matches2)
        else:
            supplementary_information = decision["decision"]
    sub_questions = decision["sub-tasks"]
    sub_answers = decision["sub-answers"]
    
    if sub_questions:
        supplementary_information +=  "\nModules\' tasks:\n"
    
    for sub_q, sub_a in zip(sub_questions, sub_answers):
        reform_sub = f"{sub_q} Answer:{sub_a}\n"
        supplementary_information += reform_sub
    
    decision["supplementary_information"] = supplementary_information
    
    with open(args.decision_path, 'w') as json_file:
        json.dump(decision, json_file , indent=4)
    
