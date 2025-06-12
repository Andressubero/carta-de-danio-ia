from extensions import db
from models.models import Role
import uuid

class RoleRepository:
    @staticmethod
    def get_by_id(id):
        return db.session.query(Role).filter_by(id=id).one_or_none()