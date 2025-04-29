from app.utils.db import get_db
from app.models.drivers import Driver

class DriversService:

    def getAllDrivers(self) -> list:
        db = next(get_db())
        return db.query(Driver).all()