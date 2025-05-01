from flask import Blueprint, request, jsonify
from http import HTTPStatus
from models.assignment import AssignmentSchema
from services.assignment_service import AssignmentService

assignment_blueprint = Blueprint('assignments', __name__)
service = AssignmentService()

# Asignar vehículo a conductor
@assignment_blueprint.route('/', methods=['POST'])
def create_assignment():
    data = request.get_json()
    if not all(field in data for field in ['vehicle_id', 'driver_id']):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    assignment = AssignmentSchema(**data)
    assignment_id = service.createAssignment(assignment)
    return jsonify({"id": assignment_id}), HTTPStatus.CREATED

#Consultar asignaciones de vehículo (todos los registros)
@assignment_blueprint.route('/', methods=['GET'])
def get_assignments():
    return jsonify(service.getAllAssignments()), HTTPStatus.OK