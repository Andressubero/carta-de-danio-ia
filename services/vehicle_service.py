from sqlalchemy.orm import joinedload
from repositories.vehicle_repository import VehicleRepository
from models.models import Vehicle
import uuid

def create(user_id, vehicle_type_id, model, brand, year, plate):
    # Verificar si el vehículo ya existe
    if VehicleRepository.get_by_plate(plate):
        return {'message': 'Vehículo existente', 'success': False}, 200

    # Crear instancia del vehículo
    vehicle = Vehicle(
        id=str(uuid.uuid4()),  # Convertimos UUID a string
        user_id=user_id,
        vehicle_type_id=vehicle_type_id,
        model=model,
        brand=brand,
        year=year,
        plate=plate
    )

    try:
        VehicleRepository.save(vehicle)
        return {'message': 'Vehículo creado con éxito', 'success': True}, 201
    except Exception as e:
        return {'message': f'Error al crear vehículo: {str(e)}'}, 500


def get_vehicle_by_id(id):
    return VehicleRepository.get_by_id(id)

def get_vehicle_with_parts(vehicle_id):
    return VehicleRepository.get_vehicle_with_parts(vehicle_id)