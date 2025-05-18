from flask import Blueprint
from controllers.UserController import login_controller, create_user_controller, get_all_users_controller
from auth.utils import token_required

user_bp = Blueprint('users', __name__, url_prefix='/user')
user_bp.route('/login', methods=['POST'])(login_controller)
user_bp.route('/create', methods=['POST'])(create_user_controller)

@user_bp.route('/findAll', methods=['GET'])
@token_required
def get_all_users_route(): return get_all_users_controller()