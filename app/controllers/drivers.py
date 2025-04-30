from flask import Blueprint, jsonify, request
from app.services import DriversService
from http import HTTPStatus
from app.models.drivers import DriverSchema


drivers_blueprint = Blueprint('drivers', __name__)

@drivers_blueprint.route('/', methods=['GET'])
def get_drivers():
    driversService = DriversService()
    resp = driversService.getAllDrivers()
    return jsonify(resp), HTTPStatus.OK

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

