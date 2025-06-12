from flask import Blueprint
from controllers.vehicle_state_controller import create_vehicle_state, get_all_vehicle_state
from auth.utils import token_required

vehicle_state_bp = Blueprint('states', __name__, url_prefix='/vehicle-state')

@vehicle_state_bp.route('/create', methods=['POST'])
@token_required
def create_vehicle_state_route(): return create_vehicle_state()


@vehicle_state_bp.route('/get-all', methods=['GET'])
@token_required
def get_all_vehicle_state_route(): return get_all_vehicle_state()

