# src/models/datos_informatica_models.py
from src.configs.extensions import db

class DatosInformaticaDesercion(db.Model):
    __tablename__ = "datos_informatica_desercion"

    id = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column("IDAlumno", db.Integer, unique=True, nullable=False)
    estado = db.Column("Estado", db.SmallInteger, nullable=True)

    # === VARIABLES GENERALES ===
    sexo = db.Column("Sexo", db.String(20), nullable=True)
    estado_carrera = db.Column("Estado_Carrera", db.String(50), nullable=True)
    tiempo_estudio = db.Column("TiempoEstudio", db.Integer, nullable=True)
    ausencias = db.Column("Ausencias", db.Integer, nullable=True)
    cinco_f = db.Column("CincoF", db.Integer, nullable=True)
    aplazos = db.Column("aplazos", db.Integer, nullable=True)
    promedio = db.Column("Promedio", db.Float, nullable=True)

    # === MATERIAS (todas, con nombres exactamente como en el Excel) ===
    admin_mercadotecnia = db.Column("ADMINISTRACION Y MERCADOTECNIA", db.Float, nullable=True)
    bases_datos_i = db.Column("BASES DE DATOS I", db.Float, nullable=True)
    bases_datos_ii = db.Column("BASES DE DATOS II", db.Float, nullable=True)
    computacion_i = db.Column("COMPUTACION I", db.Float, nullable=True)
    computacion_ii = db.Column("COMPUTACION II", db.Float, nullable=True)
    computacion_iii = db.Column("COMPUTACION III", db.Float, nullable=True)
    contabilidad_i = db.Column("CONTABILIDAD I", db.Float, nullable=True)
    calculo_i = db.Column("CALCULO I", db.Float, nullable=True)
    calculo_ii = db.Column("CALCULO II", db.Float, nullable=True)
    calculo_iii = db.Column("CALCULO III", db.Float, nullable=True)
    derecho_laboral = db.Column("DERECHO INTELECTUAL Y LABORAL", db.Float, nullable=True)
    diseno_sistemas = db.Column("DISENO DE SISTEMA INFORMATICO I", db.Float, nullable=True)
    diseno_tecnico = db.Column("DISENO TECNICO", db.Float, nullable=True)
    electronica_i = db.Column("ELECTRONICA I", db.Float, nullable=True)
    emprendedorismo = db.Column("EMPRENDEDORISMO", db.Float, nullable=True)
    estructura_datos_i = db.Column("ESTRUCTURA DE DATOS I", db.Float, nullable=True)
    estructuras_lenguajes = db.Column("ESTRUCTURAS DE LOS LENGUAJES", db.Float, nullable=True)

    eventos_deportes_i = db.Column("EVENTOS Y DEPORTES I", db.Float, nullable=True)
    eventos_deportes_ii = db.Column("EVENTOS Y DEPORTES II", db.Float, nullable=True)
    eventos_deportes_iii = db.Column("EVENTOS Y DEPORTES III", db.Float, nullable=True)
    eventos_deportes_iv = db.Column("EVENTOS Y DEPORTES IV", db.Float, nullable=True)
    eventos_deportes_v = db.Column("EVENTOS Y DEPORTES V", db.Float, nullable=True)
    eventos_deportes_vi = db.Column("EVENTOS Y DEPORTES VI", db.Float, nullable=True)

    expresion_oral = db.Column("EXPRESION ORAL Y ESCRITA", db.Float, nullable=True)

    fisica_i = db.Column("FISICA I", db.Float, nullable=True)
    fisica_ii = db.Column("FISICA II", db.Float, nullable=True)
    fisica_iii = db.Column("FISICA III", db.Float, nullable=True)

    geometria_analitica = db.Column("GEOMETRIA ANALITICA Y VECTORIAL", db.Float, nullable=True)
    idiomas_i = db.Column("IDIOMAS I", db.Float, nullable=True)
    informatica_i = db.Column("INFORMATICA I", db.Float, nullable=True)

    ingenieria_software_i = db.Column("INGENIERIA DE SOFTWARE I", db.Float, nullable=True)

    ingles_ii = db.Column("INGLES II", db.Float, nullable=True)
    ingles_iii = db.Column("INGLES III", db.Float, nullable=True)
    ingles_i = db.Column("INGLES I", db.Float, nullable=True)

    investigacion_operaciones = db.Column("INVESTIGACION DE OPERACIONES I", db.Float, nullable=True)

    laboratorio_idiomas_i = db.Column("LABORATORIO DE IDIOMAS I", db.Float, nullable=True)
    laboratorio_i = db.Column("LABORATORIO I", db.Float, nullable=True)

    lenguaje_programacion_i = db.Column("LENGUAJE DE PROGRAMACION I", db.Float, nullable=True)
    lenguaje_programacion_ii = db.Column("LENGUAJE DE PROGRAMACION II", db.Float, nullable=True)
    lenguaje_programacion_iv = db.Column("LENGUAJE DE PROGRAMACION IV", db.Float, nullable=True)
    lenguajes_programacion_iii = db.Column("LENGUAJES DE PROGRAMACION III", db.Float, nullable=True)

    matematica_aplicada = db.Column("MATEMATICA APLICADA", db.Float, nullable=True)

    metodologia_investigacion_i = db.Column("METODOLOGIA DE LA INVESTIGACION I", db.Float, nullable=True)

    metodos_numericos = db.Column("METODOS NUMERICOS", db.Float, nullable=True)

    probabilidades_estadisticas = db.Column("PROBABILIDADES Y ESTADISTICAS", db.Float, nullable=True)

    quimica = db.Column("QUIMICA", db.Float, nullable=True)

    redes_i = db.Column("REDES DE COMPUTADORAS I", db.Float, nullable=True)
    redes_ii = db.Column("REDES DE COMPUTADORAS II", db.Float, nullable=True)

    sis_op_i = db.Column("SISTEMAS OPERATIVOS I", db.Float, nullable=True)
    sis_op_ii = db.Column("SISTEMAS OPERATIVOS II", db.Float, nullable=True)

    taller_hw_i = db.Column("TALLER DE HARDWARE I", db.Float, nullable=True)
    taller_hw_ii = db.Column("TALLER DE HARDWARE II", db.Float, nullable=True)

    algebra_i = db.Column("ALGEBRA I", db.Float, nullable=True)
    algebra_ii = db.Column("ALGEBRA II", db.Float, nullable=True)

    etica_profesional = db.Column("ETICA PROFESIONAL", db.Float, nullable=True)

    def __repr__(self):
        return f"<Informatica {self.id_alumno}>"
