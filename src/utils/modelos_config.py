DEFAULT_MODEL_CONFIG = {
    "informatica": {
        "algorithm": "knn",
        "model_file": "src/utils/modelos/modelo_knn_informatica.joblib",
        "scaler_file": "src/utils/scalers/scaler_informatica.joblib",
    },
    "electricidad": {
        "algorithm": "decision_tree",
        "model_file": "src/utils/modelos/modelo_dt_electricidad.joblib",
        "scaler_file": "src/utils/scalers/scaler_electricidad.joblib",
    },
    "civil": {
        "algorithm": "decision_tree",
        "model_file": "src/utils/modelos/modelo_dt_civil.joblib",
        "scaler_file": "src/utils/scalers/scaler_civil.joblib",
    },
    "electronica": {
        "algorithm": "logistic_regression",
        "model_file": "src/utils/modelos/modelo_rl_electronica.joblib",
        "scaler_file": "src/utils/scalers/scaler_electronica.joblib",
    },
}
