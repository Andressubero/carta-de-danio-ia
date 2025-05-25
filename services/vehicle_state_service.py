from flask import request, jsonify
from repositories.vehicle_state_repository import VehicleStateRepository
from extensions import db
from utils.date import get_image_capture_date
from models.models import ImageTypeEnum, Part
from datetime import datetime, timedelta

def create(
vehicle_id,
states,
date,
image_lateral_right=None,
image_lateral_left=None,
image_front=None,
image_back=None,
image_top=None
):
    if not vehicle_id or not date:
        raise ValueError("Datos necesarios incorrectos")
    
    if not isinstance(states, list) or not states:
        raise ValueError("Estado de partes inválida")

    available_images = {
        ImageTypeEnum.LATERAL_RIGHT: image_lateral_right,
        ImageTypeEnum.LATERAL_LEFT: image_lateral_left,
        ImageTypeEnum.FRONT: image_front,
        ImageTypeEnum.BACK: image_back,
        ImageTypeEnum.TOP: image_top,
    }

    try:
        reference_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Formato de fecha inválido. Se espera YYYY-MM-DD")

    validation_reasons = []

    for state in states:
        part_id = state.get('part_id')
        damages = state.get('damages')

        if not part_id or not damages:
            raise ValueError("Datos incorrectos en states")
        
        part = db.session.query(Part).filter_by(id=part_id).first()
        if not part:
            raise ValueError(f"Part con id {part_id} no encontrada")
        
        image_type_required = part.image_type
        image_file = available_images.get(image_type_required)

        if not image_file:
            raise ValueError(
                f"Falta la imagen requerida para la parte '{part.name}': {image_type_required.value}"
            )

        capture_date = None

        try:
            capture_date = get_image_capture_date(image_file)
            if capture_date < reference_date:
                validation_reasons.append({
                    "reason": f"Imagen fue tomada antes de la fecha declarada ({capture_date} < {reference_date}), para la parte {part_id}"
                })

            if capture_date - reference_date > timedelta(days=90):
                validation_reasons.append({
                    "reason": f"Fecha declarada es mayor a 90 días antes de la imagen ({capture_date} - {reference_date}), para la parte {part_id}"
                })
        except ValueError as e:
            validation_reasons.append({"reason": "FECHA NO ENCONTRADA O FORMATO INVALIDO"})
        except RuntimeError as e:
            validation_reasons.append({"reason": "ERROR INESPERADO VALIDANDO FECHA"})



    return VehicleStateRepository.save(vehicle_id, states, validation_reasons)

