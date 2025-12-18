from flask import Blueprint, request, jsonify
from src.services.user_services import create_user_service, update_user_service, reset_password_service, get_all_users_service
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__, url_prefix="/api/users")

@user_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    # 1. Validación básica de entrada
    if not data:
        return jsonify({'error': 'No se enviaron datos (JSON body missing)'}), 400
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Faltan campos obligatorios: email y password'}), 400

    try:
        # 2. Delegar a la capa de servicio
        new_user = create_user_service(data)
        # 3. Respuesta exitosa
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'user': {
                'email': new_user.email,
                'nombre': new_user.nombre,
                'apellido': new_user.apellido
            }
        }), 201

    except ValueError as e:
        # Errores de negocio (ej. el email ya existe) lanzados por el servicio
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Errores inesperados del servidor
        return jsonify({'error': 'Error interno del servidor'}), 500

@user_bp.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No se enviaron datos'}), 400

    try:
        updated_user = update_user_service(user_id, data)

        if not updated_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        return jsonify({
            'message': 'Usuario actualizado correctamente',
            'user': {
                'id': updated_user.id,
                'email': updated_user.email,
                'nombre': updated_user.nombre,
                'apellido': updated_user.apellido
            }
        }), 200

    except ValueError as e:
        # Error de negocio (ej. email duplicado)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno al actualizar'}), 500

# URL Final: PUT user/reset_password/1
@user_bp.route('/reset_password/<int:user_id>', methods=['PUT'])
def reset_password(user_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se enviaron datos'}), 400

    try:
        result = reset_password_service(user_id, data)

        if result is None:
             return jsonify({'error': 'Usuario no encontrado'}), 404

        return jsonify({
            'message': 'Contraseña actualizada exitosamente.'
        }), 200

    except ValueError as e:
        # Aquí caerán los errores: "Pass actual incorrecta" o "Campos faltantes"
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno al cambiar contraseña'}), 500

@user_bp.route('/list', methods=['GET'])
def list_users():
    users = get_all_users_service()
    print(users)
    return jsonify([
        {
            "id": u.id,
            "email": u.email,
            "nombre": u.nombre,
            "apellido": u.apellido,
        }
        for u in users
    ]), 200