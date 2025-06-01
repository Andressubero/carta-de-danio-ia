import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

def img_to_bytes(path):
    img_bytes = bytes
    abs_path = os.path.join(os.path.dirname(__file__), '../', path)
    with open(abs_path, 'rb') as img_file:
        img_bytes = img_file.read()
    return img_bytes

def load_paths():
    try:
        paths = {} 
        abs_path = os.path.join(os.path.dirname(__file__), '../prompts/', os.getenv('PROMPTS_LOCATION'))
        with open(abs_path) as f:
            paths = json.load(f)
        return paths
    except Exception as e:
        print('Error al importar prompts paths: ', e)

def load_prompt(path):
    try:
        prompt = '' 
        abs_path = os.path.join(os.path.dirname(__file__), '../prompts/', path)
        with open(abs_path) as file:
            prompt = file.read()
        return prompt
    except Exception as e:
        print('Error al importar ai prompts: ', e)

def get_prompt(action):
    paths = load_paths()
    path = ''

    if action == 'ALTA':
        path = paths['alta_validacion']
    elif action == 'COMP':
        path = paths['comparacion_validacion']

    return load_prompt(path)

def call_llm(data, action):
    load_dotenv()
    genai.configure(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = get_prompt(action)
    parts = [{'text': prompt +' '+ str(data)}]
    
    for index in range(len(data)):
        img_bytes = img_to_bytes(data[index]['image'])

        parts.append({"inline_data": {
            "mime_type": "image/jpeg",
            "data": img_bytes
        }})

    model = genai.GenerativeModel(os.getenv('GEMINI_MODEL'))

    try:
        response = model.generate_content([
            {'role': 'user', 'parts': parts}
        ])
        return response.text
    except Exception as e:
        print(f'Error: {e}')
