from flask import Blueprint, jsonify
from app.services import DriversService
from http import HTTPStatus

drivers_blueprint = Blueprint('drivers', __name__)

@drivers_blueprint.route('/', methods=['GET'])
def get_drivers():
    driversService = DriversService()
    drivers = driversService.getAllDrivers()
    return drivers, HTTPStatus.OK