from flask import Blueprint, request, jsonify
from models.admin import AdminSchema
import re
import logging
from services.admin_service import AdminService
from http import HTTPStatus
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from utils.auth_middleware import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity

logger = logging.getLogger(__name__)
admin_blueprint = Blueprint('admins', __name__)

@admin_blueprint.route('/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    logger.info(f"Registration attempt for email: {data.get('email')}")
    required_fields = ['email', 'password', 'invite_code']
    if not all(field in data for field in required_fields):
        logger.warning("Registration failed: Missing required fields")
        return jsonify({"message": "Faltan campos obligatorios"}), HTTPStatus.BAD_REQUEST
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data['email']):
        logger.warning(f"Registration failed for email {data.get('email')}: Invalid email format")
        return jsonify({"message": "Formato de correo electrónico inválido"}), HTTPStatus.BAD_REQUEST
    
    if len(data['password']) < 8:
        logger.warning(f"Registration failed for email {data.get('email')}: Password too short")
        return jsonify({"message": "La contraseña debe tener al menos 8 caracteres"}), HTTPStatus.BAD_REQUEST
    
    if data['invite_code'] != "INVITE-1234":
        logger.warning(f"Registration failed for email {data.get('email')}: Invalid invite code")
        return jsonify({"message": "Código de invitación inválido"}), HTTPStatus.BAD_REQUEST

    try:
        admin = AdminSchema(
            email=data['email'],
            password=data['password'],
            invite_code=data['invite_code']
        )

        admin_service = AdminService()
        result = admin_service.find_admin_by_email(admin.email)

        if result:
            logger.info(f"Registration failed for email {admin.email}: Email already registered")
            return jsonify({"message": "El correo ya está registrado"}), HTTPStatus.CONFLICT

        new_admin = admin_service.register_admin(admin)
        logger.info(f"Admin registered successfully: {new_admin.email}, ID: {new_admin.id}")
        return jsonify({"message": "Administrador registrado con éxito", "id": new_admin.id}), HTTPStatus.CREATED
    except Exception as e:
        logger.exception(f"Error during admin registration for email {data.get('email')}: {e}")
        return jsonify({"message": "Error interno del servidor"}), HTTPStatus.INTERNAL_SERVER_ERROR


@admin_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    logger.info(f"Login attempt for email: {data.get('email')}")
    
    if not data or not data.get('email') or not data.get('password'):
        logger.warning("Login failed: Email or password missing")
        return jsonify({"message": "Email y contraseña son requeridos"}), 400
    
    try:
        admin_service = AdminService()
        admin = admin_service.find_admin_by_email(data['email'])
        
        if not admin or not check_password_hash(admin.password, data['password']):
            logger.warning(f"Login failed for email {data.get('email')}: Invalid credentials")
            return jsonify({"message": "Credenciales inválidas"}), 401
        
        access_token = create_access_token(identity=str(admin.id))
        logger.info(f"Admin login successful for email: {admin.email}, ID: {admin.id}")
        return jsonify({
            "message": "Login exitoso",
            "access_token": access_token,
            "id": admin.id,
            "email": admin.email
        }), HTTPStatus.OK
    except Exception as e:
        logger.exception(f"Error during login for email {data.get('email')}: {e}")
        return jsonify({"message": "Error interno del servidor"}), HTTPStatus.INTERNAL_SERVER_ERROR

@admin_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_my_profile():
    """Obtiene el perfil del administrador autenticado usando el JWT"""
    current_admin_id = get_jwt_identity()
    try:
        logger.info(f"Profile requested by admin ID: {current_admin_id}")
        
        admin_service = AdminService()
        admin = admin_service.find_admin_by_id(int(current_admin_id))
        
        if not admin:
            logger.warning(f"Profile request: Admin not found for ID {current_admin_id}")
            return jsonify({"message": "Administrador no encontrado"}), HTTPStatus.NOT_FOUND
        
        
        admin_data = {
            "id": admin.id,
            "email": admin.email,
        }
        logger.info(f"Profile successfully retrieved for admin ID: {current_admin_id}")
        return jsonify({
            "message": "Perfil obtenido exitosamente", 
            "data": admin_data
        }), HTTPStatus.OK   
        
    except Exception as e:
        logger.exception(f"Error retrieving profile for admin ID {current_admin_id}: {e}")
        return jsonify({"message": f"Error al obtener el perfil: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR

@admin_required()
@admin_blueprint.route('/', methods=['GET'])
def get_admins():
    logger.info("Request to get all admins")
    try:
        admin_service = AdminService()
        admins = admin_service.get_admins()
        if not admins:
            logger.info("No admins found")
            return jsonify({"message":"No hay administradores registrados"}), HTTPStatus.NOT_FOUND
        logger.info(f"Successfully retrieved {len(admins)} admins")
        return jsonify({"message":"Administradores obtenidos exitosamente", "data": admins}), HTTPStatus.OK
    except Exception as e:
        logger.exception(f"Error retrieving admins: {e}")
        return jsonify({"message": "Error interno del servidor al obtener administradores"}), HTTPStatus.INTERNAL_SERVER_ERROR