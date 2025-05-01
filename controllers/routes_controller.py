from flask import Blueprint, jsonify, request
from services.routes_service import RouteService
from http import HTTPStatus
from models.routes import RouteSchema

rutas_blueprint = Blueprint('rutas', __name__)

@rutas_blueprint.route('/<int:route_id>', methods=['GET'])
def get_route(route_id):
    ruta_service = RouteService()
    
    try:
        route = ruta_service.get_route_by_id(route_id)
        return jsonify({
            "id": route.id,
            "name": route.name,
            "date": route.date.isoformat() if route.date else None,
            "origin_lat": route.origin_lat,
            "origin_lng": route.origin_lng,
            "destination_lat": route.destination_lat,
            "destination_lng": route.destination_lng,
            "status": route.status,
            "problem_description": route.problem_description,
            "comments": route.comments,
            "vehicle_id": route.vehicle_id,
            "driver_id": route.driver_id
        }), HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

@rutas_blueprint.route('/', methods=['GET'])
def get_all_routes():

    ruta_service = RouteService()
    routes = ruta_service.get_all_routes()
    
    return jsonify([{
        "id": route.id,
        "name": route.name,
        "date": route.date.isoformat() if route.date else None,
        "origin_lat": route.origin_lat,
        "origin_lng": route.origin_lng,
        "destination_lat": route.destination_lat,
        "destination_lng": route.destination_lng,
        "status": route.status,
        "vehicle_id": route.vehicle_id,
        "driver_id": route.driver_id
    } for route in routes]), HTTPStatus.OK

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

@rutas_blueprint.route('/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    ruta_service = RouteService()
    
    try:
        ruta_service.delete_route(route_id)
        return jsonify({"message": "Ruta eliminada"}), HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND