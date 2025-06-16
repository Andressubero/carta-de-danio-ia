from flask import request, jsonify, make_response, g
from services.user_service import login_user, create_user_service, get_all_users_service, get_user_by_id

def login_controller():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    token = login_user(username, password)

    if token:
        response = make_response(jsonify({'message': 'Login satisfactorio', 'token': token}))
        response.set_cookie(
            key='token',
            value=token,
            max_age=3600,         # 1 hora
            httponly=True,        # protege contra JS (XSS) 
            samesite='Lax',       # evita CSRF básicos
            secure=False          # ⚠️ ponelo en True si usás HTTPS. Si secure=True, la cookie solo se enviará bajo HTTPS
        )
        return response
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 403
    

def logout_controller():
    # Elimina la cookie del token seteando valor vacío y expiración en el pasado
    response = make_response(jsonify({'message': 'Logout exitoso'}))
    response.set_cookie(
        key='token',
        value='',
        httponly=True,
        samesite='Lax',
        expires=0,
        secure=False # True si usás HTTPS
    )
    return response

def create_user_controller():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    result, status_code = create_user_service(username, email, password)
    return jsonify(result), status_code

def get_all_users_controller():
    result, status_code = get_all_users_service()
    return result, status_code

def get_me():
    user = get_user_by_id(g.user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    return jsonify(user.to_dict()), 200