from flask import request, jsonify
from services.report_service import get_by_state_id
from constants.errors import errors
from flask import g
import json

def get_report_by_vehicle_state_id(vehicle_state_id):
    try:
        role_id = g.role_id
        report = get_by_state_id(vehicle_state_id, role_id)
        if not report:
            return jsonify({
                "error": errors['REPORTE_NO_ENCONTRADO']['codigo']
            }), 404

        return jsonify(report.to_dict()), 200

    except Exception as e:
        error_code = str(e)
        if error_code == errors['NO_AUTORIZADO']['codigo']:
            return jsonify({"message": error_code}), 403
        return jsonify({
            "error": "Error al obtener el reporte",
            "detalle": str(e)
        }), 500


