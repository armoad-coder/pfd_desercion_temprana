# src/models/datos_civil_models.py
from src.configs.extensions import db


class DatosCivilDesercion(db.Model):
    __tablename__ = "datos_civil_desercion"

    id = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column(db.Integer, unique=True, index=True)

    # Campos generales
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
    circuitos_electricos = db.Column(db.Float)
    computacion_i = db.Column(db.Float)
    computacion_ii = db.Column(db.Float)

    calculo_i = db.Column(db.Float)
    calculo_ii = db.Column(db.Float)
    calculo_iii = db.Column(db.Float)
    calculo_iv = db.Column(db.Float)
    calculo_v = db.Column(db.Float)
    calculo_vi = db.Column(db.Float)

    diseno_asistido_pc_i = db.Column(db.Float)
    diseno_asistido_pc_ii = db.Column(db.Float)
    diseno_tecnico = db.Column(db.Float)

    estructuras_i = db.Column(db.Float)
    estructuras_ii = db.Column(db.Float)
    estructuras_iii = db.Column(db.Float)

    eventos_deportes_i = db.Column(db.Float)
    eventos_deportes_ii = db.Column(db.Float)
    eventos_deportes_iii = db.Column(db.Float)
    eventos_deportes_iv = db.Column(db.Float)
    eventos_deportes_v = db.Column(db.Float)
    eventos_deportes_vi = db.Column(db.Float)

    expresion_oral = db.Column(db.Float)

    fisica_i = db.Column(db.Float)
    fisica_ii = db.Column(db.Float)
    fisica_iii = db.Column(db.Float)
    fisica_iv = db.Column(db.Float)
    fisica_v = db.Column(db.Float)
    fisica_vi = db.Column(db.Float)

    geometria_analitica = db.Column(db.Float)

    geotecnia_i = db.Column(db.Float)
    geotecnia_ii = db.Column(db.Float)

    hidraulica_i = db.Column(db.Float)
    hidraulica_ii = db.Column(db.Float)

    hormigon_armado_i = db.Column(db.Float)

    idiomas_i = db.Column(db.Float)
    ingles_i = db.Column(db.Float)
    ingles_ii = db.Column(db.Float)
    ingles_iii = db.Column(db.Float)

    laboratorio_idiomas_i = db.Column(db.Float)

    materiales_obras_civiles = db.Column(db.Float)

    mecanica_materiales_i = db.Column(db.Float)
    mecanica_materiales_ii = db.Column(db.Float)
    mecanica_vectorial_i = db.Column(db.Float)
    mecanica_vectorial_ii = db.Column(db.Float)

    metodologia_investigacion_i = db.Column(db.Float)
    metodologia_investigacion_ii = db.Column(db.Float)

    probabilidad_estadistica = db.Column(db.Float)

    quimica = db.Column(db.Float)

    tecnologia_hormigon = db.Column(db.Float)

    topografia = db.Column(db.Float)

    vias_comunicacion_i = db.Column(db.Float)
    vias_comunicacion_ii = db.Column(db.Float)

    algebra_lineal_i = db.Column(db.Float)
    algebra_lineal_ii = db.Column(db.Float)

    etica_profesional = db.Column(db.Float)
