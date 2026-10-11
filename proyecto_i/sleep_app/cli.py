"""Punto de entrada de la Parte B.

Uso (desde la carpeta proyecto_i):
    python -m sleep_app.cli --input data/bedtime_screentime_sleep_debt.csv --output-dir salida/sleep
"""

import argparse
import json
import logging
from pathlib import Path

import pandas as pd

from .loader import DataLoadError, load
from .metrics import (horas_por_cronotipo, latencia_por_filtro_luz_azul, reparto_deuda_sueno,
                      sueno_por_app, sueno_por_tramo_movil)
from .validator import ValidationError, validar_registros

logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Lee los argumentos de la linea de comandos (argv se usa en los tests)."""
    parser = argparse.ArgumentParser(description="Valida el dataset de sueño y calcula métricas")
    parser.add_argument("--input", required=True, type=Path, help="csv del dataset de sueño")
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="carpeta donde se guardan los registros validos, los invalidos y las metricas")
    return parser.parse_args(argv)


def calcular_metricas(validos: pd.DataFrame, errores: pd.DataFrame) -> dict:
    """Junta todas las métricas en un diccionario que se puede guardar como json."""
    return {
        "registros_totales": len(validos) + len(errores),
        "registros_validos": len(validos),
        "registros_invalidos": len(errores),
        "sueno_por_tramo_movil": sueno_por_tramo_movil(validos).to_dict(orient="index"),
        "sueno_por_app": sueno_por_app(validos).to_dict(orient="index"),
        "horas_por_cronotipo": horas_por_cronotipo(validos).to_dict(),
        "reparto_deuda_sueno_pct": reparto_deuda_sueno(validos).to_dict(),
        "latencia_por_filtro_luz_azul": latencia_por_filtro_luz_azul(validos).to_dict(),
    }


def main(argv: list[str] | None = None) -> int:
    """Carga, valida, calcula las métricas y guarda los resultados.

    Devuelve 0 si todo va bien y 2 si la entrada no se puede usar.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args(argv)

    try:
        registros = load(args.input)
        validos, errores = validar_registros(registros)
    except (DataLoadError, ValidationError) as e:
        logger.error(e)
        return 2

    logger.info("Registros validos: %d | invalidos: %d", len(validos), len(errores))
    if len(errores):
        logger.info("Motivos de descarte:\n%s", errores["motivo"].value_counts().to_string())
    logger.info("Sueno segun minutos de movil:\n%s", sueno_por_tramo_movil(validos).to_string())

    metricas = calcular_metricas(validos, errores)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    validos.to_csv(args.output_dir / "registros_validos.csv", index=False)
    errores.to_csv(args.output_dir / "registros_invalidos.csv", index=False)
    (args.output_dir / "metricas.json").write_text(
        json.dumps(metricas, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info("Resultados guardados en %s", args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
