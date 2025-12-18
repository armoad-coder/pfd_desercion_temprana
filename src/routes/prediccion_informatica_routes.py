import joblib
import pandas as pd
from flask import Blueprint, jsonify

from src.models.datos_informatica_models import DatosInformaticaDesercion

# ===============================
# ORDEN EXACTO DEL ENTRENAMIENTO
# ===============================

MATERIAS_EN_ORDEN_CSV = [
    "ADMINISTRACION Y MERCADOTECNIA",
    "BASES DE DATOS I",
    "BASES DE DATOS II",
    "COMPUTACION I",
    "COMPUTACION II",
    "COMPUTACION III",
    "CONTABILIDAD I",
    "CALCULO I",
    "CALCULO II",
    "CALCULO III",
    "DERECHO INTELECTUAL Y LABORAL",
    "DISENO DE SISTEMA INFORMATICO I",
    "DISENO TECNICO",
    "ELECTRONICA I",
    "EMPRENDEDORISMO",
    "ESTRUCTURA DE DATOS I",
    "ESTRUCTURAS DE LOS LENGUAJES",
    "EVENTOS Y DEPORTES I",
    "EVENTOS Y DEPORTES II",
    "EVENTOS Y DEPORTES III",
    "EVENTOS Y DEPORTES IV",
    "EVENTOS Y DEPORTES V",
    "EVENTOS Y DEPORTES VI",
    "EXPRESION ORAL Y ESCRITA",
    "FISICA I",
    "FISICA II",
    "FISICA III",
    "GEOMETRIA ANALITICA Y VECTORIAL",
    "IDIOMAS I",
    "INFORMATICA I",
    "INGENIERIA DE SOFTWARE I",
    "INGLES II",
    "INGLES III",
    "INGLES I",
    "INVESTIGACION DE OPERACIONES I",
    "LABORATORIO DE IDIOMAS I",
    "LABORATORIO I",
    "LENGUAJE DE PROGRAMACION  I",  # ← doble espacio, se respeta
    "LENGUAJE DE PROGRAMACION II",
    "LENGUAJE DE PROGRAMACION IV",
    "LENGUAJES DE PROGRAMACION III",
    "MATEMATICA APLICADA",
    "METODOLOGIA DE LA INVESTIGACION I",
    "METODOS NUMERICOS",
    "PROBABILIDADES Y ESTADISTICAS",
    "QUIMICA",
    "REDES DE COMPUTADORAS I",
    "REDES DE COMPUTADORAS II",
    "SISTEMAS OPERATIVOS I",
    "SISTEMAS OPERATIVOS II",
    "TALLER DE HARDWARE I",
    "TALLER DE HARDWARE II",
    "ALGEBRA I",
    "ALGEBRA II",
    "ETICA PROFESIONAL",
]

FEATURES_EN_ORDEN_INFORMATICA = [
    "Sexo",
    "Estado_Carrera",
    "TiempoEstudio",
    "Ausencias",
    "CincoF",
    "aplazos",
    "Promedio",
] + MATERIAS_EN_ORDEN_CSV


# ===============================
# MAPEO CSV → MODELO (snake_case)
# ===============================

CSV_TO_MODEL_ATTR = {
    # ===== GENERALES =====
    "Sexo": "sexo",
    "Estado_Carrera": "estado_carrera",
    "TiempoEstudio": "tiempo_estudio",
    "Ausencias": "ausencias",
    "CincoF": "cinco_f",
    "aplazos": "aplazos",
    "Promedio": "promedio",

    # ===== MATERIAS =====
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

# ===============================
# MODELO / SCALER
# ===============================

MODEL_PATH = "src/utils/modelos/modelo_knn_informatica.joblib"
SCALER_PATH = "src/utils/scalers/scaler_informatica.joblib"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

prediccion_informatica_bp = Blueprint(
    "prediccion_informatica_bp",
    __name__,
    url_prefix="/prediccion/informatica"
)

# ===============================
# ENDPOINT
# ===============================

@prediccion_informatica_bp.route("/v1/<int:id_alumno>", methods=["GET"])
def prediccion_informatica(id_alumno):
    alumno = DatosInformaticaDesercion.query.filter_by(
        id_alumno=id_alumno
    ).first()

    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    # ---------------------------
    # Construir fila EXACTA CSV
    # ---------------------------
    fila = {}

    for csv_name in FEATURES_EN_ORDEN_INFORMATICA:
        model_attr = CSV_TO_MODEL_ATTR[csv_name]
        valor = getattr(alumno, model_attr)

        if valor is None:
            raise ValueError(f"Valor NULL en feature: {csv_name}")

        fila[csv_name] = float(valor)

    X_df = pd.DataFrame([fila], columns=FEATURES_EN_ORDEN_INFORMATICA)
    # ---------------------------
    # Escalar y predecir
    # ---------------------------
    X_scaled = scaler.transform(X_df)
    probs = model.predict_proba(X_scaled)[0]
    pred = model.predict(X_scaled)[0]
    state_mapping = {
        2: "Graduado",
        3: "Deserción temprana",
        4: "Deserción tardía",
    }
    materias = {}

    for csv_name, model_attr in CSV_TO_MODEL_ATTR.items():
        if csv_name in FEATURES_EN_ORDEN_INFORMATICA[7:]:  # solo materias
            valor = getattr(alumno, model_attr, None)
            if valor is not None:
                materias[csv_name] = float(valor)

    return jsonify({
        "id_alumno": id_alumno,
        "carrera": "informatica",
        "prediccion": state_mapping.get(pred, "Desconocido"),
        "probabilidades": {
            state_mapping[int(c)]: round(p * 100, 2)
            for c, p in zip(model.classes_, probs)
        },
        "materias": materias
    }), 200