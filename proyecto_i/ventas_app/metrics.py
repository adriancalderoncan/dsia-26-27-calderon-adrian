"""Métricas de negocio sobre las ventas válidas."""

import pandas as pd

TOP_PRODUCTOS = 3


def importe_por_region(validos: pd.DataFrame) -> pd.Series:
    """Importe total por región, de mayor a menor."""
    return validos.groupby("region")["importe"].sum().sort_values(ascending=False)


def top_productos(validos: pd.DataFrame, n: int = TOP_PRODUCTOS) -> pd.Series:
    """Los n productos con más importe."""
    return validos.groupby("producto")["importe"].sum().sort_values(ascending=False).head(n)


def clientes_repetidos(validos: pd.DataFrame) -> pd.Series:
    """Clientes con más de una compra y cuántas han hecho."""
    compras = validos["cliente_id"].value_counts()
    return compras[compras > 1]
