from flask import Blueprint, jsonify, request
from services.routes_service import RouteService
from http import HTTPStatus
from models.routes import RouteSchema
from utils.auth_middleware import admin_required

rutas_blueprint = Blueprint('routes', __name__)

@rutas_blueprint.route('/', methods=['POST'])
@admin_required()
def create_route():
    if not request.is_json:
        return jsonify({'message': 'Se esperaba un cuerpo de solicitud JSON'}), HTTPStatus.BAD_REQUEST

    data = request.get_json()

    if not data:
        return jsonify({'message': 'El cuerpo de la solicitud está vacío'}), HTTPStatus.BAD_REQUEST

    required_fields = [
        'vehicle_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng',
        'route_name', 'route_date', 'success', 'description', 'driver_id'
    ]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            "message": "Faltan campos requeridos",
            "missing_fields": missing_fields
        }), HTTPStatus.BAD_REQUEST

    try:
        route_service = RouteService()

        if not route_service.is_vehicle_assigned_to_driver(data['vehicle_id'], data['driver_id']):
            return jsonify({
                "message": "El vehículo no está asignado a un conductor o la asignación no es válida"
            }), HTTPStatus.CONFLICT

        data_transformed = {
            "name": data['route_name'],
            "date": data['route_date'],
            "origin_lat": data['start_lat'],
            "origin_lng": data['start_lng'],
            "destination_lat": data['end_lat'],
            "destination_lng": data['end_lng'],
            "vehicle_id": data['vehicle_id'],
            "driver_id": data['driver_id'],
            "status": "completed" if data.get("success") else "failed",
            "problem_description": data.get('description', ''),
            "comments": data.get('comments', '')
        }

        new_route_id = route_service.create_route(RouteSchema(**data_transformed))
        return jsonify({
            "message": "Ruta creada exitosamente",
            "id": new_route_id
        }), HTTPStatus.CREATED

    except ValueError as e:
        return jsonify({
            "message": "Error de validación",
            "error": str(e)
        }), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({
            "message": "Error interno al crear la ruta",
            "error": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR