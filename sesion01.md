**Sesión 1 - venv y Git**

**Conceptos**

El venv aísla las librerías de cada proyecto para que no se mezclen con el Python del ordenador.

El requirements.txt sirve para que otra persona pueda instalar lo mismo que yo.

Git guarda fotos (commits) del proyecto y GitHub las guarda en internet.

El orden es: cambio los ficheros, git add, git commit y git push.

Nunca se sube la carpeta .venv ni el .env.

**Comandos**

py -3.13 -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt

git switch -c practica/sesion-01

git add, git commit -m "mensaje", git push

**Autoevaluación**

**1. Diferencia entre Python global y .venv**

El global es el que está instalado en el ordenador y lo usan todos los proyectos. El .venv es una copia dentro del proyecto con sus propias librerías, así si un proyecto necesita otra versión de pandas no afecta a los demás.

**2. Para qué sirve python -m pip en vez de pip**

Así te aseguras de que instalas en el Python que estás usando. Si pones solo pip puede ser el de otra instalación y se instala en otro sitio.

**3. Working tree, staging y commit**

El working tree son los ficheros como los tengo ahora. El staging es lo que marco con git add para guardar. El commit es cuando se guarda en el historial con un mensaje.

**4. Clone y pull son lo mismo?**

No. Clone es para descargar el repo la primera vez y pull es para traer los cambios nuevos cuando ya lo tengo.

**5. Cuatro cosas que no se suben a GitHub**

La carpeta .venv, el .env, pycache y datos personales o muy grandes. El .env no se sube porque tiene claves y contraseñas y cualquiera podría usarlas.

**6. Reescribir los mensajes**

update -> Update README con pasos cmd

fix final -> Arreglo path de carga ventas.csv

cambios varios -> mejor separarlo en varios commits, por ejemplo Add gitignore y Add session 01 notas

**7. El IDE no importa pandas pero la terminal sí**

Seguramente el IDE está usando otro Python. Hay que ir a Python: Select Interpreter y elegir el del .venv.

**8. Subí el .env por error**

Primero cambiar las claves porque ya no son seguras. Después quitarlo con git rm --cached .env, añadirlo al .gitignore y hacer commit.
