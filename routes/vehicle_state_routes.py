from flask import Blueprint
from controllers.vehicle_state_controller import create_vehicle_state
from controllers.vehicle_state_controller import get_all_vehicle_state
from auth.utils import token_required

vehicle_state_bp = Blueprint('states', __name__, url_prefix='/vehicle-state')
vehicle_state_bp.route('/create', methods=['POST'])(create_vehicle_state)
vehicle_state_bp.route('/getall', methods=['GET'])(get_all_vehicle_state)
