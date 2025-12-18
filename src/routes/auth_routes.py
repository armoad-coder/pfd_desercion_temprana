# src/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from src.services.auth_services import (
    authenticate_user,
    AuthenticationError,
)
from src.models.user_models import User

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos."}), 400

    try:
        user = authenticate_user(email, password)
    except AuthenticationError as e:
        return jsonify({"error": str(e)}), 401
    except Exception:
        return jsonify({"error": "Error interno al autenticar."}), 500

    # IDENTIDAD DEL JWT DEBE SER STRING, NO INT
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login exitoso",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "nombre": user.nombre,
            "apellido": user.apellido,
        }
    }), 200


# Ruta opcional protegida para probar el JWT desde el front:
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """
    GET /api/auth/me
    Header: Authorization: Bearer <token>
    """
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "nombre": user.nombre,
            "apellido": user.apellido,
        }
    }), 200
