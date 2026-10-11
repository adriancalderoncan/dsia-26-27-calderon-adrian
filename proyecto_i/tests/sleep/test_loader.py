import pytest

from sleep_app.loader import DataLoadError, load


def test_load_csv(tmp_path, registros_validos):
    fichero = tmp_path / "sueno.csv"
    registros_validos.to_csv(fichero, index=False)

    df = load(fichero)

    assert len(df) == 4
    assert "total_sleep_hours" in df.columns


def test_load_path_inexistente_lanza_dataloaderror(tmp_path):
    with pytest.raises(DataLoadError, match="No existe"):
        load(tmp_path / "no_existe.csv")


def test_load_extension_no_csv_lanza_dataloaderror(tmp_path):
    fichero = tmp_path / "sueno.json"
    fichero.write_text("[]", encoding="utf-8")
    with pytest.raises(DataLoadError, match="csv"):
        load(fichero)


def test_load_fichero_vacio_lanza_dataloaderror(tmp_path):
    fichero = tmp_path / "vacio.csv"
    fichero.write_text("", encoding="utf-8")
    with pytest.raises(DataLoadError, match="vacío"):
        load(fichero)
