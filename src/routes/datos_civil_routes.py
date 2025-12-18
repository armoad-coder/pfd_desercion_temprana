# src/routes/datos_civil_routes.py
from flask import Blueprint, request, jsonify
import pandas as pd
import numpy as np

from src.models.datos_civil_models import DatosCivilDesercion
from src.configs.extensions import db
from src.utils.features_civil import (
    FEATURES_EN_ORDEN_CIVIL,
    MATERIAS_EN_ORDEN_CIVIL,
)

datos_civil_bp = Blueprint(
    "datos_civil_bp", __name__, url_prefix="/datos/civil"
)


# ----------------------------------------------------------
# Utilidades de limpieza
# ----------------------------------------------------------

def clean_number(value):
    """Convierte valores tipo np.float64, strings con puntos/comas, etc., a float o None."""
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
    except Exception:
        return None


def to_native(value):
    """Convierte numpy types en tipos Python nativos aptos para SQLAlchemy."""
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
# CARGA MASIVA CIVIL
# ----------------------------------------------------------

@datos_civil_bp.route("/carga_masiva", methods=["POST"])
def carga_masiva_civil():
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
        ] + MATERIAS_EN_ORDEN_CIVIL

        faltantes = [c for c in columnas_requeridas if c not in df.columns]
        if faltantes:
            return jsonify({
                "error": "Columnas faltantes",
                "faltantes": faltantes
            }), 400

        creados = 0
        actualizados = 0

        # ------------------------------------------------------
        # Procesar fila por fila
        # ------------------------------------------------------
        for _, row in df.iterrows():
            id_alumno = int(row["IDAlumno"])
            existente = DatosCivilDesercion.query.filter_by(id_alumno=id_alumno).first()

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

            # --------------------------------------------------
            # Mapeo materias CSV → atributos del modelo Civil
            # --------------------------------------------------
            for materia in MATERIAS_EN_ORDEN_CIVIL:
                attr = None

                if materia == "ADMINISTRACION Y MERCADOTECNIA":
                    attr = "admin_mercadotecnia"
                elif materia == "CIRCUITOS ELECTRICOS":
                    attr = "circuitos_electricos"
                elif materia == "COMPUTACION I":
                    attr = "computacion_i"
                elif materia == "COMPUTACION II":
                    attr = "computacion_ii"
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
                elif materia == "CALCULO VI":
                    attr = "calculo_vi"
                elif materia == "DISENO ASISTIDO POR COMPUTADORA I":
                    attr = "diseno_asistido_pc_i"
                elif materia == "DISENO ASISTIDO POR COMPUTADORA II":
                    attr = "diseno_asistido_pc_ii"
                elif materia == "DISENO TECNICO":
                    attr = "diseno_tecnico"
                elif materia == "ESTRUCTURAS I":
                    attr = "estructuras_i"
                elif materia == "ESTRUCTURAS II":
                    attr = "estructuras_ii"
                elif materia == "ESTRUCTURAS III":
                    attr = "estructuras_iii"
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
                elif materia == "GEOTECNIA I":
                    attr = "geotecnia_i"
                elif materia == "GEOTECNIA II":
                    attr = "geotecnia_ii"
                elif materia == "HIDRAULICA I":
                    attr = "hidraulica_i"
                elif materia == "HIDRAULICA II":
                    attr = "hidraulica_ii"
                elif materia == "HORMIGON ARMADO I":
                    attr = "hormigon_armado_i"
                elif materia == "IDIOMAS  I":  # doble espacio
                    attr = "idiomas_i"
                elif materia == "INGLES I":
                    attr = "ingles_i"
                elif materia == "INGLES II":
                    attr = "ingles_ii"
                elif materia == "INGLES III":
                    attr = "ingles_iii"
                elif materia == "LABORATORIO DE IDIOMAS I":
                    attr = "laboratorio_idiomas_i"
                elif materia == "MATERIALES DE OBRAS CIVILES":
                    attr = "materiales_obras_civiles"
                elif materia == "MECANICA DE MATERIALES I":
                    attr = "mecanica_materiales_i"
                elif materia == "MECANICA DE MATERIALES II":
                    attr = "mecanica_materiales_ii"
                elif materia == "MECANICA VECTORIAL I":
                    attr = "mecanica_vectorial_i"
                elif materia == "MECANICA VECTORIAL II":
                    attr = "mecanica_vectorial_ii"
                elif materia == "METODOLOGIA DE LA INVESTIGACION I":
                    attr = "metodologia_investigacion_i"
                elif materia == "METODOLOGIA DE LA INVESTIGACION II":
                    attr = "metodologia_investigacion_ii"
                elif materia == "PROBABILIDAD Y ESTADISTICA":
                    attr = "probabilidad_estadistica"
                elif materia == "QUIMICA":
                    attr = "quimica"
                elif materia == "TECNOLOGIA DEL HORMIGON":
                    attr = "tecnologia_hormigon"
                elif materia == "TOPOGRAFIA":
                    attr = "topografia"
                elif materia == "VIAS DE COMUNICACION I":
                    attr = "vias_comunicacion_i"
                elif materia == "VIAS DE COMUNICACION II":
                    attr = "vias_comunicacion_ii"
                elif materia == "ALGEBRA LINEAL I":
                    attr = "algebra_lineal_i"
                elif materia == "ALGEBRA LINEAL II":
                    attr = "algebra_lineal_ii"
                elif materia == "ETICA PROFESIONAL":
                    attr = "etica_profesional"

                if attr:
                    payload[attr] = clean_number(row[materia])

            # Normalización final para evitar np.float64, np.int64, etc.
            payload = {k: to_native(v) for k, v in payload.items()}

            # Insert / Update
            if existente:
                for k, v in payload.items():
                    setattr(existente, k, v)
                actualizados += 1
            else:
                nuevo = DatosCivilDesercion(
                    id_alumno=id_alumno,
                    **payload,
                )
                db.session.add(nuevo)
                creados += 1

        db.session.commit()

        return jsonify({
            "mensaje": "Carga masiva civil completada",
            "creados": creados,
            "actualizados": actualizados,
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
