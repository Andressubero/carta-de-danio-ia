from extensions import db
from models.models import Vehicle, VehicleState, VehiclePart, VehicleTypePart, VehiclePartState, Part, Damage, DamageTypeEnum
import uuid
from datetime import date

class VehicleStateRepository:

    @staticmethod
    def save(vehicle_id):
        try:
            vehicle = db.session.query(Vehicle).filter_by(id=vehicle_id).first()
            if not vehicle:
                raise ValueError("Vehículo no encontrado")

            # Se crea el estado del vehiculo
            new_state = VehicleState(id=uuid.uuid4(), vehicle_id=vehicle.id, date=date.today())
            db.session.add(new_state)
            db.session.flush()

            # Se crean las partes del vehículo según su tipo
            parts = (
                db.session.query(Part)
                .join(VehicleTypePart, VehicleTypePart.part_id == Part.id)
                .filter(VehicleTypePart.vehicle_type_id == vehicle.vehicle_type_id)
                .all()
            )
            vehicle_parts = []
            for part in parts:
                vp = VehiclePart(
                    id=uuid.uuid4(),
                    name=part.name,
                    vehicle_id=vehicle.id,
                    part_id=part.id
                )
                db.session.add(vp)
                vehicle_parts.append(vp)
            db.session.flush()

            #Se crean el estado de las partes y sus daños
            for vp in vehicle_parts:
                vps = VehiclePartState(
                    id=uuid.uuid4(),
                    vehicle_state_id=new_state.id,
                    vehicle_part_id=vp.id,
                    image_path=""
                )
                db.session.add(vps)
                db.session.flush()

                damage = Damage(
                    id=uuid.uuid4(),
                    vehicle_part_state_id=vps.id,
                    damage_type=DamageTypeEnum.SIN_DANO,
                    description="Sin daño reportado",
                    fixed=False
                )
                db.session.add(damage)

            db.session.commit()
            return new_state
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al guardar estado del vehículo: {str(e)}")
