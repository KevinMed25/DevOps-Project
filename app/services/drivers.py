from app.utils.db import get_db
from app.models.drivers import Driver
from app.models.drivers import DriverSchema

class DriversService:

    def getAllDrivers(self) -> list:
        db = next(get_db())
        return db.query(Driver).all()
    
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
    
