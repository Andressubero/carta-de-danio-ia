from flask import request, jsonify
from repositories.vehicle_state_repository import VehicleStateRepository
from repositories.ai_report_repository import AIReportRepository
from services.vehicle_service import get_vehicle_with_parts
from extensions import db
from utils.date import get_image_capture_date
from models.models import ImageTypeEnum, Part, VehiclePart
from datetime import datetime, timedelta
from constants.errors import errors
from flask import current_app as app
from utils.ai import call_llm
from repositories.role_repository import RoleRepository
import json
import uuid
import os
import re
from PIL import Image
from uuid import UUID

def clean_and_parse_llm_response(llm_response):
    cleaned = llm_response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json"):]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    return json.loads(cleaned)
    
def get_vehicle_part_by_part_id(vehicle, part_id):
    """
    Dado un Vehicle y un id de Part, devuelve el VehiclePart correspondiente
    o None si no existe.
    """
    return next(
        (vp for vp in vehicle.parts if str(vp.part_id) == str(part_id)),
        None
    )

def simple_secure_filename(filename):
    """
    Remueve caracteres no válidos y reemplaza espacios por guiones bajos.
    """
    filename = re.sub(r'[^A-Za-z0-9_.-]', '_', filename)
    return filename

def validate_parts(vehicle_parts, parts_from_body):
    backend_part_ids = {str(part.part_id) for part in vehicle_parts}
    frontend_part_ids = {str(p["part_id"]) for p in parts_from_body}

    if len(frontend_part_ids) != len(backend_part_ids):
        return False, "Cantidad de partes no coincide"
    if frontend_part_ids != backend_part_ids:
        return False, "Los IDs de partes no coinciden"
    return True, "Las partes coinciden"

def get_all(user_id, role_id):
    """
    Obtiene todos los estados de vehículos.
    """
    try:
        role = RoleRepository.get_by_id(role_id) 
        if role.name == 'admin':
            return VehicleStateRepository.get_all()
        return VehicleStateRepository.get_all_by_user(user_id) 
    except Exception as e:
        raise RuntimeError(f"Error al obtener los estados de vehículos: {str(e)}")

def get_image_mime_type(path):
    img = Image.open(path)
    format = img.format
    if format == 'JPEG':
        return 'image/jpeg'
    elif format == 'PNG':
        return 'image/png'
    elif format == 'WEBP':
        return 'image/webp'
    else:
        raise ValueError(f"Formato de imagen no soportado: {format}")


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
    
    if not isinstance(states, list):
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
    
    vehicle = get_vehicle_with_parts(vehicle_id)
    if vehicle is None:
        raise ValueError(f"{errors['ERROR-16']['mensaje']}")
    
    previous_state = VehicleStateRepository.get_latest_by_vehicle_id(vehicle_id)
    # if not previous_state:
    #     # states debe coincidir con el length porque es el primer estado
    #     #is_valid, msg = validate_parts(vehicle.parts, states)
    #     #if not is_valid:
    #     #    raise ValueError(f"{errors['DATOS_INSUFICIENTES']['codigo']}: {msg}")
    #     if not all([image_lateral_right, image_lateral_left, image_front, image_back, image_top]):
    #         raise ValueError(f"{errors['DATOS_INSUFICIENTES']['codigo']}: El primer state requiere todas las imágenes") 

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
        
        vehicle_part = db.session.query(VehiclePart).filter_by(id=part_id).first()
        if not vehicle_part:
            raise ValueError(f"{errors['PARTE_NO_ENCONTRADA']['codigo']}")
        part = db.session.query(Part).filter_by(id=vehicle_part.part_id).first()
        if not part:
            raise ValueError(f"{errors['PARTE_NO_ENCONTRADA']['codigo']}")
        
        image_type_required = part.image_type
        image_file = available_images.get(image_type_required)

        

        if not image_file:
            raise ValueError(
                f"{errors['FALTA_IMAGEN']['codigo']}:{part.name}"
            )

        capture_date = None
        
        if image_type_required not in saved_images:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], vehicle_id), exist_ok=True)
            ext = os.path.splitext(image_file.filename)[1]
            if not ext or ext == '.':
                ext = '.jpg'
            unique_id = str(uuid.uuid4())
            safe_name = simple_secure_filename(f"{image_type_required}-{unique_id}{ext}")
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], vehicle_id, safe_name)
            if hasattr(image_file, 'save') and callable(image_file.save):
                image_file.save(image_path)
            elif isinstance(image_file, bytes):
                with open(image_path, 'wb') as f:
                    f.write(image_file)
            else:
                raise RuntimeError(...)

            saved_images.add(image_type_required)

            reference_image_file = None
        
            if previous_state and f'reference_{image_type_required}' not in image_paths:
                finded_vehicle_part = get_vehicle_part_by_part_id(vehicle, part.id)
                if not finded_vehicle_part:
                    raise ValueError(f"{errors['PARTE_NO_ENCONTRADA']['codigo']}:{part.name}")
                last_vehicle_part_state = VehicleStateRepository.get_latest_vehicle_part_state_by_vehicle_part_id(finded_vehicle_part.id)
                if not last_vehicle_part_state:
                    raise ValueError(f"{errors['FALTA_REFERENCIA']['codigo']}:{part.name}")

                reference_image_file = last_vehicle_part_state.image
                image_paths[f'reference_{image_type_required}'] = reference_image_file

            image_paths[image_type_required] = image_path
            mime_type = get_image_mime_type(image_path)
            # Crear entrada en el diccionario si no existe
            image_groups[image_type_required] = {
                "image": image_path,
                "mime_type": mime_type,
                "image_type": image_type_required.value,
                "parts": []
            }
            if previous_state and f'reference_{image_type_required}' in image_paths:
                mime_type = get_image_mime_type(image_paths[f'reference_{image_type_required}'])
                image_groups[image_type_required]["reference_image"] = image_paths[f'reference_{image_type_required}']
                image_groups[image_type_required]["reference_mime_type"] = mime_type
        print(f'Path de la imagen requerida {image_paths.get(image_type_required)}')
        state["image_path"] = image_paths.get(image_type_required)
        # Agregar parte y daño a la entrada correspondiente
        image_groups[image_type_required]["parts"].append({
            "name": part.name,
            "damage": damages
        })
        try:
            capture_date = get_image_capture_date(image_file)
            image_file.seek(0)
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
        

    # Convertir a lista final
    grouped_structure = list(image_groups.values())

    analysis_object = {
        "states": grouped_structure,
        "brand": vehicle.brand,
        "model": vehicle.model
    }

    # acá se envia a al servicio de la ia

    # Llamar a la IA con el prompt correspondiente
    result = call_llm(analysis_object, 'COMP' if previous_state else 'ALTA')
    parsed = clean_and_parse_llm_response(result)
    print(f'Estados-------------------------${states}')
    state_to_use = VehicleStateRepository.save(vehicle_id, states, validation_reasons, date)

    # Guardar AIReport siempre
    ai_report = AIReportRepository.save(parsed, state_to_use.id)

    # Retornar ambos
    return { "state": state_to_use, "ai_report": ai_report }


def change_validation_state_service(validation_state, state_id, role_id):
    try:
        role = RoleRepository.get_by_id(role_id)  

        if not role:
            raise RuntimeError("El rol no existe")

        if role.name.lower() == "admin":
            return VehicleStateRepository.change_validation_state(state_id, validation_state)
        else:
            raise RuntimeError("Forbidden")
    except AttributeError as e:
        raise RuntimeError(f"Error en la obtención de datos: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error inesperado: {str(e)}")

