#!/usr/bin/env bash
# Cadena de 3 pasos: pipeline -> check_metrics -> notify_ok
# Con set -e si un paso sale con exit distinto de 0 la cadena se para ahi
#
# Prueba negativa (el paso 3 no se tiene que ejecutar):
#   MIN_ROWS_OUT=999999 bash ejercicios/scripts/run_cadena_ventas.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO"

# en Windows el python del venv esta en Scripts y en Linux/Mac en bin
if [ -f .venv/Scripts/python.exe ]; then
    PYTHON=.venv/Scripts/python.exe
else
    PYTHON=.venv/bin/python
fi

MIN_ROWS_OUT="${MIN_ROWS_OUT:-100}"
OUT="Datos/salida/$(date +%F)"
mkdir -p "$OUT"

echo "== 1/3 limpiar =="
"$PYTHON" -m ejercicios.pipeline_ventas \
    --input Datos/ventas.csv --output-dir "$OUT" --max-error-rate 0.5

echo "== 2/3 metrics =="
"$PYTHON" -m ejercicios.check_metrics \
    --metrics "$OUT/metrics.json" --max-error-rate 0.1 --min-rows-out "$MIN_ROWS_OUT"

echo "== 3/3 notify =="
bash ejercicios/scripts/notify_ok.sh "$(date +%F)"
echo "Cadena OK -> $OUT"
