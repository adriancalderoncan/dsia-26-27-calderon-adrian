#!/usr/bin/env bash
# Paso 3 de la cadena: solo se llama si los pasos 1 y 2 han salido bien
set -euo pipefail
mkdir -p Datos/salida
echo "PIPELINE_OK ${1:-$(date -Iseconds)}" | tee Datos/salida/LAST_OK.txt
