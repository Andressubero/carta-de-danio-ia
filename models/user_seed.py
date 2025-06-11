import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db
from werkzeug.security import generate_password_hash

from .models import User, Role
import uuid

# Lista de usuarios a insertar
initial_users = [
    {
    "username": "test_user",
    "email": "user@email.com",
    "password": "password",
    "role": "user"
    },
        {
    "username": "admin_user",
    "email": "admin@email.com",
    "password": "password",
    "role": "admin"
    }
]

def seed_users():
    for item in initial_users:
        # Obtener el Role dinámicamente
        role = db.session.query(Role).filter_by(name=item["role"]).first()
        if not role:
            print("❌ Rol no encontrado. Ejecuta primero el seed de roles.")
            continue
        
        existing = db.session.query(User).filter_by(username=item["username"]).first()
        if not existing:
            user = User(
                id=uuid.uuid4(),
                username=item["username"],
                email=item["email"],
                password=generate_password_hash(item["password"]),
                role_id=role.id
            )
            db.session.add(user)
    db.session.commit()
    print("Seeding de users completado.")
