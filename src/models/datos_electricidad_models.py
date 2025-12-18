# src/models/datos_electricidad_models.py
from src.configs.extensions import db

class DatosElectricidadDesercion(db.Model):
    __tablename__ = "datos_electricidad_desercion"

    id = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column(db.Integer, unique=True, index=True)

    # Datos generales
    estado = db.Column(db.Float)
    sexo = db.Column(db.Float)
    estado_carrera = db.Column(db.Float)
    tiempo_estudio = db.Column(db.Float)
    ausencias = db.Column(db.Float)
    cinco_f = db.Column(db.Float)
    aplazos = db.Column(db.Float)
    promedio = db.Column(db.Float)

    # Materias
    admin_mercadotecnia = db.Column(db.Float)
    algebra_ii = db.Column(db.Float)
    algebra_i = db.Column(db.Float)
    automatizacion_industrial = db.Column(db.Float)

    circuitos_electricos_i = db.Column(db.Float)
    circuitos_electricos_ii = db.Column(db.Float)

    computacion_ii = db.Column(db.Float)
    computacion_i = db.Column(db.Float)

    conversion_energia_ii = db.Column(db.Float)
    conversion_energia_i = db.Column(db.Float)

    calculo_i = db.Column(db.Float)
    calculo_ii = db.Column(db.Float)
    calculo_iii = db.Column(db.Float)
    calculo_iv = db.Column(db.Float)
    calculo_v = db.Column(db.Float)

    diseno_asistido_pc = db.Column(db.Float)
    diseno_tecnico = db.Column(db.Float)

    electrotecnia_i = db.Column(db.Float)
    electrotecnia_ii = db.Column(db.Float)

    electronica_potencia_ii = db.Column(db.Float)
    electronica_potencia_i = db.Column(db.Float)

    electronica_digital_i = db.Column(db.Float)
    electronica_digital_ii = db.Column(db.Float)

    electronica_i = db.Column(db.Float)
    electronica_ii = db.Column(db.Float)

    emprendedorismo = db.Column(db.Float)

    eventos_deportes_ii = db.Column(db.Float)
    eventos_deportes_i = db.Column(db.Float)
    eventos_deportes_iii = db.Column(db.Float)
    eventos_deportes_iv = db.Column(db.Float)
    eventos_deportes_v = db.Column(db.Float)
    eventos_deportes_vi = db.Column(db.Float)

    expresion_oral = db.Column(db.Float)

    fisica_ii = db.Column(db.Float)
    fisica_iv = db.Column(db.Float)
    fund_control_auto_i = db.Column(db.Float)
    fund_control_auto_ii = db.Column(db.Float)
    fisica_v = db.Column(db.Float)
    fisica_i = db.Column(db.Float)
    fisica_iii = db.Column(db.Float)
    fisica_vi = db.Column(db.Float)

    geometria_analitica = db.Column(db.Float)

    idiomas_i = db.Column(db.Float)
    ingles_i = db.Column(db.Float)
    ingles_ii = db.Column(db.Float)
    ingles_iii = db.Column(db.Float)

    instalaciones_electricas_i = db.Column(db.Float)
    instalaciones_electricas_ii = db.Column(db.Float)
    instalaciones_electricas_iii = db.Column(db.Float)

    laboratorio_idiomas_i = db.Column(db.Float)

    medicion_instrumentacion = db.Column(db.Float)

    metodologia_investigacion_i = db.Column(db.Float)

    probabilidades_estadisticas = db.Column(db.Float)

    programacion_lenguajes_computadora = db.Column(db.Float)

    quimica = db.Column(db.Float)

    seguridad_higiene_laboral = db.Column(db.Float)

    etica_profesional = db.Column(db.Float)
