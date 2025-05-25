from extensions import db
from models.models import Vehicle, VehicleState, VehiclePart, VehicleTypePart, VehiclePartState, Part, Damage, DamageTypeEnum
import uuid
from datetime import date

class VehicleStateRepository:

    @staticmethod
    def save(vehicle_id, states_from_body, validation_reasons):
        try:
            vehicle = db.session.query(Vehicle).filter_by(id=vehicle_id).first()
            if not vehicle:
                raise ValueError("Vehículo no encontrado")

            if not validation_reasons or not isinstance(validation_reasons, list):
                validation_reasons = []  # Asegura que siempre sea una lista

            # convierto el array a string
            validation_reasons_string = ", ".join(item["reason"] for item in validation_reasons)

            # Se crea el estado del vehiculo
            new_state = VehicleState(id=uuid.uuid4(), vehicle_id=vehicle.id, date=date.today(), validation_reasons=validation_reasons_string if validation_reasons_string else None)
            db.session.add(new_state)
            db.session.flush()

            # Se obtienen las partes del vehiculo
            vehicle_parts = db.session.query(VehiclePart).filter_by(vehicle_id=vehicle.id,).all()

            # Creamos un diccionario con los estados recibidos desde el body, usando el partId como clave
            states_dict = {state['part_id']: state for state in states_from_body}

            # Se crean el estado de las partes y sus daños
            for vp in vehicle_parts:
                vps = VehiclePartState(
                    id=uuid.uuid4(),
                    vehicle_state_id=new_state.id,
                    vehicle_part_id=vp.id,
                    image_id="08c3d5b0-bfb2-487b-bec2-1a685ce1bf79"
                )
                db.session.add(vps)
                db.session.flush()

                # Verificamos si hay datos de daños enviados desde el front para esta parte
                part_state = states_dict.get(str(vp.part_id))
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
            raise Exception(f"Error al guardar estado del vehículo: {str(e)}")
