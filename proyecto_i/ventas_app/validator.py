"""Reglas de calidad de las ventas: separa filas válidas e inválidas."""

import pandas as pd

COLUMNAS_OBLIGATORIAS = ["fecha", "region", "producto", "unidades", "precio_unitario", "cliente_id"]


class ValidationError(Exception):
    """Los datos no tienen la estructura que se espera."""


def validar_ventas(ventas: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa las ventas en (validos, errores).

    Una fila es válida si unidades y precio_unitario son numéricos y mayores
    que 0. A las válidas se les añade la columna importe. No modifica el
    DataFrame original.

    Lanza ValidationError si falta alguna columna obligatoria.
    """
    faltan = [col for col in COLUMNAS_OBLIGATORIAS if col not in ventas.columns]
    if faltan:
        raise ValidationError(f"Faltan columnas: {faltan}")

    ventas = ventas.copy()
    ventas["unidades"] = pd.to_numeric(ventas["unidades"], errors="coerce")
    ventas["precio_unitario"] = pd.to_numeric(ventas["precio_unitario"], errors="coerce")

    # NaN > 0 da False, asi que los nulos tambien van a errores
    es_valida = (ventas["unidades"] > 0) & (ventas["precio_unitario"] > 0)

    validos = ventas[es_valida].copy()
    errores = ventas[~es_valida].copy()
    validos["importe"] = validos["unidades"] * validos["precio_unitario"]
    return validos, errores
