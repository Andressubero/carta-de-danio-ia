import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

def img_to_bytes(path):
    with open(path, 'rb') as img_file:
        return img_file.read()

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
        with open(abs_path, encoding='utf-8') as file:
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

    parts = []

    # 1️⃣ Agregamos el prompt + datos en texto
    parts.append({'text': prompt + ' ' + str(data)})

    # 2️⃣ Recorremos cada imagen
    for index in range(len(data["states"])):
        image_entry = data["states"][index]

        # Imagen principal
        img_bytes = img_to_bytes(image_entry['image'])
        mime_type = image_entry['mime_type']

        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": img_bytes
            }
        })

        # Si hay imagen de referencia, la agregamos también
        if 'reference_image' in image_entry and image_entry['reference_image']:
            reference_img_bytes = img_to_bytes(image_entry['reference_image'])
            reference_mime_type = image_entry['reference_mime_type']

            parts.append({
                "inline_data": {
                    "mime_type": reference_mime_type,
                    "data": reference_img_bytes
                }
            })

    # Logueamos lo que se va a enviar (opcional)
    print(">>> Enviando a la IA los siguientes parts:")
    for i, part in enumerate(parts):
        if 'text' in part:
            print(f"Part {i}: Text prompt ({len(part['text'])} chars)")
        else:
            print(f"Part {i}: Image with mime_type = {part['inline_data']['mime_type']} ({len(part['inline_data']['data'])} bytes)")

    # 3️⃣ Llamamos a la IA
    model = genai.GenerativeModel(os.getenv('GEMINI_MODEL'))

    try:
        response = model.generate_content([
            {'role': 'user', 'parts': parts}
        ])

        return response.text

    except Exception as e:
        print(f'Error: {e}')
