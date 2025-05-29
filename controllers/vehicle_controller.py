from flask import Blueprint, request, jsonify
from models.vehicle import VehicleSchema
from services import VehicleService
from http import HTTPStatus
import logging
from utils.auth_middleware import admin_required
from datetime import datetime

logger = logging.getLogger(__name__)
vehicle_blueprint = Blueprint('vehicles',__name__)

@vehicle_blueprint.route('/', methods=['POST'])
@admin_required()
def create_vehicle():
    logger.info(f"Create vehicle attempt. Request data: {request.data[:256]}...")
    try: 
        if not request.is_json:
            logger.warning("Create vehicle failed: Request body not JSON.")
            return jsonify({'message': 'Se esperaba un cuerpo de solicitud JSON'}), HTTPStatus.BAD_REQUEST

        data = request.get_json()

        if not data:
            logger.warning("Create vehicle failed: Request body empty.")
            return jsonify({'message': 'Cuerpo de la solicitud vacío'}), HTTPStatus.BAD_REQUEST

        required_fields = ['brand', 'model', 'vin', 'license_plate', 'purchase_date', 'cost', 'entry_date']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            logger.warning(f"Create vehicle failed: Missing required fields: {missing_fields}")
            return jsonify(
                {
                    "message": "faltan campos requeridos",
                    "missing_fields": missing_fields
                }), HTTPStatus.BAD_REQUEST
        
        vehicle_service = VehicleService()
        vehicle = vehicle_service.createVehicle(VehicleSchema(**data))
        logger.info(f"Vehicle created successfully: {vehicle}")
        return jsonify({"message":"vehículo creado exitosamente", "data": vehicle}), HTTPStatus.CREATED
    
    except Exception as e: 
        logger.exception(f"Internal error creating vehicle: {e}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@vehicle_blueprint.route('/', methods=['GET'])
@admin_required()
def get_vehicles():
    logger.info("Request to get all vehicles.")
    try:
        vehicle_service = VehicleService()
        vehicles_response = vehicle_service.getAllVehicles() 
        
        data_list = []
        if isinstance(vehicles_response, tuple) and len(vehicles_response) > 0: 
             actual_data = vehicles_response[0]
             if isinstance(actual_data, dict) and 'data' in actual_data and isinstance(actual_data['data'], list):
                 data_list = actual_data['data']
        elif isinstance(vehicles_response, dict) and 'data' in vehicles_response and isinstance(vehicles_response['data'], list):
             data_list = vehicles_response['data']

        logger.info(f"Successfully retrieved all vehicles. Count: {len(data_list)}")
        return jsonify({"message":"vehículos obtenidos exitosamente", "data": vehicles_response}), HTTPStatus.OK 
    except Exception as e: 
        logger.exception(f"Internal error retrieving all vehicles: {e}")
        return jsonify({"message":"error al obtener los vehículos","error":str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@vehicle_blueprint.route('/<int:id>', methods=['GET'])
@admin_required()
def get_vehicle(id): 
    logger.info(f"Request to get vehicle by ID: {id}")
    try:
        vehicle_service = VehicleService()
        vehicle = vehicle_service.getVehicle(id)
        if not vehicle:
            logger.warning(f"Vehicle with ID {id} not found.")
            return jsonify({"message":"vehículo no encontrado"}), HTTPStatus.NOT_FOUND
        logger.info(f"Successfully retrieved vehicle ID {id}.")
        return jsonify({"message":"vehículo obtenido exitosamente", "data": vehicle}), HTTPStatus.OK
    except Exception as e: 
        logger.exception(f"Internal error retrieving vehicle ID {id}: {e}")
        return jsonify({"message":"error al obtener el vehículo","error":str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@vehicle_blueprint.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_vehicle(id):
    logger.info(f"Update vehicle attempt for ID: {id}. Request data: {request.data[:256]}...")
    try:
        data = request.get_json()
        if not data: 
            logger.warning(f"Update vehicle ID {id} failed: Request body empty.")
            return jsonify({"message": "Cuerpo de la solicitud vacío"}), HTTPStatus.BAD_REQUEST
        
        vehicle_service = VehicleService()

        exist_vehicle = vehicle_service.getVehicle(id) 
        if not exist_vehicle:
            logger.warning(f"Update vehicle ID {id} failed: Vehicle not found by service.")
            return jsonify({"message":"vehiculo no encontrado"}), HTTPStatus.NOT_FOUND
        
        if 'purchase_date' in data and isinstance(data['purchase_date'], str):
             data['purchase_date'] = datetime.strptime(data['purchase_date'], "%a, %d %b %Y %H:%M:%S %Z")
        if 'entry_date' in data and isinstance(data['entry_date'], str):
            data['entry_date'] = datetime.strptime(data['entry_date'], "%a, %d %b %Y %H:%M:%S %Z")

        updated_vehicle_data = vehicle_service.updateVehicle(VehicleSchema(id=id, **data))
        logger.info(f"Vehicle ID {id} updated successfully.")
        return jsonify({"message":"vehiculo actualizado exitosamente","data":updated_vehicle_data}), HTTPStatus.OK
    except Exception as e: 
        logger.exception(f"Internal error updating vehicle ID {id}: {e}")
        return jsonify({"message": "error al actualizar el vehículo", "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@vehicle_blueprint.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_vehicle(id):
    logger.info(f"Delete vehicle attempt for ID: {id}")
    try: 
        vehicle_service = VehicleService()
        result = vehicle_service.deleteVehicle(id) 
        log_result_text = result.get_data(as_text=True) if hasattr(result, 'get_data') else str(result)
        logger.info(f"Vehicle ID {id} deletion processed by service. Result: {log_result_text[:256]}...")
        return result
    except Exception as e: 
        logger.exception(f"Internal error deleting vehicle ID {id}: {e}")
        return jsonify({"message": "error al eliminar el vehículo"}), HTTPStatus.INTERNAL_SERVER_ERROR