from flask import Blueprint, jsonify, request
from services.routes_service import RouteService
from http import HTTPStatus
from models.routes import RouteSchema

rutas_blueprint = Blueprint('rutas', __name__)

@rutas_blueprint.route('/', methods=['POST'])
def create_route():
    route_data = request.get_json()
    ruta_service = RouteService()
    
    try:
        new_route = ruta_service.create_route(RouteSchema(**route_data))
        return jsonify({"id": new_route}), HTTPStatus.CREATED
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    
@rutas_blueprint.route('/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    route_data = request.get_json()
    ruta_service = RouteService()
    
    try:
        updated_route = ruta_service.update_route(route_id, RouteSchema(**route_data))
        return jsonify({"id": updated_route}), HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST