import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db
from .models import VehicleTypePart, VehicleType, Part


# Lista de relaciones a insertar
initial_two_door_type_part_seed = [
    "Techo",
    "Parabrisas",
    "Luneta Trasera",
    "Baúl",
    "Paragolpes trasero",
    "Capó",
    "Paragolpes delantero",
    "Rueda delantera derecha",
    "Rueda trasera derecha",
    "Ventana delantera derecha",
    "Ventana trasera derecha",
    "Puerta delantera derecha",
    "Guarda fango delantero derecho",
    "Guarda fango trasero derecho",
    "Luz delantera derecha",
    "Luz trasera derecha",
    "Retrovisor derecho",
    "Rueda delantera izquierda",
    "Rueda trasera izquierda",
    "Ventana delantera izquierda",
    "Ventana trasera izquierda",
    "Puerta delantera izquierda",
    "Guarda fango delantero izquierdo",
    "Guarda fango trasero izquierdo",
    "Luz delantera izquierda",
    "Luz trasera izquierda",
    "Retrovisor izquierdo"
]


def seed_hatchback_vehicles_type_parts():
    # Buscar el vehicle_type por nombre
    vehicle_type = db.session.query(VehicleType).filter_by(name="Hatchback").first()
    if not vehicle_type:
        print("❌ VehicleType 'Hatchback' no encontrado. Ejecutá primero el seed de VehicleType.")
        return

    for part_name in initial_two_door_type_part_seed:
        part = db.session.query(Part).filter_by(name=part_name).first()
        if not part:
            print(f"❌ Parte '{part_name}' no encontrada. Ejecutá primero el seed de Part.")
            continue

        # Verificar que no exista ya la relación
        existing = db.session.query(VehicleTypePart).filter_by(part_id=part.id, vehicle_type_id=vehicle_type.id).first()
        if not existing:
            new_relation = VehicleTypePart(
                id=uuid.uuid4(),
                vehicle_type_id=vehicle_type.id,
                part_id=part.id
            )
            db.session.add(new_relation)

    db.session.commit()
    print("----------------------------✅ Seeding de vehicle_type_parts para Hatchback completado.------------------------------")