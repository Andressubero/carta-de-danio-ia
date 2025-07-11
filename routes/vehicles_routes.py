from flask import Blueprint
from controllers.vehicle_controller import create_vehicle, get_vehicles_by_user_controller, get_vehicle_by_id, get_vehicle_with_parts_by_id, edit_vehicle_controller, delete_vehicle_controller
from auth.utils import token_required

vehicle_bp = Blueprint('vehicles', __name__, url_prefix='/vehicle')

@vehicle_bp.route('/create', methods=['POST'])
@token_required
def create_vehicle_route(): return create_vehicle()

@vehicle_bp.route('/myVehicles', methods=['GET'])
@token_required
def get_vehicles_by_user(): return get_vehicles_by_user_controller()

@vehicle_bp.route('/<string:vehicle_id>', methods=['GET'])
@token_required
def get_by_id(vehicle_id): return get_vehicle_by_id(vehicle_id)

@vehicle_bp.route('vehicle-with-parts/<string:vehicle_id>', methods=['GET'])
@token_required
def get_vehicle_with_parts_by_id_route(vehicle_id):
    return get_vehicle_with_parts_by_id(vehicle_id)

@vehicle_bp.route('edit/<string:vehicle_id>', methods=['PUT'])
@token_required
def edit_vehicle(vehicle_id):
    return edit_vehicle_controller(vehicle_id)

@vehicle_bp.route('delete/<string:vehicle_id>', methods=['PUT'])
@token_required
def delete_vehicle(vehicle_id):
    return delete_vehicle_controller(vehicle_id)