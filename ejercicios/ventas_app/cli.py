import argparse
import json
import logging
from pathlib import Path

from .loader import DataLoadError, load
from .metrics import clientes_repetidos, importe_por_region, top_productos
from .validator import ValidationError, validar_ventas

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Limpia y resume el fichero de ventas")
    parser.add_argument("--input", required=True, help="csv o json de ventas")
    parser.add_argument("--output", required=True, help="csv donde guardar las ventas validas")
    args = parser.parse_args()

    try:
        ventas = load(Path(args.input))
        validos, errores = validar_ventas(ventas)
    except (DataLoadError, ValidationError) as e:
        logger.error(e)
        raise SystemExit(1)

    logger.info("Filas validas: %d | invalidas: %d", len(validos), len(errores))
    logger.info("Importe por region:\n%s", importe_por_region(validos).to_string())
    logger.info("Top productos:\n%s", top_productos(validos).to_string())
    logger.info("Clientes con mas de una compra: %d", len(clientes_repetidos(validos)))

    salida = Path(args.output)
    validos.to_csv(salida, index=False)

    calidad = {
        "filas_totales": len(ventas),
        "filas_validas": len(validos),
        "filas_invalidas": len(errores),
        "importe_total": round(float(validos["importe"].sum()), 2),
    }
    ruta_calidad = salida.parent / "calidad_datos.json"
    with open(ruta_calidad, "w", encoding="utf-8") as f:
        json.dump(calidad, f, indent=2)

    logger.info("Guardado %s y %s", salida, ruta_calidad)


if __name__ == "__main__":
    main()
