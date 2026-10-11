import json
from pathlib import Path

import pandas as pd
import pytest

from sleep_app import cli

RUTA_DATASET = Path(__file__).resolve().parents[2] / "data" / "bedtime_screentime_sleep_debt.csv"


def test_parse_args():
    args = cli.parse_args(["--input", "datos.csv", "--output-dir", "salida"])
    assert args.input == Path("datos.csv")
    assert args.output_dir == Path("salida")


def test_cli_genera_los_tres_ficheros(tmp_path, registros_validos, crear_registro):
    entrada = tmp_path / "sueno.csv"
    con_un_error = pd.concat([registros_validos, pd.DataFrame([crear_registro("USR-00009", age=5)])])
    con_un_error.to_csv(entrada, index=False)
    salida = tmp_path / "out"

    codigo = cli.main(["--input", str(entrada), "--output-dir", str(salida)])

    assert codigo == 0
    metricas = json.loads((salida / "metricas.json").read_text(encoding="utf-8"))
    assert metricas["registros_validos"] == 4
    assert metricas["registros_invalidos"] == 1
    invalidos = pd.read_csv(salida / "registros_invalidos.csv")
    assert invalidos["motivo"].tolist() == ["age fuera de rango"]


def test_cli_fichero_inexistente_devuelve_2(tmp_path):
    codigo = cli.main(["--input", str(tmp_path / "no_existe.csv"), "--output-dir", str(tmp_path)])
    assert codigo == 2


@pytest.mark.integration
def test_dataset_real_8500_validos(tmp_path):
    codigo = cli.main(["--input", str(RUTA_DATASET), "--output-dir", str(tmp_path)])

    metricas = json.loads((tmp_path / "metricas.json").read_text(encoding="utf-8"))
    assert codigo == 0
    assert metricas["registros_totales"] == 8500
    assert metricas["registros_validos"] == 8500
    assert metricas["registros_invalidos"] == 0
