from flask import Blueprint, request, jsonify
from models.vehiculo import VehicleSchema
from services import VehicleService
from http import HTTPStatus


vehicle_blueprint = Blueprint('vehicles',__name__)

@vehicle_blueprint.route('/', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    # Data validation
    required_fields = ['brand', 'model', 'vin', 'license_plate', 'purchase_date', 'cost', 'entry_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    vehicle_service = VehicleService()
    resp = vehicle_service.createVehicle(VehicleSchema(**data))
    return jsonify(resp), HTTPStatus.CREATED