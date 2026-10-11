from pathlib import Path

import pytest

from ejercicios.ventas_app.loader import DataLoadError, load


def test_load_path_inexistente_lanza_dataloaderror():
    with pytest.raises(DataLoadError):
        load(Path("no_existe.csv"))


def test_load_csv(tmp_path):
    fichero = tmp_path / "mini.csv"
    fichero.write_text("unidades,precio_unitario\n1,10\n2,20\n", encoding="utf-8")
    df = load(fichero)
    assert len(df) == 2


def test_load_json(tmp_path):
    fichero = tmp_path / "mini.json"
    fichero.write_text('[{"unidades": 1, "precio_unitario": 10}]', encoding="utf-8")
    df = load(fichero)
    assert len(df) == 1
    assert df["unidades"].iloc[0] == 1
