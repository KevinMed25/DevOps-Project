from models.admin import Admin, AdminSchema
from utils.db import get_db
from flask import jsonify
from werkzeug.security import generate_password_hash

class AdminService:

    def register_admin(self, admin: AdminSchema):
        db = next(get_db())

        new_admin = Admin(
            email=admin.email,
            password=generate_password_hash(admin.password),
            invite_code=admin.invite_code
        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        return new_admin

    def find_admin_by_email(self, email: str):
        db = next(get_db())
        admin = db.query(Admin).filter(Admin.email == email).first()
        return admin
    
    def find_admin_by_id(self, admin_id: int):
        db = next(get_db())
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        return admin    
    
    def get_admins(self):
        db = next(get_db())
        admins = db.query(Admin).all()
        return [admin.to_dict() for admin in admins]