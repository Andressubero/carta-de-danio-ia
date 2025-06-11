import jwt
from flask import request, jsonify, current_app, g
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return jsonify({'message': 'Token requerido'}), 403

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
        
        g.user_id = payload['user_id']

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        admin_role_id = "b756cc08-b981-4183-9c81-2246937485a2"  
        if not hasattr(g, 'user') or g.user.role_id != admin_role_id:  
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated
