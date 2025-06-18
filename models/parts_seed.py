import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db

from .models import Part, ImageTypeEnum
import uuid

# Lista de partes a insertar
initial_parts = [
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
"Puerta trasera derecha",
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
"Puerta trasera izquierda",
"Guarda fango delantero izquierdo",
"Guarda fango trasero izquierdo",
"Luz delantera izquierda",
"Luz trasera izquierda",
"Retrovisor izquierdo",
#de motocicleta
"Manillar izquierdo",
"Manillar derecho",
"Luz delantera",
"Tanque",
"Asiento",
"Rueda delantera",
"Rueda trasera",
"Luz trasera",
"Luz delantera lateral derecha",
"Luz delantera lateral izquierda",
"Guardabarro delantero",
"Estribo izquierdo",
"Estribo derecho",
"Chasis lateral izquierdo",
"Chasis lateral derecho",
"Chasis trasero izquierdo",
"Chasis trasero derecho",
"Guardabarro trasero",
"Tablero",
# Pickup
"Caja de carga",
]

def infer_image_type(part_name: str) -> ImageTypeEnum:
    name = part_name.lower()
    if "derech" in name:
        return ImageTypeEnum.LATERAL_RIGHT
    elif "izquierd" in name:
        return ImageTypeEnum.LATERAL_LEFT
    elif "capó" in name or "parabrisas" in name or "luz delantera" in name or "paragolpes delantero" in name or "guarda fango delantero" in name or "manillar" in name or "guardabarro delantero" in name or "rueda delantera" in name or "capó" in name or "parabrisas" in name or "paragolpes delantero" in name or "guarda fango delantero" in name:
        return ImageTypeEnum.FRONT
    elif "baúl" in name or "luneta" in name or "paragolpes trasero" in name or "luz trasera" in name or "guarda fango trasero" in name or "guardabarro trasero" in name or "rueda trasera" in name:
        return ImageTypeEnum.BACK
    elif "techo" in name or "estribo" in name or "tablero" in name or "tanque" in name or "asiento" in name:
        return ImageTypeEnum.TOP
    else:
        # Valor por defecto en caso de que no coincida nada (puedes ajustar esto)
        return ImageTypeEnum.TOP


def seed_parts():
    for name in initial_parts:
        # Verifica si ya existe una parte con ese nombre
        existing = db.session.query(Part).filter_by(name=name).first()
        if not existing:
            image_type = infer_image_type(name)
            part = Part(id=uuid.uuid4(), name=name, image_type=image_type)
            db.session.add(part)
    db.session.commit()
    print("Seeding de parts completado.")

