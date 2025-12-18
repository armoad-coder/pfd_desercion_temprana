from src.configs.extensions import db

class PredictionModelConfig(db.Model):
    __tablename__ = "prediction_model_config"

    id = db.Column(db.Integer, primary_key=True)
    career = db.Column(db.String(50), unique=True, nullable=False)  # ej: "informatica"
    algorithm = db.Column(db.String(50), nullable=False)            # ej: "knn", "decision_tree"
    model_file = db.Column(db.String(255), nullable=False)          # ruta del modelo .joblib
    scaler_file = db.Column(db.String(255), nullable=False)         # ruta del scaler .joblib

    def __repr__(self):
        return f"<PredictionModelConfig {self.career} -> {self.algorithm}>"
