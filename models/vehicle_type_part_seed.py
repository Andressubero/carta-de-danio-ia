import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db
from .models import VehicleTypePart
from .models import VehicleType

# Sedán
vehicle_type_id = "65267e97-a850-4f82-b08f-e29779a438e4"

# Lista de relaciones a insertar
initial_vehicles_type_parts = [
    {"part_id": "58e3bffa-763b-45fc-8145-394973e7bcb0"},  # Techo
    {"part_id": "30d5a8b3-d32a-4c79-8b3d-b4f2fb21ed1d"},  # Parabrisas
    {"part_id": "d82579f8-d8b9-4727-b3c4-d7c5e4b4753e"},  # Luneta Trasera
    {"part_id": "852b75d4-d286-4c2e-854f-d74e34aa6ea9"},  # Baúl
    {"part_id": "9e3ddcb0-95ef-4d5f-ab1b-1073513241c3"},  # Paragolpes trasero
    {"part_id": "44bd7c34-8509-4fb1-a996-bc12dc1007bd"},  # Capó
    {"part_id": "96332e25-3e66-470a-8afa-6a1965954cf7"},  # Paragolpes delantero
    {"part_id": "02feee43-6436-49f7-987c-9068029c16db"},  # Rueda delantera derecha
    {"part_id": "5f7572ea-7ba7-429c-b6ad-d4f7fd040741"},  # Rueda trasera derecha
    {"part_id": "84e9afb2-5fd9-45bd-b362-636c330920e0"},  # Ventana delantera derecha
    {"part_id": "398a1eaf-4c8c-41fa-8a95-52dd29dbe01b"},  # Ventana trasera derecha
    {"part_id": "6c7be999-f9cc-4b07-8cfa-c75deba4157d"},  # Puerta delantera derecha
    {"part_id": "964db38a-a909-4e01-a632-8179aaa95c79"},  # Puerta trasera derecha
    {"part_id": "b4f8e32b-c556-457d-970a-1a4affe9295f"},  # Guarda fango delantero derecho
    {"part_id": "2bf9fbeb-362a-479c-a36c-0476f4febd57"},  # Guarda fango trasero derecho
    {"part_id": "2bf4b7c4-9c86-49d7-93d1-f2c5d31386d8"},  # Luz delantera derecha
    {"part_id": "d65eb6fb-e9ba-409f-8f90-a17f9495d078"},  # Luz trasera derecha
    {"part_id": "5881c3d2-69b4-4e75-8401-3cbcbb7852ab"},  # Retrovisor derecho
    {"part_id": "f59bfc9e-9312-402e-93ac-7b130a1ac1ac"},  # Rueda delantera izquierda
    {"part_id": "533df821-897e-4875-9e42-29a8cf8c7413"},  # Rueda trasera izquierda
    {"part_id": "f45ea6e1-98ae-4da4-a12b-f09b0246fa8d"},  # Ventana delantera izquierda
    {"part_id": "67245747-b5a4-4609-929a-47a92e628e10"},  # Ventana trasera izquierda
    {"part_id": "76f43f88-5351-427e-9253-6bb1a55326d8"},  # Puerta delantera izquierda
    {"part_id": "34bb0a0f-c680-4ee9-832d-5d006ae819cc"},  # Puerta trasera izquierda
    {"part_id": "802e0c23-5a39-43c2-98c1-c5184bbf038b"},  # Guarda fango delantero izquierdo
    {"part_id": "95e70550-6d68-4284-8f24-827fdad19195"},  # Guarda fango trasero izquierdo
    {"part_id": "dcbec0c5-5773-4af0-bf86-905e01f2d913"},  # Luz delantera izquierda
    {"part_id": "daddbf18-4912-4e33-9963-529d18d6e8df"},  # Luz trasera izquierda
    {"part_id": "3ee6e340-893c-4e54-b2a7-830775406e66"},  # Retrovisor izquierdo
]

def seed_vehicles_type_parts():
    # ✅ Validación del vehicle_type_id
    vehicle_type = db.session.query(VehicleType).filter_by(id=vehicle_type_id).first()
    if not vehicle_type:
        print(f"❌ El VehicleType con ID {vehicle_type_id} no existe.")
        return
    for item in initial_vehicles_type_parts:
        # Verifica si ya existe
        existing = db.session.query(VehicleTypePart).filter_by(part_id=item["part_id"],vehicle_type_id=vehicle_type_id).first()
        if not existing:
            new_relation = VehicleTypePart(
                id=uuid.uuid4(),
                vehicle_type_id=vehicle_type_id,
                part_id=item["part_id"]
            )
            db.session.add(new_relation)

    db.session.commit()
    print("Seeding de vehicle_type_parts completado.")