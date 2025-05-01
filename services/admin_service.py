from models.admin import Admin, AdminSchema
from utils.db import get_db
from flask import jsonify
from werkzeug.security import generate_password_hash

class AdminService:

    def registerAdmin(self, admin: AdminSchema):
        db = next(get_db())

        if admin.invite_code != "INVITE-1234":
            return jsonify({"error": "Código de invitación inválido"}), 403

        existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
        if existing_admin:
            return jsonify({"error": "El correo ya está registrado"}), 409

        new_admin = Admin(
            email=admin.email,
            password=generate_password_hash(admin.password),
            invite_code=admin.invite_code
        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        return jsonify({"message": "Administrador registrado con éxito", "email": new_admin.email}), 201
