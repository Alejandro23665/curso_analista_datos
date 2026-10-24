from ._helpers import quiz, sql

TABLAS = r"""
## Las tablas de práctica

Todos los ejercicios usan la misma base de datos (pestaña **Tablas** del editor): `customers`, `products`,
`orders`, `order_items` y `employees`. Los textos no llevan tildes (por ejemplo `Tecnologia`, `Mexico`) para que
no tengas que preocuparte por ellas al escribir.
"""

TOPICS = [
    {
        "slug": "sql-select",
        "phase": "sql",
        "title": "SELECT, filtros y orden",
        "summary": "Consulta una tabla: columnas, WHERE, ORDER BY, LIMIT, DISTINCT, LIKE, IN, BETWEEN y NULL.",
        "hours": 8,
        "theory": r"""
# SELECT, filtros y orden

SQL es un lenguaje **declarativo**: describes *qué* datos quieres, no *cómo* obtenerlos. Casi todo análisis
empieza con una consulta `SELECT`.

## Estructura básica

```sql
SELECT columna1, columna2
FROM tabla
WHERE condicion
ORDER BY columna1 DESC
LIMIT 10;
```

El orden **escrito** es ese, pero el motor lo **evalúa** así: `FROM` → `WHERE` → `SELECT` → `ORDER BY` → `LIMIT`.
Entender esto explica muchos errores (por ejemplo, por qué no puedes usar un alias del `SELECT` dentro del `WHERE`).

## Filtrar con WHERE

| Necesitas | Operador | Ejemplo |
|---|---|---|
| Comparar | `=  <>  <  >  <=  >=` | `price > 100` |
| Varios valores | `IN` | `country IN ('Chile', 'Mexico')` |
| Rango (incluye extremos) | `BETWEEN` | `order_date BETWEEN '2024-03-01' AND '2024-03-31'` |
| Patrón de texto | `LIKE` | `name LIKE 'A%'` (`%` = cualquier cantidad de caracteres) |
| Combinar | `AND`, `OR`, `NOT` | `status = 'completado' AND channel = 'web'` |

Usa paréntesis cuando mezcles `AND` y `OR`: `AND` se evalúa antes y suele sorprender.

## NULL no es un valor, es "desconocido"

`NULL = NULL` no es verdadero. Para comprobarlo usa `IS NULL` / `IS NOT NULL`. Cualquier comparación con `NULL`
da "desconocido" y la fila **no** pasa el filtro.

## Ordenar, limitar y quitar duplicados

```sql
SELECT DISTINCT country FROM customers ORDER BY country;
SELECT name, price FROM products ORDER BY price DESC, name ASC LIMIT 5;
```

`LIMIT` sin `ORDER BY` devuelve filas en un orden **no garantizado**. Si importa cuáles filas salen, ordena.

## Buenas prácticas desde el primer día

- Evita `SELECT *` en consultas que vayan a producción: pide solo las columnas necesarias.
- Escribe palabras clave en MAYÚSCULAS y un `FROM`/`WHERE` por línea. Tu yo del futuro (y tus compañeros) lo agradecerán.
- Los textos van entre comillas **simples**: `'Chile'`.
""" + TABLAS + r"""
## Cómo sabes que dominas este tema

- Traduces una pregunta de negocio ("clientes de Chile registrados en 2024") a un `WHERE` correcto.
- Sabes por qué `WHERE columna = NULL` no funciona.
- Distingues `BETWEEN` (inclusivo) de `<` y `>`.
""",
        "exercises": [
            sql("sql-select-1", "Productos caros", "SQL: SELECT y filtros",
                "Muestra el **nombre** y el **precio** de los productos con precio mayor a 100, del más caro al más barato.",
                "SELECT name, price FROM products WHERE price > 100 ORDER BY price DESC",
                starter="SELECT name, price\nFROM products\n", ordered=True,
                hint="Necesitas WHERE price > 100 y ORDER BY price DESC."),
            sql("sql-select-2", "Clientes de dos países", "SQL: SELECT y filtros",
                "Lista el nombre y el país de los clientes de **Venezuela** o **Colombia**, ordenados alfabéticamente por nombre.",
                "SELECT name, country FROM customers WHERE country IN ('Venezuela', 'Colombia') ORDER BY name",
                starter="SELECT name, country\nFROM customers\n", ordered=True,
                hint="IN ('Venezuela', 'Colombia')"),
            sql("sql-select-3", "Pedidos completados de marzo de 2024", "SQL: SELECT y filtros",
                "Muestra `id` y `order_date` de los pedidos con estado `completado` realizados entre el 1 y el 31 de marzo de 2024, "
                "ordenados por fecha y luego por id.",
                "SELECT id, order_date FROM orders WHERE status = 'completado' "
                "AND order_date BETWEEN '2024-03-01' AND '2024-03-31' ORDER BY order_date, id",
                starter="SELECT id, order_date\nFROM orders\n", ordered=True,
                hint="BETWEEN incluye ambos extremos."),
            sql("sql-select-4", "Países con clientes", "SQL: SELECT y filtros",
                "Lista los países distintos donde hay clientes, ordenados alfabéticamente.",
                "SELECT DISTINCT country FROM customers ORDER BY country",
                starter="SELECT \nFROM customers\n", ordered=True, hint="DISTINCT elimina duplicados."),
            sql("sql-select-5", "Nombres que empiezan con A", "SQL: SELECT y filtros",
                "Muestra el nombre de los clientes cuyo nombre **empieza con la letra A** (mayúscula), ordenados alfabéticamente.",
                "SELECT name FROM customers WHERE name LIKE 'A%' ORDER BY name",
                starter="SELECT name\nFROM customers\n", ordered=True, hint="LIKE 'A%'"),
            quiz("sql-select-q1", "Comparar con NULL", "SQL: SELECT y filtros",
                 "Quieres las filas donde `manager_id` no tiene valor. ¿Qué condición es correcta?",
                 ["WHERE manager_id = NULL", "WHERE manager_id IS NULL", "WHERE manager_id = ''", "WHERE NOT manager_id"], 1,
                 "`NULL` representa un valor desconocido; ninguna comparación con `=` es verdadera. Se usa `IS NULL`."),
        ],
    },
    {
        "slug": "sql-agregaciones",
        "phase": "sql",
        "title": "Agregaciones y GROUP BY",
        "summary": "COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING y CASE para resumir datos.",
        "hours": 10,
        "theory": r"""
# Agregaciones y GROUP BY

Un analista rara vez mira filas sueltas: resume. Las **funciones de agregación** convierten muchas filas en un valor.

| Función | Qué hace |
|---|---|
| `COUNT(*)` | Cuenta filas |
| `COUNT(columna)` | Cuenta filas donde la columna **no es NULL** |
| `COUNT(DISTINCT columna)` | Cuenta valores distintos |
| `SUM`, `AVG`, `MIN`, `MAX` | Suma, promedio, mínimo y máximo (ignoran NULL) |

```sql
SELECT COUNT(*) AS pedidos, MIN(order_date) AS primero, MAX(order_date) AS ultimo
FROM orders;
```

## GROUP BY: un resumen por grupo

```sql
SELECT status, COUNT(*) AS total
FROM orders
GROUP BY status
ORDER BY total DESC;
```

**Regla de oro:** toda columna del `SELECT` que no esté dentro de una agregación debe aparecer en el `GROUP BY`.

## WHERE vs HAVING

- `WHERE` filtra **filas antes** de agrupar.
- `HAVING` filtra **grupos después** de agrupar (aquí sí puedes usar agregaciones).

```sql
SELECT customer_id, COUNT(*) AS pedidos
FROM orders
WHERE status = 'completado'      -- primero filtra filas
GROUP BY customer_id
HAVING COUNT(*) > 5;             -- luego filtra grupos
```

## CASE: crear categorías

```sql
SELECT
  CASE WHEN price < 50 THEN 'barato'
       WHEN price < 150 THEN 'medio'
       ELSE 'premium' END AS rango,
  COUNT(*) AS productos
FROM products
GROUP BY 1;     -- 1 = primera columna del SELECT
```

## Trampas frecuentes

- **Promedio con NULL:** `AVG` ignora los NULL; si necesitas tratarlos como 0 usa `COALESCE(col, 0)`.
- **Divisiones enteras:** en algunos motores `5 / 2 = 2`. Multiplica por `1.0` para forzar decimales.
- **Redondeo:** usa `ROUND(valor, 2)` solo para mostrar; no redondees en pasos intermedios.
""" + TABLAS + r"""
## Cómo sabes que dominas este tema

- Explicas la diferencia entre `WHERE` y `HAVING` con un ejemplo.
- Sabes qué cuenta `COUNT(*)` frente a `COUNT(columna)`.
- Creas segmentos con `CASE` y los cuentas con `GROUP BY`.
""",
        "exercises": [
            sql("sql-agg-1", "Pedidos por estado", "SQL: agregaciones y GROUP BY",
                "Cuenta cuántos pedidos hay por `status`. Devuelve `status` y `total`, de mayor a menor total (si hay empate, por status).",
                "SELECT status, COUNT(*) AS total FROM orders GROUP BY status ORDER BY total DESC, status",
                starter="SELECT status, COUNT(*) AS total\nFROM orders\n", ordered=True),
            sql("sql-agg-2", "Resumen de precios por categoría", "SQL: agregaciones y GROUP BY",
                "Por cada categoría de producto muestra el precio promedio (redondeado a 2 decimales) como `promedio`, "
                "el mínimo como `minimo` y el máximo como `maximo`. Ordena por categoría.",
                "SELECT category, ROUND(AVG(price), 2) AS promedio, MIN(price) AS minimo, MAX(price) AS maximo "
                "FROM products GROUP BY category ORDER BY category",
                starter="SELECT category,\nFROM products\n", ordered=True),
            sql("sql-agg-3", "Clientes frecuentes", "SQL: HAVING",
                "Muestra los clientes (`customer_id`) con **más de 5 pedidos**, junto con su número de pedidos (`pedidos`). "
                "Ordena de más a menos pedidos y, en empate, por customer_id.",
                "SELECT customer_id, COUNT(*) AS pedidos FROM orders GROUP BY customer_id "
                "HAVING COUNT(*) > 5 ORDER BY pedidos DESC, customer_id",
                starter="SELECT customer_id, COUNT(*) AS pedidos\nFROM orders\n", ordered=True,
                hint="La condición sobre COUNT(*) va en HAVING, no en WHERE."),
            sql("sql-agg-4", "Rangos de precio con CASE", "SQL: CASE",
                "Clasifica los productos en `rango`: `barato` (precio < 50), `medio` (< 150) o `premium` (el resto) "
                "y cuenta cuántos productos hay en cada rango (`productos`). Ordena por productos de mayor a menor y, en empate, por rango.",
                "SELECT CASE WHEN price < 50 THEN 'barato' WHEN price < 150 THEN 'medio' ELSE 'premium' END AS rango, "
                "COUNT(*) AS productos FROM products GROUP BY 1 ORDER BY productos DESC, rango",
                starter="SELECT\n  CASE\n    WHEN price < 50 THEN 'barato'\n    -- completa aquí\n  END AS rango,\n  COUNT(*) AS productos\nFROM products\n",
                ordered=True),
            sql("sql-agg-5", "Pedidos y clientes únicos por canal", "SQL: agregaciones y GROUP BY",
                "Para cada `channel` muestra el total de pedidos (`pedidos`) y cuántos clientes distintos compraron (`clientes`). Ordena por channel.",
                "SELECT channel, COUNT(*) AS pedidos, COUNT(DISTINCT customer_id) AS clientes FROM orders "
                "GROUP BY channel ORDER BY channel",
                starter="SELECT channel,\nFROM orders\n", ordered=True, hint="COUNT(DISTINCT columna)"),
            quiz("sql-agg-q1", "WHERE o HAVING", "SQL: HAVING",
                 "Quieres los departamentos cuyo salario promedio supera 4000. ¿Dónde va esa condición?",
                 ["En WHERE, porque filtra filas", "En HAVING, porque filtra grupos ya agregados",
                  "En ORDER BY", "En cualquiera de los dos, es igual"], 1,
                 "`WHERE` se evalúa antes de agrupar y no puede usar agregaciones. `HAVING` filtra los grupos resultantes."),
        ],
    },
    {
        "slug": "sql-joins",
        "phase": "sql",
        "title": "JOINs: combinar tablas",
        "summary": "INNER y LEFT JOIN, varios JOIN encadenados, anti-joins y auto-joins.",
        "hours": 12,
        "theory": r"""
# JOINs: combinar tablas

Los datos están repartidos en tablas relacionadas (un pedido pertenece a un cliente, contiene productos...). Un
`JOIN` las une usando una condición, normalmente **clave foránea = clave primaria**.

```sql
SELECT o.id, c.name, o.order_date
FROM orders o
JOIN customers c ON c.id = o.customer_id;
```

`o` y `c` son **alias**: hacen la consulta más corta y evitan ambigüedades.

## Tipos de JOIN

| Tipo | Devuelve |
|---|---|
| `INNER JOIN` (o `JOIN`) | Solo las filas con pareja en **ambas** tablas |
| `LEFT JOIN` | Todas las filas de la izquierda; si no hay pareja, las columnas de la derecha salen `NULL` |
| `RIGHT JOIN` | Lo mismo pero al revés (se usa poco; cambia el orden y usa `LEFT`) |
| `FULL JOIN` | Todo de ambos lados (útil para conciliaciones) |

## El patrón "anti-join": lo que NO tiene pareja

```sql
SELECT c.id, c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;      -- clientes que nunca compraron
```

## Encadenar varios JOIN

```sql
SELECT p.category, SUM(oi.quantity * oi.unit_price) AS ingresos
FROM order_items oi
JOIN products p ON p.id = oi.product_id
JOIN orders o   ON o.id = oi.order_id
WHERE o.status = 'completado'
GROUP BY p.category;
```

## Auto-join: una tabla contra sí misma

`employees.manager_id` apunta a otro empleado. Para ver empleado y jefe unes la tabla consigo misma con dos alias:

```sql
SELECT e.name AS empleado, m.name AS jefe
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id;
```

## Errores que cuestan caro

- **Multiplicación de filas:** si unes por una columna que **no es única** en una de las tablas, las filas se
  duplican y tus `SUM` salen inflados. Antes de sumar, comprueba cuántas filas devuelve el JOIN.
- **LEFT JOIN + WHERE:** poner en el `WHERE` una condición sobre la tabla derecha convierte el `LEFT JOIN` en
  `INNER JOIN` (descarta los NULL). Pon esa condición en el `ON`.
- **Unir por columnas equivocadas** produce un producto cartesiano (todas contra todas).
""" + TABLAS + r"""
## Cómo sabes que dominas este tema

- Dibujas en papel qué filas devolvería un `INNER` y un `LEFT` con dos tablas pequeñas.
- Encuentras registros huérfanos o sin actividad con un anti-join.
- Detectas cuando un JOIN duplica filas.
""",
        "exercises": [
            sql("sql-joins-1", "Pedidos con el nombre del cliente", "SQL: JOINs",
                "Muestra `id` del pedido, nombre del cliente (`name`) y `order_date` de los **primeros 15 pedidos completados** "
                "(ordenados por id del pedido).",
                "SELECT o.id, c.name, o.order_date FROM orders o JOIN customers c ON c.id = o.customer_id "
                "WHERE o.status = 'completado' ORDER BY o.id LIMIT 15",
                starter="SELECT o.id, c.name, o.order_date\nFROM orders o\n", ordered=True),
            sql("sql-joins-2", "Clientes que nunca han comprado", "SQL: JOINs",
                "Lista `id` y `name` de los clientes **sin ningún pedido**, ordenados por id.",
                "SELECT c.id, c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id "
                "WHERE o.id IS NULL ORDER BY c.id",
                starter="SELECT c.id, c.name\nFROM customers c\n", ordered=True,
                hint="LEFT JOIN y filtra donde la columna de orders sea NULL."),
            sql("sql-joins-3", "Ingresos por categoría", "SQL: JOINs",
                "Calcula los ingresos (`quantity * unit_price`) por categoría de producto, **solo de pedidos completados**. "
                "Devuelve `category` e `ingresos` (redondeado a 2 decimales), de mayor a menor ingreso.",
                "SELECT p.category, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS ingresos FROM order_items oi "
                "JOIN products p ON p.id = oi.product_id JOIN orders o ON o.id = oi.order_id "
                "WHERE o.status = 'completado' GROUP BY p.category ORDER BY ingresos DESC",
                starter="SELECT p.category, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS ingresos\nFROM order_items oi\n",
                ordered=True, hint="Necesitas unir order_items con products y con orders."),
            sql("sql-joins-4", "Productos nunca vendidos", "SQL: JOINs",
                "Muestra el nombre de los productos que **nunca** aparecen en `order_items`, ordenados alfabéticamente.",
                "SELECT p.name FROM products p LEFT JOIN order_items oi ON oi.product_id = p.id "
                "WHERE oi.id IS NULL ORDER BY p.name",
                starter="SELECT p.name\nFROM products p\n", ordered=True),
            sql("sql-joins-5", "Empleado y su jefe", "SQL: JOINs",
                "Muestra el nombre de cada empleado (`empleado`) y el nombre de su jefe (`jefe`). "
                "Incluye a quien no tiene jefe (su `jefe` será NULL). Ordena por el id del empleado.",
                "SELECT e.name AS empleado, m.name AS jefe FROM employees e LEFT JOIN employees m "
                "ON m.id = e.manager_id ORDER BY e.id",
                starter="SELECT e.name AS empleado, m.name AS jefe\nFROM employees e\n", ordered=True,
                hint="Une employees consigo misma con dos alias."),
            quiz("sql-joins-q1", "Cuántas filas devuelve un LEFT JOIN", "SQL: JOINs",
                 "`customers` tiene 40 filas y 6 de ellos no tienen pedidos. Haces `customers LEFT JOIN orders` y cada cliente con "
                 "pedidos tiene varios. Sobre el número de filas del resultado, ¿qué es cierto?",
                 ["Es exactamente 40", "Es como mínimo 40 (los clientes sin pedidos aparecen una vez)",
                  "Es menor que 40", "No se puede saber nunca"], 1,
                 "Un LEFT JOIN conserva todas las filas de la izquierda y repite la fila de un cliente por cada pedido. "
                 "Por eso el resultado tiene al menos tantas filas como `customers`."),
        ],
    },
    {
        "slug": "sql-subconsultas-cte",
        "phase": "sql",
        "title": "Subconsultas y CTE",
        "summary": "Consultas dentro de consultas, WITH (CTE), EXISTS y cómo estructurar SQL legible.",
        "hours": 10,
        "theory": r"""
# Subconsultas y CTE

Cuando una pregunta tiene varios pasos ("clientes cuyo gasto supera el **promedio** de gasto"), necesitas
construir resultados intermedios. Tienes tres herramientas.

## 1. Subconsulta escalar (devuelve un valor)

```sql
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

## 2. CTE con `WITH`: nombrar pasos intermedios

Una **CTE** (Common Table Expression) es una consulta con nombre que puedes usar después como si fuera una tabla.
Hace el SQL legible de arriba hacia abajo, como una receta.

```sql
WITH gasto AS (
  SELECT o.customer_id, SUM(oi.quantity * oi.unit_price) AS total
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.id
  WHERE o.status = 'completado'
  GROUP BY o.customer_id
)
SELECT c.name, ROUND(g.total, 2) AS total
FROM gasto g
JOIN customers c ON c.id = g.customer_id
WHERE g.total > (SELECT AVG(total) FROM gasto);
```

Puedes encadenar varias CTE separadas por comas. En entrevistas y en el trabajo, **una CTE bien nombrada vale más
que tres subconsultas anidadas**.

## 3. EXISTS / NOT EXISTS: "¿hay alguna fila que...?"

```sql
SELECT c.name
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.id AND o.status = 'cancelado'
);
```

La subconsulta se refiere a `c` de la consulta externa: es una **subconsulta correlacionada**. `EXISTS` se detiene
en cuanto encuentra una fila, y `NOT EXISTS` es la forma más segura de escribir "no tiene ninguno".

## IN vs EXISTS vs JOIN

- `IN (subconsulta)`: simple cuando comparas contra una lista pequeña. Cuidado con `NOT IN` si la subconsulta puede
  devolver `NULL`: el resultado queda vacío. Prefiere `NOT EXISTS`.
- `JOIN`: cuando además necesitas columnas de la otra tabla.
- `EXISTS`: cuando solo importa si existe coincidencia.

## Consejos de estilo

1. Un paso por CTE, con un nombre que diga qué contiene (`gasto_por_cliente`, no `t1`).
2. Prueba cada CTE por separado antes de encadenarlas.
3. Si una subconsulta correlacionada se ejecuta por cada fila y la consulta va lenta, intenta reescribirla con `JOIN` + `GROUP BY` o con funciones de ventana.
""" + TABLAS + r"""
## Cómo sabes que dominas este tema

- Conviertes una pregunta de varios pasos en una cadena de CTE.
- Sabes cuándo usar `EXISTS` en lugar de `IN`.
- Evitas `NOT IN` cuando puede haber NULL.
""",
        "exercises": [
            sql("sql-cte-1", "Productos sobre el precio promedio", "SQL: subconsultas y CTE",
                "Muestra nombre y precio de los productos **más caros que el precio promedio** de todos los productos. "
                "Ordena de más caro a más barato y, en empate, por nombre.",
                "SELECT name, price FROM products WHERE price > (SELECT AVG(price) FROM products) ORDER BY price DESC, name",
                starter="SELECT name, price\nFROM products\n", ordered=True),
            sql("sql-cte-2", "Clientes con gasto sobre el promedio", "SQL: subconsultas y CTE",
                "Calcula el gasto total de cada cliente en pedidos **completados** (`quantity * unit_price`). Devuelve el `name` y el `total` "
                "(redondeado a 2 decimales) de los clientes cuyo gasto supera el **promedio de gasto entre clientes**. Orden: mayor gasto primero.",
                """WITH gasto AS (
  SELECT o.customer_id, SUM(oi.quantity * oi.unit_price) AS total
  FROM orders o JOIN order_items oi ON oi.order_id = o.id
  WHERE o.status = 'completado'
  GROUP BY o.customer_id
)
SELECT c.name, ROUND(g.total, 2) AS total
FROM gasto g JOIN customers c ON c.id = g.customer_id
WHERE g.total > (SELECT AVG(total) FROM gasto)
ORDER BY g.total DESC""",
                starter="WITH gasto AS (\n  -- gasto total por cliente\n)\nSELECT\nFROM gasto\n", ordered=True,
                hint="Primero la CTE con el total por cliente; luego compara contra (SELECT AVG(total) FROM gasto)."),
            sql("sql-cte-3", "Clientes que compraron Tecnologia", "SQL: subconsultas y CTE",
                "Lista el nombre de los clientes que han comprado **al menos un producto** de la categoría `Tecnologia` "
                "(en cualquier pedido). Usa `EXISTS`. Ordena por nombre.",
                """SELECT c.name FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  JOIN order_items oi ON oi.order_id = o.id
  JOIN products p ON p.id = oi.product_id
  WHERE o.customer_id = c.id AND p.category = 'Tecnologia'
)
ORDER BY c.name""",
                starter="SELECT c.name\nFROM customers c\nWHERE EXISTS (\n  -- subconsulta correlacionada\n)\nORDER BY c.name", ordered=True),
            sql("sql-cte-4", "Top 3 productos por unidades vendidas", "SQL: subconsultas y CTE",
                "Con una CTE, calcula las unidades vendidas (`SUM(quantity)`) por producto y devuelve el `name` y `unidades` de los **3 más vendidos**. "
                "Desempata por nombre.",
                """WITH ventas AS (
  SELECT product_id, SUM(quantity) AS unidades FROM order_items GROUP BY product_id
)
SELECT p.name, v.unidades
FROM ventas v JOIN products p ON p.id = v.product_id
ORDER BY v.unidades DESC, p.name
LIMIT 3""",
                starter="WITH ventas AS (\n  SELECT product_id, SUM(quantity) AS unidades\n  FROM order_items\n  GROUP BY product_id\n)\nSELECT\nFROM ventas v\n",
                ordered=True),
            quiz("sql-cte-q1", "NOT IN y los NULL", "SQL: subconsultas y CTE",
                 "¿Por qué es peligroso `WHERE id NOT IN (SELECT manager_id FROM employees)`?",
                 ["Porque NOT IN es siempre más lento que NOT EXISTS",
                  "Porque si manager_id contiene algún NULL, el resultado queda vacío",
                  "Porque NOT IN no existe en PostgreSQL", "No tiene ningún peligro"], 1,
                 "Con `NOT IN`, si la lista incluye un `NULL` la comparación se vuelve 'desconocida' para todas las filas y no se devuelve nada. "
                 "`NOT EXISTS` no tiene ese problema."),
        ],
    },
    {
        "slug": "sql-ventanas",
        "phase": "sql",
        "title": "Funciones de ventana",
        "summary": "ROW_NUMBER, RANK, LAG/LEAD, sumas acumuladas y porcentajes sobre el total.",
        "hours": 12,
        "theory": r"""
# Funciones de ventana (window functions)

Son la herramienta que separa a quien "sabe SQL" de quien lo domina. Una función de ventana calcula un valor **por
cada fila** mirando un conjunto de filas relacionadas, **sin colapsar** las filas como hace `GROUP BY`.

```sql
función() OVER (
  PARTITION BY columna_grupo   -- reinicia el cálculo por grupo (opcional)
  ORDER BY columna_orden       -- define el orden dentro del grupo
)
```

## Ranking

| Función | Con empates (3200, 3200, 3500) |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3 (siempre únicos) |
| `RANK()` | 1, 1, 3 (salta posiciones) |
| `DENSE_RANK()` | 1, 1, 2 (no salta) |

```sql
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS posicion
FROM employees;
```

**Patrón estrella: "el último / el mejor de cada grupo".** Numeras con `ROW_NUMBER` y filtras en una consulta externa
(no puedes filtrar una ventana en el mismo `WHERE`):

```sql
SELECT * FROM (
  SELECT customer_id, id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, id DESC) AS rn
  FROM orders
) t
WHERE rn = 1;
```

## Comparar con la fila anterior: LAG y LEAD

```sql
SELECT mes, pedidos,
       pedidos - LAG(pedidos) OVER (ORDER BY mes) AS variacion
FROM mensual;
```

`LAG` mira hacia atrás y `LEAD` hacia delante; la primera fila no tiene anterior y devuelve `NULL`.

## Acumulados y porcentajes

```sql
SUM(venta) OVER (ORDER BY dia)                          -- suma acumulada
100.0 * salary / SUM(salary) OVER (PARTITION BY department)   -- % sobre el total del grupo
AVG(x) OVER (ORDER BY dia ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)  -- promedio móvil de 3
```

## Cómo pensar una consulta con ventanas

1. Escribe primero la consulta base (con CTE) que produce las filas que necesitas.
2. Añade la función de ventana como una columna nueva.
3. Si necesitas filtrar por el resultado de la ventana, envuélvelo en una CTE/subconsulta.

> **Para entrevistas:** "segundo salario más alto por departamento", "último pedido por cliente" y "variación mes a
> mes" son preguntas clásicas. Si te sale cada una sin mirar, vas muy bien.
""" + TABLAS + r"""
## Cómo sabes que dominas este tema

- Explicas la diferencia entre `ROW_NUMBER`, `RANK` y `DENSE_RANK`.
- Resuelves "top N por grupo" sin pensarlo.
- Calculas acumulados y variaciones periodo a periodo.
""",
        "exercises": [
            sql("sql-win-1", "Último pedido de cada cliente", "SQL: funciones de ventana",
                "Para cada cliente con pedidos, muestra su pedido más reciente: `customer_id`, `id` y `order_date`. "
                "Si hay dos pedidos el mismo día, toma el de mayor id. Ordena por customer_id.",
                """SELECT customer_id, id, order_date FROM (
  SELECT customer_id, id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, id DESC) AS rn
  FROM orders
) t
WHERE rn = 1
ORDER BY customer_id""",
                starter="SELECT customer_id, id, order_date FROM (\n  SELECT customer_id, id, order_date,\n         ROW_NUMBER() OVER (\n           -- completa\n         ) AS rn\n  FROM orders\n) t\nWHERE rn = 1\n",
                ordered=True),
            sql("sql-win-2", "Ranking de salarios por departamento", "SQL: funciones de ventana",
                "Muestra `name`, `department`, `salary` y `posicion`: el ranking del salario dentro de su departamento "
                "(mayor salario = 1) usando `RANK()`. Ordena por departamento, posición y nombre.",
                "SELECT name, department, salary, RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS posicion "
                "FROM employees ORDER BY department, posicion, name",
                starter="SELECT name, department, salary,\n       RANK() OVER (\n         -- completa\n       ) AS posicion\nFROM employees\n",
                ordered=True),
            sql("sql-win-3", "Variación mensual de pedidos", "SQL: funciones de ventana",
                "Cuenta los pedidos por mes (usa `SUBSTR(CAST(order_date AS TEXT), 1, 7)` para obtener el mes como 'AAAA-MM'). "
                "Devuelve `mes`, `pedidos` y `variacion` = pedidos del mes menos los del mes anterior (NULL en el primer mes). Ordena por mes.",
                """WITH mensual AS (
  SELECT SUBSTR(CAST(order_date AS TEXT), 1, 7) AS mes, COUNT(*) AS pedidos
  FROM orders
  GROUP BY 1
)
SELECT mes, pedidos, pedidos - LAG(pedidos) OVER (ORDER BY mes) AS variacion
FROM mensual
ORDER BY mes""",
                starter="WITH mensual AS (\n  SELECT SUBSTR(CAST(order_date AS TEXT), 1, 7) AS mes, COUNT(*) AS pedidos\n  FROM orders\n  GROUP BY 1\n)\nSELECT mes, pedidos\nFROM mensual\nORDER BY mes",
                ordered=True, hint="LAG(pedidos) OVER (ORDER BY mes)"),
            sql("sql-win-4", "Ventas acumuladas de enero 2024", "SQL: funciones de ventana",
                "Calcula la venta diaria (`SUM(quantity * unit_price)`) de pedidos **completados** entre el 2024-01-01 y el 2024-01-31. "
                "Devuelve `dia`, `venta` (redondeada a 2 decimales) y `acumulado` (suma acumulada, redondeada a 2 decimales). Ordena por día.",
                """WITH diario AS (
  SELECT o.order_date AS dia, SUM(oi.quantity * oi.unit_price) AS venta
  FROM orders o JOIN order_items oi ON oi.order_id = o.id
  WHERE o.status = 'completado' AND o.order_date BETWEEN '2024-01-01' AND '2024-01-31'
  GROUP BY o.order_date
)
SELECT dia, ROUND(venta, 2) AS venta, ROUND(SUM(venta) OVER (ORDER BY dia), 2) AS acumulado
FROM diario
ORDER BY dia""",
                starter="WITH diario AS (\n  -- venta por día\n)\nSELECT dia, venta\nFROM diario\nORDER BY dia", ordered=True),
            sql("sql-win-5", "Porcentaje del salario sobre su departamento", "SQL: funciones de ventana",
                "Muestra `name`, `department`, `salary` y `pct`: el porcentaje que representa su salario sobre la suma de salarios "
                "de su departamento, redondeado a 1 decimal. Ordena por departamento y nombre.",
                "SELECT name, department, salary, ROUND(100.0 * salary / SUM(salary) OVER (PARTITION BY department), 1) AS pct "
                "FROM employees ORDER BY department, name",
                starter="SELECT name, department, salary,\n       ROUND(100.0 * salary / SUM(salary) OVER (\n         -- completa\n       ), 1) AS pct\nFROM employees\n",
                ordered=True),
            quiz("sql-win-q1", "RANK, DENSE_RANK y ROW_NUMBER", "SQL: funciones de ventana",
                 "Los salarios de un departamento son 5000, 4000, 4000, 3000 (ordenados de mayor a menor). "
                 "¿Qué posición tiene el salario 3000 con `DENSE_RANK()`?",
                 ["2", "3", "4", "1"], 1,
                 "`DENSE_RANK` no salta posiciones: 5000→1, 4000→2 (ambos), 3000→3. Con `RANK` sería 4 y con `ROW_NUMBER` también 4."),
        ],
    },
    {
        "slug": "sql-avanzado",
        "phase": "sql",
        "title": "SQL en PostgreSQL: fechas, texto e índices",
        "summary": "DATE_TRUNC, EXTRACT, FILTER, ILIKE, funciones de texto y fundamentos de rendimiento (índices, EXPLAIN).",
        "hours": 8,
        "theory": r"""
# SQL en PostgreSQL: fechas, texto e índices

Este tema usa funciones **propias de PostgreSQL**, el motor que usaras en muchos trabajos de datos (y el de esta app).

## Fechas

```sql
SELECT DATE_TRUNC('month', order_date)::date AS mes, COUNT(*) AS pedidos
FROM orders
GROUP BY 1
ORDER BY 1;                                     -- pedidos por mes

EXTRACT(YEAR FROM order_date)                    -- año
EXTRACT(DOW FROM order_date)                     -- día de la semana (0 = domingo)
order_date + INTERVAL '30 days'                  -- sumar intervalos
CURRENT_DATE - signup_date                       -- días entre fechas (entero)
```

`DATE_TRUNC('month', fecha)` "redondea hacia abajo" al inicio del mes: es la base de casi cualquier serie temporal.
El `::date` convierte (cast) el resultado a fecha simple.

## Texto

```sql
UPPER(texto), LOWER(texto), TRIM(texto), LENGTH(texto)
SUBSTRING(texto FROM 1 FOR 3)
texto1 || ' ' || texto2          -- concatenar
name ILIKE 'a%'                  -- LIKE sin distinguir mayúsculas
COALESCE(columna, 'sin dato')    -- primer valor no nulo
```

## Agregaciones condicionales con FILTER

```sql
SELECT
  COUNT(*) AS total,
  COUNT(*) FILTER (WHERE status = 'cancelado') AS cancelados
FROM orders;
```

Es la versión legible de `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` y muy útil para tasas y KPIs.

## Rendimiento: lo mínimo que debes saber

- Un **índice** es una estructura auxiliar que acelera búsquedas por una columna: `CREATE INDEX ON orders (customer_id);`.
  Acelera `WHERE`, `JOIN` y `ORDER BY` sobre esa columna, pero hace más lentas las escrituras y ocupa espacio.
- `EXPLAIN ANALYZE SELECT ...` muestra el plan real de ejecución. Busca `Seq Scan` (lee toda la tabla) en tablas grandes.
- Aplicar una función a la columna filtrada (`WHERE EXTRACT(YEAR FROM fecha) = 2024`) suele impedir usar el índice;
  prefiere rangos: `WHERE fecha >= '2024-01-01' AND fecha < '2025-01-01'`.
- Filtra lo antes posible y selecciona solo las columnas que necesitas.

## Cómo sabes que dominas este tema

- Construyes series por día/semana/mes con `DATE_TRUNC`.
- Calculas tasas con `FILTER` o `CASE`.
- Sabes qué es un índice y cuándo ayuda.
""" + TABLAS,
        "exercises": [
            sql("sql-pg-1", "Pedidos por mes", "SQL: fechas y texto (PostgreSQL)",
                "Cuenta los pedidos por mes usando `DATE_TRUNC('month', order_date)`. Devuelve `mes` (como fecha, con `::date`) y `pedidos`. Ordena por mes.",
                "SELECT DATE_TRUNC('month', order_date)::date AS mes, COUNT(*) AS pedidos FROM orders GROUP BY 1 ORDER BY 1",
                starter="SELECT DATE_TRUNC('month', order_date)::date AS mes,\nFROM orders\n", ordered=True, pg_only=True),
            sql("sql-pg-2", "Pedidos por día de la semana", "SQL: fechas y texto (PostgreSQL)",
                "Devuelve `dow` (día de la semana con `EXTRACT(DOW FROM order_date)`, convertido a entero con `::int`) y el número de pedidos (`pedidos`). Ordena por dow.",
                "SELECT EXTRACT(DOW FROM order_date)::int AS dow, COUNT(*) AS pedidos FROM orders GROUP BY 1 ORDER BY 1",
                starter="SELECT EXTRACT(DOW FROM order_date)::int AS dow,\nFROM orders\n", ordered=True, pg_only=True),
            sql("sql-pg-3", "Tasa de cancelación por canal", "SQL: fechas y texto (PostgreSQL)",
                "Para cada canal calcula `tasa`: el porcentaje de pedidos con estado `cancelado` (redondeado a 1 decimal). "
                "Usa `COUNT(*) FILTER (WHERE ...)`. Ordena por channel.",
                "SELECT channel, ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'cancelado') / COUNT(*), 1) AS tasa "
                "FROM orders GROUP BY channel ORDER BY channel",
                starter="SELECT channel,\n       ROUND(100.0 * COUNT(*) FILTER (WHERE /* completa */) / COUNT(*), 1) AS tasa\nFROM orders\n",
                ordered=True, pg_only=True),
            sql("sql-pg-4", "Clientes por país en mayúsculas", "SQL: fechas y texto (PostgreSQL)",
                "Devuelve `pais` (el país en MAYÚSCULAS con `UPPER`) y `clientes` (cuántos clientes hay). Ordena por país.",
                "SELECT UPPER(country) AS pais, COUNT(*) AS clientes FROM customers GROUP BY 1 ORDER BY 1",
                starter="SELECT UPPER(country) AS pais,\nFROM customers\n", ordered=True, pg_only=True),
            quiz("sql-pg-q1", "¿Cuándo ayuda un índice?", "SQL: rendimiento",
                 "Tienes la consulta `SELECT * FROM orders WHERE customer_id = 17` sobre una tabla de 50 millones de filas y tarda varios segundos. "
                 "¿Qué es lo primero que probarías?",
                 ["Cambiar SELECT * por SELECT COUNT(*)", "Crear un índice en orders(customer_id) y revisar el plan con EXPLAIN ANALYZE",
                  "Añadir DISTINCT", "Ordenar los resultados"], 1,
                 "Una búsqueda por igualdad sobre una columna muy selectiva es el caso típico donde un índice evita leer toda la tabla (`Seq Scan`)."),
        ],
    },
]
