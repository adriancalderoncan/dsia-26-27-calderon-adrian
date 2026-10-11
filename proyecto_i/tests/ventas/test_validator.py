import pandas as pd
import pytest

from ventas_app.validator import ValidationError, validar_ventas


def venta(unidades, precio):
    return pd.DataFrame({
        "fecha": ["2026-01-01"], "region": ["Norte"], "producto": ["A"],
        "unidades": [unidades], "precio_unitario": [precio], "cliente_id": ["C1"],
    })


def test_validar_ventas_cuenta_validos_e_invalidos(ventas_mini):
    # Arrange: los datos vienen de la fixture ventas_mini
    # Act
    validos, errores = validar_ventas(ventas_mini)
    # Assert
    assert len(validos) == 1
    assert len(errores) == 2


def test_validar_ventas_calcula_importe(ventas_mini):
    validos, _ = validar_ventas(ventas_mini)
    assert validos["importe"].iloc[0] == 20.0


def test_validar_ventas_no_modifica_el_original(ventas_mini):
    validar_ventas(ventas_mini)
    assert "importe" not in ventas_mini.columns


@pytest.mark.parametrize("precio, es_valida", [(0, False), (-1, False), (None, False), (1, True)])
def test_validar_ventas_precio(precio, es_valida):
    validos, errores = validar_ventas(venta(1, precio))
    assert len(validos) == int(es_valida)
    assert len(errores) == int(not es_valida)


@pytest.mark.parametrize("unidades", [0, -2, None, "na"])
def test_validar_ventas_unidades_no_validas(unidades):
    validos, errores = validar_ventas(venta(unidades, 10.0))
    assert len(validos) == 0
    assert len(errores) == 1


def test_validar_ventas_sin_columnas_lanza_error():
    with pytest.raises(ValidationError):
        validar_ventas(pd.DataFrame({"unidades": [1], "precio_unitario": [10.0]}))
