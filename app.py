import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request
from sqlalchemy import text
from config import Config
from extensions import db
from models.models import Base
from routes.UserRoutes import user_bp  # Importá el Base desde tu models
from routes.vehicles_routes import vehicle_bp 
from routes.vehicle_state_routes import vehicle_state_bp 
from utils.ai import call_llm

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(user_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(vehicle_state_bp)

# Inicializar extensiones
db.init_app(app)

# Configurar carpeta de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

            ref_image_path = ''
            if ref_image and ref_image.filename != "":
                ref_image_path = os.path.join(app.config['UPLOAD_FOLDER'], ref_image.filename)
                ref_image.save(ref_image_path)

            llm_data = [
	            {	#imagen lateral izquierda
	        	    'image': image_path,
	        	    'parts': [
                        { 
                            'part': 'frente delantero antes', 
                            'damages': []
                        }
                    ]
                },
	            {	#imagen lateral derecha
	        	    'image': ref_image_path,
	        	    'parts': [
                        { 
                            'part': 'frente delantero despues', 
                            'damages': ['abolladura', 'rayon']
                        }
                    ]
                }
            ]

            try:
                result = call_llm(llm_data, 'COMP')
            except Exception as e:
                result = f'Error: {e}'

    return render_template('index.html', result=result)

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


