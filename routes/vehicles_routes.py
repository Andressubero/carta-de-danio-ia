from flask import Blueprint
from controllers.vehicle_controller import create_vehicle
from controllers.vehicle_controller import get_vehicle_by_id  

from auth.utils import token_required

vehicle_bp = Blueprint('vehicles', __name__, url_prefix='/vehicle')
vehicle_bp.route('/create', methods=['POST'])(create_vehicle)
vehicle_bp.route('/:id/', methods=['GET'])(get_vehicle_by_id)  # Assuming this is a placeholder for a get vehicle by ID route