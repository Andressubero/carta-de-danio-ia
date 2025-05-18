from flask import Blueprint
from controllers.vehicle_controller import create_vehicle
from auth.utils import token_required

vehicle_bp = Blueprint('vehicles', __name__, url_prefix='/vehicle')
vehicle_bp.route('/create', methods=['POST'])(create_vehicle)