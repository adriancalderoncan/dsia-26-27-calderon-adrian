#!/usr/bin/env bash
# Wrapper para cron. Cron no hace cd al repo ni activa el venv,
# por eso aqui se fija todo antes de lanzar el pipeline.
#
# Linea de crontab (todos los dias a las 02:15):
# 15 2 * * * /ruta/absoluta/al/repo/ejercicios/scripts/run_pipeline_ventas.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO"

if [ -f .venv/Scripts/python.exe ]; then
    PYTHON="$REPO/.venv/Scripts/python.exe"
else
    PYTHON="$REPO/.venv/bin/python"
fi

DAY="$(date +%F)"
OUT="$REPO/Datos/salida/$DAY"
LOG_DIR="$REPO/Datos/salida/cron_logs"
mkdir -p "$OUT" "$LOG_DIR"

"$PYTHON" -m ejercicios.pipeline_ventas \
    --input Datos/ventas.csv \
    --output-dir "$OUT" \
    --max-error-rate 0.1 \
    >> "$LOG_DIR/ventas_$DAY.log" 2>&1

echo "OK $DAY exit=0" >> "$LOG_DIR/ventas_$DAY.log"
