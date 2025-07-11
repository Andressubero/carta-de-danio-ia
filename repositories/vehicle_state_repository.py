from extensions import db
from models.models import Vehicle, VehicleState, VehiclePart, VehicleTypePart, VehiclePartState, Part, Damage, DamageTypeEnum
import uuid
from datetime import date, datetime
from constants.errors import errors

class VehicleStateRepository:

    @staticmethod
    def save(vehicle_id, states_from_body, validation_reasons, declared_date):
        try:
            vehicle = db.session.query(Vehicle).filter_by(id=vehicle_id).first()
            if not vehicle:
                raise ValueError(f"{errors['DATOS_INSUFICIENTES']['codigo']}")

            if not validation_reasons or not isinstance(validation_reasons, list):
                validation_reasons = []  # Asegura que siempre sea una lista

            # convierto el array a string
            validation_reasons_string = ", ".join(item["reason"] for item in validation_reasons)

            # Se crea el estado del vehiculo
            new_state = VehicleState(id=uuid.uuid4(), vehicle_id=vehicle.id, creation_date=datetime.utcnow(),declared_date=declared_date, validation_reasons=validation_reasons_string if validation_reasons_string else None)
            db.session.add(new_state)
            db.session.flush()

            # Se obtienen las partes del vehiculo
            vehicle_parts = db.session.query(VehiclePart).filter_by(vehicle_id=vehicle.id,).all()

            # Creamos un diccionario con los estados recibidos desde el body, usando el partId como clave
            states_dict = {str(state['part_id']): state for state in states_from_body}
            
            # Se crean el estado de las partes y sus daños
            for vp in vehicle_parts:
                part_state = states_dict.get(str(vp.id))
                image_path = part_state.get("image_path") if part_state else None
                if not image_path:
                    print(f"⚠️ Parte {vp.id} omitida: sin imagen")
                    continue
                vps = VehiclePartState(
                    id=uuid.uuid4(),
                    vehicle_state_id=new_state.id,
                    vehicle_part_id=vp.id,
                    image = image_path
                )
                db.session.add(vps)
                db.session.flush()

                # Verificamos si hay datos de daños enviados desde el front para esta parte
                
                if part_state and part_state.get("damages"):
                    for dmg in part_state["damages"]:
                        damage = Damage(
                            id=uuid.uuid4(),
                            vehicle_part_state_id=vps.id,
                            damage_type=dmg["damage_type"],
                            description=dmg.get("description", ""),
                            fixed=False
                        )
                        db.session.add(damage)
                else:
                    # Si no hay daños especificados, agregamos uno por defecto
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
            print(f" error: {e}")
            raise Exception(f"{errors['ERROR_GUARDAR_ESTADO']['codigo']}")


    @staticmethod
    def get_all_by_vehicle_id(vehicle_id):
        return (
            db.session.query(VehicleState)
            .filter_by(vehicle_id=vehicle_id)
            .order_by(VehicleState.creation_date.desc())
            .all()
        )
    
    @staticmethod
    def get_all():
        return (
            db.session.query(VehicleState)
            .order_by(VehicleState.creation_date.desc())
            .all()
        )

    @staticmethod
    def get_by_id(id):
        query = db.session.query(VehicleState).filter(VehicleState.id == id)
        return query.order_by(VehicleState.creation_date.desc()).first()

    @staticmethod
    def get_all_summary():
        return (
            db.session.query(VehicleState)
            .order_by(VehicleState.creation_date.desc())
            .all()
        )

    @staticmethod
    def get_all_by_user(user_id):
        return (
            db.session.query(VehicleState)
            .join(Vehicle)
            .filter(Vehicle.user_id == user_id)
            .order_by(VehicleState.creation_date.desc())
            .all()
        )

    @staticmethod
    def get_all_by_user_summary(user_id):
        return (
            db.session.query(VehicleState)
            .join(Vehicle)
            .filter(Vehicle.user_id == user_id)
            .order_by(VehicleState.creation_date.desc())
            .all()
        )
    
    @staticmethod
    def get_latest_by_vehicle_id(vehicle_id):
        return (
            db.session.query(VehicleState)
            .filter_by(vehicle_id=vehicle_id)
            .order_by(VehicleState.creation_date.desc())
            .first()
        )

    @staticmethod
    def get_latest_vehicle_part_state_by_vehicle_part_id(vehicle_part_id):
        return (
            db.session.query(VehiclePartState)
            .filter(VehiclePartState.vehicle_part_id == vehicle_part_id)
            .order_by(VehiclePartState.creation_date.desc())
            .first()
        )

    @staticmethod
    def change_validation_state(id, validation_state):
        state = db.session.query(VehicleState).filter_by(id=id).first()
        if state:
            state.validation_state = validation_state
            db.session.commit()
        else:
            raise ValueError(f"VehicleState con id {id} no encontrado.")
    
    @staticmethod
    def is_first_state(vehicle_id):
        state = db.session.query(VehicleState).filter_by(vehicle_id=vehicle_id).first()
        if state:
            return False
        else:
            return True

