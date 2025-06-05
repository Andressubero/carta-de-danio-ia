from flask import jsonify
from services.vehicle_type_service import get_all

def get_all_vehicle_types():
    try:
        vehicle_types = get_all()
        if not vehicle_types:
            return jsonify({"message": "No se encontraron tipos de vehículos"}), 404

        return jsonify({"vehicle_types": vehicle_types}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500