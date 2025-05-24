from flask import Blueprint, request, jsonify
from models.admin import AdminSchema
import re 
from services.admin_service import AdminService
from http import HTTPStatus
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from utils.auth_middleware import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_blueprint = Blueprint('admins', __name__)

@admin_blueprint.route('/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    required_fields = ['email', 'password', 'invite_code']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Faltan campos obligatorios"}), HTTPStatus.BAD_REQUEST
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data['email']):
        return jsonify({"message": "Formato de correo electrónico inválido"}), HTTPStatus.BAD_REQUEST
    
    if len(data['password']) < 8:
        return jsonify({"message": "La contraseña debe tener al menos 8 caracteres"}), HTTPStatus.BAD_REQUEST
    
    if data['invite_code'] != "INVITE-1234":
        return jsonify({"message": "Código de invitación inválido"}), HTTPStatus.BAD_REQUEST

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


@admin_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validar campos obligatorios
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email y contraseña son requeridos"}), 400
    
    # Buscar admin por email
    admin_service = AdminService()
    admin = admin_service.find_admin_by_email(data['email'])
    
    # Verificar si existe y la contraseña es correcta
    if not admin or not check_password_hash(admin.password, data['password']):
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    # Generar token JWT
    access_token = create_access_token(identity=str(admin.id))
    
    return jsonify({
        "message": "Login exitoso",
        "access_token": access_token,
        "admin_id": admin.id,
        "email": admin.email
    }), HTTPStatus.OK

@admin_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_my_profile():
    """Obtiene el perfil del administrador autenticado usando el JWT"""
    try:
        # Obtener el ID del admin desde el JWT
        current_admin_id = get_jwt_identity()
        
        admin_service = AdminService()
        admin = admin_service.find_admin_by_id(int(current_admin_id))
        
        if not admin:
            return jsonify({"message": "Administrador no encontrado"}), HTTPStatus.NOT_FOUND
        
        
        admin_data = {
            "id": admin.id,
            "email": admin.email,
        }
        
        return jsonify({
            "message": "Perfil obtenido exitosamente", 
            "data": admin_data
        }), HTTPStatus.OK   
        
    except Exception as e:
        return jsonify({"message": f"Error al obtener el perfil: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR

@admin_required()
@admin_blueprint.route('/', methods=['GET'])
def get_admins():
    admin_service = AdminService()
    admins = admin_service.get_admins()
    if not admins:
        return jsonify({"message":"No hay administradores registrados"}), HTTPStatus.NOT_FOUND
    return jsonify({"message":"Administradores obtenidos exitosamente", "data": admins}), HTTPStatus.OK