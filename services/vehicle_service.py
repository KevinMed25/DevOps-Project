from utils.db import get_db
from models.vehiculo import Vehicle
from models.vehiculo import VehicleSchema

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

    def createVehicle(self, vehicle: VehicleSchema):
        db = next(get_db())
        
        vehicle = Vehicle(
            brand = vehicle.brand,
            model = vehicle.model,
            vin = vehicle.vin,
            license_plate = vehicle.license_plate,
            purchase_date = vehicle.purchase_date,
            cost = vehicle.cost,
            entry_date = vehicle.entry_date
        )
        
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        
        return vehicle.id
