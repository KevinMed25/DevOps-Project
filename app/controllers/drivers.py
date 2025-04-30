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

