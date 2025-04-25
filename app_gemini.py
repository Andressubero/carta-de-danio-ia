import os
import google.generativeai as genai
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configurá tu API KEY de Gemini
genai.configure(api_key="TU_API_KEY_AQUÍ")

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        prompt = request.form['prompt']
        image = request.files['image']

        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)

            # Cargar imagen como bytes
            with open(image_path, "rb") as img_file:
                img_bytes = img_file.read()

            # Crear modelo de Gemini multimodal
            model = genai.GenerativeModel("gemini-1.5-flash")

            try:
                response = model.generate_content([
                    prompt,
                    genai.types.Content.Image(data=img_bytes, mime_type="image/jpeg")
                ])
                result = response.text
            except Exception as e:
                result = f"Error: {e}"

    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
