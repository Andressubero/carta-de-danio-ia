import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db

from .models import VehicleType
import uuid

# Lista de partes a insertar
initial_vehicles_type = [
"Sedán"
]

def seed_vehicles_type():
    for name in initial_vehicles_type:
        # Verifica si ya existe una parte con ese nombre
        existing = db.session.query(VehicleType).filter_by(name=name).first()
        if not existing:
            vehicle = VehicleType(id=uuid.uuid4(), name=name)
            db.session.add(vehicle)
    db.session.commit()
    print("Seeding de vehicles types completado.")

