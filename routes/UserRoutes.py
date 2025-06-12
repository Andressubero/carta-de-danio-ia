from flask import Blueprint
from controllers.UserController import login_controller, create_user_controller, get_all_users_controller, get_me
from auth.utils import token_required
from controllers.UserController import logout_controller
from auth.utils import admin_required

user_bp = Blueprint('users', __name__, url_prefix='/user')
user_bp.route('/login', methods=['POST'])(login_controller)
user_bp.route('/logout', methods=['POST'])(logout_controller)
user_bp.route('/create', methods=['POST'])(create_user_controller)

@user_bp.route('/findAll', methods=['GET'])
@token_required
@admin_required
def get_all_users_route():
    return get_all_users_controller()


@user_bp.route('/me', methods=['GET'])
@token_required
def get_me_route():
    return get_me()