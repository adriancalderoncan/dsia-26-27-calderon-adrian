**DSIA 2026-2027 - Calderon, Adrian**

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

**Cómo ejecutar ventas_app**

Desde la carpeta del repo con el .venv activado:

python -m ejercicios.ventas_app.cli --input Datos/ventas.csv --output Datos/ventas_limpias.csv

También acepta un json: --input Datos/ventas.json

Espera las columnas fecha, region, producto, unidades, precio_unitario y cliente_id. Guarda las ventas válidas en el csv de --output y el calidad_datos.json en la misma carpeta.

**Variables de entorno**

De momento no hace falta ninguna. Si más adelante uso claves irán en un .env que no se sube.
