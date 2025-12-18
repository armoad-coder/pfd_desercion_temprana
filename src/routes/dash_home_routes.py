# src/routes/dashboard_home_routes.py
from flask import Blueprint, jsonify
from src.configs.extensions import db
from sqlalchemy import text

# Importar modelos de las 4 carreras
from src.models.datos_informatica_models import DatosInformaticaDesercion
from src.models.datos_electronica_models import DatosElectronicaDesercion
from src.models.datos_electricidad_models import DatosElectricidadDesercion
from src.models.datos_civil_models import DatosCivilDesercion

dashboard_home_bp = Blueprint("dashboard_home_bp", __name__, url_prefix="/dashboard")

def normalize_column(name: str) -> str:
    return (
        name.lower()
        .replace("_", "")
        .replace(" ", "")
    )
# Mapear carrera → modelo correspondiente
MODELOS = {
    "informatica": DatosInformaticaDesercion,
    "electronica": DatosElectronicaDesercion,
    "electricidad": DatosElectricidadDesercion,
    "civil": DatosCivilDesercion,
}

# Columnas generales (NO son materias)
COLUMNAS_GENERALES = {
    "id", "id_alumno",
    "estado", "sexo", "estado_carrera",
    "tiempo_estudio", "ausencias",
    "cinco_f", "aplazos", "promedio"
}

# No son materias
NON_SUBJECT_COLUMNS = {
    "id",
    "idalumno",
    "estado",
    "sexo",
    "estadocarrera",
    "tiempoestudio",
    "ausencias",
    "cincof",
    "aplazos",
    "promedio",
}
TABLES = {
    "informatica": "datos_informatica_desercion",
    "electronica": "datos_electronica_desercion",
    "electricidad": "datos_electricidad_desercion",
    "civil": "datos_civil_desercion",
}

@dashboard_home_bp.route("/data", methods=["GET"])
def dashboard_home():
    respuesta = {}

    for nombre, Modelo in MODELOS.items():

        # Total alumnos
        total_alumnos = Modelo.query.count()

        # Contar materias (columnas - generales)
        columnas_modelo = [col.name for col in Modelo.__table__.columns]
        materias = [c for c in columnas_modelo if c not in COLUMNAS_GENERALES]
        cantidad_materias = len(materias)

        respuesta[nombre] = {
            "alumnos": total_alumnos,
            "materias": cantidad_materias
        }

    return jsonify(respuesta), 200

@dashboard_home_bp.route("/top-aplazos-por-carrera", methods=["GET"])
def top_aplazos_por_carrera():
    response = {}

    for carrera, table_name in TABLES.items():
        conteo_carrera = {}

        # Obtener columnas reales de la tabla
        columns_query = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = :table
        """)
        result = db.session.execute(columns_query, {"table": table_name})

        columnas = [
            {
                "real": row[0],
                "norm": normalize_column(row[0])
            }
            for row in result
        ]

        # Filtrar solo materias reales
        materias = [
            c for c in columnas
            if c["norm"] not in NON_SUBJECT_COLUMNS
        ]

        # Contar nota = 1 por materia
        for col in materias:
            materia_real = col["real"]

            count_query = text(f"""
                SELECT COUNT(*)
                FROM {table_name}
                WHERE "{materia_real}" = 1
            """)

            count = db.session.execute(count_query).scalar()

            if count and count > 0:
                conteo_carrera[materia_real] = count

        # Ordenar y tomar TOP 5
        top_materias = sorted(
            conteo_carrera.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        response[carrera] = [
            {"materia": materia, "aplazos": aplazos}
            for materia, aplazos in top_materias
        ]

    return jsonify(response)
