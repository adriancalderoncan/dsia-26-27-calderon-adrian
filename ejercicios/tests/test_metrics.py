from ejercicios.ventas_app.metrics import clientes_repetidos, importe_por_region, top_productos
from ejercicios.ventas_app.validator import validar_ventas


def test_importe_por_region(ventas_mini):
    validos, _ = validar_ventas(ventas_mini)
    resultado = importe_por_region(validos)
    assert resultado["Norte"] == 20.0


def test_top_productos_devuelve_como_maximo_n(ventas_mini):
    ventas_mini["precio_unitario"] = [10.0, 20.0, 5.0]
    ventas_mini["unidades"] = [2, 1, 5]
    validos, _ = validar_ventas(ventas_mini)
    resultado = top_productos(validos, n=1)
    assert len(resultado) == 1
    assert resultado.index[0] == "A"


def test_clientes_repetidos(ventas_mini):
    ventas_mini["precio_unitario"] = [10.0, 20.0, 5.0]
    ventas_mini["unidades"] = [2, 1, 5]
    validos, _ = validar_ventas(ventas_mini)
    resultado = clientes_repetidos(validos)
    assert list(resultado.index) == ["C1"]
