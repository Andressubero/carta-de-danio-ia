import jwt
import datetime
from flask import current_app, jsonify
from extensions import db
from werkzeug.security import check_password_hash
from models.models import User
from werkzeug.security import generate_password_hash
import uuid

def login_user(username, password):
    user = db.session.query(User).filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        payload = {
            'user_id': str(user.id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    return None

def create_user_service(username, email, password, role_id):
    if not username or not email or not password or not role_id:
        return {"success": False, "message": "Faltan datos"}, 200
    
    existing_user = db.session.query(User).filter_by(username=username).first()
    if existing_user:
        return {"success": False, "message": "Ya hay una cuenta registrada con este usuario"}, 200
    
    existing_email = db.session.query(User).filter_by(email=email).first()
    if existing_email:
        return {"success": False, "message": "Ya hay una cuenta registrada con este email"}, 200

    hashed_password = generate_password_hash(password)

    new_user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        password=hashed_password,
        role_id=role_id
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