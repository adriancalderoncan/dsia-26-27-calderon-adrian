**DSIA 2026-2027 - Calderon, Adrian**

![CI](https://github.com/adriancalderoncan/dsia-26-27-calderon-adrian/actions/workflows/ci.yml/badge.svg)

Repositorio de la asignatura Desarrollo de Soluciones de IA. Aquí van los ejercicios de clase y el Proyecto 1.

**Cómo instalar**

Hace falta Python 3.13. En la terminal, desde la carpeta del repo:

py -3.13 -m venv .venv

.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

**Carpetas**

Datos: los csv de ventas e iris y las salidas del E1

ejercicios: los ejercicios de clase

ejercicios/sesion01.md: E0, apuntes y respuestas de la sesión 1

ejercicios/e1_pandas.ipynb: E1, pandas con ventas.csv

ejercicios/ventas_app: E2, el E1 pasado a paquete (loader, validator, metrics y cli)

ejercicios/tests: E3, los tests de ventas_app con pytest

.github/workflows/ci.yml: E4 del tema 2, la CI de GitHub Actions

ejercicios/pipeline_ventas.py, check_metrics.py y scripts/: E4 del tema 3, el pipeline de ventas como job automatizable

ejercicios/ai_api_client.py, prompts.txt y respuestas.jsonl: E5, cliente de IA con batch y reintentos

ejercicios/notas_tema3.md: respuestas escritas del E4 y el E5

proyecto_i: el Proyecto I (Parte A ventas_app y Parte B sleep_app). Cómo se ejecuta, el dataset y los tests están en proyecto_i/README.md

**Cómo ejecutar ventas_app**

Desde la carpeta del repo con el .venv activado:

python -m ejercicios.ventas_app.cli --input Datos/ventas.csv --output Datos/ventas_limpias.csv

También acepta un json: --input Datos/ventas.json

Espera las columnas fecha, region, producto, unidades, precio_unitario y cliente_id. Guarda las ventas válidas en el csv de --output y el calidad_datos.json en la misma carpeta.

**Pipeline de ventas (E4 tema 3)**

python -m ejercicios.pipeline_ventas --input Datos/ventas.csv --output-dir Datos/salida/prueba --max-error-rate 0.5

Deja en --output-dir el ventas_limpias.csv, el metrics.json y el run.log. Si se vuelve a lanzar con la misma carpeta sobrescribe los ficheros, no duplica nada.

Códigos de salida (echo $? en bash o $LASTEXITCODE en PowerShell):

0: todo bien

1: demasiados errores en los datos (error_rate mayor que --max-error-rate). Con el ventas.csv del curso el error_rate es 0.067, así que con --max-error-rate 0.05 sale 1

2: la entrada está mal (no existe el fichero o faltan columnas)

Cadena de 3 pasos (pipeline, check_metrics y notify_ok), desde Git Bash. Si un paso falla no se ejecuta el siguiente (prueba: MIN_ROWS_OUT=999999 delante del comando):

bash ejercicios/scripts/run_cadena_ventas.sh

Wrapper para cron:

bash ejercicios/scripts/run_pipeline_ventas.sh

Línea de crontab para lanzarlo todos los días a las 02:15 (en Windows no hay cron, se dejaría en el programador de tareas o en un servidor Linux):

15 2 * * * /ruta/absoluta/al/repo/ejercicios/scripts/run_pipeline_ventas.sh

**Cliente de IA (E5)**

Funciona sin claves en modo mock:

python -m ejercicios.ai_api_client --provider mock --prompt "Hola"

python -m ejercicios.ai_api_client --provider mock --batch ejercicios/prompts.txt --output ejercicios/respuestas.jsonl --fail-once

--batch lee un prompt por línea y guarda una línea json por respuesta. --fail-once simula un fallo en la primera llamada y se reintenta hasta 2 veces.

**Tests**

Todos los tests:

pytest -q

Solo los unitarios (sin el que lee el ventas.csv real):

pytest -q -m "not integration"

Con cobertura:

pytest -q --cov=ejercicios.ventas_app --cov=ejercicios.pipeline_ventas --cov=ejercicios.check_metrics --cov=ejercicios.ai_api_client --cov-report=term-missing --cov-fail-under=60

**CI**

Workflow: .github/workflows/ci.yml

En cada push a main y en cada pull request GitHub instala el requirements.txt con Python 3.12 y pasa los tests con pytest en dos pasos: primero los de los ejercicios y después los del Proyecto I (dentro de proyecto_i, con cobertura de ventas_app y sleep_app). Si falla algún test o la cobertura baja del 60% se pone en rojo.

Último run en verde: (https://github.com/adriancalderoncan/dsia-26-27-calderon-adrian/actions/runs/38136729700)

**Variables de entorno**

Solo hacen falta para usar proveedores de IA reales (openai, anthropic o hf). Se copia .env.example a .env y se rellenan las claves. El .env no se sube a GitHub. El modo mock no necesita ninguna.
