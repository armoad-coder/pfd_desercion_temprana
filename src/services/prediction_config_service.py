from src.models.prediction_config_models import PredictionModelConfig
from src.configs.extensions import db
from src.utils.modelos_config import DEFAULT_MODEL_CONFIG


def initialize_prediction_config():
    """
    Carga configuraciones por defecto si la tabla está vacía.
    """
    if PredictionModelConfig.query.count() > 0:
        return
    
    for career, cfg in DEFAULT_MODEL_CONFIG.items():
        entry = PredictionModelConfig(
            career=career,
            algorithm=cfg["algorithm"],
            model_file=cfg["model_file"],
            scaler_file=cfg["scaler_file"],
        )
        db.session.add(entry)

    db.session.commit()


def get_all_configs():
    configs = PredictionModelConfig.query.all()
    
    return [
        {
            "career": c.career,
            "algorithm": c.algorithm,
            "model_file": c.model_file,
            "scaler_file": c.scaler_file,
        }
        for c in configs
    ]


def update_config_for_career(career, data):
    """
    Actualiza la configuración de una carrera específica.
    """
    config = PredictionModelConfig.query.filter_by(career=career).first()
    if not config:
        return None

    # Validaciones simples
    if "algorithm" in data:
        config.algorithm = data["algorithm"]

    if "model_file" in data:
        config.model_file = data["model_file"]

    if "scaler_file" in data:
        config.scaler_file = data["scaler_file"]

    db.session.commit()

    return {
        "career": config.career,
        "algorithm": config.algorithm,
        "model_file": config.model_file,
        "scaler_file": config.scaler_file,
    }
