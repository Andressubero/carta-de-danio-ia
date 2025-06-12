from repositories.report_repository import ReportRepository
from repositories.role_repository import RoleRepository
from constants.errors import errors
import uuid


def get_by_state_id(id, role_id):
    role = RoleRepository.get_by_id(role_id)
    if role is None or role.name != 'admin':
        raise Exception(errors['NO_AUTORIZADO']['codigo'])
    return ReportRepository.get_by_state_id(id)
