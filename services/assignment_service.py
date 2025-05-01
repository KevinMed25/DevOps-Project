from utils.db import get_db
from flask import jsonify
from models.assignment import Assignment, AssignmentSchema

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
        if assignment_to_update:
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