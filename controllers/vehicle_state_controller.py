from flask import request, jsonify, g
from services.vehicle_state_service import create, change_validation_state_service, get_all, is_first_state_service, get_all_summary, get_by_id
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
        role_id = g.role_id
        user_id = g.user_id
        vehicle_states = get_all(user_id, role_id)
        serialized_states = [vs.to_dict() for vs in vehicle_states]
        return jsonify(serialized_states), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_state_by_id(id):
    try:
        role_id = g.role_id
        vs = get_by_id(role_id, id)
        serialized_state = vs.to_dict()
        return jsonify(serialized_state), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_all_vehicle_state_summary():
    try:
        role_id = g.role_id
        user_id = g.user_id
        vehicle_states = get_all_summary(user_id, role_id)
        serialized_states = [vs.to_summary_dict() for vs in vehicle_states]
        return jsonify(serialized_states), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def change_validation_state():
    try:
        data = request.get_json()
        state_id = data.get("id")
        validation_state = data.get("validation_state")

        if not state_id or not validation_state:
            raise ValueError("Faltan datos requeridos")

        role_id = g.get("role_id")
        if not role_id:
            raise RuntimeError("No se encontró el role_id")

        change_validation_state_service(validation_state, state_id, role_id)

        return jsonify({"message": "Estado cambiado correctamente"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
def is_first_state(vehicle_id):
    try:
        if not vehicle_id:
            raise ValueError("Faltan datos requeridos")
        isFirst = is_first_state_service(vehicle_id)
        return jsonify({"isFirst": bool(isFirst)}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

