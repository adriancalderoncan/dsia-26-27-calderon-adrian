**Proyecto I - Programación avanzada en Python**

![CI](https://github.com/adriancalderoncan/dsia-26-27-calderon-adrian/actions/workflows/ci.yml/badge.svg)

Dos pipelines con la misma forma (carga, validación, métricas y CLI), cada uno con sus tests:

Parte A (ventas_app): calidad de datos del ventas.csv del curso.

Parte B (sleep_app): dataset público de Kaggle sobre uso del móvil antes de dormir y deuda de sueño.

**Estructura**

ventas_app/ y sleep_app/: un paquete por parte, cada uno con loader.py, validator.py, metrics.py y cli.py

tests/ventas/ y tests/sleep/: los tests de cada parte (loader, validator, metrics y cli)

data/: ventas.csv y bedtime_screentime_sleep_debt.csv

pytest.ini: configuración de pytest del proyecto

El workflow de CI está en .github/workflows/ci.yml en la raíz del repositorio y el requirements.txt también está en la raíz.

**Instalación**

Desde la raíz del repositorio:

py -3.13 -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt

Todos los comandos de abajo se lanzan desde la carpeta proyecto_i (cd proyecto_i).

**Parte A - Pipeline de ventas**

python -m ventas_app.cli --input data/ventas.csv --output salida/ventas/ventas_limpias.csv

Una venta es válida si unidades y precio_unitario son números mayores que 0. Si falta alguna columna salta ValidationError y si el fichero no existe DataLoadError. En los dos casos el programa termina con código 2.

Guarda las ventas válidas (con la columna importe) y un calidad_datos.json en la misma carpeta. Por pantalla saca el importe por región, el top 3 de productos y los clientes con más de una compra.

Con el ventas.csv del curso salen 140 válidas y 10 inválidas.

**Parte B - Pipeline de sueño y móvil antes de dormir**

python -m sleep_app.cli --input data/bedtime_screentime_sleep_debt.csv --output-dir salida/sleep

En --output-dir deja registros_validos.csv, registros_invalidos.csv (con una columna motivo que dice qué regla no cumple) y metricas.json.

**Dataset de la Parte B**

Nombre: Sleep Debt & Screen Time: Late Night Phone Habits

Autor: Samar Talwar

URL: https://www.kaggle.com/datasets/samartalwar/sleep-debt-and-screen-time-late-night-phone-habits/data

Licencia: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). Se puede usar y compartir citando al autor, y la copia de los datos que hay en data/ mantiene la misma licencia.

Fecha de descarga: 11/10/2026 (versión actualizada en Kaggle el 21/09/2026)

Fichero: data/bedtime_screentime_sleep_debt.csv, 8500 filas y 18 columnas (menos de 1 MB, por eso está entero en el repo)

Lo he elegido porque relaciona hábitos de uso del móvil (minutos en la cama, app, brillo, filtro de luz azul) con medidas del sueño (horas, latencia, fases) y el cansancio del día siguiente, y permite sacar conclusiones fáciles de entender. Hay que tener en cuenta que el autor indica que los datos son simulados (generados con un modelo), no medidos a personas reales, así que las conclusiones sirven para practicar pero no como estudio real.

Columnas: user_id, age, gender, occupation_type, chronotype, bedtime_phone_minutes, primary_bedtime_app, screen_brightness_pct, blue_light_filter_active, caffeine_post_5pm_mg, physical_activity_min, sleep_latency_min, total_sleep_hours, deep_sleep_pct, rem_sleep_pct, morning_alarm_snoozes, next_day_fatigue_score y sleep_debt_category.

**Reglas de validación (sleep_app/validator.py)**

Si falta alguna de las 18 columnas salta ValidationError. Después cada fila se comprueba con estas reglas y si no cumple alguna va a inválidos con el motivo de la primera que falla:

1. Sin valores nulos. Si en una columna numérica hay texto también cuenta como nulo.

2. user_id con el formato USR-00000.

3. user_id sin repetir (se queda el primero).

4. gender, occupation_type, chronotype, primary_bedtime_app y sleep_debt_category tienen que tener uno de los valores conocidos, y blue_light_filter_active solo puede ser 0 o 1.

5. Rangos: edad de 18 a 100, minutos de móvil de 0 a 600, brillo de 0 a 100, cafeína de 0 a 1000 mg, actividad física de 0 a 600 min, latencia de 0 a 300 min, horas de sueño de 0 a 24, porcentajes de sueño profundo y REM de 0 a 100, alarmas pospuestas de 0 a 50 y fatiga de 1 a 10. Son límites posibles en la realidad, no los mínimos y máximos que trae el dataset.

6. deep_sleep_pct + rem_sleep_pct no puede pasar de 100.

El dataset descargado no tiene ningún fallo (8500 válidos y 0 inválidos), por eso las reglas se prueban en los tests con registros fabricados que no las cumplen.

**Métricas (sleep_app/metrics.py)**

Horas de sueño y fatiga media según los minutos de móvil antes de dormir (0-30, 31-60, 61-120 y más de 120).

Horas de sueño y fatiga media por app usada antes de dormir.

Horas de sueño medias por cronotipo.

Porcentaje de personas en cada categoría de deuda de sueño.

Minutos que se tarda en dormir con y sin filtro de luz azul.

Resultados con el dataset completo:

Con 0-30 minutos de móvil se duermen 7.15 horas de media con una fatiga de 1.93. Con más de 120 minutos bajan a 4.45 horas y la fatiga sube a 8.36.

TikTok / Reels es la app con más fatiga (4.16) y News / Reading la que menos (3.33).

Los Night Owl duermen 5.01 horas de media, los Intermediate 6.44 y los Morning Lark 7.38.

Un 52.5% tiene Moderate Debt, un 23.6% Mild Deficit, un 16.3% Optimal Recovery y un 7.6% Severe Sleep Debt.

Con filtro de luz azul se tarda 39.62 minutos en dormir y sin filtro 41.6.

**Tests**

pytest -q

pytest -q -m "not integration"

pytest --cov=ventas_app --cov=sleep_app --cov-report=term-missing --cov-fail-under=60

Hay tests de loader, validator, metrics y cli en las dos partes (tests/ventas y tests/sleep). Casi todos usan datos en memoria (fixtures) o tmp_path. Los dos marcados como integration leen los ficheros reales de data/: el de ventas comprueba 140 válidas y 10 inválidas y el de sueño 8500 válidos.

**CI**

Workflow: .github/workflows/ci.yml (en la raíz del repositorio, uno solo para todo el repo)

En cada push a main y en cada pull request instala el requirements.txt con Python 3.12 y en la carpeta proyecto_i lanza pytest con cobertura de ventas_app y sleep_app. Si falla algún test o la cobertura baja del 60% se pone en rojo.

Último run en verde: (pegar aquí el enlace de Actions)
