# src/models/datos_electronica_models.py
from src.configs.extensions import db


class DatosElectronicaDesercion(db.Model):
    __tablename__ = "datos_electronica_desercion"

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

    # === MATERIAS (nombres de columna EXACTOS como en el CSV) ===
    admin_mercadotecnia = db.Column("ADMINISTRACION Y MERCADOTECNIA", db.Float, nullable=True)
    algebra_i = db.Column("ALGEBRA I", db.Float, nullable=True)
    automatizacion_industrial = db.Column("AUTOMATIZACION INDUSTRIAL", db.Float, nullable=True)
    circuitos_electricos_i = db.Column("CIRCUITOS ELECTRICOS I", db.Float, nullable=True)
    circuitos_electricos_ii = db.Column("CIRCUITOS ELECTRICOS II", db.Float, nullable=True)
    computacion_ii = db.Column("COMPUTACION II", db.Float, nullable=True)
    computacion_i = db.Column("COMPUTACION I", db.Float, nullable=True)

    calculo_i = db.Column("CALCULO I", db.Float, nullable=True)
    calculo_ii = db.Column("CALCULO II", db.Float, nullable=True)
    calculo_iii = db.Column("CALCULO III", db.Float, nullable=True)
    calculo_iv = db.Column("CALCULO IV", db.Float, nullable=True)
    calculo_v = db.Column("CALCULO V", db.Float, nullable=True)

    diseno_asistido_pc = db.Column("DISENO ASISTIDO POR COMPUTADORA", db.Float, nullable=True)
    diseno_tecnico = db.Column("DISENO TECNICO", db.Float, nullable=True)

    electrotecnia_i = db.Column("ELECTROTECNIA I", db.Float, nullable=True)
    electrotecnia_ii = db.Column("ELECTROTECNIA II", db.Float, nullable=True)

    electronica_digital_ii = db.Column("ELECTRONICA  DIGITAL II", db.Float, nullable=True)  # doble espacio
    electronica_potencia_i = db.Column("ELECTRONICA DE POTENCIA I", db.Float, nullable=True)
    electronica_potencia_ii = db.Column("ELECTRONICA DE POTENCIA II", db.Float, nullable=True)
    electronica_digital_i = db.Column("ELECTRONICA DIGITAL I", db.Float, nullable=True)

    electronica_i = db.Column("ELECTRONICA I", db.Float, nullable=True)
    electronica_ii = db.Column("ELECTRONICA II", db.Float, nullable=True)
    electronica_iii = db.Column("ELECTRONICA III", db.Float, nullable=True)
    electronica_industrial = db.Column("ELECTRONICA INDUSTRIAL", db.Float, nullable=True)

    emprendedorismo = db.Column("EMPRENDEDORISMO", db.Float, nullable=True)

    eventos_deportes_i = db.Column("EVENTOS Y DEPORTES I", db.Float, nullable=True)
    eventos_deportes_ii = db.Column("EVENTOS Y DEPORTES II", db.Float, nullable=True)
    eventos_deportes_iii = db.Column("EVENTOS Y DEPORTES III", db.Float, nullable=True)
    eventos_deportes_iv = db.Column("EVENTOS Y DEPORTES IV", db.Float, nullable=True)
    eventos_deportes_v = db.Column("EVENTOS Y DEPORTES V", db.Float, nullable=True)
    eventos_deportes_vi = db.Column("EVENTOS Y DEPORTES VI", db.Float, nullable=True)

    expresion_oral = db.Column("EXPRESION ORAL Y ESCRITA", db.Float, nullable=True)

    fund_control_auto_ii = db.Column("FUNDAMENTOS DE CONTROL  AUTOMATIZADO II", db.Float, nullable=True)  # doble espacio
    fund_control_auto_i = db.Column("FUNDAMENTOS DE CONTROL AUTOMATIZADO I", db.Float, nullable=True)

    fisica_i = db.Column("FISICA I", db.Float, nullable=True)
    fisica_ii = db.Column("FISICA II", db.Float, nullable=True)
    fisica_iii = db.Column("FISICA III", db.Float, nullable=True)
    fisica_iv = db.Column("FISICA IV", db.Float, nullable=True)
    fisica_v = db.Column("FISICA V", db.Float, nullable=True)
    fisica_vi = db.Column("FISICA VI", db.Float, nullable=True)

    geometria_analitica = db.Column("GEOMETRIA ANALITICA", db.Float, nullable=True)

    idiomas_i = db.Column("IDIOMAS I", db.Float, nullable=True)

    ingles_i = db.Column("INGLES I", db.Float, nullable=True)
    ingles_ii = db.Column("INGLES II", db.Float, nullable=True)
    ingles_iii = db.Column("INGLES III", db.Float, nullable=True)

    instalaciones_electricas_i = db.Column("INSTALACIONES ELECTRICAS I", db.Float, nullable=True)

    laboratorio_idiomas_i = db.Column("LABORATORIO DE IDIOMAS I", db.Float, nullable=True)

    medicion_instrumentacion = db.Column("MEDICION E INSTRUMENTACION", db.Float, nullable=True)

    metodologia_investigacion_i = db.Column("METODOLOGIA DE LA INVESTIGACION I", db.Float, nullable=True)

    microcontroladores = db.Column("MICROCONTROLADORES", db.Float, nullable=True)

    probabilidades_estadisticas = db.Column("PROBABILIDADES Y ESTADISTICAS", db.Float, nullable=True)

    programacion_lenguaje_computadoras = db.Column(
        "PROGRAMACION EN LENGUAJE DE COMPUTADORAS", db.Float, nullable=True
    )

    quimica = db.Column("QUIMICA", db.Float, nullable=True)

    seguridad_higiene_laboral = db.Column("SEGURIDAD E HIGIENE LABORAL", db.Float, nullable=True)

    simulacion_circuitos_pc = db.Column("SIMULACION DE CIRCUITOS POR COMPUTADORA", db.Float, nullable=True)

    algebra_ii = db.Column("ALGEBRA II", db.Float, nullable=True)

    etica_profesional = db.Column("ETICA PROFESIONAL", db.Float, nullable=True)

    def __repr__(self):
        return f"<Electronica {self.id_alumno}>"
