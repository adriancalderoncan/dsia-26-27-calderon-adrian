import json
import sys
from pathlib import Path

import pytest

from ejercicios.ventas_app import cli

RUTA_VENTAS = Path(__file__).resolve().parents[2] / "Datos" / "ventas.csv"


def test_cli_genera_csv_y_json(tmp_path, monkeypatch, ventas_mini):
    entrada = tmp_path / "ventas.csv"
    ventas_mini.to_csv(entrada, index=False)
    salida = tmp_path / "limpias.csv"
    monkeypatch.setattr(sys, "argv", ["cli", "--input", str(entrada), "--output", str(salida)])

    cli.main()

    assert salida.exists()
    calidad = json.loads((tmp_path / "calidad_datos.json").read_text(encoding="utf-8"))
    assert calidad["filas_validas"] == 1
    assert calidad["filas_invalidas"] == 2


def test_cli_fichero_inexistente_sale_con_error(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["cli", "--input", "no_existe.csv", "--output", str(tmp_path / "x.csv")])
    with pytest.raises(SystemExit):
        cli.main()


@pytest.mark.integration
def test_csv_curso_tiene_140_validas_y_10_invalidas(tmp_path, monkeypatch):
    salida = tmp_path / "limpias.csv"
    monkeypatch.setattr(sys, "argv", ["cli", "--input", str(RUTA_VENTAS), "--output", str(salida)])

    cli.main()

    calidad = json.loads((tmp_path / "calidad_datos.json").read_text(encoding="utf-8"))
    assert calidad["filas_validas"] == 140
    assert calidad["filas_invalidas"] == 10
