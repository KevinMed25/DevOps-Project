from flask import Blueprint, request, jsonify
from http import HTTPStatus
import logging
from models.assignment import AssignmentSchema
from services.assignment_service import AssignmentService

logger = logging.getLogger(__name__)
assignment_blueprint = Blueprint('assignments', __name__)
service = AssignmentService()

# Asignar vehículo a conductor
@assignment_blueprint.route('/', methods=['POST'])
def create_assignment():
    try:
        data = request.get_json()
        logger.info(f"Create assignment attempt for vehicle_id: {data.get('vehicle_id')}, driver_id: {data.get('driver_id')}")
        if not all(field in data for field in ['vehicle_id', 'driver_id']):
            logger.warning("Create assignment failed: Missing required fields")
            return jsonify({'error': 'Faltan campos requeridos'}), HTTPStatus.BAD_REQUEST

        assignment = AssignmentSchema(**data)
        assignment_id = service.createAssignment(assignment)
        logger.info(f"Assignment created successfully with ID: {assignment_id}")
        return jsonify({"id": assignment_id, "message": "Asignación creada exitosamente"}), HTTPStatus.CREATED
    
    except ValueError as e:
        logger.warning(f"Create assignment failed due to ValueError: {e}")
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        logger.exception(f"Error during assignment creation: {e}")
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR

#Consultar asignaciones de vehículo (todos los registros)
@assignment_blueprint.route('/', methods=['GET'])
def get_assignments():
    try:
        logger.info("Request to get all assignments")
        assignments = service.getAllAssignments()
        logger.info(f"Successfully retrieved {len(assignments)} assignments") 
        return jsonify(assignments), HTTPStatus.OK
    except Exception as e:
        logger.exception(f"Error retrieving all assignments: {e}")
        return jsonify({'error': 'Error al obtener las asignaciones'}), HTTPStatus.INTERNAL_SERVER_ERROR

# Cambiar asignaciones a vehículo
@assignment_blueprint.route('/<int:id>', methods=['PUT'])
def update_assignment(id):
    data = request.get_json() 
    logger.info(f"Update assignment attempt for ID: {id}, data: {data}")
    try:
        if not data:
            logger.warning(f"Update assignment failed for ID {id}: No data provided")
            return jsonify({'error': 'Datos no proporcionados'}), HTTPStatus.BAD_REQUEST

        assignment = AssignmentSchema(id=id, **data)
        updated_id = service.updateAssignment(assignment)
        logger.info(f"Assignment ID {updated_id} updated successfully")
        return jsonify({"id": updated_id, "message": "Asignación actualizada exitosamente"}), HTTPStatus.OK
    
    except ValueError as e:
        logger.warning(f"Update assignment for ID {id} failed due to ValueError: {e}")
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        logger.exception(f"Error during assignment update for ID {id}: {e}")
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR

#Eliminar assignment
@assignment_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_assignment(id):
    logger.info(f"Delete assignment attempt for ID: {id}")
    try:
        response = service.deleteAssignment(id) 
        logger.info(f"Assignment ID {id} processed for deletion by service.")
        return response
    except Exception as e:
        logger.exception(f"Error during assignment deletion for ID {id}: {e}")
        return jsonify({'error': 'Error al eliminar la asignación'}), HTTPStatus.INTERNAL_SERVER_ERROR