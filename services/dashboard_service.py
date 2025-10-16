from utils.db import get_db
from models import Driver, Vehicle, Admin, Route

class DashboardService:

    def getCounts(self) -> dict:
        db = next(get_db())
        driversCount = db.query(Driver).count()
        vehiclesCount = db.query(Vehicle).count()
        adminsCount = db.query(Admin).count()
        routesCount = db.query(Route).count()
        return {
            "drivers": driversCount,
            "vehicles": vehiclesCount,
            "admins": adminsCount,
            "routes": routesCount
        }
