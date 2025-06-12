from flask import Blueprint
from controllers.vehicle_type_controller import get_all_vehicle_types
from auth.utils import token_required

vehicle_types_bp = Blueprint('types', __name__, url_prefix='/vehicle-type')

@vehicle_types_bp.route('/findAll', methods=['GET'])
@token_required
def protected_get_all_vehicle_types(*args, **kwargs):
    return get_all_vehicle_types(*args, **kwargs)