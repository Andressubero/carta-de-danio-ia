from extensions import db
from models.models import AIReport
import uuid

class ReportRepository:
    @staticmethod
    def get_by_state_id(id):
        return db.session.query(AIReport).filter_by(vehicle_state_id=id).one_or_none()