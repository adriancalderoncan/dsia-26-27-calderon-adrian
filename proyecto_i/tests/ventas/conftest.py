import pandas as pd
import pytest


@pytest.fixture
def ventas_mini():
    """3 ventas: una valida, una sin unidades y otra con precio negativo."""
    return pd.DataFrame({
        "fecha": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "region": ["Norte", "Sur", "Norte"],
        "producto": ["A", "B", "A"],
        "unidades": [2, None, 5],
        "precio_unitario": [10.0, 20.0, -1.0],
        "cliente_id": ["C1", "C2", "C1"],
    })


@pytest.fixture
def ventas_validas():
    """4 ventas todas validas para probar las metricas."""
    return pd.DataFrame({
        "fecha": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "region": ["Norte", "Sur", "Norte", "Este"],
        "producto": ["A", "B", "A", "C"],
        "unidades": [2, 1, 5, 1],
        "precio_unitario": [10.0, 20.0, 5.0, 3.0],
        "cliente_id": ["C1", "C2", "C1", "C3"],
    })
