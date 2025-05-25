from utils.db import get_db
from flask import jsonify
from models.vehicle import Vehicle
from models.vehicle import VehicleSchema

class VehicleService:

    def getAllVehicles(self) -> list:
        db = next(get_db())
        vehicles = db.query(Vehicle).all()
        return list(map(lambda vehicle: {
            "id": vehicle.id,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "vin": vehicle.vin,
            "license_plate": vehicle.license_plate,
            "purchase_date": vehicle.purchase_date,
            "cost": vehicle.cost,
            "entry_date": vehicle.entry_date
        }, vehicles))
    
    def getVehicle(self, vehicle_id: int) -> Vehicle:
        db = next(get_db())
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            return None
        return {
            "id": vehicle.id,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "vin": vehicle.vin,
            "license_plate": vehicle.license_plate,
            "purchase_date": vehicle.purchase_date,
            "cost": vehicle.cost,
            "entry_date": vehicle.entry_date
        } 

    def createVehicle(self, vehicle: VehicleSchema):
        db = next(get_db())
        
        new_vehicle = Vehicle(
            brand = vehicle.brand,
            model = vehicle.model,
            vin = vehicle.vin,
            license_plate = vehicle.license_plate,
            purchase_date = vehicle.purchase_date,
            cost = vehicle.cost,
            entry_date = vehicle.entry_date
        )
        
        db.add(new_vehicle)
        db.commit()
        db.refresh(new_vehicle)
        
        return {
            "id": new_vehicle.id,
            "brand": new_vehicle.brand,
            "model": new_vehicle.model,
            "vin": new_vehicle.vin,
            "license_plate": new_vehicle.license_plate,
            "purchase_date": new_vehicle.purchase_date,
            "cost": new_vehicle.cost,
            "entry_date": new_vehicle.entry_date
        }
    
    def updateVehicle(self, vehicle: VehicleSchema):
        db = next(get_db())
        vehicle_to_update = db.query(Vehicle).filter(Vehicle.id == vehicle.id).first()
        if vehicle_to_update:
            vehicle_to_update.brand = vehicle.brand
            vehicle_to_update.model = vehicle.model
            vehicle_to_update.vin = vehicle.vin
            vehicle_to_update.license_plate = vehicle.license_plate
            vehicle_to_update.purchase_date = vehicle.purchase_date
            vehicle_to_update.cost = vehicle.cost
            vehicle_to_update.entry_date=vehicle.entry_date
            db.commit()
            db.refresh(vehicle_to_update)
            return {
                "id": vehicle_to_update.id,
                "brand": vehicle_to_update.brand,
                "model": vehicle_to_update.model,
                "vin": vehicle_to_update.vin,
                "license_plate": vehicle_to_update.license_plate,
                "purchase_date": vehicle_to_update.purchase_date,
                "cost": vehicle_to_update.cost,
                "entry_date": vehicle_to_update.entry_date
            }
    
    def deleteVehicle(self, vehicle_id: int):
        db = next(get_db())
        vehicle_to_delete = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if vehicle_to_delete:
            db.delete(vehicle_to_delete)
            db.commit()
            return jsonify({"message": "Vehículo eliminado correctamente", "id": vehicle_id}), 200
        return jsonify({"error": "Vehículo no encontrado"}), 404

