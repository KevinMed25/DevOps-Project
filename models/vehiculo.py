from sqlalchemy import Column, Integer, DateTime, String, Float
from utils.db import Base

class Vehicle(Base):
    __tablename__ = "Vehicles"
    id = Column(Integer, primary_key=True)               
    brand = Column(String(50), nullable=False)           
    model = Column(String(50), nullable=False)           
    vin = Column(String(17), unique=True, nullable=False) 
    license_plate = Column(String(15), unique=True, nullable=False)  
    purchase_date = Column(DateTime, nullable=False)      
    cost = Column(Float, nullable=False)                                      
    entry_date = Column(DateTime, nullable=False)         

class VehicleSchema():
    
    def __init__(self, brand: str, model: str, vin: str, license_plate: str,purchase_date, cost: float, entry_date,  id: int= None):
        self.id = id 
        self.brand = brand
        self.model = model
        self.vin = vin
        self.license_plate = license_plate
        self.purchase_date = purchase_date
        self.cost = cost 
        self.entry_date= entry_date
