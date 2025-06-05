from flask import Blueprint
from controllers.vehicle_controller import create_vehicle, get_vehicles_by_user_controller
from auth.utils import token_required

vehicle_bp = Blueprint('vehicles', __name__, url_prefix='/vehicle')

@vehicle_bp.route('/create', methods=['POST'])
@token_required
def create_vehicle_route(): return create_vehicle()

@vehicle_bp.route('/myVehicles', methods=['GET'])
@token_required
def get_vehicles_by_user(): return get_vehicles_by_user_controller()
from controllers.vehicle_controller import create_vehicle
from controllers.vehicle_controller import get_vehicle_by_id  

from auth.utils import token_required

vehicle_bp = Blueprint('vehicles', __name__, url_prefix='/vehicle')
vehicle_bp.route('/create', methods=['POST'])(create_vehicle)
vehicle_bp.route('/:id/', methods=['GET'])(get_vehicle_by_id)  # Assuming this is a placeholder for a get vehicle by ID route
