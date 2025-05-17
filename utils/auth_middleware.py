from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, exceptions

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                return fn(*args, **kwargs)
            except exceptions.NoAuthorizationError:
                return jsonify({"error": "Se requiere token de autorización"}), 401
            except exceptions.InvalidHeaderError:
                return jsonify({"error": "Formato de header de autorización inválido"}), 401
            except exceptions.JWTDecodeError:
                return jsonify({"error": "Token inválido o expirado"}), 401
            except Exception as e:
                return jsonify({"error": f"Error de autenticación: {str(e)}"}), 401
        return decorator
    return wrapper