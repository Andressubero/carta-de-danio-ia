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
"Retrovisor izquierdo",
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

    if "chasis lateral derecho" in name or "chasis trasero derecho" in name:
        return ImageTypeEnum.LATERAL_RIGHT
    if "chasis lateral izquierdo" in name or "chasis trasero izquierdo" in name:
        return ImageTypeEnum.LATERAL_LEFT
    if "estribo" in name or "tablero" in name or "tanque" in name or "asiento" in name or "techo" in name:
        return ImageTypeEnum.TOP
    if "manillar" in name or "espejo retrovisor" in name or "luz delantera lateral" in name or "guardabarro delantero" in name or "rueda delantera" in name or "capó" in name or "parabrisas" in name or "paragolpes delantero" in name or "guarda fango delantero" in name:
        return ImageTypeEnum.FRONT
    if "luz trasera" in name or "guardabarro trasero" in name or "rueda trasera" in name or "baúl" in name or "luneta" in name or "paragolpes trasero" in name or "guarda fango trasero" in name:
        return ImageTypeEnum.BACK
    if "derech" in name:
        return ImageTypeEnum.LATERAL_RIGHT
    if "izquierd" in name:
        return ImageTypeEnum.LATERAL_LEFT
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

