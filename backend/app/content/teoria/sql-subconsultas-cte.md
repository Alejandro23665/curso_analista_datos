# Subconsultas y CTE

Algunas preguntas no se pueden responder en un solo paso. "¿Qué empleados ganan más que el promedio?" exige **primero** calcular el
promedio y **después** comparar cada salario con él. "¿Cuáles son los tres clientes que más gastaron?" exige primero calcular el gasto de
cada cliente y después quedarse con los mejores.

Para eso SQL permite usar **una consulta dentro de otra** (subconsulta) y, mucho más legible, **nombrar resultados intermedios** con
`WITH` (CTE, *Common Table Expression*). Con estas herramientas puedes resolver problemas complejos dividiéndolos en pasos, exactamente
como harías en Python con funciones.

---

## 1. Qué es una subconsulta

Una **subconsulta** es un `SELECT` escrito entre paréntesis dentro de otra consulta. La base de datos ejecuta primero la de dentro y usa
su resultado en la de fuera.

Según **qué devuelve**, se usa en un sitio u otro:

| La subconsulta devuelve... | Se usa... | Ejemplo |
|---|---|---|
| Un solo valor (una fila, una columna) | Donde iría un valor: `WHERE x > (...)`, en el `SELECT` | El promedio de salarios |
| Una lista (una columna, varias filas) | Con `IN` / `NOT IN` | Los ids de clientes de Chile |
| Una tabla (varias columnas y filas) | En el `FROM`, como si fuera una tabla | El gasto por cliente |
| "¿Hay alguna fila?" | Con `EXISTS` / `NOT EXISTS` | ¿Tiene este cliente algún pedido cancelado? |

---

## 2. Subconsultas escalares: un solo valor

```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC, name;
```

1. La subconsulta `(SELECT AVG(salary) FROM employees)` devuelve un número (el salario promedio).
2. La consulta de fuera compara cada salario con ese número.

¿Por qué no basta con `WHERE salary > AVG(salary)`? Porque `WHERE` trabaja fila a fila y no puede usar agregaciones (lo viste en el
capítulo anterior). La subconsulta calcula el agregado aparte.

Otro uso típico: encontrar **el elemento que tiene el máximo**:

```sql
SELECT id, customer_id, order_date
FROM orders
WHERE order_date = (SELECT MAX(order_date) FROM orders);
```

Esto devuelve **todos** los pedidos del último día, si hay varios (a diferencia de `ORDER BY ... LIMIT 1`, que devolvería solo uno).

### En el SELECT

Una subconsulta escalar también puede ser una columna. Por ejemplo, la diferencia de cada salario con el promedio:

```sql
SELECT name,
       salary,
       salary - (SELECT ROUND(AVG(salary), 2) FROM employees) AS diferencia_con_promedio
FROM employees
ORDER BY diferencia_con_promedio DESC;
```

**Regla:** una subconsulta escalar tiene que devolver **exactamente un valor**. Si devuelve varias filas, la consulta falla con
`more than one row returned by a subquery used as an expression`.

---

## 3. Subconsultas que devuelven una lista: IN

```sql
SELECT id, order_date, status
FROM orders
WHERE customer_id IN (
    SELECT id
    FROM customers
    WHERE country = 'Chile'
)
ORDER BY order_date, id;
```

La subconsulta devuelve la lista de ids de clientes chilenos, y la consulta de fuera se queda con sus pedidos. Muchas veces se puede
escribir también con un JOIN; usa la forma que se lea más clara.

### La trampa de NOT IN con NULL

Esta es una de las preguntas de entrevista más conocidas. Queremos los empleados que **no son jefes de nadie**:

```sql
-- PELIGROSO
SELECT name
FROM employees
WHERE id NOT IN (SELECT manager_id FROM employees);
```

Devuelve **cero filas**, aunque es evidente que hay empleados que no son jefes. ¿Por qué?

La columna `manager_id` contiene un `NULL` (la directora no tiene jefe), así que la lista de la subconsulta es algo como
`(1, 1, 2, ..., NULL)`. Para un empleado con `id = 6`, la condición `6 NOT IN (1, 2, NULL)` equivale a:

```
6 <> 1  AND  6 <> 2  AND  6 <> NULL
TRUE    AND  TRUE    AND  desconocido   =   desconocido
```

Cualquier comparación con `NULL` es "desconocido", y un `AND` con un "desconocido" ya no puede ser verdadero. `WHERE` descarta las filas
que no son verdaderas, así que **todas** se descartan.

Soluciones:

```sql
-- 1. Excluir los NULL de la subconsulta
WHERE id NOT IN (SELECT manager_id FROM employees WHERE manager_id IS NOT NULL)

-- 2. Mejor: usar NOT EXISTS, que no tiene este problema (sección 6)
```

**Regla práctica: para "los que no están en...", prefiere `NOT EXISTS` o el anti-join con `LEFT JOIN`.**

---

## 4. Subconsultas en el FROM: tablas derivadas

Una subconsulta que devuelve una tabla puede usarse en el `FROM`, como si fuera una tabla más. Necesita un **alias**:

```sql
SELECT ROUND(AVG(pedidos), 2) AS pedidos_promedio_por_cliente
FROM (
    SELECT customer_id, COUNT(*) AS pedidos
    FROM orders
    GROUP BY customer_id
) AS por_cliente;
```

1. La subconsulta calcula cuántos pedidos tiene cada cliente (una fila por cliente).
2. La consulta de fuera promedia esa columna.

Es un **promedio de un agregado**: algo imposible en un solo nivel (`AVG(COUNT(*))` no está permitido). Siempre que necesites "agregar
algo que ya está agregado", necesitas dos niveles.

Este tipo de subconsulta funciona, pero se vuelve difícil de leer cuando hay varias anidadas. Para eso están las CTE.

---

## 5. Subconsultas correlacionadas

Las subconsultas anteriores se ejecutan **una sola vez**. Una subconsulta **correlacionada** usa columnas de la consulta de fuera, así que
conceptualmente se ejecuta **una vez por cada fila**. Empleados que ganan más que el promedio **de su propio departamento**:

```sql
SELECT e.name, e.department, e.salary
FROM employees AS e
WHERE e.salary > (
    SELECT AVG(otro.salary)
    FROM employees AS otro
    WHERE otro.department = e.department     -- usa la fila de fuera
)
ORDER BY e.department, e.salary DESC;
```

Para cada empleado `e`, la subconsulta calcula el promedio de **su** departamento (`otro.department = e.department`) y lo compara con su
salario. Los alias son imprescindibles para distinguir las dos "copias" de la tabla.

Son muy expresivas, pero con tablas grandes pueden ser lentas. En el capítulo de funciones de ventana verás otra forma de resolver este
mismo problema.

---

## 6. EXISTS y NOT EXISTS: "¿hay alguna fila que...?"

`EXISTS (subconsulta)` es verdadero si la subconsulta devuelve **al menos una fila**. No importa qué columnas devuelva, por eso se
escribe `SELECT 1` por convención.

Clientes que tienen **al menos un pedido cancelado en la app**:

```sql
SELECT c.name
FROM customers AS c
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.id
      AND o.channel = 'app'
      AND o.status = 'cancelado'
)
ORDER BY c.name;
```

Léelo literalmente: "dame los clientes para los que **existe** un pedido suyo, de la app, cancelado". Fíjate en que es correlacionada:
`o.customer_id = c.id` conecta la subconsulta con cada cliente.

### Por qué EXISTS en lugar de JOIN

Con un `JOIN`, un cliente con tres pedidos cancelados en la app aparecería **tres veces**, y tendrías que añadir `DISTINCT`. `EXISTS`
solo pregunta "¿hay alguno?", así que cada cliente aparece **una vez**. Además, la base de datos puede dejar de buscar en cuanto encuentra
la primera fila.

`EXISTS` es la herramienta natural para preguntas del tipo **"los que han hecho al menos una vez algo"**, incluso cuando ese "algo"
requiere cruzar varias tablas dentro de la subconsulta (se pueden usar JOIN dentro del `EXISTS`).

### NOT EXISTS: la forma segura del "nunca"

Clientes que **nunca** han cancelado un pedido:

```sql
SELECT c.name
FROM customers AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.id
      AND o.status = 'cancelado'
)
ORDER BY c.name;
```

A diferencia de `NOT IN`, **no tiene problemas con los `NULL`**.

---

## 7. CTE: dar nombre a los pasos con WITH

Una **CTE** es una consulta con nombre que defines al principio con `WITH` y luego usas como una tabla:

```sql
WITH pedidos_por_cliente AS (
    SELECT customer_id, COUNT(*) AS pedidos
    FROM orders
    GROUP BY customer_id
)
SELECT ROUND(AVG(pedidos), 2) AS pedidos_promedio_por_cliente
FROM pedidos_por_cliente;
```

Hace lo mismo que la tabla derivada de la sección 4, pero se lee **de arriba abajo**, como una receta: primero calculo los pedidos por
cliente, después los promedio.

### Varias CTE encadenadas

Se separan con comas, y cada una puede usar las anteriores:

```sql
WITH pedidos_por_dia AS (
    SELECT order_date, COUNT(*) AS pedidos
    FROM orders
    GROUP BY order_date
),
promedio AS (
    SELECT AVG(pedidos) AS media
    FROM pedidos_por_dia
)
SELECT d.order_date, d.pedidos
FROM pedidos_por_dia AS d, promedio AS p
WHERE d.pedidos > p.media
ORDER BY d.pedidos DESC, d.order_date;
```

Tres pasos con nombre: pedidos por día, el promedio de esos días, y los días que lo superan. (`FROM pedidos_por_dia AS d, promedio AS p`
combina cada día con la única fila de `promedio`; es un `CROSS JOIN` de una tabla con una sola fila, una forma cómoda de "tener a mano" un
valor.)

### Por qué las CTE son tan útiles

- **Legibilidad**: cada paso tiene un nombre que explica qué es. Elige nombres descriptivos (`gasto_por_cliente`, no `t1`).
- **Depuración**: puedes ejecutar cada CTE por separado (copiándola como consulta suelta) para comprobar su resultado.
- **Reutilización**: una CTE se puede usar varias veces en la consulta final.
- En entrevistas y en el trabajo, una consulta con CTE bien nombradas transmite que piensas de forma ordenada.

### El patrón "top N" con CTE

Calcular algo por entidad y quedarte con las mejores. Las dos categorías con más facturación:

```sql
WITH facturacion_por_categoria AS (
    SELECT p.category, SUM(oi.quantity * oi.unit_price) AS facturacion
    FROM order_items AS oi
    JOIN products AS p ON p.id = oi.product_id
    GROUP BY p.category
)
SELECT category, ROUND(facturacion, 2) AS facturacion
FROM facturacion_por_categoria
ORDER BY facturacion DESC, category
LIMIT 2;
```

---

## 8. Construir consultas complejas paso a paso

El método profesional, el mismo que usarías en Python:

1. **Escribe y ejecuta el primer paso solo.** Por ejemplo, el gasto de cada cliente. Comprueba que el resultado tiene sentido (¿una fila
   por cliente?, ¿los números son razonables?).
2. **Envuélvelo en una CTE** con un buen nombre.
3. **Escribe el siguiente paso** usando esa CTE. Ejecuta y comprueba.
4. Repite hasta llegar a la respuesta.

Nunca escribas una consulta de 40 líneas de golpe para ejecutarla al final: si falla, no sabrás en qué paso.

### Ejemplo completo: clientes por encima del ticket medio

*"Clientes cuyo ticket medio (importe promedio por pedido) supera el ticket medio de todos los pedidos."*

Paso 1, el importe de cada pedido:

```sql
SELECT order_id, SUM(quantity * unit_price) AS importe
FROM order_items
GROUP BY order_id;
```

Paso 2, envuelto en una CTE y añadiendo el cliente y su ticket medio:

```sql
WITH importe_pedido AS (
    SELECT order_id, SUM(quantity * unit_price) AS importe
    FROM order_items
    GROUP BY order_id
),
ticket_cliente AS (
    SELECT o.customer_id, AVG(ip.importe) AS ticket_medio
    FROM importe_pedido AS ip
    JOIN orders AS o ON o.id = ip.order_id
    GROUP BY o.customer_id
)
SELECT c.name, ROUND(tc.ticket_medio, 2) AS ticket_medio
FROM ticket_cliente AS tc
JOIN customers AS c ON c.id = tc.customer_id
WHERE tc.ticket_medio > (SELECT AVG(importe) FROM importe_pedido)
ORDER BY tc.ticket_medio DESC;
```

Fíjate en cómo la subconsulta escalar del final usa también la CTE `importe_pedido`.

---

## 9. CTE recursivas (para conocerlas)

Una CTE puede referirse a sí misma para recorrer **jerarquías**: la cadena de jefes de un empleado, las categorías dentro de categorías,
los comentarios que responden a otros comentarios.

```sql
WITH RECURSIVE cadena AS (
    SELECT id, name, manager_id, 0 AS nivel
    FROM employees
    WHERE manager_id IS NULL                  -- caso base: la cima
    UNION ALL
    SELECT e.id, e.name, e.manager_id, c.nivel + 1
    FROM employees AS e
    JOIN cadena AS c ON e.manager_id = c.id   -- paso: los subordinados del nivel anterior
)
SELECT name, nivel
FROM cadena
ORDER BY nivel, name;
```

Calcula el nivel de cada empleado en el organigrama. Es avanzado y no lo necesitarás a menudo, pero conviene que reconozcas la estructura:
un caso base, `UNION ALL` y un paso que se une a la propia CTE.

---

## 10. ¿JOIN, subconsulta o CTE?

| Situación | Herramienta recomendada |
|---|---|
| Traer columnas de otra tabla | `JOIN` |
| Comparar con un valor agregado (promedio, máximo) | Subconsulta escalar |
| "Los que han hecho algo al menos una vez" | `EXISTS` |
| "Los que nunca han hecho algo" | `NOT EXISTS` o anti-join (nunca `NOT IN` con posibles `NULL`) |
| Agregar sobre algo ya agregado | CTE (o subconsulta en el `FROM`) |
| Varios pasos encadenados | CTE con nombres claros |

No hay una única forma correcta: la mejor es la que otra persona entiende a la primera.

---

## 11. Errores típicos

| Error | Causa | Solución |
|---|---|---|
| `more than one row returned by a subquery used as an expression` | La subconsulta escalar devuelve varias filas | Agrégala (`MAX`, `AVG`) o usa `IN` |
| `subquery in FROM must have an alias` | Tabla derivada sin alias | Añade `AS nombre` |
| `NOT IN` devuelve cero filas | La subconsulta contiene `NULL` | `NOT EXISTS` o filtra `IS NOT NULL` |
| `aggregate function calls cannot be nested` | `AVG(COUNT(*))` | Agrega en una CTE y luego agrega otra vez |
| Duplicados al buscar "los que tienen algo" | `JOIN` en lugar de `EXISTS` | Usa `EXISTS` |
| La correlacionada da resultados raros | Alias confundidos dentro y fuera | Usa alias distintos y califica todo |
| `relation "mi_cte" does not exist` | Usaste la CTE en otra consulta | Una CTE solo existe en la consulta donde se define |

---

## Resumen del capítulo

| Herramienta | Para qué | Recuerda |
|---|---|---|
| Subconsulta escalar | Comparar con un agregado | Debe devolver un solo valor |
| `IN (subconsulta)` | Pertenecer a una lista calculada | |
| `NOT IN` | Excluir una lista | Peligroso con `NULL`: devuelve vacío |
| Tabla derivada | Agregar sobre algo agregado | Necesita alias |
| Correlacionada | Comparar cada fila con su grupo | Usa columnas de la consulta de fuera |
| `EXISTS` / `NOT EXISTS` | ¿Hay alguna fila que...? | Sin duplicados; seguro con `NULL` |
| `WITH` (CTE) | Pasos con nombre | Se leen de arriba abajo; se depuran por partes |
| `WITH RECURSIVE` | Jerarquías | Caso base + `UNION ALL` + paso |

## Autoevaluación final

1. ¿Por qué no se puede escribir `WHERE salary > AVG(salary)`?
2. ¿Qué pasa si una subconsulta usada con `>` devuelve varias filas?
3. ¿Por qué `NOT IN (SELECT manager_id FROM employees)` devuelve cero filas?
4. ¿Qué diferencia hay entre una subconsulta normal y una correlacionada?
5. ¿Por qué `EXISTS` no produce duplicados y un `JOIN` sí?
6. ¿Cómo calculas el promedio de pedidos por cliente?
7. ¿Qué ventajas tiene una CTE frente a una subconsulta anidada?
8. ¿Puedes usar una CTE definida en una consulta en otra consulta distinta?

**Respuestas:** 1) Porque `WHERE` trabaja fila a fila y no admite agregaciones; el promedio se calcula en una subconsulta. 2) Da error:
una subconsulta escalar debe devolver un único valor. 3) Porque la lista contiene un `NULL` y cualquier `x <> NULL` es desconocido, así
que ninguna fila cumple la condición. 4) La correlacionada usa columnas de la consulta de fuera y se evalúa para cada fila. 5) Porque
`EXISTS` solo pregunta si hay al menos una fila; el `JOIN` crea una fila por cada coincidencia. 6) Contando pedidos por cliente en una CTE
(o tabla derivada) y promediando ese conteo fuera. 7) Se lee de arriba abajo, cada paso tiene nombre, se puede probar por partes y
reutilizar. 8) No: una CTE solo existe dentro de la consulta en la que se define.
