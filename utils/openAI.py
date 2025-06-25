import os
import json
import base64
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI


# --- 🔁 Utilidades comunes ---
def img_to_bytes(path):
    with open(path, 'rb') as img_file:
        return img_file.read()

def encode_image_to_base64(path):
    mime_type = "image/jpeg" if path.endswith((".jpg", ".jpeg")) else "image/png"
    img_bytes = img_to_bytes(path)
    base64_str = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{base64_str}"

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
    if action == 'ALTA':
        return load_prompt(paths['alta_validacion'])
    elif action == 'COMP':
        return load_prompt(paths['comparacion_validacion'])
    return ""


# --- 🧠 GEMINI ---
def call_gemini(data, action):
    genai.configure(api_key=os.getenv('OPENAI_API_KEY_GEMINI'))
    prompt = get_prompt(action)
    parts = []

    parts.append({'text': prompt + ' ' + str(data)})

    for image_entry in data["states"]:
        #Imagen de referencia
        if 'reference_image' in image_entry and image_entry['reference_image']:
            ref_bytes = img_to_bytes(image_entry['reference_image'])
            parts.append({'text': 'La siguiente imagen es de referencia'})
            parts.append({
                "inline_data": {
                    "mime_type": image_entry["reference_mime_type"],
                    "data": ref_bytes
                }
            })
        #Imagen actual
        img_bytes = img_to_bytes(image_entry['image'])
        parts.append({'text': 'La siguiente imagen es actual'})
        parts.append({
            "inline_data": {
                "mime_type": image_entry["mime_type"],
                "data": img_bytes
            }
        })

    model = genai.GenerativeModel(os.getenv('GEMINI_MODEL'))
    print(f'----------------consultando a gemini------------------')
    try:
        response = model.generate_content([
            {'role': 'user', 'parts': parts}
        ])
        return response.text
    except Exception as e:
        print(f'Error: {e}')


# --- 🧠 OPENAI (GPT-4o, 4.1, o4-mini) ---
def call_openai(data, action):
    prompt = get_prompt(action)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Construcción del input en el formato que requiere responses.create
    input_data = [{
        "role": "user",
        "content": [
            { "type": "input_text", "text": prompt + ' ' + str(data) }
        ]
    }]

    for idx, image_entry in enumerate(data["states"]):

        # Imagen de referencia (si existe)
        if 'reference_image' in image_entry and image_entry['reference_image']:
            print(f"Imagen de referencia {image_entry['reference_image']}")
            ref_b64 = encode_image_to_base64(image_entry["reference_image"])
            input_data[0]["content"].append({
                "type": "input_image",
                "image_url": ref_b64,
                "detail": "high"
            })
            input_data[0]["content"].append({
                "type": "input_text",
                "text": f"La imagen anterior muestra el estado anterior del vehiculo (parte {idx + 1})."
            })

        # Imagen actual
        image_b64 = encode_image_to_base64(image_entry["image"])
        input_data[0]["content"].append({
            "type": "input_image",
            "image_url": image_b64,
            "detail": "high"
        })
        input_data[0]["content"].append({
            "type": "input_text",
            "text": f"La imagen anterior muestra el estado actual del vehículo (parte {idx + 1})."
        })


    print(f'----------------consultando a gpt------------------')
    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            input=input_data,
        )
        return response.output_text
    except Exception as e:
        print(f'Error: {e}')



# --- 🚀 Entry point principal ---
def call_llm(data, action):
    load_dotenv()
    ia = os.getenv("IA_UTILIZADA", "gemini").lower()

    if ia == "gpt":
        return call_openai(data, action)
    else:
        return call_gemini(data, action)
