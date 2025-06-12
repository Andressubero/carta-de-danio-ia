from extensions import db
from sqlalchemy.orm import joinedload
from models.models import AIReport, AIReportPartDamage
import uuid
from constants.errors import errors

class AIReportRepository:

    @staticmethod
    def save(data, vehicle_state_id):
        try:
            # Crear AIReport
            ai_report = AIReport(
                vehicle_state_id=vehicle_state_id,
                is_vehicle_valid=data.get("is_vehicle_valid"),
                image_type=data.get("image_type"),
                vehicle_type=data.get("vehicle_type"),
                estimated_brand=data.get("estimated_brand"),
                estimated_model=data.get("estimated_model"),
                image_quality=data.get("image_quality"),
                is_same_unit_as_reference=data.get("is_same_unit_as_reference"),
                same_unit_confidence=data.get("same_unit_confidence"),
                total_vehicle_damage_percentage=data.get("total_vehicle_damage_percentage"),
                additional_comments=data.get("additional_comments"),
                comparison_with_reference=data.get("comparison_with_reference"),
                validation_reasons=", ".join(data.get("validation_reasons", []))  # guarda como string separado por comas
            )

            # Guardar daños por parte
            part_damages_data = data.get("states", [])
            for state in part_damages_data:
                for part in state.get("parts", []):
                    for damage in part.get("damages", []):
                        part_damage = AIReportPartDamage(
                            part_name=part.get("name"),
                            severity=part.get("severity"),
                            damage_type=damage.get("type"),
                            damage_description=damage.get("description"),
                            confidence_percentage=damage.get("confidence_percentage"),
                            present_in_reference=damage.get("present_in_reference")
                        )
                        ai_report.part_damages.append(part_damage)

            # Guardar en DB
            db.session.add(ai_report)
            db.session.commit()

            return ai_report

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error saving AIReport: {str(e)}")

        
    @staticmethod
    def get_by_id(id):
        if not id:
            return None
        return db.session.query(AIReport).filter_by(id=id).first()

