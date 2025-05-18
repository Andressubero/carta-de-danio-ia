import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db

from .models import Vehicle
import uuid

# Lista de partes a insertar
initial_vehicles = [
    {
    "user_id": "9a40de0c-796f-49de-89a6-c33046397858",
    "vehicle_type_id": "65267e97-a850-4f82-b08f-e29779a438e4",
    "model": "Serie 3",
    "brand": "BMW",
    "year": 2012,
    "plate": "ABC1234"
    }
]

def seed_vehicles():
    for item in initial_vehicles:
        # Verifica si ya existe un vehiculo con esa patente
        existing = db.session.query(Vehicle).filter_by(plate=item["plate"]).first()
        if not existing:
            vehicle = Vehicle(
                id=uuid.uuid4(),
                user_id=item["user_id"],
                vehicle_type_id=item["vehicle_type_id"],
                model=item["model"],
                brand=item["brand"],
                year=item["year"],
                plate=item["plate"]
            )
            db.session.add(vehicle)
    db.session.commit()
    print("Seeding de vehicles completado.")