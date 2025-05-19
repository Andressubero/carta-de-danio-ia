from extensions import db
from models.models import Vehicle

class VehicleRepository:
    @staticmethod
    def get_by_plate(plate):
        return db.session.query(Vehicle).filter_by(plate=plate).first()

    @staticmethod
    def save(vehicle):
        try:
            db.session.add(vehicle)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al guardar vehículo: {str(e)}")