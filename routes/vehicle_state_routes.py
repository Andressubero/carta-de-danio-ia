from flask import Blueprint
from controllers.vehicle_state_controller import create_vehicle_state, get_all_vehicle_state, change_validation_state, is_first_state
from auth.utils import token_required
from auth.utils import admin_required

vehicle_state_bp = Blueprint('states', __name__, url_prefix='/vehicle-state')

@vehicle_state_bp.route('/create', methods=['POST'])
def create_vehicle_state_route(): return create_vehicle_state()


@vehicle_state_bp.route('/get-all', methods=['GET'])
@token_required
def get_all_vehicle_state_route(): return get_all_vehicle_state()

@vehicle_state_bp.route('/change-state', methods=['POST'])
@token_required
def change_validation_state_route(): return change_validation_state()

@vehicle_state_bp.route('/is-first-state/<string:vehicle_id>', methods=['GET'])
@token_required
def is_first_state_route(vehicle_id): return is_first_state(vehicle_id)


