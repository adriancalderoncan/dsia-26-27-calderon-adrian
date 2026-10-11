"""E4 - Pipeline de ventas como job: csv -> limpieza -> metrics.json + run.log"""

import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd

from ejercicios.ventas_app.loader import DataLoadError, load
from ejercicios.ventas_app.validator import ValidationError, validar_ventas

EXIT_OK = 0
EXIT_DATOS_MALOS = 1
EXIT_ENTRADA_ROTA = 2


def preparar_logger(log_file: Path) -> logging.Logger:
    logger = logging.getLogger("pipeline_ventas")
    for handler in logger.handlers:
        handler.close()
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    consola = logging.StreamHandler()
    consola.setFormatter(formato)
    logger.addHandler(consola)

    log_file.parent.mkdir(parents=True, exist_ok=True)
    fichero = logging.FileHandler(log_file, encoding="utf-8")
    fichero.setFormatter(formato)
    logger.addHandler(fichero)
    return logger


def transform(ventas: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    # no lee ni escribe nada, solo calcula (asi se puede testear sin disco)
    validos, errores = validar_ventas(ventas)
    filas = len(ventas)
    report = {
        "rows_in": filas,
        "rows_out": len(validos),
        "rows_dropped": len(errores),
        "importe_total": round(float(validos["importe"].sum()), 2),
        "error_rate": round(len(errores) / filas, 4) if filas else 0.0,
    }
    return validos, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pipeline de ventas")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-error-rate", type=float, default=0.5,
                        help="si el error_rate es mayor se aborta con exit 1")
    args = parser.parse_args(argv)

    logger = preparar_logger(args.output_dir / "run.log")
    logger.info("Inicio: input=%s output-dir=%s max-error-rate=%s",
                args.input, args.output_dir, args.max_error_rate)

    try:
        ventas = load(args.input)
        validos, report = transform(ventas)
    except (DataLoadError, ValidationError) as e:
        logger.error("Entrada no valida: %s", e)
        return EXIT_ENTRADA_ROTA

    logger.info("Metricas: %s", report)

    # se guarda metrics.json siempre para poder ver por que ha fallado
    metrics_path = args.output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if report["error_rate"] > args.max_error_rate:
        logger.error("error_rate %.3f > %.3f, abortando sin guardar las ventas limpias",
                     report["error_rate"], args.max_error_rate)
        return EXIT_DATOS_MALOS

    validos.to_csv(args.output_dir / "ventas_limpias.csv", index=False)
    logger.info("Guardado en %s", args.output_dir)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
