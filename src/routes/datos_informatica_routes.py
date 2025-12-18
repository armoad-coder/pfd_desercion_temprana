from flask import Blueprint, request, jsonify
import pandas as pd
from src.models.datos_informatica_models import DatosInformaticaDesercion
from src.configs.extensions import db
import numpy as np
import re

datos_informatica_bp = Blueprint(
    "datos_informatica_bp", __name__, url_prefix="/datos/informatica"
)

# ==============================
#  MAPEADO CSV → MODELO
# ==============================
CSV_TO_MODEL = {
    "ADMINISTRACION Y MERCADOTECNIA": "admin_mercadotecnia",
    "BASES DE DATOS I": "bases_datos_i",
    "BASES DE DATOS II": "bases_datos_ii",
    "COMPUTACION I": "computacion_i",
    "COMPUTACION II": "computacion_ii",
    "COMPUTACION III": "computacion_iii",
    "CONTABILIDAD I": "contabilidad_i",
    "CALCULO I": "calculo_i",
    "CALCULO II": "calculo_ii",
    "CALCULO III": "calculo_iii",
    "DERECHO INTELECTUAL Y LABORAL": "derecho_laboral",
    "DISENO DE SISTEMA INFORMATICO I": "diseno_sistemas",
    "DISENO TECNICO": "diseno_tecnico",
    "ELECTRONICA I": "electronica_i",
    "EMPRENDEDORISMO": "emprendedorismo",
    "ESTRUCTURA DE DATOS I": "estructura_datos_i",
    "ESTRUCTURAS DE LOS LENGUAJES": "estructuras_lenguajes",
    "EVENTOS Y DEPORTES I": "eventos_deportes_i",
    "EVENTOS Y DEPORTES II": "eventos_deportes_ii",
    "EVENTOS Y DEPORTES III": "eventos_deportes_iii",
    "EVENTOS Y DEPORTES IV": "eventos_deportes_iv",
    "EVENTOS Y DEPORTES V": "eventos_deportes_v",
    "EVENTOS Y DEPORTES VI": "eventos_deportes_vi",
    "EXPRESION ORAL Y ESCRITA": "expresion_oral",
    "FISICA I": "fisica_i",
    "FISICA II": "fisica_ii",
    "FISICA III": "fisica_iii",
    "GEOMETRIA ANALITICA Y VECTORIAL": "geometria_analitica",
    "IDIOMAS I": "idiomas_i",
    "INFORMATICA I": "informatica_i",
    "INGENIERIA DE SOFTWARE I": "ingenieria_software_i",
    "INGLES II": "ingles_ii",
    "INGLES III": "ingles_iii",
    "INGLES I": "ingles_i",
    "INVESTIGACION DE OPERACIONES I": "investigacion_operaciones",
    "LABORATORIO DE IDIOMAS I": "laboratorio_idiomas_i",
    "LABORATORIO I": "laboratorio_i",
    "LENGUAJE DE PROGRAMACION  I": "lenguaje_programacion_i",
    "LENGUAJE DE PROGRAMACION II": "lenguaje_programacion_ii",
    "LENGUAJE DE PROGRAMACION IV": "lenguaje_programacion_iv",
    "LENGUAJES DE PROGRAMACION III": "lenguajes_programacion_iii",
    "MATEMATICA APLICADA": "matematica_aplicada",
    "METODOLOGIA DE LA INVESTIGACION I": "metodologia_investigacion_i",
    "METODOS NUMERICOS": "metodos_numericos",
    "PROBABILIDADES Y ESTADISTICAS": "probabilidades_estadisticas",
    "QUIMICA": "quimica",
    "REDES DE COMPUTADORAS I": "redes_i",
    "REDES DE COMPUTADORAS II": "redes_ii",
    "SISTEMAS OPERATIVOS I": "sis_op_i",
    "SISTEMAS OPERATIVOS II": "sis_op_ii",
    "TALLER DE HARDWARE I": "taller_hw_i",
    "TALLER DE HARDWARE II": "taller_hw_ii",
    "ALGEBRA I": "algebra_i",
    "ALGEBRA II": "algebra_ii",
    "ETICA PROFESIONAL": "etica_profesional",
}

def clean_int(value):
    if pd.isna(value):
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def clean_promedio(value):
    if pd.isna(value):
        return None

    # numpy -> python
    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return None

        # Formato latino: 1.234,56
        if "," in value and "." in value:
            value = value.replace(".", "").replace(",", ".")
        # Solo coma decimal: 6,75
        elif "," in value:
            value = value.replace(",", ".")

    try:
        num = float(value)
    except (ValueError, TypeError):
        return None

    # Protección mínima contra basura extrema
    if abs(num) > 1000:   # << límite amplio, no académico
        return None

    return round(num, 2)



@datos_informatica_bp.route("/carga_masiva", methods=["POST"])
def carga_masiva_informatica():

    if "file" not in request.files:
        return jsonify({"error": "Debe enviar un archivo"}), 400

    file = request.files["file"]

    try:
        # === Leer CSV / Excel igual que la interfaz ===
        df = (
            pd.read_csv(file, sep=";")
            if file.filename.endswith(".csv")
            else pd.read_excel(file)
        )

        columnas_requeridas = (
            ["IDAlumno", "Estado", "Sexo", "Estado_Carrera",
             "TiempoEstudio", "Ausencias", "CincoF", "aplazos", "Promedio"]
            + list(CSV_TO_MODEL.keys())
        )

        faltantes = [c for c in columnas_requeridas if c not in df.columns]
        if faltantes:
            return jsonify({"error": "Columnas faltantes", "faltantes": faltantes}), 400

        creados = 0
        actualizados = 0

        # === IMPORTANTE: evitar autoflush prematuro ===
        with db.session.no_autoflush:

            for _, row in df.iterrows():

                id_alumno = int(row["IDAlumno"])

                existente = DatosInformaticaDesercion.query.filter_by(
                    id_alumno=id_alumno
                ).first()

                payload = {
                    "estado": int(row["Estado"]) if not pd.isna(row["Estado"]) else None,
                    "sexo": str(row["Sexo"]) if not pd.isna(row["Sexo"]) else None,
                    "estado_carrera": str(row["Estado_Carrera"]) if not pd.isna(row["Estado_Carrera"]) else None,
                    "tiempo_estudio": int(row["TiempoEstudio"]) if not pd.isna(row["TiempoEstudio"]) else None,
                    "ausencias": int(row["Ausencias"]) if not pd.isna(row["Ausencias"]) else None,
                    "cinco_f": int(row["CincoF"]) if not pd.isna(row["CincoF"]) else None,
                    "aplazos": int(row["aplazos"]) if not pd.isna(row["aplazos"]) else None,

                    # 🔑 PROMEDIO DEL CSV (SIN PROCESAR)
                    "promedio": clean_promedio(row["Promedio"]),
                }

                # === Materias: confiar en pandas (igual que interfaz) ===
                for csv_name, model_field in CSV_TO_MODEL.items():
                    val = row[csv_name]
                    payload[model_field] = float(val) if not pd.isna(val) else None

                if existente:
                    for k, v in payload.items():
                        setattr(existente, k, v)
                    actualizados += 1
                else:
                    db.session.add(
                        DatosInformaticaDesercion(
                            id_alumno=id_alumno,
                            **payload
                        )
                    )
                    creados += 1

        db.session.commit()

        return jsonify({
            "mensaje": "Carga masiva realizada correctamente",
            "creados": creados,
            "actualizados": actualizados
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@datos_informatica_bp.route("/dashboard/alumno/<int:id_alumno>", methods=["GET"])
def dashboard_alumno(id_alumno):

    alumno = DatosInformaticaDesercion.query.filter_by(
        id_alumno=id_alumno
    ).first()

    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    # ==========================
    # Recolectar materias
    # ==========================
    materias = []
    notas_validas = []
    aplazos_1 = 0
    ausencias_0 = 0

    for csv_name, model_field in CSV_TO_MODEL.items():
        nota = getattr(alumno, model_field)

        if nota is None:
            continue

        materias.append({
            "materia": csv_name,
            "nota": float(nota)
        })

        notas_validas.append(nota)

        if nota == 1:
            aplazos_1 += 1
        elif nota == 0:
            ausencias_0 += 1

    total_materias = len(materias)

    # ==========================
    # KPIs del alumno
    # ==========================
    kpis = {
        "promedio_general": alumno.promedio,
        "total_materias": total_materias,
        "aplazos_nota_1": aplazos_1,
        "ausencias_nota_0": ausencias_0,
        "cinco_f": alumno.cinco_f or 0,
    }

    # ==========================
    # Distribución de notas
    # ==========================
    distribucion_notas = {
        "0": 0,
        "1": 0,
        "2_4": 0,
        "5_7": 0,
        "8_10": 0
    }

    for n in notas_validas:
        if n == 0:
            distribucion_notas["0"] += 1
        elif n == 1:
            distribucion_notas["1"] += 1
        elif 2 <= n <= 4:
            distribucion_notas["2_4"] += 1
        elif 5 <= n <= 7:
            distribucion_notas["5_7"] += 1
        elif 8 <= n <= 10:
            distribucion_notas["8_10"] += 1

    # ==========================
    # Respuesta final
    # ==========================
    return jsonify({
        "alumno": {
            "id_alumno": alumno.id_alumno,
            "sexo": alumno.sexo,
            "estado": alumno.estado,
            "estado_carrera": alumno.estado_carrera
        },
        "kpis": kpis,
        "distribucion_notas": distribucion_notas,
        "materias": materias
    }), 200