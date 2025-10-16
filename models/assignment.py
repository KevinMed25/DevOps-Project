from sqlalchemy import Column, Integer, ForeignKey
from utils.db import Base

class Assignment(Base):
    __tablename__ = "Assignments"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("Vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)

class AssignmentSchema:
    def __init__(self, vehicle_id: int, driver_id: int, id: int = None):
        self.id = id
        self.vehicle_id = vehicle_id
        self.driver_id = driver_id
