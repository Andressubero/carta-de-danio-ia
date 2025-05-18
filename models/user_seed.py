import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db

from .models import User
import uuid

# Lista de partes a insertar
initial_users = [
    {
    "username": "test_user",
    "email": "user@email.com",
    "password": "password",
    "role_id": "2c62c309-8762-4923-974e-cc220bb66c58"
    }
]

def seed_users():
    for item in initial_users:
        # Verifica si ya existe una parte con ese nombre
        existing = db.session.query(User).filter_by(username=item["username"]).first()
        if not existing:
            user = User(
                id=uuid.uuid4(),
                username=item["username"],
                email=item["email"],
                password=item["password"],
                role_id=item["role_id"]
            )
            db.session.add(user)
    db.session.commit()
    print("Seeding de users completado.")