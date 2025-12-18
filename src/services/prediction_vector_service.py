# src/routes/datos_informatica_routes.py
from flask import Blueprint, request, jsonify
import pandas as pd
from src.models.datos_informatica_models import DatosInformaticaDesercion
from src.configs.extensions import db
from src.utils.features_informatica import FEATURES_EN_ORDEN_INFORMATICA

datos_informatica_bp = Blueprint(
    "datos_informatica_bp", __name__, url_prefix="/datos/informatica"
)


# ============================================
# FUNCIÓN DE NORMALIZACIÓN DE NÚMEROS
# ============================================
def limpiar_numero(valor):
    """
    Normaliza valores numéricos que vienen como strings con separadores de miles,
    comas decimales o formatos regionales.
    """
    if isinstance(valor, (int, float)):
        return valor

    if isinstance(valor, str):
        # eliminar espacios en blanco
        valor = valor.strip()

        # eliminar separadores de miles
        valor = valor.replace(".", "")

        # convertir coma decimal a punto
        valor = valor.replace(",", ".")

        # si queda vacío, devolver None
        if valor == "":
            return None

        try:
            return float(valor)
        except:
            return None

    return None


# ============================================
# ENDPOINT DE CARGA MASIVA
# ============================================
@datos_informatica_bp.route("/carga_masiva", methods=["POST"])
def carga_masiva_informatica():
    if "file" not in request.files:
        return jsonify({"error": "Debe enviar un archivo"}), 400

    file = request.files["file"]

    try:
        # CSV o Excel
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file, sep=";")
        else:
            df = pd.read_excel(file)

        # Normalizar columnas numéricas
        for col in df.columns:
            df[col] = df[col].apply(limpiar_numero)

        # Validación de columnas obligatorias
        columnas_requeridas = ["IDAlumno", "Estado"] + FEATURES_EN_ORDEN_INFORMATICA
        faltantes = [col for col in columnas_requeridas if col not in df.columns]

        if faltantes:
            return jsonify({
                "error": "Columnas faltantes en el archivo",
                "faltantes": faltantes
            }), 400

        creados = 0
        actualizados = 0

        # ============================================
        # PROCESAR CADA FILA
        # ============================================
        for _, row in df.iterrows():
            id_alumno = int(row["IDAlumno"])
            existente = DatosInformaticaDesercion.query.filter_by(id_alumno=id_alumno).first()

            if existente:
                # Actualizar campos generales
                existente.estado = row["Estado"]
                existente.sexo = row["Sexo"]
                existente.estado_carrera = row["Estado_Carrera"]
                existente.tiempo_estudio = row["TiempoEstudio"]
                existente.ausencias = row["Ausencias"]
                existente.cinco_f = row["CincoF"]
                existente.aplazos = row["aplazos"]
                existente.promedio = row["Promedio"]

                # Actualizar materias
                for col in FEATURES_EN_ORDEN_INFORMATICA[7:]:
                    for c in DatosInformaticaDesercion.__table__.columns:
                        if c.name == col:
                            setattr(existente, c.key, row[col])
                            break

                actualizados += 1

            else:
                # Crear un nuevo registro
                nuevo = DatosInformaticaDesercion(
                    id_alumno=row["IDAlumno"],
                    estado=row["Estado"],
                    sexo=row["Sexo"],
                    estado_carrera=row["Estado_Carrera"],
                    tiempo_estudio=row["TiempoEstudio"],
                    ausencias=row["Ausencias"],
                    cinco_f=row["CincoF"],
                    aplazos=row["aplazos"],
                    promedio=row["Promedio"],
                )

                # Materias
                for col in FEATURES_EN_ORDEN_INFORMATICA[7:]:
                    for c in DatosInformaticaDesercion.__table__.columns:
                        if c.name == col:
                            setattr(nuevo, c.key, row[col])
                            break

                db.session.add(nuevo)
                creados += 1

        db.session.commit()

        return jsonify({
            "mensaje": "Carga masiva completada",
            "creados": creados,
            "actualizados": actualizados
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
