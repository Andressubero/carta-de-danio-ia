import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory, send_file, abort
from sqlalchemy import text
from config import Config
from extensions import db
from models.models import Base
from flask_cors import CORS
from routes.UserRoutes import user_bp  # Importá el Base desde tu models
from routes.vehicles_routes import vehicle_bp 
from routes.vehicle_state_routes import vehicle_state_bp 
from routes.vehicle_type_routes import vehicle_types_bp
from routes.ai_report_routes import report_bp
from PIL import Image
import io

load_dotenv()
app = Flask(__name__)
CORS(app, supports_credentials=True ,origins=["http://localhost:5173"],)
app.config.from_object(Config)
app.register_blueprint(user_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(vehicle_types_bp)
app.register_blueprint(vehicle_state_bp)
app.register_blueprint(report_bp)
#CORS(app)


# Inicializar extensiones
db.init_app(app)

# Configurar carpeta de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from flask import render_template, request, redirect, url_for, flash

@app.route("/", methods=["GET"])
def index():
    return render_template("carta.html")

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.isfile(file_path):
        abort(404, description="Archivo no encontrado")

    # Redimensionar y comprimir imagen
    try:
        with Image.open(file_path) as img:
            # Convertimos a RGB para evitar errores con PNGs con transparencia
            img = img.convert('RGB')

            # Redimensionar si es muy grande (por ejemplo, ancho máx. 800px)
            max_width = 400
            if img.width > max_width:
                ratio = max_width / float(img.width)
                new_height = int(float(img.height) * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)

            # Guardamos en un buffer en memoria como JPEG con compresión
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=70)  # calidad entre 1-100 (70 es un buen balance)
            img_io.seek(0)

            return send_file(
                img_io,
                mimetype='image/jpeg',
                download_name='compressed.jpg'
            )
    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")
        abort(500, description="Error procesando imagen")

    

# app.py

if __name__ == '__main__':
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print('✅ Conexión exitosa a la base de datos.')
        except Exception as e:
            print(f'❌ Error de conexión a la base de datos: {e}')
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
        from models.motorcicle_type_part_seed import seed_motorcycle_type_parts
        seed_motorcycle_type_parts()
        from models.pickup_type_part_seed import seed_pickup_type_parts
        seed_pickup_type_parts()
        from models.hatchback_type_part_seed import seed_hatchback_vehicles_type_parts
        seed_hatchback_vehicles_type_parts()

    app.run(debug=True)


