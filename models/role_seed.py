import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db

from .models import Role
import uuid

# Lista de partes a insertar
initial_roles = [
    "admin",
    "user"
]

def seed_roles():
    for item in initial_roles:
        # Verifica si ya existe una parte con ese nombre
        existing = db.session.query(Role).filter_by(name=item).first()
        if not existing:
            role = Role(
                name=item
            )
            db.session.add(role)
    db.session.commit()
    print("Seeding de roles completado.")