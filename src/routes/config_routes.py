from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.services.prediction_config_service import (
    get_all_configs,
    update_config_for_career
)

config_bp = Blueprint("config_bp", __name__, url_prefix="/config")

# GET /config/models
@config_bp.route("/models", methods=["GET"])
@jwt_required()
def get_model_configs():
    try:
        configs = get_all_configs()
        return jsonify(configs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# PUT /config/models/<career>
@config_bp.route("/models/<career>", methods=["PUT"])
@jwt_required()
def update_model_config(career):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    try:
        updated = update_config_for_career(career, data)
        if not updated:
            return jsonify({"error": "Carrera no encontrada"}), 404

        return jsonify({
            "message": "Configuración actualizada correctamente",
            "config": updated
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Error interno"}), 500
