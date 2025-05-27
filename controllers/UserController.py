from flask import request, jsonify, make_response
from services.UserService import login_user, create_user_service, get_all_users_service
from services.role_service import get_role_by_name

def login_controller():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    token = login_user(username, password)

    if token:
        response = make_response(jsonify({'message': 'Login satisfactorio'}))
        response.set_cookie(
            key='token',
            value=token,
            httponly=True,        # protege contra JS (XSS) 
            samesite='Lax',       # evita CSRF básicos
            secure=False          # ⚠️ ponelo en True si usás HTTPS. Si secure=True, la cookie solo se enviará bajo HTTPS
        )
        return response
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 200

def create_user_controller():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_id = get_role_by_name("user").id

    result, status_code = create_user_service(username, email, password, role_id)
    return jsonify(result), status_code

def get_all_users_controller():
    result, status_code = get_all_users_service()
    return result, status_code