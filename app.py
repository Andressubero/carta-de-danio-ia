import os
from os.path import join, dirname
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request
from sqlalchemy import text
from config import Config
from extensions import db
from models.models import Base
from routes.UserRoutes import user_bp  # Importá el Base desde tu models

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(user_bp)

# Inicializar extensiones
db.init_app(app)

# Configurar carpeta de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

# app.py

if __name__ == '__main__':
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print("✅ Conexión exitosa a la base de datos.")
        except Exception as e:
            print(f"❌ Error de conexión a la base de datos: {e}")
        Base.metadata.create_all(bind=db.engine)

        from models.parts_seed import seed_parts
        seed_parts()
        from models.vehicle_type_seed import seed_vehicles_type
        seed_vehicles_type()
        from models.vehicle_type_part_seed import seed_vehicles_type_parts
        seed_vehicles_type_parts()
        from models.role_seed import seed_roles
        seed_roles()
        from models.user_seed import seed_users
        seed_users()
        from models.vehicle_seed import seed_vehicles
        seed_vehicles()

    app.run(debug=True)


