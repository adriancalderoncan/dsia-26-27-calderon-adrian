from pathlib import Path

import pytest

from ventas_app.loader import DataLoadError, load


def test_load_csv(tmp_path):
    fichero = tmp_path / "mini.csv"
    fichero.write_text("unidades,precio_unitario\n1,10\n2,20\n", encoding="utf-8")

    df = load(fichero)

    assert len(df) == 2
    assert list(df.columns) == ["unidades", "precio_unitario"]


def test_load_json(tmp_path):
    fichero = tmp_path / "mini.json"
    fichero.write_text('[{"unidades": 1, "precio_unitario": 10}]', encoding="utf-8")

    df = load(fichero)

    assert len(df) == 1


@pytest.mark.parametrize("nombre", ["no_existe.csv", "no_existe.json"])
def test_load_path_inexistente_lanza_dataloaderror(tmp_path, nombre):
    with pytest.raises(DataLoadError):
        load(tmp_path / nombre)
