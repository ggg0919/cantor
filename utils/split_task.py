import re
import json


def split_task(args):
    keywords = ["N/A", "Not required", "Not needed", "None", "No", "List the objects to be identified or counted in the image", "Specify the text or information to be extracted from the image", "Pose any specific questions you have about the image that require deeper visual analysis"]
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
        
    if filter_mathches:
        decision["sub-tasks"] = filter_mathches
    else:
        decision["sub-tasks"] = []
    with open(args.decision_path, 'w') as json_file:
        json.dump(decision, json_file , indent=4)

    # print(f"task_num:{len(decision["sub-tasks"])}")