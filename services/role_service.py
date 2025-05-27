from extensions import db
from models.models import Role

def get_role_by_name(role_name):
    role = db.session.query(Role).filter_by(name=role_name).first()
    if not role:
        raise LookupError(f"No se encontró el rol con nombre: {role_name}")

    return role