from sqlalchemy import Column, Integer, String
from utils.db import Base

class Admin(Base):
    __tablename__ = "Admins"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    invite_code = Column(String(50), nullable=False)

class AdminSchema:
    def __init__(self, email: str, password: str, invite_code: str, id: int = None):
        self.id = id
        self.email = email
        self.password = password
        self.invite_code = invite_code
