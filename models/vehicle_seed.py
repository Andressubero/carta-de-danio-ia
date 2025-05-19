import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db
from .models import Vehicle, User, VehicleType
import uuid

# Lista de vehículos a insertar
initial_vehicles = [
    {
        "user_email": "user@email.com",        # Buscar por email
        "vehicle_type_name": "Sedán",          # Buscar por nombre
        "model": "Serie 3",
        "brand": "BMW",
        "year": 2012,
        "plate": "ABC1234"
    }
]

def seed_vehicles():
    for item in initial_vehicles:
        # Buscar el usuario por email
        user = db.session.query(User).filter_by(email=item["user_email"]).first()
        if not user:
            print(f"❌ Usuario con email '{item['user_email']}' no encontrado. Ejecuta primero el seed de usuarios.")
            continue

        # Buscar el tipo de vehículo por nombre
        vehicle_type = db.session.query(VehicleType).filter_by(name=item["vehicle_type_name"]).first()
        if not vehicle_type:
            print(f"❌ Tipo de vehículo '{item['vehicle_type_name']}' no encontrado. Ejecuta primero el seed de tipos de vehículos.")
            continue

        # Verificar si ya existe la patente
        existing = db.session.query(Vehicle).filter_by(plate=item["plate"]).first()
        if not existing:
            vehicle = Vehicle(
                id=uuid.uuid4(),
                user_id=user.id,
                vehicle_type_id=vehicle_type.id,
                model=item["model"],
                brand=item["brand"],
                year=item["year"],
                plate=item["plate"]
            )
            db.session.add(vehicle)
            print(f"✅ Vehículo '{item['plate']}' insertado.")
        else:
            print(f"ℹ️ Vehículo con patente '{item['plate']}' ya existe. Saltando.")

    db.session.commit()
    print("✅ Seeding de vehicles completado.")
