from flask import request, jsonify
from services.vehicle_state_service import create
from services.vehicle_state_service import get_all
import json

def create_vehicle_state():
    vehicle_id = request.form.get('vehicle_id')
    date = request.form.get('date')
    states_raw = request.form.get('states')
    states = json.loads(states_raw) if states_raw else None

    image_lateral_right = request.files.get('lateral_right')
    image_lateral_left = request.files.get('lateral_left')
    image_front = request.files.get('front')
    image_back = request.files.get('back')
    image_top = request.files.get('top')
    print("Received images:", {
        "lateral_right": image_lateral_right,
        "lateral_left": image_lateral_left,
        "front": image_front,
        "back": image_back,
        "top": image_top
    })

    try:
        vehicle_state = create(
        vehicle_id,
        states,
        date,
        image_lateral_right,
        image_lateral_left,
        image_front,
        image_back,
        image_top
        )
        return jsonify({
            "message": "Estado del vehículo creado exitosamente",
        }), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_all_vehicle_state():
    try:
        vehicle_states = get_all()
        serialized_states = [vs.to_dict() for vs in vehicle_states]
        return jsonify(serialized_states), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


