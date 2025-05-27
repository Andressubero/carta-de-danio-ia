from extensions import db
from sqlalchemy.orm import joinedload
from models.models import Vehicle, Part, VehiclePart, VehicleTypePart
import uuid
from constants.errors import errors

class VehicleRepository:
    @staticmethod
    def get_by_plate(plate):
        return db.session.query(Vehicle).filter_by(plate=plate).first()

    @staticmethod
    def save(vehicle):
        try:
            db.session.add(vehicle)
            db.session.flush()

            parts = (
                db.session.query(Part)
                .join(VehicleTypePart, VehicleTypePart.part_id == Part.id)
                .filter(VehicleTypePart.vehicle_type_id == vehicle.vehicle_type_id)
                .all()
            )

            for part in parts:
                vp = VehiclePart(
                    id=uuid.uuid4(),
                    name=part.name,
                    vehicle_id=vehicle.id,
                    part_id=part.id
                )
                db.session.add(vp)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"{errors['ERROR_GUARDAR_VEHICULO']['codigo']}: {str(e)}")


    def get_by_id(id):
        return db.session.query(Vehicle).filter_by(id=vehicle_id).first()
    
    def get_vehicle_with_parts(vehicle_id):
        return db.session.query(Vehicle)\
            .options(joinedload(Vehicle.parts))\
            .filter(Vehicle.id == vehicle_id)\
            .first()
