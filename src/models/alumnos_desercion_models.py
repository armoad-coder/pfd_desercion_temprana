# src/models/alumnos_desercion_models.py
from src.configs.extensions import db

class DatosAlumnosDesercion(db.Model):
    __tablename__ = "datos_alumnos_desercion"

    id = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column("IDAlumno", db.Integer, unique=True, nullable=False)

    # Estado real (solo si existe la etiqueta en los CSV)
    estado = db.Column("Estado", db.SmallInteger, nullable=True)

    # === VARIABLES GENERALES ===
    sexo = db.Column("Sexo", db.String(20), nullable=True)
    estado_carrera = db.Column("Estado_Carrera", db.String(50), nullable=True)
    tiempo_estudio = db.Column("TiempoEstudio", db.Integer, nullable=True)
    ausencias = db.Column("Ausencias", db.Integer, nullable=True)
    cinco_f = db.Column("CincoF", db.Integer, nullable=True)
    aplazos = db.Column("aplazos", db.Integer, nullable=True)
    promedio = db.Column("Promedio", db.Float, nullable=True)

    # === TODAS LAS MATERIAS EN ORDEN EXACTO ===
    admin_mercadotecnia = db.Column("ADMINISTRACION Y MERCADOTECNIA", db.Float)
    bases_datos_i = db.Column("BASES DE DATOS I", db.Float)
    bases_datos_ii = db.Column("BASES DE DATOS II", db.Float)
    computacion_i = db.Column("COMPUTACION I", db.Float)
    computacion_ii = db.Column("COMPUTACION II", db.Float)
    computacion_iii = db.Column("COMPUTACION III", db.Float)
    contabilidad_i = db.Column("CONTABILIDAD I", db.Float)
    calculo_i = db.Column("CALCULO I", db.Float)
    calculo_ii = db.Column("CALCULO II", db.Float)
    calculo_iii = db.Column("CALCULO III", db.Float)
    derecho_laboral = db.Column("DERECHO INTELECTUAL Y LABORAL", db.Float)
    diseno_sistemas = db.Column("DISENO DE SISTEMA INFORMATICO I", db.Float)
    diseno_tecnico = db.Column("DISENO TECNICO", db.Float)
    electronica_i = db.Column("ELECTRONICA I", db.Float)
    emprendedorismo = db.Column("EMPRENDEDORISMO", db.Float)
    estructura_datos_i = db.Column("ESTRUCTURA DE DATOS I", db.Float)
    estructuras_lenguajes = db.Column("ESTRUCTURAS DE LOS LENGUAJES", db.Float)

    eventos_deportes_i = db.Column("EVENTOS Y DEPORTES I", db.Float)
    eventos_deportes_ii = db.Column("EVENTOS Y DEPORTES II", db.Float)
    eventos_deportes_iii = db.Column("EVENTOS Y DEPORTES III", db.Float)
    eventos_deportes_iv = db.Column("EVENTOS Y DEPORTES IV", db.Float)
    eventos_deportes_v = db.Column("EVENTOS Y DEPORTES V", db.Float)
    eventos_deportes_vi = db.Column("EVENTOS Y DEPORTES VI", db.Float)

    expresion_oral = db.Column("EXPRESION ORAL Y ESCRITA", db.Float)

    fisica_i = db.Column("FISICA I", db.Float)
    fisica_ii = db.Column("FISICA II", db.Float)
    fisica_iii = db.Column("FISICA III", db.Float)

    geometria_analitica = db.Column("GEOMETRIA ANALITICA Y VECTORIAL", db.Float)

    idiomas_i = db.Column("IDIOMAS I", db.Float)

    informatica_i = db.Column("INFORMATICA I", db.Float)

    ingenieria_software_i = db.Column("INGENIERIA DE SOFTWARE I", db.Float)

    ingles_ii = db.Column("INGLES II", db.Float)
    ingles_iii = db.Column("INGLES III", db.Float)
    ingles_i = db.Column("INGLES I", db.Float)

    investigacion_operaciones = db.Column("INVESTIGACION DE OPERACIONES I", db.Float)

    laboratorio_idiomas_i = db.Column("LABORATORIO DE IDIOMAS I", db.Float)
    laboratorio_i = db.Column("LABORATORIO I", db.Float)

    lenguaje_programacion_i = db.Column("LENGUAJE DE PROGRAMACION I", db.Float)
    lenguaje_programacion_ii = db.Column("LENGUAJE DE PROGRAMACION II", db.Float)
    lenguaje_programacion_iv = db.Column("LENGUAJE DE PROGRAMACION IV", db.Float)
    lenguajes_programacion_iii = db.Column("LENGUAJES DE PROGRAMACION III", db.Float)

    matematica_aplicada = db.Column("MATEMATICA APLICADA", db.Float)

    metodologia_investigacion_i = db.Column("METODOLOGIA DE LA INVESTIGACION I", db.Float)

    metodos_numericos = db.Column("METODOS NUMERICOS", db.Float)

    probabilidades_estadisticas = db.Column("PROBABILIDADES Y ESTADISTICAS", db.Float)

    quimica = db.Column("QUIMICA", db.Float)

    redes_i = db.Column("REDES DE COMPUTADORAS I", db.Float)
    redes_ii = db.Column("REDES DE COMPUTADORAS II", db.Float)

    sis_op_i = db.Column("SISTEMAS OPERATIVOS I", db.Float)
    sis_op_ii = db.Column("SISTEMAS OPERATIVOS II", db.Float)

    taller_hw_i = db.Column("TALLER DE HARDWARE I", db.Float)
    taller_hw_ii = db.Column("TALLER DE HARDWARE II", db.Float)

    algebra_i = db.Column("ALGEBRA I", db.Float)
    algebra_ii = db.Column("ALGEBRA II", db.Float)

    etica_profesional = db.Column("ETICA PROFESIONAL", db.Float)

    carrera = db.Column("Carrera", db.String(30), nullable=True)

    def __repr__(self):
        return f"<Alumno {self.id_alumno}>"
