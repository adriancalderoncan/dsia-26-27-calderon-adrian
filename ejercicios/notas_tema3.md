**Tema 3 - Automatización e IA**

**E4 - Pipeline de ventas**

**Parte 1. Qué cambió y qué no**

Solo cambia el flag --max-error-rate (de 0.5 a 0.05), el código de pipeline_ventas.py es el mismo. Con 0.5 sale exit 0 y con 0.05 sale exit 1 porque el error_rate del csv es 0.067.

**Parte 2. Señales**

Exit 0: todo bien y se escriben ventas_limpias.csv, metrics.json y run.log.

Exit 1: no pasa el gate de calidad, se escribe el metrics.json para ver por qué pero no el csv limpio.

Exit 2: la entrada está mal. Por ejemplo quitando la columna region sale "Faltan columnas: ['region']" en el log y no se escribe el csv limpio.

El log sale por consola y también se guarda en run.log.

**Parte 4. Por qué cron exige idempotencia y exit codes**

Cron lanza el job solo y nadie mira la pantalla, así que la única forma de saber si ha ido bien es el exit code (y el log). Y como lo vuelve a lanzar cada día, tiene que poder repetirse sin duplicar ficheros ni dar por bueno algo que ha fallado.

**Partes 5 y 6. Cadena y cron**

La cadena está en scripts/run_cadena_ventas.sh. Con set -euo pipefail si el pipeline o check_metrics salen con un exit distinto de 0 se para y no se ejecuta notify_ok.sh. Lo he comprobado con MIN_ROWS_OUT=999999 y no se crea LAST_OK.txt.

El wrapper para cron es scripts/run_pipeline_ventas.sh. La línea de crontab sería:

15 2 * * * /ruta/absoluta/al/repo/ejercicios/scripts/run_pipeline_ventas.sh

**Parte 7. Test de transform**

Está en tests/test_pipeline.py (test_transform_report_cuenta_filas). transform no lee ni escribe ficheros, así que se prueba con un DataFrame en memoria.

**Tres frases**

CLI no es lo mismo que notebook: el job se lanza con un comando y flags, sin tener que ejecutar celdas a mano, así lo puede lanzar cron u otro script.

Exit, metrics y log son señales para máquinas: el siguiente paso decide si sigue mirando el exit code, y el metrics.json y el run.log sirven para saber qué ha pasado.

Idempotencia más gate es lo que hace seguro re-ejecutar: si se lanza otra vez sobrescribe lo mismo, y si los datos son malos sale con error en vez de publicarlos.

**E5 - Cliente de IA**

**Por qué el modo mock es obligatorio en CI y desarrollo offline**

Porque no necesita claves ni internet. En la CI no hay que meter claves de pago y los tests no dependen de que la API responda, así que son rápidos, gratis y siempre dan lo mismo. También permite probar los reintentos con --fail-once sin gastar nada.
