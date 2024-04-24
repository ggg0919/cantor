import pathlib
import textwrap
import os
import PIL.Image
import json
import argparse
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from utils.decision_generation import decision_generation
from utils.split_task import split_task
from utils.execute_modularization import execute_modularization, summary
from utils.execute_synthesis import execute_synthesis

parser = argparse.ArgumentParser()
parser.add_argument('--decision_path', type=str, default='./data/decision.json')
parser.add_argument('--image_path', type=str, default='./images/image.png')
parser.add_argument('--query', type=str, default="Which month is the hottest on average in Detroit?")
parser.add_argument('--api_key', type=str, default='')
args = parser.parse_args()

if not os.path.exists(args.decision_path):
    dic = {}
    with open(args.decision_path, 'w') as json_file:
        json.dump(dic, json_file , indent=4)
        
def run_demo(arg):
    decision_generation(args)
    split_task(args)
    execute_modularization(args)
    summary(args)
    execute_synthesis(args)

run_demo(args)