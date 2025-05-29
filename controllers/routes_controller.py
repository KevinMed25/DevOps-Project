from flask import Blueprint, jsonify, request
from services.routes_service import RouteService
from http import HTTPStatus
import logging
from models.routes import RouteSchema
from utils.auth_middleware import admin_required
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)
rutas_blueprint = Blueprint('routes', __name__)

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> tuple:
    """Valida los campos requeridos y devuelve los campos faltantes si hay alguno."""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, missing_fields
    return True, None

def transform_route_data(data: Dict[str, Any], existing_route: Optional[Dict] = None) -> Dict[str, Any]:
    """Transforma los nombres de campos del JSON a los nombres del modelo."""
    transformed = {
        "name": data.get('route_name', existing_route.get('name') if existing_route else None),
        "date": data.get('route_date', existing_route.get('date') if existing_route else None),
        "origin_lat": data.get('start_lat', existing_route.get('origin_lat') if existing_route else None),
        "origin_lng": data.get('start_lng', existing_route.get('origin_lng') if existing_route else None),
        "destination_lat": data.get('end_lat', existing_route.get('destination_lat') if existing_route else None),
        "destination_lng": data.get('end_lng', existing_route.get('destination_lng') if existing_route else None),
        "assignment_id": data.get('assignment_id', existing_route.get('assignment_id') if existing_route else None),
        "status": data.get('status', existing_route.get('status') if existing_route else None),
        "problem_description": data.get('description', existing_route.get('problem_description') if existing_route else ''),
        "comments": data.get('comments', existing_route.get('comments') if existing_route else '')
    }
    
    # Manejo especial para el campo success que afecta al status
    if 'success' in data:
        transformed['status'] = "completed" if data['success'] else "failed"
    
    return transformed

@rutas_blueprint.route('/', methods=['POST'])
@admin_required()
def create_route():
    logger.info(f"Create route attempt. Request data: {request.data[:256]}...")
    if not request.is_json:
        logger.warning("Create route failed: Request body not JSON.")
        return jsonify({'message': 'Se esperaba un cuerpo de solicitud JSON'}), HTTPStatus.BAD_REQUEST

    data = request.get_json()

    if not data:
        logger.warning("Create route failed: Request body empty.")
        return jsonify({'message': 'El cuerpo de la solicitud está vacío'}), HTTPStatus.BAD_REQUEST

    required_fields = [
        'assignment_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng',
        'route_name', 'route_date'
    ]
    
    is_valid, missing_fields = validate_required_fields(data, required_fields)
    if not is_valid:
        logger.warning(f"Create route failed: Missing required fields: {missing_fields}")
        return jsonify({
            "message": "Faltan campos requeridos",
            "missing_fields": missing_fields
        }), HTTPStatus.BAD_REQUEST

    try:
        route_service = RouteService()
        data_transformed = transform_route_data(data)
        new_route_id, message = route_service.create_route(RouteSchema(**data_transformed))
        logger.info(f"Route created successfully with ID: {new_route_id}, Message: {message}")
        return jsonify({
            "message": message,
            "id": new_route_id
        }), HTTPStatus.CREATED

    except ValueError as e:
        logger.warning(f"Create route validation error: {e}")
        return jsonify({
            "message": str(e),
            "error": "Error de validación"
        }), HTTPStatus.BAD_REQUEST
    except Exception as e:
        logger.exception(f"Internal error creating route: {e}")
        return jsonify({
            "message": "Error interno al crear la ruta",
            "error": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@rutas_blueprint.route('/', methods=['GET'])
@admin_required()
def get_all_routes():
    logger.info("Request to get all routes.")
    try:
        route_service = RouteService()
        routes, message = route_service.get_all_routes()
        logger.info(f"Successfully retrieved all routes. Count: {len(routes) if routes else 0}. Message: {message}")
        return jsonify({
            "message": message,
            "data": routes
        }), HTTPStatus.OK

    except Exception as e:
        logger.exception(f"Internal error retrieving all routes: {e}")
        return jsonify({
            "message": "Error interno al obtener las rutas",
            "error": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@rutas_blueprint.route('/<int:route_id>', methods=['GET'])
@admin_required()
def get_route_by_id(route_id):
    logger.info(f"Request to get route by ID: {route_id}")
    try:
        route_service = RouteService()
        route_data, message = route_service.get_route_by_id(route_id)
        
        if not route_data:
            logger.info(f"Route with ID {route_id} not found. Message: {message}")
            return jsonify({
                "data": None,
                "message": message
            }), HTTPStatus.NOT_FOUND
            
        logger.info(f"Successfully retrieved route ID {route_id}. Message: {message}")
        return jsonify({
            "data": route_data,
            "message": message
        }), HTTPStatus.OK
        
    except Exception as e:
        logger.exception(f"Internal error retrieving route ID {route_id}: {e}")
        return jsonify({
            "data": None,
            "message": "Error interno al procesar la solicitud",
            "error": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@rutas_blueprint.route('/<int:route_id>', methods=['PUT'])
@admin_required()
def update_route(route_id):
    logger.info(f"Update route attempt for ID: {route_id}. Request data: {request.data[:256]}...")
    if not request.is_json:
        logger.warning(f"Update route ID {route_id} failed: Request body not JSON.")
        return jsonify({'message': 'Se esperaba un cuerpo de solicitud JSON'}), HTTPStatus.BAD_REQUEST

    data = request.get_json()

    if not data:
        logger.warning(f"Update route ID {route_id} failed: Request body empty.")
        return jsonify({'message': 'El cuerpo de la solicitud está vacío'}), HTTPStatus.BAD_REQUEST

    try:
        route_service = RouteService()
        
        existing_route, _ = route_service.get_route_by_id(route_id) 
        if not existing_route:
            logger.warning(f"Update route ID {route_id} failed: Route not found by service.") 
            return jsonify({"message": f"No se encontró la ruta con ID {route_id}"}), HTTPStatus.NOT_FOUND

        data_transformed = transform_route_data(data, existing_route)
        updated_route, message = route_service.update_route(route_id, RouteSchema(**data_transformed))
        logger.info(f"Route ID {route_id} updated successfully. Message: {message}")
        return jsonify({
            "message": message,
            "data": updated_route
        }), HTTPStatus.OK
        
    except ValueError as e:
        logger.warning(f"Update route ID {route_id} validation error: {e}")
        error_message = str(e)
        status_code = HTTPStatus.BAD_REQUEST
        
        if "no existe" in error_message.lower(): 
            status_code = HTTPStatus.NOT_FOUND
        elif "no está asignado" in error_message.lower():
            status_code = HTTPStatus.CONFLICT
            
        return jsonify({
            "message": error_message,
            "error": "Error de validación"
        }), status_code
    except Exception as e:
        logger.exception(f"Internal error updating route ID {route_id}: {e}")
        return jsonify({
            "message": "Error interno al actualizar la ruta",
            "error": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@rutas_blueprint.route('/<int:route_id>', methods=['DELETE'])
@admin_required()
def delete_route(route_id):
    logger.info(f"Delete route attempt for ID: {route_id}")
    try:
        route_service = RouteService()

        route_data, _ = route_service.get_route_by_id(route_id) 
        if not route_data:
            logger.warning(f"Delete route ID {route_id} failed: Route not found by service.") 
            return jsonify({
                "message": f"No se encontró la ruta con ID {route_id}"
            }), HTTPStatus.NOT_FOUND

        success, message = route_service.delete_route(route_id)
        if not success:
            logger.error(f"Service failed to delete route ID {route_id}. Message: {message}")
            return jsonify({
                "message": message
            }), HTTPStatus.INTERNAL_SERVER_ERROR 

        logger.info(f"Route ID {route_id} deleted successfully. Message: {message}")
        return jsonify({
            "message": message
        }), HTTPStatus.OK

    except Exception as e:
        logger.exception(f"Internal error deleting route ID {route_id}: {e}")
        return jsonify({
            "message": "Error interno al eliminar la ruta",
            "error": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR