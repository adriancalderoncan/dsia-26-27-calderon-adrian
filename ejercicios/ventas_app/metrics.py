import pandas as pd

TOP_PRODUCTOS = 3


def importe_por_region(validos: pd.DataFrame) -> pd.Series:
    return validos.groupby("region")["importe"].sum().sort_values(ascending=False)


def top_productos(validos: pd.DataFrame, n: int = TOP_PRODUCTOS) -> pd.Series:
    return validos.groupby("producto")["importe"].sum().sort_values(ascending=False).head(n)


def clientes_repetidos(validos: pd.DataFrame) -> pd.Series:
    compras = validos["cliente_id"].value_counts()
    return compras[compras > 1]
