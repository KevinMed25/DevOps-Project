from flask import Blueprint, jsonify, request
from services import DriversService
from http import HTTPStatus
from models.drivers import DriverSchema


drivers_blueprint = Blueprint('drivers', __name__)

@drivers_blueprint.route('/', methods=['GET'])
def get_drivers():
    driversService = DriversService()
    drivers = driversService.getAllDrivers()
    return drivers, HTTPStatus.OK

@drivers_blueprint.route('/', methods=['POST'])
def create_driver():
    driver = request.get_json()
    driversService = DriversService()
    resp = driversService.createDriver(DriverSchema(**driver))
    return jsonify(resp), HTTPStatus.OK

@drivers_blueprint.route('/<int:id>', methods=['PUT'])
def update_driver(id):

    driver = request.get_json()
    driversService = DriversService()
    if not driver:
        return jsonify({"error": "Driver not found"}), HTTPStatus.NOT_FOUND
    resp = driversService.updateDriver(DriverSchema(id=id, **driver))
    return jsonify(resp), HTTPStatus.OK

@drivers_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_driver(id):
    driversService = DriversService()
    try:
        result = driversService.deleteDriver(id)
        return result
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND