from flask import Blueprint
from controllers.vehicle_state_controller import create_vehicle_state
from controllers.vehicle_state_controller import get_all_vehicle_state
from auth.utils import token_required
from auth.utils import admin_required

vehicle_state_bp = Blueprint('states', __name__, url_prefix='/vehicle-state')


@vehicle_state_bp.route('/create', methods=['POST'])
@token_required
def protected_create_vehicle_state(*args, **kwargs):
    return create_vehicle_state(*args, **kwargs)

@vehicle_state_bp.route('/getall', methods=['GET'])
@token_required
def protected_get_all_vehicle_state(*args, **kwargs):
    return get_all_vehicle_state(*args, **kwargs)


