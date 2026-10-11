from ventas_app.metrics import clientes_repetidos, importe_por_region, top_productos
from ventas_app.validator import validar_ventas


def test_importe_por_region(ventas_validas):
    validos, _ = validar_ventas(ventas_validas)

    resultado = importe_por_region(validos)

    # Norte: 2*10 + 5*5 = 45, Sur: 20, Este: 3
    assert resultado.to_dict() == {"Norte": 45.0, "Sur": 20.0, "Este": 3.0}
    assert list(resultado.index) == ["Norte", "Sur", "Este"]


def test_top_productos(ventas_validas):
    validos, _ = validar_ventas(ventas_validas)

    resultado = top_productos(validos, n=2)

    assert list(resultado.index) == ["A", "B"]
    assert resultado["A"] == 45.0


def test_clientes_repetidos(ventas_validas):
    validos, _ = validar_ventas(ventas_validas)

    resultado = clientes_repetidos(validos)

    assert resultado.to_dict() == {"C1": 2}
