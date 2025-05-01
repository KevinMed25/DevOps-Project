from flask import Blueprint, request, jsonify
from models.admin import AdminSchema
from services.admin_service import AdminService

admin_blueprint = Blueprint('admins', __name__)

@admin_blueprint.route('/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    required_fields = ['email', 'password', 'invite_code']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    admin = AdminSchema(
        email=data['email'],
        password=data['password'],
        invite_code=data['invite_code']
    )

    admin_service = AdminService()
    return admin_service.registerAdmin(admin)
