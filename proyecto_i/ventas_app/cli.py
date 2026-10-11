"""Punto de entrada de la Parte A.

Uso (desde la carpeta proyecto_i):
    python -m ventas_app.cli --input data/ventas.csv --output salida/ventas_limpias.csv
"""

import argparse
import json
import logging
from pathlib import Path

from .loader import DataLoadError, load
from .metrics import clientes_repetidos, importe_por_region, top_productos
from .validator import ValidationError, validar_ventas

logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Lee los argumentos de la linea de comandos (argv se usa en los tests)."""
    parser = argparse.ArgumentParser(description="Limpia y resume el fichero de ventas")
    parser.add_argument("--input", required=True, type=Path, help="csv o json de ventas")
    parser.add_argument("--output", required=True, type=Path, help="csv donde guardar las ventas validas")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Carga, valida, calcula las métricas y guarda los resultados.

    Devuelve 0 si todo va bien y 2 si la entrada no se puede usar.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args(argv)

    try:
        ventas = load(args.input)
        validos, errores = validar_ventas(ventas)
    except (DataLoadError, ValidationError) as e:
        logger.error(e)
        return 2

    logger.info("Filas validas: %d | invalidas: %d", len(validos), len(errores))
    logger.info("Importe por region:\n%s", importe_por_region(validos).to_string())
    logger.info("Top productos:\n%s", top_productos(validos).to_string())
    logger.info("Clientes con mas de una compra: %d", len(clientes_repetidos(validos)))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    validos.to_csv(args.output, index=False)

    calidad = {
        "filas_totales": len(ventas),
        "filas_validas": len(validos),
        "filas_invalidas": len(errores),
        "importe_total": round(float(validos["importe"].sum()), 2),
    }
    ruta_calidad = args.output.parent / "calidad_datos.json"
    ruta_calidad.write_text(json.dumps(calidad, indent=2), encoding="utf-8")

    logger.info("Guardado %s y %s", args.output, ruta_calidad)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
