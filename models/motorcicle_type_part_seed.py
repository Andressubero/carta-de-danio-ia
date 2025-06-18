import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db
from .models import VehicleTypePart, VehicleType, Part

# Lista de partes asociadas a una motocicleta
initial_motorcycle_part_names = [
    "Manillar izquierdo",
    "Manillar derecho",
    "Retrovisor izquierdo",
    "Retrovisor derecho",
    "Luz delantera",
    "Tanque",
    "Asiento",
    "Rueda delantera",
    "Rueda trasera",
    "Luz trasera",
    "Luz trasera derecha",
    "Luz trasera izquierda",
    "Luz delantera lateral derecha",
    "Luz delantera lateral izquierda",
    "Guardabarro delantero",
    "Guardabarro trasero",
    "Estribo izquierdo",
    "Estribo derecho",
    "Chasis lateral izquierdo",
    "Chasis lateral derecho",
    "Chasis trasero izquierdo",
    "Chasis trasero derecho",
    "Tablero"
]

def seed_motorcycle_type_parts():
    vehicle_type = db.session.query(VehicleType).filter_by(name="Motocicleta").first()
    if not vehicle_type:
        print("❌ VehicleType 'Motocicleta' no encontrado. Ejecutá primero el seed de VehicleType.")
        return

    for part_name in initial_motorcycle_part_names:
        part = db.session.query(Part).filter_by(name=part_name).first()
        if not part:
            print(f"❌ Parte '{part_name}' no encontrada. Ejecutá primero el seed de Part. Motocicleta")
            continue

        # Verificar si ya existe la relación
        existing = db.session.query(VehicleTypePart).filter_by(
            part_id=part.id,
            vehicle_type_id=vehicle_type.id
        ).first()

        if not existing:
            new_relation = VehicleTypePart(
                id=uuid.uuid4(),
                vehicle_type_id=vehicle_type.id,
                part_id=part.id
            )
            db.session.add(new_relation)

    db.session.commit()
    print("✅ Seeding de partes para 'Motocicleta' completado.")