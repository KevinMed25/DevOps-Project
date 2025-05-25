from flask import Blueprint, request, jsonify
from models.vehicle import VehicleSchema
from services import VehicleService
from http import HTTPStatus
from utils.auth_middleware import admin_required
from datetime import datetime


vehicle_blueprint = Blueprint('vehicles',__name__)

@vehicle_blueprint.route('/', methods=['POST'])
@admin_required()
def create_vehicle():

    try: 

        if not request.is_json:
            return jsonify({'message': 'Se esperaba un cuerpo de solicitud JSON'}), HTTPStatus.BAD_REQUEST

        data = request.get_json()

        if not data:
            return jsonify({'message': 'Cuerpo de la solicitud vacío'}), HTTPStatus.BAD_REQUEST

        # Data validation
        required_fields = ['brand', 'model', 'vin', 'license_plate', 'purchase_date', 'cost', 'entry_date']
        
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify(
                {
                    "message": "faltan campos requeridos",
                    "missing_fields": missing_fields
                }), HTTPStatus.BAD_REQUEST
        
        vehicle_service = VehicleService()
        vehicle = vehicle_service.createVehicle(VehicleSchema(**data))
        
        return jsonify({"message":"vehículo creado exitosamente", "data": vehicle}), HTTPStatus.CREATED
    
    except Exception as e: 
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@vehicle_blueprint.route('/', methods=['GET'])
@admin_required()
def get_vehicles():
    try:
        vehicle_service = VehicleService()
        vehicles = vehicle_service.getAllVehicles()
        return jsonify({"message":"vehículos obtenidos exitosamente", "data": vehicles}), HTTPStatus.OK
    except Exception as e: 
        return jsonify({"message":"error al obtener los vehículos","error":str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@vehicle_blueprint.route('/<int:id>', methods=['GET'])
@admin_required()
def get_vehicle(id): 
    try:
        vehicle_service = VehicleService()
        vehicle = vehicle_service.getVehicle(id)
        if not vehicle:
            return jsonify({"message":"vehículo no encontrado"}), HTTPStatus.NOT_FOUND
        return jsonify({"message":"vehículo obtenido exitosamente", "data": vehicle}), HTTPStatus.OK
    except Exception as e: 
        return jsonify({"message":"error al obtener el vehículo","error":str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@vehicle_blueprint.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_vehicle(id):
    try:
        data = request.get_json()
        if not data: 
            return jsonify({"message": "Cuerpo de la solicitud vacío"}), HTTPStatus.BAD_REQUEST
        
        vehicle_service = VehicleService()
        exist_vehicle = vehicle_service.getVehicle(id)
        if not exist_vehicle:
            return jsonify({"message":"vehiculo no encontrado"}), HTTPStatus.NOT_FOUND
        
        data['purchase_date'] = datetime.strptime(data['purchase_date'], "%a, %d %b %Y %H:%M:%S %Z")
        data['entry_date'] = datetime.strptime(data['entry_date'], "%a, %d %b %Y %H:%M:%S %Z")

        update_vehicle = vehicle_service.updateVehicle(VehicleSchema(id=id, **data))
        return jsonify({"message":"vehiculo actualizado exitosamente","data":update_vehicle}), HTTPStatus.OK
    except Exception as e: 
        return jsonify({"message": "error al actualizar el vehículo", "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@vehicle_blueprint.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_vehicle(id):
    try: 

        vehicle_service = VehicleService()
        result = vehicle_service.deleteVehicle(id)
        return result
    except Exception as e: 
        return jsonify({"message": "error al eliminar el vehículo"}), HTTPStatus.INTERNAL_SERVER_ERROR