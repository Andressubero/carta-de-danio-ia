from flask import Blueprint
from controllers.vehicle_type_controller import get_all_vehicle_types

vehicle_types_bp = Blueprint('types', __name__, url_prefix='/vehicle-type')
vehicle_types_bp.route('/findAll', methods=['GET'])(get_all_vehicle_types)
