from repositories.vehicle_state_repository import VehicleStateRepository

def create(vehicle_id):
    return VehicleStateRepository.save(vehicle_id)

   
