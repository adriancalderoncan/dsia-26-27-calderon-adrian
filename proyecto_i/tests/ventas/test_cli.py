import json
from pathlib import Path

import pytest

from ventas_app import cli

RUTA_VENTAS = Path(__file__).resolve().parents[2] / "data" / "ventas.csv"


def test_parse_args():
    args = cli.parse_args(["--input", "a.csv", "--output", "b.csv"])
    assert args.input == Path("a.csv")
    assert args.output == Path("b.csv")


def test_cli_genera_csv_y_json(tmp_path, ventas_mini):
    entrada = tmp_path / "ventas.csv"
    ventas_mini.to_csv(entrada, index=False)
    salida = tmp_path / "out" / "limpias.csv"

    codigo = cli.main(["--input", str(entrada), "--output", str(salida)])

    assert codigo == 0
    assert salida.exists()
    calidad = json.loads((salida.parent / "calidad_datos.json").read_text(encoding="utf-8"))
    assert calidad["filas_validas"] == 1
    assert calidad["filas_invalidas"] == 2


def test_cli_fichero_inexistente_devuelve_2(tmp_path):
    codigo = cli.main(["--input", str(tmp_path / "no_existe.csv"), "--output", str(tmp_path / "x.csv")])
    assert codigo == 2


@pytest.mark.integration
def test_csv_curso_tiene_140_validas_y_10_invalidas(tmp_path):
    salida = tmp_path / "limpias.csv"

    codigo = cli.main(["--input", str(RUTA_VENTAS), "--output", str(salida)])

    calidad = json.loads((tmp_path / "calidad_datos.json").read_text(encoding="utf-8"))
    assert codigo == 0
    assert calidad["filas_validas"] == 140
    assert calidad["filas_invalidas"] == 10
