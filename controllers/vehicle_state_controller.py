from flask import request, jsonify
from services.vehicle_state_service import create

def create_vehicle_state():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')

    try:
        vehicle_state = create(vehicle_id)
        return jsonify({
            "message": "Estado del vehículo creado exitosamente",
            "vehicle_state_id": str(vehicle_state.id)
        }), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


