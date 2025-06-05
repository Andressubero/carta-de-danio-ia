from extensions import db
from models.models import VehicleType

def get_all():
    vehicle_types = db.session.query(VehicleType).all()
    return [
        {
            'id': str(vehicle_type.id),
            'name': vehicle_type.name
        } for vehicle_type in vehicle_types
    ]