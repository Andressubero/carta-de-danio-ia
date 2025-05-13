import jwt
import datetime
from flask import current_app
from extensions import db
from werkzeug.security import check_password_hash
from models.models import User
from werkzeug.security import generate_password_hash
import uuid

def login_user(username, password):
    user = db.session.query(User).filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        payload = {
            'user': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    return None

def create_user_service(username, email, password, role_id):
    if not username or not email or not password or not role_id:
        return {'message': 'Faltan campos obligatorios'}, 400

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

    return {'message': 'Usuario creado con éxito'}, 201