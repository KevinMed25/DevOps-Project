from utils.db import get_db
from flask import jsonify
from models.assignment import Assignment, AssignmentSchema
from models.vehicle import Vehicle
from models.drivers import Driver

class AssignmentService:

    def getAllAssignments(self) -> list:
        db = next(get_db())
        assignments = db.query(Assignment).all()
        return list(map(lambda a: {
            "id": a.id,
            "vehicle_id": a.vehicle_id,
            "driver_id": a.driver_id
        }, assignments))

    def createAssignment(self, assignment: AssignmentSchema):
        db = next(get_db())
        
        # Verificar que el vehículo existe
        vehicle = db.query(Vehicle).filter(Vehicle.id == assignment.vehicle_id).first()
        if not vehicle:
            raise ValueError("El vehículo especificado no existe")
        
        # Verificar que el conductor existe
        driver = db.query(Driver).filter(Driver.id == assignment.driver_id).first()
        if not driver:
            raise ValueError("El conductor especificado no existe")
        
        # Verificar que el vehículo no esté ya asignado
        existing_vehicle_assignment = db.query(Assignment).filter(
            Assignment.vehicle_id == assignment.vehicle_id
        ).first()
        if existing_vehicle_assignment:
            raise ValueError("Este vehículo ya está asignado a otro conductor")
        
        # Verificar que el conductor no tenga ya un vehículo asignado
        existing_driver_assignment = db.query(Assignment).filter(
            Assignment.driver_id == assignment.driver_id
        ).first()
        if existing_driver_assignment:
            raise ValueError("Este conductor ya tiene un vehículo asignado")
        
        new_assignment = Assignment(
            vehicle_id=assignment.vehicle_id,
            driver_id=assignment.driver_id
        )
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)
        return new_assignment.id

    def updateAssignment(self, assignment: AssignmentSchema):
        db = next(get_db())
        assignment_to_update = db.query(Assignment).filter(Assignment.id == assignment.id).first()
        
        if not assignment_to_update:
            raise ValueError("Asignación no encontrada")
        
        # Verificar que el vehículo existe
        vehicle = db.query(Vehicle).filter(Vehicle.id == assignment.vehicle_id).first()
        if not vehicle:
            raise ValueError("El vehículo especificado no existe")
        
        # Verificar que el conductor existe
        driver = db.query(Driver).filter(Driver.id == assignment.driver_id).first()
        if not driver:
            raise ValueError("El conductor especificado no existe")
        
        # Verificar que el vehículo no esté ya asignado (excluyendo la asignación actual)
        existing_vehicle_assignment = db.query(Assignment).filter(
            Assignment.vehicle_id == assignment.vehicle_id,
            Assignment.id != assignment.id
        ).first()
        if existing_vehicle_assignment:
            raise ValueError("Este vehículo ya está asignado a otro conductor")
        
        # Verificar que el conductor no tenga ya un vehículo asignado (excluyendo la asignación actual)
        existing_driver_assignment = db.query(Assignment).filter(
            Assignment.driver_id == assignment.driver_id,
            Assignment.id != assignment.id
        ).first()
        if existing_driver_assignment:
            raise ValueError("Este conductor ya tiene un vehículo asignado")
        
        assignment_to_update.vehicle_id = assignment.vehicle_id
        assignment_to_update.driver_id = assignment.driver_id
        db.commit()
        db.refresh(assignment_to_update)
        return assignment_to_update.id

    def deleteAssignment(self, assignment_id: int):
        db = next(get_db())
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if assignment:
            db.delete(assignment)
            db.commit()
            return jsonify({"message": "Asignación eliminada correctamente", "id": assignment_id}), 200
        return jsonify({"error": "Asignación no encontrada"}), 404