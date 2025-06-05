from flask import request, jsonify
from services.vehicle_service import  create
from services.vehicle_service import get_vehicle_by_id


def create_vehicle():
    data = request.get_json()
    # el user_id se debe sacar del jwt y añadirlo en la siguiente linea
    user_id = data.get('user_id')
    vehicle_type_id = data.get('vehicle_type_id')
    model = data.get('model')
    brand = data.get('brand')
    year = data.get('year')
    plate = data.get('plate')
    
    result, status_code = create(user_id, vehicle_type_id, model, brand, year, plate)
    return jsonify(result), status_code

def get_vehicle_by_id(vehicle_id):
    try:
        vehicle = get_vehicle_by_id(vehicle_id)
        if not vehicle:
            return jsonify({"message": "Vehicle not found"}), 404
        return jsonify(vehicle.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500