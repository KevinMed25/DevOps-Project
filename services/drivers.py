from utils.db import get_db
from models.drivers import Driver
from models.drivers import DriverSchema
from models.assignment import Assignment

class DriversService:

    def getAllDrivers(self) -> list:
        db = next(get_db())
        drivers = db.query(Driver).all()
        return list(map(lambda driver: {
            "id": driver.id,
            "name": driver.name,
            "birthday": driver.birthday,
            "curp": driver.curp,
            "address": driver.address,
            "monthly_salary": driver.monthly_salary,
            "hire_date": driver.hire_date,
            "license_number": driver.license_number
        }, drivers))
    
    def createDriver(self, driver: DriverSchema):
        db = next(get_db())
        driver = Driver(
            name=driver.name,
            birthday=driver.birthday,
            curp=driver.curp,
            address=driver.address,
            monthly_salary=driver.monthly_salary,
            hire_date=driver.hire_date,
            license_number=driver.license_number
        )
        db.add(driver)
        db.commit()
        db.refresh(driver)
        
        return driver.id

    def updateDriver(self, driver: DriverSchema):
        db = next(get_db())
        driverToUpdate = db.query(Driver).filter(Driver.id == driver.id).first()
        if driverToUpdate:
            driverToUpdate.name = driver.name
            driverToUpdate.birthday = driver.birthday
            driverToUpdate.curp = driver.curp
            driverToUpdate.address = driver.address
            driverToUpdate.monthly_salary = driver.monthly_salary
            driverToUpdate.hire_date = driver.hire_date
            driverToUpdate.license_number = driver.license_number
            db.commit()
            db.refresh(driverToUpdate)
        return {
            "id": driverToUpdate.id,
            "name": driverToUpdate.name,
            "birthday": driverToUpdate.birthday,
            "curp": driverToUpdate.curp,
            "address": driverToUpdate.address,
            "monthly_salary": driverToUpdate.monthly_salary,
            "hire_date": driverToUpdate.hire_date,
            "license_number": driverToUpdate.license_number
        }

    def deleteDriver(self, driver_id: int):
        db = next(get_db())
        driver = db.query(Driver).get(driver_id)
        
        if not driver:
            raise ValueError("Conductor no encontrado")
        
        active_assignments = db.query(Assignment).filter(
            Assignment.driver_id == driver_id
        ).count()
        
        if active_assignments > 0:
            raise ValueError("El conductor tiene asignaciones activas")
        
        db.delete(driver)
        db.commit()
        return {"message": "Conductor eliminado exitosamente", "id": driver_id}
