import json

import pytest

from ejercicios import check_metrics, pipeline_ventas
from ejercicios.pipeline_ventas import transform


def test_transform_report_cuenta_filas(ventas_mini):
    validos, report = transform(ventas_mini)
    assert report["rows_in"] == 3
    assert report["rows_out"] == 1
    assert report["rows_dropped"] == 2
    assert report["error_rate"] == round(2 / 3, 4)


def test_pipeline_ok_devuelve_0_y_guarda_artefactos(tmp_path, ventas_mini):
    entrada = tmp_path / "ventas.csv"
    ventas_mini.to_csv(entrada, index=False)
    salida = tmp_path / "out"

    codigo = pipeline_ventas.main(["--input", str(entrada), "--output-dir", str(salida), "--max-error-rate", "0.9"])

    assert codigo == 0
    assert (salida / "ventas_limpias.csv").exists()
    assert (salida / "metrics.json").exists()
    assert (salida / "run.log").exists()


def test_pipeline_gate_devuelve_1(tmp_path, ventas_mini):
    entrada = tmp_path / "ventas.csv"
    ventas_mini.to_csv(entrada, index=False)
    salida = tmp_path / "out"

    codigo = pipeline_ventas.main(["--input", str(entrada), "--output-dir", str(salida), "--max-error-rate", "0.5"])

    assert codigo == 1
    assert not (salida / "ventas_limpias.csv").exists()


def test_pipeline_fichero_inexistente_devuelve_2(tmp_path):
    codigo = pipeline_ventas.main(["--input", "no_existe.csv", "--output-dir", str(tmp_path)])
    assert codigo == 2


def test_pipeline_es_idempotente(tmp_path, ventas_mini):
    entrada = tmp_path / "ventas.csv"
    ventas_mini.to_csv(entrada, index=False)
    salida = tmp_path / "out"
    argumentos = ["--input", str(entrada), "--output-dir", str(salida), "--max-error-rate", "0.9"]

    pipeline_ventas.main(argumentos)
    primera = (salida / "metrics.json").read_text(encoding="utf-8")
    pipeline_ventas.main(argumentos)

    assert (salida / "metrics.json").read_text(encoding="utf-8") == primera
    assert sorted(f.name for f in salida.iterdir()) == ["metrics.json", "run.log", "ventas_limpias.csv"]


@pytest.mark.parametrize("error_rate, esperado", [(0.05, 0), (0.2, 1)])
def test_check_metrics(tmp_path, error_rate, esperado):
    metrics = tmp_path / "metrics.json"
    metrics.write_text(json.dumps({"error_rate": error_rate, "rows_out": 140}), encoding="utf-8")
    assert check_metrics.main(["--metrics", str(metrics), "--max-error-rate", "0.1"]) == esperado
