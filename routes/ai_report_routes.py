from flask import Blueprint
from controllers.report_controller import get_report_by_vehicle_state_id
from auth.utils import token_required

report_bp = Blueprint('reports', __name__, url_prefix='/report')

@report_bp.route('/get-detail/<string:vehicle_state_id>', methods=['GET'])
@token_required
def get_report_by_vehicle_state_id_route(vehicle_state_id):
    return get_report_by_vehicle_state_id(vehicle_state_id)
