import jwt
import datetime
from flask import current_app
from extensions import db
from werkzeug.security import check_password_hash
from models.models import User
from werkzeug.security import generate_password_hash
from services.role_service import get_role_by_name
import uuid
import re

def validar_password(password):
    if not 8 <= len(password) <= 15:
        raise ValueError("La contraseña debe tener entre 8 y 15 caracteres")

    if not re.search(r"\d", password):
        raise ValueError("La contraseña debe contener al menos un número")

    if not re.search(r"[^\w\s]", password):  # busca un carácter especial
        raise ValueError("La contraseña debe contener al menos un carácter especial")

def login_user(username, password):
    user = db.session.query(User).filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        payload = {
            'user_id': str(user.id),
            "username": user.username,
            'role_id': str(user.role_id) if user.role_id else 'user',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    return None

def create_user_service(username, email, password):
    if not username or not email or not password:
        return {"success": False, "message": "Faltan datos"}, 200
    
    existing_user = db.session.query(User).filter_by(username=username).first()
    if existing_user:
        return {"success": False, "message": "Ya hay una cuenta registrada con este usuario"}, 200
    
    existing_email = db.session.query(User).filter_by(email=email).first()
    if existing_email:
        return {"success": False, "message": "Ya hay una cuenta registrada con este email"}, 200

    validar_password(password)

    hashed_password = generate_password_hash(password)

    new_user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        password=hashed_password,
        role_id=get_role_by_name("user").id
    )

    db.session.add(new_user)
    db.session.commit()

    return {"success": True, "message": "Usuario registrado con éxito"}, 201

def get_all_users_service():
    try:
        users = db.session.query(User).all()
        users_data = [
            {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'role_id': str(user.role_id)
            } for user in users
        ]
        return {'users': users_data}, 200
    except Exception as e:
        return {'error': str(e)}, 500
    

def get_user_by_id(user_id):
    return db.session.query(User).get(user_id)

def edit_password_service(user_id, new_password):
    if not user_id or not new_password:
        raise ValueError("Faltan datos")

    validar_password(new_password)

    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado")

    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password
    db.session.commit()

    return user
