import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db

from .models import Part
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
"Retrovisor izquierdo"
]

def seed_parts():
    for name in initial_parts:
        # Verifica si ya existe una parte con ese nombre
        existing = db.session.query(Part).filter_by(name=name).first()
        if not existing:
            part = Part(id=uuid.uuid4(), name=name)
            db.session.add(part)
    db.session.commit()
    print("Seeding de parts completado.")

