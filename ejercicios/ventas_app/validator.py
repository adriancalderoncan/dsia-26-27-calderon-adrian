import pandas as pd

COLUMNAS_OBLIGATORIAS = ["fecha", "region", "producto", "unidades", "precio_unitario", "cliente_id"]


class ValidationError(Exception):
    pass


def validar_ventas(ventas: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    faltan = [col for col in COLUMNAS_OBLIGATORIAS if col not in ventas.columns]
    if faltan:
        raise ValidationError(f"Faltan columnas: {faltan}")

    ventas = ventas.copy()
    ventas["unidades"] = pd.to_numeric(ventas["unidades"], errors="coerce")
    ventas["precio_unitario"] = pd.to_numeric(ventas["precio_unitario"], errors="coerce")

    es_valida = (ventas["unidades"] > 0) & (ventas["precio_unitario"] > 0)

    validos = ventas[es_valida].copy()
    errores = ventas[~es_valida].copy()
    validos["importe"] = validos["unidades"] * validos["precio_unitario"]
    return validos, errores
