from flask import request, jsonify
from services.UserService import login_user, create_user_service, get_all_users_service

def login_controller():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    token = login_user(username, password)

    if token:
        return jsonify({'message': 'Login satisfactorio.', 'token': token})
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401

def create_user_controller():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')

    result, status_code = create_user_service(username, email, password, role_id)
    return jsonify(result), status_code

def get_all_users_controller():
    result, status_code = get_all_users_service()
    return result, status_code