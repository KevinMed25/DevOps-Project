from flask import Blueprint, request, jsonify
from http import HTTPStatus
from models.assignment import AssignmentSchema
from services.assignment_service import AssignmentService

assignment_blueprint = Blueprint('assignments', __name__)
service = AssignmentService()

# Asignar vehículo a conductor
@assignment_blueprint.route('/', methods=['POST'])
def create_assignment():
    try:
        data = request.get_json()
        if not all(field in data for field in ['vehicle_id', 'driver_id']):
            return jsonify({'error': 'Faltan campos requeridos'}), HTTPStatus.BAD_REQUEST

        assignment = AssignmentSchema(**data)
        assignment_id = service.createAssignment(assignment)
        return jsonify({"id": assignment_id, "message": "Asignación creada exitosamente"}), HTTPStatus.CREATED
    
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR

#Consultar asignaciones de vehículo (todos los registros)
@assignment_blueprint.route('/', methods=['GET'])
def get_assignments():
    try:
        return jsonify(service.getAllAssignments()), HTTPStatus.OK
    except Exception as e:
        return jsonify({'error': 'Error al obtener las asignaciones'}), HTTPStatus.INTERNAL_SERVER_ERROR

# Cambiar asignaciones a vehículo
@assignment_blueprint.route('/<int:id>', methods=['PUT'])
def update_assignment(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos no proporcionados'}), HTTPStatus.BAD_REQUEST

        assignment = AssignmentSchema(id=id, **data)
        updated_id = service.updateAssignment(assignment)
        return jsonify({"id": updated_id, "message": "Asignación actualizada exitosamente"}), HTTPStatus.OK
    
    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR

#Eliminar assignment
@assignment_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_assignment(id):
    try:
        return service.deleteAssignment(id)
    except Exception as e:
        return jsonify({'error': 'Error al eliminar la asignación'}), HTTPStatus.INTERNAL_SERVER_ERROR