from flask import Blueprint, request
from controllers.UserController import login_controller, create_user_controller

user_bp = Blueprint('users', __name__)
user_bp.route('/login', methods=['POST'])(login_controller)
user_bp.route('/create', methods=['POST'])(create_user_controller)