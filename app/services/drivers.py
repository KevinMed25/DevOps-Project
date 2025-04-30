from app.utils.db import get_db
from app.models.drivers import Driver

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
