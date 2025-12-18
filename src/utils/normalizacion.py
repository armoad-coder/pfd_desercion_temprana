import numpy as np
import re
import pandas as pd

def limpiar_numero(valor):
    """Convierte un valor a float nativo de Python o None."""
    
    if valor is None:
        return None

    # Si es numpy → convertir a float Python
    if isinstance(valor, (np.floating, np.integer)):
        return float(valor)

    # Convertir a string
    s = str(valor).strip()

    if s.lower() in ["nan", "none", "", "-", "null"]:
        return None

    # Remover todo excepto números, puntos o comas
    s = re.sub(r"[^0-9\.,]", "", s)

    # Si hay más de un punto → eran separadores de miles
    if s.count('.') > 1:
        s = s.replace('.', '')

    # Convertir coma decimal a punto
    s = s.replace(",", ".")

    try:
        return float(s)
    except:
        return None


def normalizar_dataframe(df):
    """Normaliza todas las columnas numéricas a float Python."""
    
    for col in df.columns:
        # Convertir la columna a string primero
        df[col] = df[col].astype(str).str.strip()

        # Limpiar
        df[col] = df[col].apply(limpiar_numero)

        # Intentar convertir a float
        try:
            df[col] = df[col].astype(float)
        except:
            # Columnas no numéricas se quedan como texto/None
            pass

        # Asegurar que no quede nada numpy
        df[col] = df[col].apply(
            lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else x
        )

    return df
