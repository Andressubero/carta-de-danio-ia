import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db
from .models import VehicleTypePart, VehicleType, Part

pickup_part_names = [
    "Techo",
    "Parabrisas",
    "Luneta Trasera",
    "Paragolpes trasero",
    "Capó",
    "Paragolpes delantero",
    "Rueda delantera derecha",
    "Rueda trasera derecha",
    "Puerta delantera derecha",
    "Guarda fango delantero derecho",
    "Guarda fango trasero derecho",
    "Luz delantera derecha",
    "Luz trasera derecha",
    "Retrovisor derecho",
    "Rueda delantera izquierda",
    "Rueda trasera izquierda",
    "Puerta delantera izquierda",
    "Guarda fango delantero izquierdo",
    "Guarda fango trasero izquierdo",
    "Luz delantera izquierda",
    "Luz trasera izquierda",
    "Retrovisor izquierdo",
    "Caja de carga",
    "Ventana delantera izquierda",
    "Ventana delantera derecha",
]

def seed_pickup_type_parts():
    vehicle_type = db.session.query(VehicleType).filter_by(name="Pickup").first()
    if not vehicle_type:
        print("❌ VehicleType 'Pickup' no encontrado. Ejecutá primero el seed de VehicleType.")
        return

    for part_name in pickup_part_names:
        part = db.session.query(Part).filter_by(name=part_name).first()
        if not part:
            print(f"❌ Parte '{part_name}' no encontrada. Ejecutá primero el seed de Part. Pickup")
            continue

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
    print("✅ Seeding de partes para 'Pickup' completado.")