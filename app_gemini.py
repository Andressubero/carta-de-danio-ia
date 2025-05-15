import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request
from sqlalchemy import text
from config import Config
from extensions import db
from models.models import Base  # Importá el Base desde tu models

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)

# Configurar carpeta de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

load_dotenv()
# Configurá tu API KEY de Gemini

genai.configure(api_key=app.config['GEMINI_API_KEY'])


@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        prompt = request.form['prompt']
        image = request.files['image']
        ref_image = request.files.get('ref_image')  # Imagen de referencia opcional

        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)

            with open(image_path, "rb") as img_file:
                img_bytes = img_file.read()

            parts = [{"text": prompt},
                     {"inline_data": {
                         "mime_type": "image/jpeg",
                         "data": img_bytes
                     }}]

            if ref_image and ref_image.filename != "":
                ref_image_path = os.path.join(app.config['UPLOAD_FOLDER'], ref_image.filename)
                ref_image.save(ref_image_path)
                with open(ref_image_path, "rb") as ref_img_file:
                    ref_img_bytes = ref_img_file.read()

                # Añadir mensaje contextual
                parts.insert(0, {"text": "Compará el estado actual del vehículo con la imagen de referencia anterior, identificando solo los daños nuevos si los hubiera."})
                parts.append({"inline_data": {
                    "mime_type": "image/jpeg",
                    "data": ref_img_bytes
                }})

            model = genai.GenerativeModel("gemini-1.5-flash")

            try:
                response = model.generate_content([
                    {"role": "user", "parts": parts}
                ])
                result = response.text
            except Exception as e:
                result = f"Error: {e}"

    return render_template("index.html", result=result)

if __name__ == '__main__':
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))  # Prueba simple
            print("✅ Conexión exitosa a la base de datos.")
        except Exception as e:
            print(f"❌ Error de conexión a la base de datos: {e}")
        Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)

