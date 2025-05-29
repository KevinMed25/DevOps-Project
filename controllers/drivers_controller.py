from flask import Blueprint, jsonify, request
from services import DriversService
from http import HTTPStatus
import logging
from models.drivers import DriverSchema
from utils.auth_middleware import admin_required

logger = logging.getLogger(__name__)
drivers_blueprint = Blueprint('drivers', __name__)

@drivers_blueprint.route('/', methods=['GET'])
@admin_required()
def get_drivers():
    logger.info("Request to get all drivers.")
    try:
        driversService = DriversService()
        drivers = driversService.getAllDrivers()
        logger.info(f"Successfully retrieved {len(drivers) if isinstance(drivers, list) else 'drivers data'}.")
        return drivers, HTTPStatus.OK
    except Exception as e:
        logger.exception(f"Error retrieving all drivers: {e}")
        return jsonify({'error': 'Error interno del servidor al obtener conductores'}), HTTPStatus.INTERNAL_SERVER_ERROR

@drivers_blueprint.route('/', methods=['POST'])
@admin_required()
def create_driver():
    driver = request.get_json()
    logger.info(f"Create driver attempt with data: {driver}")
    try:
        driversService = DriversService()
        created_driver_info = driversService.createDriver(DriverSchema(**driver)) 
        logger.info(f"Driver created successfully: {driver.get('name', 'N/A')}") 
        return jsonify({
            "message": "Driver created successfully",
            "driver": driver 
        }), HTTPStatus.OK
    except Exception as e:
        logger.exception(f"Error creating driver with data {driver}: {e}")
        return jsonify({'error': 'Error interno del servidor al crear conductor'}), HTTPStatus.INTERNAL_SERVER_ERROR

@drivers_blueprint.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_driver(id):
    driver = request.get_json()
    logger.info(f"Update driver attempt for ID: {id} with data: {driver}")
    try:
        driversService = DriversService()
        if not driver: 
            logger.warning(f"Update driver failed for ID {id}: Driver data not provided in request.")
            return jsonify({"error": "Driver data not provided"}), HTTPStatus.BAD_REQUEST 
        
        respDriver = driversService.updateDriver(DriverSchema(id=id, **driver))
        if respDriver is None: 
            logger.warning(f"Update driver failed for ID {id}: Driver not found by service.")
            return jsonify({"error": "Driver not found"}), HTTPStatus.NOT_FOUND

        logger.info(f"Driver ID {id} updated successfully.")
        return jsonify(respDriver), HTTPStatus.OK
    except Exception as e:
        logger.exception(f"Error updating driver ID {id} with data {driver}: {e}")
        return jsonify({'error': 'Error interno del servidor al actualizar conductor'}), HTTPStatus.INTERNAL_SERVER_ERROR

@drivers_blueprint.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_driver(id):
    logger.info(f"Delete driver attempt for ID: {id}")
    try:
        driversService = DriversService()
        result = driversService.deleteDriver(id)
        logger.info(f"Driver ID {id} deletion processed by service.")
        return result
    except ValueError as e:
        logger.warning(f"Failed to delete driver ID {id}: {e}")
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        logger.exception(f"Error deleting driver ID {id}: {e}")
        return jsonify({'error': 'Error interno del servidor al eliminar conductor'}), HTTPStatus.INTERNAL_SERVER_ERROR