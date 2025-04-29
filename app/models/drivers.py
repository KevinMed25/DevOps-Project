from sqlalchemy import Column, Integer, Date, String
from app.utils.db import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    birthday = Column(Date)
    curp= Column(String(255), unique=True, index=True)
    address = Column(String(255))
    monthly_salary = Column(Integer)
    hire_date = Column(Date)
    license_number = Column(String(255), unique=True, index=True)
 