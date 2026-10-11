"""E4 - Paso 2 de la cadena: lee el metrics.json del pipeline y decide si sigue"""

import argparse
import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--max-error-rate", type=float, default=0.1)
    parser.add_argument("--min-rows-out", type=int, default=1)
    args = parser.parse_args(argv)

    report = json.loads(args.metrics.read_text(encoding="utf-8"))
    if report["error_rate"] > args.max_error_rate or report["rows_out"] < args.min_rows_out:
        print(f"KO {report}", file=sys.stderr)
        return 1
    print(f"OK {report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
