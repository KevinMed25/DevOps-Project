from flask import Blueprint, request, jsonify
from models.admin import AdminSchema
import re 
from services.admin_service import AdminService
from http import HTTPStatus

admin_blueprint = Blueprint('admins', __name__)

@admin_blueprint.route('/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    required_fields = ['email', 'password', 'invite_code']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), HTTPStatus.BAD_REQUEST
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data['email']):
        return jsonify({"error": "Formato de correo electrónico inválido"}), HTTPStatus.BAD_REQUEST
    
    if len(data['password']) < 8:
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres"}), HTTPStatus.BAD_REQUEST
    
    if data['invite_code'] != "INVITE-1234":
        return jsonify({"error": "Código de invitación inválido"}), HTTPStatus.BAD_REQUEST

    admin = AdminSchema(
        email=data['email'],
        password=data['password'],
        invite_code=data['invite_code']
    )

    admin_service = AdminService()
    result = admin_service.find_admin_by_email(admin.email)

    if result:
        return jsonify({"message": "El correo ya está registrado"}), HTTPStatus.CONFLICT

    new_admin = admin_service.register_admin(admin)
    return jsonify({"message": "Administrador registrado con éxito", "id": new_admin.id}), HTTPStatus.CREATED


