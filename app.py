from flask import Flask
from flask_migrate import Migrate
from src.configs.configs import Config
from src.configs.extensions import db, bcrypt, jwt, cors
from src.services.prediction_config_service import initialize_prediction_config
from src.routes.user_routes import user_bp
from src.routes.auth_routes import auth_bp
from src.routes.config_routes import config_bp
from src.routes.datos_informatica_routes import datos_informatica_bp
from src.routes.datos_electronica_routes import datos_electronica_bp
from src.routes.datos_civil_routes import datos_civil_bp
from src.routes.datos_electricidad_routes import datos_electricidad_bp
from src.routes.dash_home_routes import dashboard_home_bp
from src.routes.prediccion_informatica_routes import prediccion_informatica_bp


def create_app():
    app = Flask(__name__)
    # Importamos la configuracion de conexion de la BD desde configs.py
    app.config.from_object(Config)

    # Inicializamos extenciones en el proyecto.
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # === MODELOS DE BASE DE DATOS ===
    # Importar modelos para que Migrate los detecte(No son utilizados en app.py como tal)
    from src.models.user_models import User
    from src.models.prediction_config_models import PredictionModelConfig
    from src.models.alumnos_desercion_models import DatosAlumnosDesercion
    # Importamos los 4 modelos para las carreras correspondientes
    from src.models.datos_informatica_models import DatosInformaticaDesercion
    from src.models.datos_electronica_models import DatosElectronicaDesercion
    from src.models.datos_civil_models import DatosCivilDesercion
    from src.models.datos_electricidad_models import DatosElectricidadDesercion




    # Registramos los blueprint para routes.
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(config_bp)
    app.register_blueprint(datos_informatica_bp)
    app.register_blueprint(datos_electronica_bp)
    app.register_blueprint(datos_civil_bp)
    app.register_blueprint(datos_electricidad_bp)
    app.register_blueprint(dashboard_home_bp)
    app.register_blueprint(prediccion_informatica_bp)


    

    # Para migraciones
    Migrate(app, db)
    with app.app_context():
        try:
            initialize_prediction_config()
        except Exception as e:
            print("Warning: Could not initialize prediction config:", e)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)