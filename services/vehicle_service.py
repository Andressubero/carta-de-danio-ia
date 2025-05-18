import jwt
import datetime
from flask import current_app
from extensions import db
from werkzeug.security import check_password_hash
from models.models import Vehicle
from werkzeug.security import generate_password_hash
import uuid

def create(user_id, vehicle_type_id, model, brand, year, plate):
    if not user_id or not vehicle_type_id or not model or not brand or not year or not plate:
        return {'message': 'Faltan campos obligatorios'}, 400

    existing = db.session.query(Vehicle).filter_by(plate=plate).first()
    if existing:
        return {'message': 'Vehículo existente'}, 400

    vehicle = Vehicle(
        id=uuid.uuid4(),
        user_id=user_id,
        vehicle_type_id=vehicle_type_id,
        model=model,
        brand=brand,
        year=year,
        plate=plate
    )

    db.session.add(vehicle)
    db.session.commit()

    return {'message': 'Vehículo creado con éxito'}, 201
