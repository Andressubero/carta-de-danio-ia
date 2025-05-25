from flask import request, jsonify
from repositories.vehicle_state_repository import VehicleStateRepository
from extensions import db
from utils.date import get_image_capture_date
from models.models import ImageTypeEnum, Part
from datetime import datetime, timedelta
from constants.errors import errors
from flask import current_app as app
import uuid
import os
import re

def simple_secure_filename(filename):
    """
    Remueve caracteres no válidos y reemplaza espacios por guiones bajos.
    """
    filename = re.sub(r'[^A-Za-z0-9_.-]', '_', filename)
    return filename

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
        raise ValueError(f"{errors['VEHICULO_NO_ENCONTRADO']['codigo']}")
    
    if not isinstance(states, list) or not states:
        raise ValueError(f"{errors['DATOS_INSUFICIENTES']['codigo']}")

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
        raise ValueError(f"{errors['FECHA_FORMATO_INCORRECTO']['codigo']}")

    validation_reasons = []
    saved_images = set()
    # Estructura auxiliar para agrupar por image_type
    image_groups = {}
    image_paths = {}

    for state in states:
        part_id = state.get('part_id')
        damages = state.get('damages')
        if not isinstance(damages, list) or not damages:
            raise ValueError(f"{errors['STATES_DATOS_INCORRECTOS']['codigo']}")

        if not part_id or not damages:
            raise ValueError(f"{errors['STATES_DATOS_INCORRECTOS']['codigo']}")
        
        part = db.session.query(Part).filter_by(id=part_id).first()
        if not part:
            raise ValueError(f"{errors['PARTE_NO_ENCONTRADA']['codigo']}")
        
        image_type_required = part.image_type
        image_file = available_images.get(image_type_required)

        if not image_file:
            raise ValueError(
                f"{errors['FALTA_IMAGEN']['codigo']}:{part.name}"
            )

        capture_date = None
        
        try:
            capture_date = get_image_capture_date(image_file)
            if capture_date.date() < reference_date.date():
                validation_reasons.append({
                    "reason": f"{errors['FECHA_TOMADA_ANTES']['codigo']}:{image_type_required}"
                })

            if (capture_date.date() - reference_date.date()) > timedelta(days=90):
                validation_reasons.append({
                    "reason": f"{errors['FECHA_MAYOR_90_DIAS']['codigo']}:{image_type_required}"
                })
        except ValueError as e:
            validation_reasons.append({"reason": f"{errors['FECHA_NO_ENCONTRADA']['codigo']}:{image_type_required}"})
        except RuntimeError as e:
            validation_reasons.append({"reason": f"{errors['ERROR_EXIF']['codigo']}:{image_type_required}"})
        # Guardar imagen solo si no fue guardada ya
        if image_type_required not in saved_images:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], vehicle_id), exist_ok=True)
            ext = os.path.splitext(image_file.filename)[1]
            if not ext or ext == '.':
                ext = '.jpg'
            unique_id = str(uuid.uuid4())
            safe_name = simple_secure_filename(f"{image_type_required}-{unique_id}{ext}")
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], vehicle_id, safe_name)
            image_file.save(image_path)
            saved_images.add(image_type_required)
            image_paths[image_type_required] = image_path
            # Leer la imagen en bytes
            with open(image_path, "rb") as img_file:
                img_bytes = img_file.read()

            # Crear entrada en el diccionario si no existe
            image_groups[image_type_required] = {
                "img": img_bytes,
                "image_type": image_type_required,
                "parts": []
            }
        state["image_path"] = image_paths.get(image_type_required)
        # Agregar parte y daño a la entrada correspondiente
        image_groups[image_type_required]["parts"].append({
            "name": part.name,
            "damage": damages
        })

    # Convertir a lista final
    grouped_structure = list(image_groups.values())

    # acá se envia a al servicio de la ia

    print(f"Estructura a enviar a la ia { grouped_structure}")

    return VehicleStateRepository.save(vehicle_id, states, validation_reasons)