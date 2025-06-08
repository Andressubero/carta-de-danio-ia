import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request
from sqlalchemy import text
from config import Config
from extensions import db
from models.models import Base
from flask_cors import CORS
from routes.UserRoutes import user_bp  # Importá el Base desde tu models
from routes.vehicles_routes import vehicle_bp 
from routes.vehicle_state_routes import vehicle_state_bp 
from routes.vehicle_type_routes import vehicle_types_bp
from utils.ai import call_llm

load_dotenv()
app = Flask(__name__)
CORS(app, supports_credentials=True ,origins=["http://localhost:5173"],)
app.config.from_object(Config)
app.register_blueprint(user_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(vehicle_types_bp)
app.register_blueprint(vehicle_state_bp)
#CORS(app)


# Inicializar extensiones
db.init_app(app)

# Configurar carpeta de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from flask import render_template, request, redirect, url_for, flash

@app.route("/", methods=["GET"])
def index():
    return render_template("carta.html")

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

    app.run(debug=True)


