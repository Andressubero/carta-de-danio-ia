from flask import request, jsonify, g
from services.vehicle_service import create, get_vehicles

def create_vehicle():
    data = request.get_json()
    user_id = g.user_id
    vehicle_type_id = data.get('vehicle_type_id')
    model = data.get('model')
    brand = data.get('brand')
    year = data.get('year')
    plate = data.get('plate')
    
    result, status_code = create(user_id, vehicle_type_id, model, brand, year, plate)
    return jsonify(result), status_code

def get_vehicles_by_user_controller():
    user_id = g.user_id
    vehicles = get_vehicles(user_id)

    vehicle_list = [
        {
            "id": v.id,
            "brand": v.brand,
            "model": v.model,
            "year": v.year,
            "plate": v.plate,
            "vehicle_type_id": v.vehicle_type_id
        }
        for v in vehicles
    ]

    return jsonify(vehicle_list), 200