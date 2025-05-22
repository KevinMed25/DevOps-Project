from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from utils.db import Base

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    date = Column(Date)
    origin_lat = Column(Float)
    origin_lng = Column(Float)
    destination_lat = Column(Float)
    destination_lng = Column(Float)
    status = Column(String(50))  # "completed", "failed", "in_progress"
    problem_description = Column(String(500))
    comments = Column(String(500))
    vehicle_id = Column(Integer, ForeignKey("Vehicles.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))

     # Relaciones
    vehicle = relationship("Vehicle", backref="routes")  # "Vehicle" debe coincidir con el nombre de la clase del modelo
    driver = relationship("Driver", backref="routes")   # "Driver" debe coincidir con el nombre de la clase del modelo

class RouteSchema:
    def __init__(self, name: str, date: str, origin_lat: float, origin_lng: float,
                 destination_lat: float, destination_lng: float, vehicle_id: int,
                 driver_id: int, status: str = None, problem_description: str = None,
                 comments: str = None, id: int = None):
        self.id = id
        self.name = name
        self.date = date
        self.origin_lat = origin_lat
        self.origin_lng = origin_lng
        self.destination_lat = destination_lat
        self.destination_lng = destination_lng
        self.status = status
        self.problem_description = problem_description
        self.comments = comments
        self.vehicle_id = vehicle_id
        self.driver_id = driver_id