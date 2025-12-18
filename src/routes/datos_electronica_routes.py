# src/routes/datos_electronica_routes.py
from flask import Blueprint, request, jsonify
import pandas as pd
import numpy as np

from src.models.datos_electronica_models import DatosElectronicaDesercion
from src.configs.extensions import db
from src.utils.features_electronica import (
    FEATURES_EN_ORDEN_ELECTRONICA,
    MATERIAS_EN_ORDEN_ELECTRONICA,
)

datos_electronica_bp = Blueprint(
    "datos_electronica_bp", __name__, url_prefix="/datos/electronica"
)


# ----------------------------------------------------------
# Utilidades de limpieza
# ----------------------------------------------------------

def clean_number(value):
    """ Convierte valores tipo np.float64, strings con puntos/comas, etc., a float o None. """
    if value is None:
        return None

    if isinstance(value, (int, float, np.integer, np.floating)):
        if isinstance(value, float) and np.isnan(value):
            return None
        return float(value)

    s = str(value).strip()
    if s == "":
        return None

    # miles y coma decimal
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except:
        return None


def to_native(value):
    """Convierte numpy types en tipos Python nativos."""
    if isinstance(value, (np.floating, np.float32, np.float64)):
        return float(value)
    if isinstance(value, (np.integer, np.int32, np.int64)):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if value is None:
        return None
    if isinstance(value, float) and np.isnan(value):
        return None
    return value


# ----------------------------------------------------------
# CARGA MASIVA ELECTRÓNICA
# ----------------------------------------------------------

@datos_electronica_bp.route("/carga_masiva", methods=["POST"])
def carga_masiva_electronica():

    if "file" not in request.files:
        return jsonify({"error": "Debe enviar un archivo"}), 400

    file = request.files["file"]

    try:
        # Cargar archivo
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file, sep=";")
        else:
            df = pd.read_excel(file)

        # Validar columnas requeridas
        columnas_requeridas = [
            "IDAlumno",
            "Estado",
            "Sexo",
            "Estado_Carrera",
            "TiempoEstudio",
            "Ausencias",
            "CincoF",
            "aplazos",
            "Promedio",
        ] + MATERIAS_EN_ORDEN_ELECTRONICA

        faltantes = [c for c in columnas_requeridas if c not in df.columns]
        if faltantes:
            return jsonify({
                "error": "Columnas faltantes",
                "faltantes": faltantes
            }), 400

        creados = 0
        actualizados = 0

        # ----------------------------------------------------------
        # Procesar cada fila
        # ----------------------------------------------------------
        for _, row in df.iterrows():

            id_alumno = int(row["IDAlumno"])
            existente = DatosElectronicaDesercion.query.filter_by(id_alumno=id_alumno).first()

            # Datos generales
            payload = {
                "estado": clean_number(row["Estado"]),
                "sexo": to_native(row["Sexo"]),
                "estado_carrera": to_native(row["Estado_Carrera"]),
                "tiempo_estudio": clean_number(row["TiempoEstudio"]),
                "ausencias": clean_number(row["Ausencias"]),
                "cinco_f": clean_number(row["CincoF"]),
                "aplazos": clean_number(row["aplazos"]),
                "promedio": clean_number(row["Promedio"]),
            }

            # ------------------------------------------------------
            # MAPEO MATERIAS
            # ------------------------------------------------------
            for materia in MATERIAS_EN_ORDEN_ELECTRONICA:
                attr = None

                # MAPEOS
                if materia == "ADMINISTRACION Y MERCADOTECNIA":
                    attr = "admin_mercadotecnia"
                elif materia == "ALGEBRA I":
                    attr = "algebra_i"
                elif materia == "AUTOMATIZACION INDUSTRIAL":
                    attr = "automatizacion_industrial"
                elif materia == "CIRCUITOS ELECTRICOS I":
                    attr = "circuitos_electricos_i"
                elif materia == "CIRCUITOS ELECTRICOS II":
                    attr = "circuitos_electricos_ii"
                elif materia == "COMPUTACION II":
                    attr = "computacion_ii"
                elif materia == "COMPUTACION I":
                    attr = "computacion_i"
                elif materia == "CALCULO I":
                    attr = "calculo_i"
                elif materia == "CALCULO II":
                    attr = "calculo_ii"
                elif materia == "CALCULO III":
                    attr = "calculo_iii"
                elif materia == "CALCULO IV":
                    attr = "calculo_iv"
                elif materia == "CALCULO V":
                    attr = "calculo_v"
                elif materia == "DISENO ASISTIDO POR COMPUTADORA":
                    attr = "diseno_asistido_pc"
                elif materia == "DISENO TECNICO":
                    attr = "diseno_tecnico"
                elif materia == "ELECTROTECNIA I":
                    attr = "electrotecnia_i"
                elif materia == "ELECTROTECNIA II":
                    attr = "electrotecnia_ii"
                elif materia == "ELECTRONICA  DIGITAL II":
                    attr = "electronica_digital_ii"
                elif materia == "ELECTRONICA DE POTENCIA I":
                    attr = "electronica_potencia_i"
                elif materia == "ELECTRONICA DE POTENCIA II":
                    attr = "electronica_potencia_ii"
                elif materia == "ELECTRONICA DIGITAL I":
                    attr = "electronica_digital_i"
                elif materia == "ELECTRONICA I":
                    attr = "electronica_i"
                elif materia == "ELECTRONICA II":
                    attr = "electronica_ii"
                elif materia == "ELECTRONICA III":
                    attr = "electronica_iii"
                elif materia == "ELECTRONICA INDUSTRIAL":
                    attr = "electronica_industrial"
                elif materia == "EMPRENDEDORISMO":
                    attr = "emprendedorismo"
                elif materia == "EVENTOS Y DEPORTES I":
                    attr = "eventos_deportes_i"
                elif materia == "EVENTOS Y DEPORTES II":
                    attr = "eventos_deportes_ii"
                elif materia == "EVENTOS Y DEPORTES III":
                    attr = "eventos_deportes_iii"
                elif materia == "EVENTOS Y DEPORTES IV":
                    attr = "eventos_deportes_iv"
                elif materia == "EVENTOS Y DEPORTES V":
                    attr = "eventos_deportes_v"
                elif materia == "EVENTOS Y DEPORTES VI":
                    attr = "eventos_deportes_vi"
                elif materia == "EXPRESION ORAL Y ESCRITA":
                    attr = "expresion_oral"
                elif materia == "FUNDAMENTOS DE CONTROL  AUTOMATIZADO II":
                    attr = "fund_control_auto_ii"
                elif materia == "FUNDAMENTOS DE CONTROL AUTOMATIZADO I":
                    attr = "fund_control_auto_i"
                elif materia == "FISICA I":
                    attr = "fisica_i"
                elif materia == "FISICA II":
                    attr = "fisica_ii"
                elif materia == "FISICA III":
                    attr = "fisica_iii"
                elif materia == "FISICA IV":
                    attr = "fisica_iv"
                elif materia == "FISICA V":
                    attr = "fisica_v"
                elif materia == "FISICA VI":
                    attr = "fisica_vi"
                elif materia == "GEOMETRIA ANALITICA":
                    attr = "geometria_analitica"
                elif materia == "IDIOMAS I":
                    attr = "idiomas_i"
                elif materia == "INGLES I":
                    attr = "ingles_i"
                elif materia == "INGLES II":
                    attr = "ingles_ii"
                elif materia == "INGLES III":
                    attr = "ingles_iii"
                elif materia == "INSTALACIONES ELECTRICAS I":
                    attr = "instalaciones_electricas_i"
                elif materia == "LABORATORIO DE IDIOMAS I":
                    attr = "laboratorio_idiomas_i"
                elif materia == "MEDICION E INSTRUMENTACION":
                    attr = "medicion_instrumentacion"
                elif materia == "METODOLOGIA DE LA INVESTIGACION I":
                    attr = "metodologia_investigacion_i"
                elif materia == "MICROCONTROLADORES":
                    attr = "microcontroladores"
                elif materia == "PROBABILIDADES Y ESTADISTICAS":
                    attr = "probabilidades_estadisticas"
                elif materia == "PROGRAMACION EN LENGUAJE DE COMPUTADORAS":
                    attr = "programacion_lenguaje_computadoras"
                elif materia == "QUIMICA":
                    attr = "quimica"
                elif materia == "SEGURIDAD E HIGIENE LABORAL":
                    attr = "seguridad_higiene_laboral"
                elif materia == "SIMULACION DE CIRCUITOS POR COMPUTADORA":
                    attr = "simulacion_circuitos_pc"
                elif materia == "ALGEBRA II":
                    attr = "algebra_ii"
                elif materia == "ETICA PROFESIONAL":
                    attr = "etica_profesional"

                # Aplicar clean_number a cada materia
                if attr:
                    payload[attr] = clean_number(row[materia])

            # ------------------------------------------------------
            # Normalización final del payload (clave)
            # ------------------------------------------------------
            payload = {k: to_native(v) for k, v in payload.items()}

            # ------------------------------------------------------
            # Insert / Update
            # ------------------------------------------------------
            if existente:
                for k, v in payload.items():
                    setattr(existente, k, v)
                actualizados += 1
            else:
                nuevo = DatosElectronicaDesercion(
                    id_alumno=id_alumno,
                    **payload,
                )
                db.session.add(nuevo)
                creados += 1

        db.session.commit()

        return jsonify({
            "mensaje": "Carga masiva electrónica completada",
            "creados": creados,
            "actualizados": actualizados
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
