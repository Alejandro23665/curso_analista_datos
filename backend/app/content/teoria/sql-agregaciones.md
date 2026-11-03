# Agregaciones y GROUP BY

En el capítulo anterior aprendiste a **elegir** filas. Pero las preguntas de negocio casi nunca piden filas sueltas: piden **resúmenes**.
¿Cuántos pedidos hubo por canal? ¿Cuál es el salario promedio de cada departamento? ¿Qué clientes compraron más de cinco veces? ¿Cuánto
facturamos este mes?

Responder a eso se llama **agregar**: convertir muchas filas en un número (o en un número por grupo). Es la base de todos los dashboards,
informes y métricas que verás, y aparece en casi todas las pruebas técnicas.

---

## 1. Funciones de agregación

Una **función de agregación** recibe muchas filas y devuelve un solo valor:

| Función | Qué calcula | Ejemplo |
|---|---|---|
| `COUNT(*)` | Cuántas filas hay | `COUNT(*)` |
| `COUNT(columna)` | Cuántas filas tienen esa columna **no nula** | `COUNT(manager_id)` |
| `COUNT(DISTINCT columna)` | Cuántos valores **distintos** hay | `COUNT(DISTINCT country)` |
| `SUM(columna)` | La suma | `SUM(salary)` |
| `AVG(columna)` | El promedio | `AVG(price)` |
| `MIN(columna)` / `MAX(columna)` | El menor / el mayor | `MAX(order_date)` |

Usadas sin más, resumen **toda la tabla** (o las filas que dejó pasar el `WHERE`) en una sola fila:

```sql
SELECT COUNT(*)            AS empleados,
       SUM(salary)         AS nomina_total,
       ROUND(AVG(salary), 2) AS salario_promedio,
       MIN(salary)         AS minimo,
       MAX(salary)         AS maximo
FROM employees;
```

Resultado: una sola fila con cinco columnas.

`ROUND(valor, 2)` redondea a dos decimales. Úsalo para presentar promedios: `AVG` suele devolver muchos decimales.

### Agregar con filtro

`WHERE` se aplica **antes** de agregar, así que puedes resumir solo una parte:

```sql
SELECT COUNT(*) AS cancelados_2025
FROM orders
WHERE status = 'cancelado'
  AND order_date >= '2025-01-01';
```

### `COUNT(*)`, `COUNT(columna)` y `COUNT(DISTINCT columna)`

Son tres preguntas distintas. Con la tabla `employees`:

```sql
SELECT COUNT(*)                AS filas,          -- 24: todos los empleados
       COUNT(manager_id)       AS con_jefe,       -- 23: la directora no tiene jefe (NULL)
       COUNT(DISTINCT department) AS departamentos -- 6: departamentos distintos
FROM employees;
```

### Las agregaciones ignoran los NULL

`SUM`, `AVG`, `MIN`, `MAX` y `COUNT(columna)` **saltan** los valores `NULL`. Esto tiene una consecuencia importante con `AVG`: el
promedio de `[10, NULL, 20]` es `15` (suma 30 entre **2** valores), no `10` (30 entre 3). Si para tu negocio un `NULL` significa "cero",
conviértelo antes: `AVG(COALESCE(columna, 0))`.

---

## 2. GROUP BY: un resumen por grupo

`GROUP BY` divide las filas en **grupos** según el valor de una columna y calcula las agregaciones **para cada grupo**:

```sql
SELECT department,
       COUNT(*)              AS empleados,
       ROUND(AVG(salary), 2) AS salario_promedio
FROM employees
GROUP BY department
ORDER BY department;
```

| department | empleados | salario_promedio |
|---|---|---|
| Datos | 6 | 4550.00 |
| Direccion | 1 | 9500.00 |
| Finanzas | 4 | 4075.00 |
| ... | ... | ... |

Visualízalo en tres pasos (en inglés lo llaman *split-apply-combine*):

```
1. SEPARAR en grupos     2. CALCULAR en cada grupo     3. COMBINAR en una tabla
   Datos:  6 filas  ──>   COUNT=6, AVG=4550.00    ──┐
   Ventas: 5 filas  ──>   COUNT=5, AVG=3660.00    ──┼──> una fila por departamento
   ...                                              ┘
```

### La regla de oro del GROUP BY

**Toda columna del `SELECT` que no esté dentro de una función de agregación tiene que estar en el `GROUP BY`.**

```sql
-- MAL
SELECT department, name, COUNT(*)
FROM employees
GROUP BY department;
```

```
ERROR: column "employees.name" must appear in the GROUP BY clause or be used in an aggregate function
```

¿Por qué? El resultado tiene **una fila por departamento**, pero cada departamento tiene varios nombres: ¿cuál pondría? La base de datos
no puede adivinarlo. O agrupas también por `name` (y entonces cada grupo es una persona, lo que no tiene sentido aquí), o lo metes en una
agregación (`MIN(name)`, `COUNT(name)`), o lo quitas.

(SQLite, a diferencia de PostgreSQL, a veces deja pasar esta consulta y elige un nombre cualquiera. No te fíes: es un error lógico
aunque no dé error de sintaxis.)

### Agrupar por varias columnas

Cada combinación distinta de valores forma un grupo:

```sql
SELECT country, segment, COUNT(*) AS clientes
FROM customers
GROUP BY country, segment
ORDER BY country, segment;
```

Una fila por cada par (país, segmento) que exista.

### Contar valores distintos por grupo

`COUNT(DISTINCT ...)` dentro de un `GROUP BY` responde preguntas como "¿en cuántos países distintos tenemos clientes de cada segmento?":

```sql
SELECT segment,
       COUNT(*)                AS clientes,
       COUNT(DISTINCT country) AS paises
FROM customers
GROUP BY segment
ORDER BY segment;
```

### Comprueba que entendiste

**Pregunta:** ¿cuántas filas devuelve `SELECT status, COUNT(*) FROM orders GROUP BY status`?

**Respuesta:** tres, una por cada estado distinto (`completado`, `cancelado`, `pendiente`).

---

## 3. HAVING: filtrar grupos

`WHERE` filtra **filas antes de agrupar**. Pero ¿cómo te quedas solo con los departamentos cuyo promedio supera 4000? Ese promedio no
existe hasta que se agrupa. Para filtrar **grupos después de agregar** existe `HAVING`:

```sql
SELECT department, ROUND(AVG(salary), 2) AS salario_promedio
FROM employees
GROUP BY department
HAVING AVG(salary) > 4000
ORDER BY salario_promedio DESC;
```

### WHERE y HAVING juntos

```sql
SELECT department, COUNT(*) AS empleados_bien_pagados
FROM employees
WHERE salary >= 3500           -- 1. primero: solo empleados con salario >= 3500
GROUP BY department            -- 2. agrupar los que quedaron
HAVING COUNT(*) >= 2           -- 3. quedarse con los departamentos que tienen 2 o más
ORDER BY empleados_bien_pagados DESC, department;
```

| | `WHERE` | `HAVING` |
|---|---|---|
| Filtra | filas individuales | grupos |
| Cuándo | antes de agrupar | después de agregar |
| Puede usar agregaciones | **no** (`WHERE COUNT(*) > 5` da error) | **sí** |

Regla práctica: si la condición menciona `COUNT`, `SUM`, `AVG`, `MIN` o `MAX`, va en `HAVING`. Si se refiere a una columna de cada fila,
va en `WHERE` (y es más eficiente, porque reduce las filas antes de agrupar).

### El orden completo de ejecución

Con estas cláusulas, el orden en que la base de datos procesa una consulta es:

```
FROM  →  WHERE  →  GROUP BY  →  HAVING  →  SELECT  →  ORDER BY  →  LIMIT
```

Por eso en `HAVING` se repite la expresión (`HAVING AVG(salary) > 4000`) en lugar de usar el alias del `SELECT`, que todavía no existe
(PostgreSQL es estricto con esto). En `ORDER BY`, en cambio, sí puedes usar el alias.

---

## 4. CASE: lógica condicional dentro de SQL

`CASE` es el `if/elif/else` de SQL. Devuelve un valor según condiciones:

```sql
SELECT name,
       salary,
       CASE
           WHEN salary >= 6000 THEN 'directivo'
           WHEN salary >= 4000 THEN 'senior'
           ELSE 'base'
       END AS banda
FROM employees;
```

Igual que en Python, se evalúan **en orden** y gana el **primer** `WHEN` que se cumple. Por eso las condiciones van de la más exigente a
la menos exigente. Si ningún `WHEN` se cumple y no hay `ELSE`, el resultado es `NULL`.

### Agrupar por una categoría calculada

Combinando `CASE` con `GROUP BY` puedes crear categorías que no existen en la tabla y contar cuántos hay en cada una:

```sql
SELECT CASE
           WHEN salary >= 6000 THEN 'directivo'
           WHEN salary >= 4000 THEN 'senior'
           ELSE 'base'
       END AS banda,
       COUNT(*) AS empleados
FROM employees
GROUP BY banda
ORDER BY empleados DESC, banda;
```

PostgreSQL y SQLite permiten `GROUP BY banda` (el alias). En otros motores tendrías que repetir el `CASE` completo en el `GROUP BY`, o usar
la posición de la columna (`GROUP BY 1`).

### Contar con condición: SUM(CASE ...)

Un truco muy usado para calcular varias métricas en una sola consulta. `CASE` devuelve 1 si la fila cumple la condición y 0 si no, y
`SUM` cuenta los unos:

```sql
SELECT channel,
       COUNT(*)                                              AS pedidos,
       SUM(CASE WHEN status = 'completado' THEN 1 ELSE 0 END) AS completados,
       SUM(CASE WHEN status = 'cancelado'  THEN 1 ELSE 0 END) AS cancelados
FROM orders
GROUP BY channel
ORDER BY channel;
```

Una fila por canal, con el total y el desglose por estado en columnas. Así se construye la tabla de un dashboard.

PostgreSQL tiene además una sintaxis más legible para lo mismo: `COUNT(*) FILTER (WHERE status = 'cancelado')`.

---

## 5. Porcentajes y la trampa de la división entera

Calcular la **tasa de cancelación** por canal:

```sql
SELECT channel,
       ROUND(100.0 * SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_cancelados
FROM orders
GROUP BY channel
ORDER BY pct_cancelados DESC;
```

¿Por qué `100.0` y no `100`? En SQL, **dividir dos enteros da un entero**: `7 / 20` es `0`, no `0.35`. Si multiplicas primero por
`100.0` (un decimal), toda la operación pasa a ser decimal. Es uno de los errores más comunes en las pruebas de SQL: el resultado sale
`0` y no se entiende por qué.

Otras formas de forzar decimales: `CAST(x AS NUMERIC)` o `x::numeric` en PostgreSQL.

---

## 6. Métricas de negocio con `order_items`

La facturación no está en una sola columna: cada línea de pedido tiene una cantidad y un precio unitario. El importe de una línea es
`quantity * unit_price`, y se puede agregar directamente:

```sql
-- Facturación total y unidades vendidas de todas las líneas
SELECT SUM(quantity * unit_price) AS facturacion,
       SUM(quantity)              AS unidades
FROM order_items;
```

```sql
-- Importe de cada pedido (una fila por pedido)
SELECT order_id,
       SUM(quantity * unit_price) AS importe,
       COUNT(*)                   AS lineas
FROM order_items
GROUP BY order_id
ORDER BY importe DESC
LIMIT 5;
```

Fíjate en que la agregación puede ser sobre una **expresión** (`quantity * unit_price`), no solo sobre una columna.

Para saber, por ejemplo, la facturación **por categoría de producto** o **por país del cliente** hace falta combinar tablas: es justo lo
que aprenderás en el capítulo de JOINs.

---

## 7. Cómo plantear una consulta de agregación

1. **¿Qué es una fila del resultado?** "Una fila por departamento", "una fila por cliente", "una sola fila". Esa respuesta es tu
   `GROUP BY` (o ninguno, si es una sola fila).
2. **¿Qué números calculo para cada fila?** → las agregaciones del `SELECT`, con sus alias.
3. **¿Hay filas que excluir antes de calcular?** → `WHERE`.
4. **¿Hay grupos que excluir después de calcular?** → `HAVING`.
5. **¿Orden y límite?** → `ORDER BY` (con desempate) y `LIMIT`.

Ejemplo: *"Para cada canal, cuántos pedidos completados hubo en 2025, solo para los canales con al menos 10"*.

1. Una fila por canal → `GROUP BY channel`.
2. Contar pedidos → `COUNT(*)`.
3. Solo completados de 2025 → `WHERE`.
4. Al menos 10 → `HAVING COUNT(*) >= 10`.

```sql
SELECT channel, COUNT(*) AS completados_2025
FROM orders
WHERE status = 'completado'
  AND order_date >= '2025-01-01'
GROUP BY channel
HAVING COUNT(*) >= 10
ORDER BY completados_2025 DESC, channel;
```

---

## 8. Errores típicos

| Error | Causa | Solución |
|---|---|---|
| `must appear in the GROUP BY clause` | Una columna del `SELECT` no está agregada ni agrupada | Añádela al `GROUP BY` o agrégala |
| `aggregate functions are not allowed in WHERE` | Condición con `COUNT`/`AVG`... en `WHERE` | Muévela a `HAVING` |
| El porcentaje sale 0 | División entre enteros | Multiplica por `100.0` primero |
| El promedio "no cuadra" | `AVG` ignora los `NULL` | `AVG(COALESCE(col, 0))` si `NULL` significa 0 |
| `COUNT(columna)` da menos que `COUNT(*)` | La columna tiene `NULL` | Elige conscientemente qué quieres contar |
| Una categoría del `CASE` sale vacía o `NULL` | Orden incorrecto de los `WHEN` o falta `ELSE` | Del más exigente al menos; añade `ELSE` |
| El orden del resultado cambia | Falta desempate en `ORDER BY` | Añade una segunda columna |

---

## Resumen del capítulo

| Herramienta | Para qué | Recuerda |
|---|---|---|
| `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | Resumir muchas filas | Ignoran `NULL` (salvo `COUNT(*)`) |
| `COUNT(DISTINCT x)` | Valores distintos | Clientes únicos, países distintos... |
| `GROUP BY` | Un resumen por grupo | Toda columna no agregada del `SELECT` va en el `GROUP BY` |
| `HAVING` | Filtrar grupos | Después de agregar; `WHERE` filtra filas antes |
| `CASE WHEN` | Lógica condicional | Primer `WHEN` que se cumple gana; `ELSE` |
| `SUM(CASE ... THEN 1 ELSE 0 END)` | Contar con condición | Varias métricas en una consulta |
| `100.0 * a / b` | Porcentajes | Evita la división entera |
| `ROUND(x, 2)` | Presentar decimales | |

## Autoevaluación final

1. ¿Qué diferencia hay entre `COUNT(*)` y `COUNT(manager_id)`?
2. ¿Por qué `SELECT department, name, COUNT(*) FROM employees GROUP BY department` da error en PostgreSQL?
3. ¿Dónde va la condición "departamentos con más de 3 empleados"?
4. ¿En qué orden se ejecutan `WHERE`, `GROUP BY`, `HAVING` y `SELECT`?
5. ¿Qué devuelve un `CASE` si ningún `WHEN` se cumple y no hay `ELSE`?
6. ¿Cuánto vale `7 / 20` en SQL? ¿Y `100.0 * 7 / 20`?
7. ¿Cómo cuentas, en una sola consulta y por canal, los pedidos cancelados?
8. ¿Cuál es el promedio de `[10, NULL, 20]` según `AVG`?

**Respuestas:** 1) `COUNT(*)` cuenta todas las filas; `COUNT(manager_id)` solo las que tienen `manager_id` no nulo. 2) Porque `name` no
está agregado ni en el `GROUP BY`, y cada departamento tiene varios nombres. 3) En `HAVING COUNT(*) > 3`. 4) `WHERE`, `GROUP BY`,
`HAVING`, `SELECT`. 5) `NULL`. 6) `0` (división entera) y `35.0`. 7) `SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END)` con
`GROUP BY channel`. 8) `15`: ignora el `NULL` y divide 30 entre 2.
