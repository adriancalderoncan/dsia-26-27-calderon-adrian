**Diseño de ventas_app**

**SRP (responsabilidad única):** validator.py solo decide qué filas son válidas y cuáles no. No lee ni escribe ficheros, eso lo hacen loader.py y cli.py.

**OCP (abierto/cerrado):** para leer un json añadí JsonSalesRepository en loader.py sin tocar validator.py ni metrics.py. Lo mismo con las métricas: top_productos se añadió en metrics.py sin cambiar el loader.

**DIP (inversión de dependencias):** en loader.py hay un Protocol SalesRepository con el método load(). CsvSalesRepository y JsonSalesRepository lo cumplen. La función load() guarda el lector en una variable de tipo SalesRepository y solo llama a repo.load(), así que no depende de si los datos vienen de un csv o de un json.

**Clean code**

En el E1 la máscara se llamaba ok y ahora es_valida.

El 3 del top de productos ahora es la constante TOP_PRODUCTOS en metrics.py.

Los print del notebook se han cambiado por logging en cli.py.
