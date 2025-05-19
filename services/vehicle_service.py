from repositories.vehicle_repository import VehicleRepository
from models.models import Vehicle
import uuid

def create(user_id, vehicle_type_id, model, brand, year, plate):
    # Verificar si el vehículo ya existe
    if VehicleRepository.get_by_plate(plate):
        return {'message': 'Vehículo existente'}, 400

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
        return {'message': 'Vehículo creado con éxito'}, 201
    except Exception as e:
        return {'message': f'Error al crear vehículo: {str(e)}'}, 500
