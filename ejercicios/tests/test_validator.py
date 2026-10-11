import pandas as pd
import pytest

from ejercicios.ventas_app.validator import ValidationError, validar_ventas


def test_validar_ventas_cuenta_validos_e_invalidos(ventas_mini):
    validos, errores = validar_ventas(ventas_mini)
    assert len(validos) == 1
    assert len(errores) == 2


def test_validar_ventas_calcula_importe(ventas_mini):
    validos, _ = validar_ventas(ventas_mini)
    assert validos["importe"].iloc[0] == 20.0


def test_validar_ventas_no_modifica_el_original(ventas_mini):
    validar_ventas(ventas_mini)
    assert "importe" not in ventas_mini.columns


@pytest.mark.parametrize("precio, num_validos", [(0, 0), (-1, 0), (1, 1)])
def test_validar_ventas_precio(precio, num_validos):
    df = pd.DataFrame({
        "fecha": ["2026-01-01"],
        "region": ["Norte"],
        "producto": ["A"],
        "unidades": [1],
        "precio_unitario": [precio],
        "cliente_id": ["C1"],
    })
    validos, errores = validar_ventas(df)
    assert len(validos) == num_validos
    assert len(errores) == 1 - num_validos


def test_validar_ventas_unidades_texto_va_a_errores(ventas_mini):
    ventas_mini["unidades"] = ["2", "na", "5"]
    validos, errores = validar_ventas(ventas_mini)
    assert len(errores) == 2


def test_validar_ventas_sin_columnas_lanza_error():
    df = pd.DataFrame({"unidades": [1], "precio_unitario": [10.0]})
    with pytest.raises(ValidationError):
        validar_ventas(df)
