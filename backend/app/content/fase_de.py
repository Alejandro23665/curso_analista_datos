from ._helpers import checklist, py, quiz, sql

TOPICS = [
    {
        "slug": "de-modelado",
        "phase": "de",
        "title": "Modelado de datos y data warehouse",
        "summary": "Normalización, OLTP vs OLAP, esquema en estrella, granularidad y dimensiones que cambian (SCD).",
        "hours": 10,
        "theory": r"""
# Modelado de datos y data warehouse

Un ingeniero de datos diseña **cómo se organizan** los datos para que otros los consulten rápido y sin errores.

## 1. OLTP vs OLAP

| | OLTP (sistemas operativos) | OLAP (analítica) |
|---|---|---|
| Ejemplo | La base de datos de la tienda online | El data warehouse |
| Operaciones | Muchas escrituras pequeñas | Pocas consultas grandes de lectura |
| Diseño | **Normalizado** (menos redundancia) | **Dimensional** (consultas simples y rápidas) |

No analices sobre la base operativa de producción: la ralentizas. Se **copian** los datos a un almacén analítico.

## 2. Normalización en una frase

Cada dato vive en **un solo lugar**. 1FN: valores atómicos; 2FN: nada depende solo de parte de la clave; 3FN: nada depende
de columnas que no son la clave. Las tablas `customers`, `orders`, `order_items` y `products` de esta plataforma están normalizadas.

## 3. Esquema en estrella (star schema)

Se organiza en:

- **Tabla de hechos (fact):** eventos medibles, una fila por evento (`fact_ventas`: fecha, cliente, producto, unidades, importe). Muchas filas, claves foráneas y métricas numéricas.
- **Tablas de dimensiones (dim):** contexto descriptivo (`dim_cliente`, `dim_producto`, `dim_fecha`). Pocas filas, muchas columnas de texto.

```
dim_cliente ──┐
dim_producto ─┼── fact_ventas
dim_fecha ────┘
```

Las consultas son siempre: unir el hecho con las dimensiones que necesitas, filtrar y agrupar. Sencillo, rápido y legible.

## 4. La decisión más importante: la granularidad (grain)

Define **qué representa una fila** de la tabla de hechos: "una línea de pedido", "un pedido", "un día por producto".
Todo lo demás se deriva de ahí. Regla: **elige el grano más fino que necesites**; siempre puedes agregar hacia arriba, nunca hacia abajo.

## 5. Dimensiones que cambian: SCD

Si un cliente cambia de segmento, ¿qué pasa con el historial?

- **SCD tipo 1:** sobrescribes (pierdes el histórico).
- **SCD tipo 2:** insertas una **fila nueva** con fechas de vigencia (`valido_desde`, `valido_hasta`, `es_actual`). Conservas el historial: las ventas antiguas siguen asociadas al segmento de entonces.

## 6. Claves

- **Clave natural:** la del sistema origen (`customer_id`).
- **Clave sustituta (surrogate):** un entero propio del warehouse, estable aunque cambie el origen. Se usa en SCD2.

## 7. Capas habituales

`raw` (copia fiel del origen) → `staging` (limpio y tipado) → `marts` (modelo dimensional listo para negocio).

## Cómo sabes que dominas este tema

- Diseñas un esquema en estrella para un caso nuevo y defines su granularidad.
- Explicas cuándo usar SCD tipo 2.
- Distingues normalizar (OLTP) de modelar dimensionalmente (OLAP).
""",
        "exercises": [
            sql("de-sql-hechos", "Construye una tabla de hechos", "Ingeniería de datos: modelado",
                "Con los datos de la tienda, construye el resultado de una tabla de hechos agregada: por `fecha` y `categoria` (de `products`), "
                "con `unidades` (suma de quantity) e `ingresos` (suma de quantity * unit_price, 2 decimales), solo pedidos **completados** "
                "del 2024-01-01 al 2024-01-31. Ordena por fecha y categoría.",
                """SELECT o.order_date AS fecha, p.category AS categoria,
       SUM(oi.quantity) AS unidades,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS ingresos
FROM order_items oi
JOIN orders o ON o.id = oi.order_id
JOIN products p ON p.id = oi.product_id
WHERE o.status = 'completado' AND o.order_date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY o.order_date, p.category
ORDER BY o.order_date, p.category""",
                starter="SELECT o.order_date AS fecha, p.category AS categoria,\n       -- unidades e ingresos\nFROM order_items oi\n", ordered=True,
                hint="Une order_items con orders y products; agrupa por fecha y categoría."),
            quiz("de-quiz-grano", "Elegir la granularidad", "Ingeniería de datos: modelado",
                 "Vas a modelar las ventas de una tienda. Hoy te piden solo totales por día, pero el negocio podría querer analizar por producto después. "
                 "¿Qué granularidad es la más segura para la tabla de hechos?",
                 ["Un registro por día", "Un registro por línea de pedido", "Un registro por mes", "Un registro por cliente"], 1,
                 "El grano más fino conserva toda la información: siempre puedes agregar a día, mes o cliente, pero no puedes 'desagregar' un total diario."),
            quiz("de-quiz-scd", "Qué tipo de SCD", "Ingeniería de datos: modelado",
                 "Un cliente pasa del segmento 'Pyme' a 'Corporativo'. Necesitas que las ventas de 2023 sigan mostrándose como 'Pyme'. ¿Qué técnica usas?",
                 ["SCD tipo 1 (sobrescribir)", "SCD tipo 2 (nueva fila con fechas de vigencia)", "Borrar y volver a insertar al cliente", "Guardar el segmento solo en la tabla de hechos sin dimensión"], 1,
                 "El tipo 2 conserva el historial: la fila antigua queda cerrada con su fecha de fin y se crea una nueva fila vigente."),
            quiz("de-quiz-oltp", "OLTP u OLAP", "Ingeniería de datos: modelado",
                 "El equipo de analítica ejecuta consultas pesadas directamente sobre la base de datos de producción y la tienda se vuelve lenta. ¿Qué arquitectura lo evita?",
                 ["Añadir más índices a producción sin límite", "Replicar los datos a un almacén analítico (warehouse) y consultar allí",
                  "Pedir a los analistas que consulten de madrugada", "Quitar la normalización de producción"], 1,
                 "Separar las cargas operativas (OLTP) de las analíticas (OLAP) evita que las consultas pesadas afecten al negocio."),
        ],
    },
    {
        "slug": "de-python-etl",
        "phase": "de",
        "title": "ETL/ELT con Python y PostgreSQL",
        "summary": "Extraer, transformar y cargar datos de forma repetible: idempotencia, lotes, upserts, logging y configuración.",
        "hours": 14,
        "theory": r"""
# ETL/ELT con Python y PostgreSQL

Un **pipeline** mueve y transforma datos de forma automática y repetible.

- **ETL:** Extract → Transform → Load (transformas antes de cargar).
- **ELT:** Extract → Load → Transform (cargas el dato crudo al warehouse y transformas allí con SQL, p. ej. con dbt). Es lo más habitual hoy.

## 1. Extraer

Fuentes típicas: archivos CSV/JSON, APIs REST, bases de datos, hojas de cálculo.

```python
import requests
resp = requests.get("https://api.ejemplo.com/ventas", params={"desde": "2024-01-01"}, timeout=30)
resp.raise_for_status()          # falla ruidosamente si hay error HTTP
registros = resp.json()
```

Siempre: **timeout**, reintentos con espera creciente y manejo de paginación.

## 2. Transformar

Limpia, valida y convierte tipos. Escribe las transformaciones como **funciones puras** que puedas probar sin base de datos.

```python
def transformar(registro):
    ...  # devuelve el registro limpio o None si es inválido
```

Los registros inválidos no se pierden en silencio: se cuentan, se registran (log) y, si son importantes, se guardan en una tabla de "rechazados".

## 3. Cargar

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://usuario:clave@localhost/dwh")
df.to_sql("stg_ventas", engine, if_exists="append", index=False, chunksize=1000)
```

Para volúmenes grandes, `COPY` de PostgreSQL es mucho más rápido que insertar fila a fila. Carga **por lotes**.

## 4. Idempotencia: la propiedad más importante

Un pipeline es **idempotente** si ejecutarlo dos veces produce el mismo resultado que una vez. Sin esto, cada reintento duplica datos.
Formas de lograrlo:

- **Upsert** con clave única:

```sql
INSERT INTO dim_cliente (id, nombre, segmento)
VALUES (%s, %s, %s)
ON CONFLICT (id) DO UPDATE SET nombre = EXCLUDED.nombre, segmento = EXCLUDED.segmento;
```

- **Reemplazar por partición:** borrar y reinsertar los datos de un día dentro de una transacción.
- Cargar primero en una tabla temporal y luego intercambiar.

## 5. Buenas prácticas de producción

- **Logging** (no `print`): qué se procesó, cuántas filas, cuánto tardó.
- **Configuración por variables de entorno** (nunca claves en el código).
- **Carga incremental:** procesa solo lo nuevo (por fecha o por id), guardando un "marcador" de hasta dónde llegaste.
- **Transacciones:** o todo se carga o nada.
- **Pruebas:** tests unitarios para transformaciones; comprobaciones de conteo y unicidad después de cargar.
- **Estructura de proyecto:** `extract.py`, `transform.py`, `load.py`, `main.py`, `tests/`.

## Cómo sabes que dominas este tema

- Explicas qué es idempotencia y cómo la garantizas.
- Escribes `INSERT ... ON CONFLICT` sin consultar.
- Tu pipeline puede fallar a la mitad, reintentarse y quedar con los datos correctos.
""",
        "exercises": [
            py("etl-transformar", "Transformar un registro", "Ingeniería de datos: ETL",
               "Escribe `transformar_registro(registro)`. Recibe un diccionario con `nombre`, `monto` (puede venir como texto con coma decimal, p. ej. `'12,5'`) y `pais`. "
               "Devuelve `{'nombre': ..., 'monto': float, 'pais': ...}` con el nombre sin espacios sobrantes y en formato Título (`.title()`), el monto como `float` y el país en MAYÚSCULAS. "
               "Devuelve `None` si falta algún campo requerido, el nombre queda vacío, el monto no es numérico o es negativo (`pais` es opcional).",
               starter="""
def transformar_registro(registro):
    # tu código aquí
    pass
""",
               solution="""
def transformar_registro(registro):
    try:
        nombre = registro["nombre"].strip().title()
        monto = float(str(registro["monto"]).replace(",", "."))
    except (KeyError, ValueError, AttributeError):
        return None
    if not nombre or monto < 0:
        return None
    pais = (registro.get("pais") or "").strip().upper()
    return {"nombre": nombre, "monto": monto, "pais": pais}
""",
               tests="""
ok = transformar_registro({"nombre": "  ana perez ", "monto": "12,5", "pais": "ve"})
assert ok == {"nombre": "Ana Perez", "monto": 12.5, "pais": "VE"}, "Resultado inesperado: %r" % (ok,)
assert transformar_registro({"nombre": "Luis", "monto": 7}) == {"nombre": "Luis", "monto": 7.0, "pais": ""}, "Sin pais debe quedar ''"
assert transformar_registro({"nombre": "Luis", "monto": "abc"}) is None, "Monto no numerico -> None"
assert transformar_registro({"monto": 5}) is None, "Sin nombre -> None"
assert transformar_registro({"nombre": "   ", "monto": 5}) is None, "Nombre vacio -> None"
assert transformar_registro({"nombre": "Eva", "monto": -3}) is None, "Monto negativo -> None"
""",
               hint="Atrapa KeyError, ValueError y AttributeError en un solo try."),
            py("etl-lotes", "Procesar en lotes", "Ingeniería de datos: ETL",
               "Escribe `en_lotes(items, tamano)` que devuelva una **lista de listas**, cada una con hasta `tamano` elementos, en el mismo orden. "
               "Ejemplo: `en_lotes([1, 2, 3, 4, 5], 2)` → `[[1, 2], [3, 4], [5]]`.",
               starter="""
def en_lotes(items, tamano):
    # tu código aquí
    pass
""",
               solution="""
def en_lotes(items, tamano):
    return [list(items[i:i + tamano]) for i in range(0, len(items), tamano)]
""",
               tests="""
assert en_lotes([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
assert en_lotes([], 3) == []
assert en_lotes([1, 2, 3], 5) == [[1, 2, 3]]
assert en_lotes(list(range(6)), 3) == [[0, 1, 2], [3, 4, 5]]
""",
               hint="range(0, len(items), tamano) y rebanadas items[i:i + tamano]."),
            py("etl-upsert", "Upsert idempotente", "Ingeniería de datos: ETL",
               "Escribe `upsert(destino, entrantes, clave)`. `destino` es una lista de diccionarios ya cargados y `entrantes` los nuevos; "
               "`clave` es el nombre del campo único. Devuelve una **nueva lista** donde los registros entrantes reemplazan a los existentes con la misma clave "
               "y los nuevos se añaden. Ejecutarlo dos veces con los mismos datos debe dar el mismo resultado (idempotencia). Ordena el resultado por la clave.",
               starter="""
def upsert(destino, entrantes, clave):
    # tu código aquí
    pass
""",
               solution="""
def upsert(destino, entrantes, clave):
    indice = {fila[clave]: fila for fila in destino}
    for fila in entrantes:
        indice[fila[clave]] = fila
    return [indice[k] for k in sorted(indice)]
""",
               tests="""
base = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
nuevos = [{"id": 2, "nombre": "Luis M."}, {"id": 3, "nombre": "Eva"}]
una_vez = upsert(base, nuevos, "id")
assert una_vez == [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis M."}, {"id": 3, "nombre": "Eva"}], "Resultado inesperado: %r" % (una_vez,)
dos_veces = upsert(una_vez, nuevos, "id")
assert dos_veces == una_vez, "Ejecutarlo dos veces debe dar lo mismo (idempotencia)"
assert base == [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}], "No modifiques la lista original"
""",
               hint="Un diccionario indexado por la clave hace trivial reemplazar o añadir."),
            quiz("etl-quiz-idem", "Idempotencia", "Ingeniería de datos: ETL",
                 "Tu pipeline diario falla a las 3 a. m. después de cargar la mitad de los datos y lo reintentas. Ahora la tabla tiene filas duplicadas. ¿Qué principio faltó?",
                 ["Normalización", "Idempotencia", "Particionado", "Compresión"], 1,
                 "Un pipeline idempotente produce el mismo resultado aunque se ejecute varias veces: usando upserts, reemplazo por partición o transacciones."),
            quiz("etl-quiz-conflict", "Upsert en PostgreSQL", "Ingeniería de datos: ETL",
                 "¿Qué cláusula de PostgreSQL permite insertar una fila y, si la clave ya existe, actualizarla?",
                 ["INSERT ... IGNORE", "INSERT ... ON CONFLICT (clave) DO UPDATE", "MERGE ... REPLACE", "UPDATE ... OR INSERT"], 1,
                 "`ON CONFLICT (columna_unica) DO UPDATE SET ...` es la forma estándar de hacer upsert en PostgreSQL (requiere una restricción única en esa columna)."),
        ],
    },
    {
        "slug": "de-herramientas",
        "phase": "de",
        "title": "Linux, Git y Docker",
        "summary": "La caja de herramientas diaria: terminal, control de versiones, contenedores y variables de entorno.",
        "hours": 12,
        "theory": r"""
# Linux, Git y Docker

Sin estas tres herramientas es difícil trabajar en equipo o desplegar un pipeline. Aquí está lo mínimo que se espera.

## 1. Terminal (bash / PowerShell)

```bash
pwd                 # dónde estoy
ls -la              # listar archivos (incluye ocultos)
cd carpeta          # entrar en una carpeta
cat archivo.txt     # ver contenido
grep "error" log.txt            # buscar texto
head -n 20 datos.csv            # primeras líneas
wc -l datos.csv                 # contar líneas
curl -s URL | jq '.campo'       # consumir una API
```

Aprende a **encadenar** comandos con `|` (pipe) y a leer logs. En Windows, usa **WSL2** para tener Linux real.

## 2. Git: el flujo que usarás todos los días

```bash
git clone URL
git switch -c feature/limpieza-ventas     # rama nueva
git add -p                                # revisa qué agregas
git commit -m "Limpia nulos en ventas"
git push -u origin feature/limpieza-ventas
# abre un Pull Request en GitHub, recibe revisión, haz merge
```

Buenas prácticas:

- **Commits pequeños** con mensajes que explican el *por qué*.
- **Nunca** subas credenciales ni datos privados: usa `.gitignore` y variables de entorno.
- No trabajes directamente en `main`: ramas + Pull Request.
- Si subiste una clave por error, **revócala** (borrar el commit no basta).

## 3. Entornos y variables de entorno

```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Las configuraciones y secretos van en variables de entorno (archivo `.env`, **fuera de Git**):

```
DATABASE_URL=postgresql://usuario:clave@localhost:5432/dwh
```

## 4. Docker: "funciona en mi máquina" deja de ser un problema

- **Imagen:** plantilla inmutable con tu código y sus dependencias.
- **Contenedor:** una imagen en ejecución.
- **Dockerfile:** la receta de la imagen.
- **docker compose:** levanta varios servicios (tu app + PostgreSQL) con un solo comando.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```bash
docker build -t mi-pipeline .
docker compose up -d
docker compose logs -f
docker compose down
```

Claves: copia primero `requirements.txt` (aprovecha la caché), usa imágenes `-slim`, y **no metas secretos en la imagen**.
Los datos de PostgreSQL deben vivir en un **volumen** o se pierden al borrar el contenedor.

## Cómo sabes que dominas este tema

- Trabajas con ramas y Pull Requests sin miedo.
- Levantas PostgreSQL + tu aplicación con `docker compose up`.
- Tus secretos nunca están en el repositorio.
""",
        "exercises": [
            py("herr-env", "Leer un archivo .env", "Ingeniería de datos: herramientas",
               "Escribe `parsear_env(texto)` que convierta el contenido de un archivo `.env` en un diccionario. Ignora líneas vacías, comentarios (que empiezan con `#`) "
               "y líneas sin `=`. Quita espacios y las comillas simples o dobles que rodeen el valor. El valor puede contener `=`.",
               starter="""
def parsear_env(texto):
    # tu código aquí
    pass
""",
               solution="""
def parsear_env(texto):
    resultado = {}
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        resultado[clave.strip()] = valor.strip().strip('"').strip("'")
    return resultado
""",
               tests="""
texto = "# configuracion\\nDB_HOST=localhost\\n\\nDB_PASS='s=ecreto'\\nVACIA=\\nNOMBRE = \\"datapath\\"\\nlinea sin igual\\n"
esperado = {"DB_HOST": "localhost", "DB_PASS": "s=ecreto", "VACIA": "", "NOMBRE": "datapath"}
assert parsear_env(texto) == esperado, "Obtuve %r" % (parsear_env(texto),)
assert parsear_env("") == {}
""",
               hint="split('=', 1) separa solo en el primer signo igual."),
            quiz("herr-quiz-docker", "Persistencia en Docker", "Ingeniería de datos: herramientas",
                 "Levantas PostgreSQL en un contenedor, cargas datos y luego ejecutas `docker compose down` y `up` otra vez. Los datos desaparecieron. ¿Qué faltó?",
                 ["Un índice", "Un volumen para guardar /var/lib/postgresql/data", "Más memoria RAM", "Usar la imagen slim"], 1,
                 "Los contenedores son efímeros. Un volumen guarda los datos fuera del contenedor para que sobrevivan a reinicios y recreaciones."),
            quiz("herr-quiz-git", "Credenciales subidas por error", "Ingeniería de datos: herramientas",
                 "Subiste una API key a un repositorio público de GitHub y la borraste en el siguiente commit. ¿Qué debes hacer?",
                 ["Nada, ya está borrada", "Revocar la clave y generar una nueva, porque sigue en el historial", "Cambiar el nombre del repositorio",
                  "Hacer el repositorio privado y olvidarlo"], 1,
                 "El historial de Git conserva el commit anterior y los bots rastrean claves expuestas en minutos. La única solución segura es revocarla."),
            checklist("herr-check", "Dockeriza tu proyecto", "Ingeniería de datos: herramientas",
                      "Aplícalo a tu Proyecto 1 o a un script ETL sencillo.",
                      ["Tiene un requirements.txt con las versiones", "Escribí un Dockerfile y construí la imagen sin errores",
                       "Un docker-compose.yml levanta mi app y PostgreSQL con un volumen", "Las credenciales vienen de variables de entorno y .env está en .gitignore",
                       "Alguien más puede ejecutar mi proyecto con un solo comando"]),
        ],
    },
    {
        "slug": "de-orquestacion-dbt",
        "phase": "de",
        "title": "Orquestación, dbt y calidad de datos",
        "summary": "DAGs, programación y reintentos (Airflow/Prefect), transformaciones versionadas con dbt y pruebas de calidad.",
        "hours": 14,
        "theory": r"""
# Orquestación, dbt y calidad de datos

Cuando un pipeline tiene varios pasos que dependen unos de otros y debe correr cada día, necesitas **orquestación**.

## 1. DAG: grafo acíclico dirigido

Un DAG describe **tareas** y sus **dependencias**, sin ciclos:

```
extraer_api ──► limpiar ──► cargar_staging ──► transformar_marts ──► actualizar_dashboard
```

Un orquestador (Apache **Airflow**, **Prefect**, **Dagster**) se encarga de:

- **Programar** (cada hora, cada día a las 6:00).
- **Ordenar** las tareas respetando dependencias.
- **Reintentar** automáticamente las que fallan, con espera.
- **Alertar** si algo falla definitivamente.
- **Backfill:** reejecutar el pipeline para fechas pasadas.
- Mostrar un **historial** de ejecuciones y logs.

Ejemplo mínimo con Prefect:

```python
from prefect import flow, task

@task(retries=3, retry_delay_seconds=30)
def extraer(): ...

@task
def cargar(datos): ...

@flow
def pipeline_diario():
    cargar(extraer())
```

Cada tarea debería ser **idempotente** (así los reintentos y backfills son seguros) y **pequeña** (más fácil de depurar).

## 2. dbt: transformaciones como código

**dbt** (*data build tool*) ejecuta transformaciones **SQL** dentro del warehouse (la "T" de ELT):

- Cada **modelo** es un archivo `.sql` con un `SELECT`. dbt lo materializa como vista o tabla.
- `{{ ref('stg_ventas') }}` referencia otro modelo y dbt calcula el orden (¡un DAG!).
- **Tests** declarativos: `unique`, `not_null`, `accepted_values`, `relationships`.
- **Documentación** y linaje generados automáticamente.
- Todo vive en Git: revisiones, historial, CI.

Capas recomendadas: `staging` (limpieza 1:1 con el origen) → `intermediate` (lógica reutilizable) → `marts` (tablas finales para negocio).

## 3. Calidad de datos

Confiar a ciegas en los datos es la causa nº 1 de dashboards equivocados. Dimensiones de calidad:

| Dimensión | Pregunta | Ejemplo de prueba |
|---|---|---|
| Completitud | ¿Faltan datos? | `% nulos en email < 2 %` |
| Unicidad | ¿Hay duplicados? | `id` único |
| Validez | ¿Respeta formato y rango? | `monto >= 0` |
| Consistencia | ¿Coincide entre tablas? | Todo `customer_id` de orders existe en customers |
| Frescura | ¿Está actualizado? | Último dato de hoy o de ayer |

**Cuándo ejecutar las pruebas:** después de cada carga. Si fallan, **detén** el pipeline antes de que el dato malo llegue al dashboard.
Herramientas: tests de dbt, Great Expectations, Soda.

## 4. Observabilidad básica

Registra duración y número de filas de cada tarea y define alertas (correo/Slack) para fallos y para anomalías
(hoy llegaron 90 % menos filas que ayer).

## Cómo sabes que dominas este tema

- Dibujas el DAG de un pipeline y explicas qué pasa si una tarea falla.
- Escribes tests de calidad para cada tabla importante.
- Sabes por qué cada tarea debe ser idempotente.
""",
        "exercises": [
            py("orq-orden", "Orden de ejecución de un DAG", "Ingeniería de datos: orquestación",
               "Escribe `orden_topologico(dag)`. `dag` es un diccionario `{tarea: [dependencias]}`. Devuelve una lista con **todas** las tareas en un orden válido "
               "(cada tarea después de sus dependencias). Si hay un ciclo, lanza `ValueError`.",
               starter="""
def orden_topologico(dag):
    # tu código aquí (pista: recorrido en profundidad con estados)
    pass
""",
               solution="""
def orden_topologico(dag):
    orden = []
    estado = {}

    def visitar(tarea):
        if estado.get(tarea) == "listo":
            return
        if estado.get(tarea) == "visitando":
            raise ValueError("ciclo detectado")
        estado[tarea] = "visitando"
        for dependencia in dag.get(tarea, []):
            visitar(dependencia)
        estado[tarea] = "listo"
        orden.append(tarea)

    for tarea in dag:
        visitar(tarea)
    return orden
""",
               tests="""
dag = {"reporte": ["limpiar"], "limpiar": ["cargar"], "cargar": [], "alertas": ["limpiar"]}
orden = orden_topologico(dag)
assert sorted(orden) == sorted(dag), "Deben aparecer todas las tareas exactamente una vez"
for tarea, deps in dag.items():
    for dep in deps:
        assert orden.index(dep) < orden.index(tarea), "'%s' debe ejecutarse antes que '%s'" % (dep, tarea)
try:
    orden_topologico({"a": ["b"], "b": ["a"]})
except ValueError:
    pass
else:
    raise AssertionError("Un ciclo debe lanzar ValueError")
""",
               hint="Marca cada tarea como 'visitando' al entrar y 'listo' al salir; encontrar una 'visitando' significa ciclo."),
            py("orq-calidad", "Reporte de calidad de datos", "Ingeniería de datos: calidad de datos",
               "Escribe `reporte_calidad(filas, obligatorias, clave)`. `filas` es una lista de diccionarios. Devuelve un diccionario con: `filas` (total), "
               "`nulos` (diccionario columna → cuántas filas la tienen vacía, es decir `None` o `''`, solo para las columnas `obligatorias`) y "
               "`duplicados` (cuántas filas repiten un valor ya visto de la columna `clave`).",
               starter="""
def reporte_calidad(filas, obligatorias, clave):
    # tu código aquí
    pass
""",
               solution="""
def reporte_calidad(filas, obligatorias, clave):
    nulos = {c: sum(1 for f in filas if f.get(c) in (None, "")) for c in obligatorias}
    vistos = set()
    duplicados = 0
    for fila in filas:
        valor = fila.get(clave)
        if valor in vistos:
            duplicados += 1
        vistos.add(valor)
    return {"filas": len(filas), "nulos": nulos, "duplicados": duplicados}
""",
               tests="""
filas = [
    {"id": 1, "email": "a@x.com", "pais": "VE"},
    {"id": 2, "email": "", "pais": "CO"},
    {"id": 2, "email": None, "pais": ""},
    {"id": 3, "email": "c@x.com", "pais": "CL"},
]
res = reporte_calidad(filas, ["email", "pais"], "id")
assert res == {"filas": 4, "nulos": {"email": 2, "pais": 1}, "duplicados": 1}, "Obtuve %r" % (res,)
""",
               hint="Usa un set de claves vistas para contar repetidos."),
            quiz("orq-quiz-retry", "Reintentos seguros", "Ingeniería de datos: orquestación",
                 "Configuras 3 reintentos automáticos en una tarea que inserta ventas. ¿Qué condición necesitas para que reintentar no duplique datos?",
                 ["Que la tarea sea idempotente", "Que la tabla no tenga índices", "Que se ejecute siempre de madrugada", "Que use pandas"], 0,
                 "Si la tarea es idempotente (upsert, reemplazo de partición, transacción), ejecutarla otra vez deja el mismo resultado."),
            quiz("orq-quiz-dbt", "Capas en dbt", "Ingeniería de datos: orquestación",
                 "¿Dónde pondrías la limpieza básica (renombrar columnas, convertir tipos) de una tabla recién cargada?",
                 ["En los marts, junto con las métricas", "En un modelo de staging por cada tabla de origen", "En el dashboard", "En el origen, modificando producción"], 1,
                 "La capa de staging hace una limpieza 1:1 con cada fuente. Así las capas superiores trabajan con datos consistentes."),
            quiz("orq-quiz-calidad", "Prueba que falla", "Ingeniería de datos: calidad de datos",
                 "Después de la carga, la prueba 'id único' falla. ¿Qué haces?",
                 ["Ignorarla y publicar el dashboard", "Detener el pipeline, investigar el origen de los duplicados y corregirlo antes de publicar",
                  "Borrar la prueba", "Cambiar el dashboard para que no muestre duplicados"], 1,
                 "Las pruebas de calidad existen para frenar datos malos antes de que lleguen a quien toma decisiones."),
        ],
    },
    {
        "slug": "de-cloud",
        "phase": "de",
        "title": "Cloud, data lakes y formatos de datos",
        "summary": "Almacenamiento de objetos, warehouses en la nube, Parquet, particionado, batch vs streaming y costos.",
        "hours": 10,
        "theory": r"""
# Cloud, data lakes y formatos de datos

La mayoría de empresas ejecutan sus datos en la nube (AWS, Google Cloud, Azure). No necesitas dominar los tres: aprende **los
conceptos** con uno y se transfieren a los demás.

## 1. Los bloques de construcción

| Concepto | Qué es | Ejemplos |
|---|---|---|
| **Almacenamiento de objetos** | Archivos baratos y prácticamente ilimitados | Amazon S3, Google Cloud Storage, Azure Blob |
| **Data lake** | Zona de almacenamiento con datos crudos y semiestructurados | Carpetas en S3 con CSV/JSON/Parquet |
| **Data warehouse** | Base analítica SQL, muy rápida para agregaciones | BigQuery, Snowflake, Redshift |
| **Lakehouse** | Lake con capacidades de warehouse (transacciones, SQL) | Delta Lake, Iceberg |
| **Cómputo** | Máquinas/servicios que ejecutan tus jobs | Contenedores, funciones serverless, Spark |

## 2. Formatos de archivo

| Formato | Pros | Contras |
|---|---|---|
| **CSV** | Universal, legible | Sin tipos, pesado, frágil con comas y saltos de línea |
| **JSON** | Flexible, ideal para APIs | Verboso, lento para analítica |
| **Parquet** | **Columnar**, comprimido, con tipos; el estándar analítico | No legible a simple vista |

Un formato **columnar** guarda cada columna junta: si tu consulta usa 3 de 50 columnas, solo lee esas 3. Pasar de CSV a Parquet suele reducir tamaño y costo varias veces.

## 3. Particionado

Organiza los archivos por una columna usada para filtrar, normalmente la fecha:

```
s3://empresa-datos/ventas/year=2024/month=03/day=15/ventas.parquet
```

Así una consulta de "marzo de 2024" **no lee** el resto de los datos. Elige columnas con cardinalidad media (la fecha sí; el id de cliente no).

## 4. Batch vs streaming

- **Batch:** procesas en bloques (cada hora o día). Simple y barato; suficiente para la mayoría de los casos.
- **Streaming:** procesas evento a evento en segundos (Kafka, Kinesis). Más complejo; úsalo solo cuando el negocio **necesita** baja latencia (detección de fraude, alertas).

## 5. Costos

En la nube pagas por **almacenamiento** y por **cómputo / datos escaneados**. Hábitos que ahorran dinero:

- Filtra por columnas de partición y selecciona solo las columnas necesarias (nunca `SELECT *` en un warehouse columnar).
- Usa Parquet y comprime.
- Apaga o dimensiona bien los recursos; define **alertas de presupuesto**.
- Elimina datos temporales con reglas de ciclo de vida.

## 6. Seguridad mínima

- **Principio de mínimo privilegio** (IAM): cada servicio solo con los permisos que necesita.
- Nunca claves en el código: usa gestores de secretos o roles.
- Cifrado en reposo y en tránsito (casi siempre viene activado por defecto).
- Cuidado con datos personales (GDPR/LOPD): anonimiza o limita el acceso.

## Cómo sabes que dominas este tema

- Explicas la diferencia entre data lake y data warehouse.
- Justificas por qué usar Parquet y particionado.
- Sabes cuándo NO necesitas streaming.
""",
        "exercises": [
            py("cloud-particion", "Ruta de partición", "Ingeniería de datos: cloud",
               "Escribe `ruta_particion(fecha_iso, archivo)` que reciba una fecha `'AAAA-MM-DD'` y el nombre de un archivo y devuelva la ruta particionada "
               "estilo Hive: `'year=2024/month=03/day=15/archivo.parquet'`.",
               starter="""
def ruta_particion(fecha_iso, archivo):
    # tu código aquí
    pass
""",
               solution="""
def ruta_particion(fecha_iso, archivo):
    anio, mes, dia = fecha_iso.split("-")
    return "year=%s/month=%s/day=%s/%s" % (anio, mes, dia, archivo)
""",
               tests="""
assert ruta_particion("2024-03-15", "ventas.parquet") == "year=2024/month=03/day=15/ventas.parquet"
assert ruta_particion("2025-12-01", "a.parquet") == "year=2025/month=12/day=01/a.parquet", "Conserva los ceros a la izquierda"
"""),
            quiz("cloud-quiz-formato", "Elegir el formato", "Ingeniería de datos: cloud",
                 "Almacenas 2 TB de eventos y tus analistas consultan casi siempre 4 columnas de 60. ¿Qué formato reduce más el costo y el tiempo de consulta?",
                 ["CSV", "JSON", "Parquet", "Un PDF"], 2,
                 "Parquet es columnar y comprimido: solo lee las columnas que la consulta necesita."),
            quiz("cloud-quiz-stream", "Batch o streaming", "Ingeniería de datos: cloud",
                 "El equipo comercial revisa un informe de ventas cada mañana. ¿Qué arquitectura es más razonable?",
                 ["Streaming con Kafka para actualizar cada segundo", "Un proceso batch nocturno", "Un servidor manual que alguien ejecuta cuando se acuerde", "Ninguna, usar hojas de cálculo"], 1,
                 "Si nadie necesita el dato en tiempo real, el batch es más simple, barato y fiable."),
            quiz("cloud-quiz-lake", "Lake vs warehouse", "Ingeniería de datos: cloud",
                 "¿Cuál es la diferencia más útil entre un data lake y un data warehouse?",
                 ["No hay ninguna", "El lake guarda datos crudos y variados a bajo costo; el warehouse ofrece SQL rápido sobre datos modelados",
                  "El warehouse solo guarda imágenes", "El lake solo existe en AWS"], 1,
                 "El lake es flexible y barato (crudo); el warehouse está optimizado para consultas analíticas sobre datos limpios y estructurados."),
        ],
    },
    {
        "slug": "proyecto-pipeline",
        "phase": "de",
        "title": "Proyecto 2: pipeline de datos de punta a punta",
        "summary": "Tu pieza de portafolio de ingeniería de datos: API → Python → PostgreSQL → dashboard, orquestado y probado.",
        "hours": 24,
        "theory": r"""
# Proyecto 2: pipeline de datos de punta a punta

Este es el proyecto que te diferencia como **ingeniero de datos**: demuestra que sabes mover datos de forma fiable, no solo analizarlos.

## 1. Idea

Construye un pipeline que **cada día** descargue datos de una fuente real, los limpie, los cargue en PostgreSQL con un modelo dimensional
y alimente un dashboard. Fuentes con API gratuita y datos que cambian: clima, criptomonedas, calidad del aire, transporte público, partidos deportivos, precios, noticias.

## 2. Arquitectura sugerida

```
API pública ──► extract.py ──► raw (JSON/Parquet) ──► transform.py ──► PostgreSQL (staging)
                                                                   └─► marts (hechos + dimensiones)
                                                                            └─► Dashboard (Metabase / Looker Studio)
Orquestación: Prefect o Airflow (o cron dentro de Docker)  ·  Contenedores: docker compose
```

## 3. Requisitos mínimos (lo que te hará destacar)

1. **Idempotente:** puedes ejecutarlo dos veces el mismo día sin duplicar datos.
2. **Carga incremental** con un marcador de la última fecha cargada.
3. **Modelo dimensional:** al menos 1 tabla de hechos y 2 dimensiones.
4. **Pruebas de calidad** (unicidad, nulos, rangos) que detienen el pipeline si fallan.
5. **Logging** claro y manejo de errores con reintentos.
6. **Configuración por variables de entorno** (sin claves en Git).
7. **Todo en Docker:** `docker compose up` levanta PostgreSQL, el pipeline y el dashboard.
8. **README profesional** con diagrama, decisiones técnicas, cómo ejecutarlo y capturas.

## 4. Plan de trabajo (≈ 24 horas)

| Horas | Etapa |
|---|---|
| 3 | Elegir la API, explorar los datos y diseñar el modelo |
| 5 | Extracción y transformación con pruebas unitarias |
| 4 | Carga a PostgreSQL (upserts, incremental) |
| 3 | Pruebas de calidad y logging |
| 3 | Orquestación y Docker |
| 3 | Dashboard |
| 3 | README, diagrama y publicación |

## 5. Extras que impresionan

- **dbt** para la capa de marts.
- **CI** con GitHub Actions que corre los tests.
- Un **diagrama de arquitectura** (draw.io o Mermaid).
- Una sección "decisiones y trade-offs": por qué elegiste batch, por qué ese grano, qué mejorarías con más tiempo.

## 6. Errores comunes

- Sin pruebas ni manejo de errores (un script que funciona "a veces").
- Credenciales en el repositorio.
- Pipeline que duplica datos al reejecutarse.
- README que no permite reproducir nada.

> Cuando termines, publica el repositorio y escribe un post en LinkedIn explicando **un problema real** que resolviste (por ejemplo, cómo lograste la idempotencia).
""",
        "exercises": [
            quiz("pipe-quiz-1", "Priorizar requisitos", "Proyecto: pipeline de datos",
                 "Tienes poco tiempo. ¿Cuál de estos requisitos es **más importante** incluir primero?",
                 ["Un diagrama animado en 3D", "Que el pipeline sea idempotente y tenga pruebas de calidad", "Usar la herramienta más de moda", "Agregar 10 fuentes de datos"], 1,
                 "La fiabilidad (idempotencia + calidad) es lo que distingue un pipeline profesional de un script frágil."),
            checklist("pipe-entregables", "Entregables del proyecto", "Proyecto: pipeline de datos",
                      "Marca cada punto cuando esté listo en tu repositorio.",
                      ["Elegí una API real y diseñé el modelo (1 hecho + 2 dimensiones)", "La extracción maneja errores, timeouts y reintentos",
                       "Las transformaciones tienen pruebas unitarias", "La carga es idempotente (upsert o reemplazo de partición)",
                       "Hay carga incremental con marcador", "Hay pruebas de calidad que detienen el pipeline",
                       "Todo se levanta con docker compose up", "Hay un dashboard conectado a PostgreSQL",
                       "El README incluye diagrama, decisiones y capturas", "Publiqué el repositorio y un post explicando un reto"]),
            checklist("pipe-revision", "Revisión final", "Proyecto: pipeline de datos",
                      "Antes de publicar, revisa estos puntos.",
                      ["Ejecuté el pipeline dos veces seguidas y no hubo duplicados", "No hay secretos en el repositorio ni en el historial",
                       "Un compañero pudo ejecutarlo siguiendo solo el README", "Puedo explicar cada decisión técnica en una entrevista"]),
        ],
    },
]
