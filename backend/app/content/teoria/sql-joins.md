# JOINs: combinar tablas

Hasta ahora cada consulta usaba una sola tabla. Pero la información útil casi siempre está **repartida**: el pedido está en `orders`, el
nombre del cliente en `customers`, el producto en `products` y la cantidad comprada en `order_items`. Para responder "¿cuánto facturó cada
país?" hay que **combinar** esas tablas. Eso es un **JOIN**, y es probablemente el tema que más aparece en las pruebas técnicas de SQL.

---

## 1. Por qué los datos están repartidos

Imagina que cada pedido guardara también el nombre, el país y el segmento del cliente. Si un cliente hace 20 pedidos, sus datos se
repetirían 20 veces; y si cambia de país, habría que actualizar 20 filas (y alguna se olvidaría). Por eso las bases de datos relacionales
**normalizan**: cada dato se guarda **una sola vez** en su tabla, y las tablas se conectan mediante **claves**:

```
customers                 orders                          order_items                          products
┌────┬───────────┐        ┌────┬─────────────┬──────┐     ┌────┬──────────┬────────────┬─────┐   ┌────┬───────────┐
│ id │ name      │◄───────│ customer_id      │ ...  │◄────│ order_id    │ product_id │ ... │──►│ id │ name      │
└────┴───────────┘        └────┴─────────────┴──────┘     └────┴──────────┴────────────┴─────┘   └────┴───────────┘
```

- `orders.customer_id` apunta a `customers.id`: **un cliente tiene muchos pedidos** (relación uno a muchos).
- `order_items.order_id` apunta a `orders.id`: un pedido tiene muchas líneas.
- `order_items.product_id` apunta a `products.id`: un producto aparece en muchas líneas.
- `employees.manager_id` apunta a `employees.id`: un empleado tiene un jefe, que también es un empleado.

Un JOIN **sigue esas flechas** para volver a juntar la información.

---

## 2. INNER JOIN: las filas que coinciden

```sql
SELECT o.id, o.order_date, c.name, c.country
FROM orders AS o
JOIN customers AS c ON c.id = o.customer_id
ORDER BY o.id
LIMIT 5;
```

Pieza por pieza:

- `FROM orders AS o`: la tabla de partida, con un **alias** corto (`o`).
- `JOIN customers AS c`: la tabla que se combina (`JOIN` a secas significa `INNER JOIN`).
- `ON c.id = o.customer_id`: **la condición de unión**: cómo se emparejan las filas. Aquí, cada pedido con el cliente cuyo `id` coincide
  con el `customer_id` del pedido.
- `o.id`, `c.name`: con varias tablas, indica de qué tabla es cada columna con `alias.columna`.

### Qué hace exactamente

Para cada fila de `orders`, busca las filas de `customers` que cumplen la condición `ON` y forma una fila nueva con las columnas de
ambas. Con datos pequeños:

```
orders                          customers                    resultado del JOIN
id | customer_id                id | name                    o.id | c.name
 1 | 14             ───►       14 | Ana                       1   | Ana
 2 | 25             ───►       25 | Luis                      2   | Luis
 3 | 14             ───►       (14 otra vez)                  3   | Ana
```

**INNER JOIN solo deja las filas que encontraron pareja.** Un pedido con un `customer_id` que no existe en `customers`, o un cliente
sin pedidos, no aparecen en el resultado.

### Columnas ambiguas

Las dos tablas tienen una columna `id`. Si escribes solo `id`, la base de datos no sabe cuál:

```
ERROR: column reference "id" is ambiguous
```

Cuando combines tablas, **califica siempre las columnas con su alias**. Y si dos columnas del resultado se llaman igual, dales alias
distintos: `o.id AS pedido_id, c.id AS cliente_id`.

### Filtrar y ordenar con columnas de cualquier tabla

Después del JOIN, todas las columnas están disponibles para `WHERE` y `ORDER BY`:

```sql
SELECT o.id, o.order_date, c.name
FROM orders AS o
JOIN customers AS c ON c.id = o.customer_id
WHERE c.country = 'Chile'
  AND o.status = 'pendiente'
ORDER BY o.order_date, o.id;
```

---

## 3. Relaciones uno a muchos: el JOIN multiplica filas

Esto es lo más importante de entender de los JOINs. Si un cliente tiene 7 pedidos, al hacer `customers JOIN orders` ese cliente
aparece en **7 filas**, una por pedido. El JOIN no "añade columnas" a cada cliente: crea **una fila por cada pareja** que cumple la
condición.

Consecuencias:

- El número de filas del resultado puede ser **mayor** que el de cualquiera de las tablas.
- Si después agregas, debes pensar **qué representa cada fila**. Tras `orders JOIN order_items`, cada fila es una **línea de pedido**, no
  un pedido: `COUNT(*)` cuenta líneas. Para contar pedidos necesitas `COUNT(DISTINCT o.id)`.

```sql
SELECT COUNT(*)             AS lineas,
       COUNT(DISTINCT o.id) AS pedidos
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.id;
```

Antes de agregar después de un JOIN, pregúntate siempre: **"¿una fila de este resultado es qué?"**.

---

## 4. Varios JOIN encadenados

Para llegar de un cliente al nombre de los productos que compró hay que recorrer tres flechas. Se encadenan los JOIN uno tras otro:

```sql
SELECT c.name AS cliente,
       o.id   AS pedido,
       p.name AS producto,
       oi.quantity
FROM customers AS c
JOIN orders      AS o  ON o.customer_id = c.id
JOIN order_items AS oi ON oi.order_id   = o.id
JOIN products    AS p  ON p.id          = oi.product_id
WHERE o.id = 1;
```

Cada `JOIN` añade una tabla conectándola con alguna de las que ya están. Escríbelos **siguiendo el camino de las claves**, como si
dibujaras el recorrido en el diagrama de la sección 1.

### JOIN + GROUP BY: la combinación más útil

Con las tablas unidas, puedes agrupar por columnas de una tabla y agregar columnas de otra. Facturación por país del cliente, solo de
pedidos completados:

```sql
SELECT c.country,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS facturacion,
       COUNT(DISTINCT o.id)                       AS pedidos
FROM customers AS c
JOIN orders      AS o  ON o.customer_id = c.id
JOIN order_items AS oi ON oi.order_id   = o.id
WHERE o.status = 'completado'
GROUP BY c.country
ORDER BY facturacion DESC;
```

Lee la consulta en orden de ejecución: une las tres tablas, se queda con las líneas de pedidos completados, agrupa por país y suma el
importe de las líneas.

---

## 5. LEFT JOIN: conservar todas las filas de la izquierda

¿Y si quieres **todos** los clientes, incluidos los que no tienen pedidos? Con `INNER JOIN` desaparecerían. `LEFT JOIN` conserva todas
las filas de la tabla de la **izquierda** (la del `FROM`), tengan pareja o no. Cuando no tienen pareja, las columnas de la tabla de la
derecha aparecen como `NULL`:

```sql
SELECT c.id, c.name, o.id AS pedido_id
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.id
ORDER BY c.id, o.id;
```

```
c.id | name  | pedido_id
  1  | Ana   |   12
  1  | Ana   |   87
  2  | Luis  |   NULL      <- Luis no tiene pedidos, pero aparece
```

### Contar con LEFT JOIN: `COUNT(*)` frente a `COUNT(columna)`

Pedidos por cliente, incluidos los que tienen cero:

```sql
SELECT c.name,
       COUNT(o.id) AS pedidos       -- COUNT(o.id), no COUNT(*)
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY pedidos DESC, c.name;
```

Un cliente sin pedidos tiene **una** fila con `o.id = NULL`. `COUNT(*)` contaría esa fila y diría 1; `COUNT(o.id)` ignora el `NULL` y
dice 0, que es lo correcto.

(Fíjate también en `GROUP BY c.id, c.name`: agrupar por el `id` evita juntar a dos clientes que se llamen igual.)

---

## 6. Anti-join: lo que NO tiene pareja

Una pregunta muy frecuente es "¿qué elementos **no** tienen relación con la otra tabla?": clientes que nunca compraron, productos que nunca
se vendieron, empleados que no son jefes de nadie. Hay dos formas estándar de hacerlo.

### Con LEFT JOIN + IS NULL

La idea: haz un `LEFT JOIN` y quédate solo con las filas en las que la tabla de la derecha **no encontró pareja** (su clave es `NULL`).
Ejemplo: empleados que no son jefes de nadie:

```sql
SELECT e.id, e.name
FROM employees AS e
LEFT JOIN employees AS sub ON sub.manager_id = e.id
WHERE sub.id IS NULL
ORDER BY e.id;
```

Para cada empleado `e`, busca a sus subordinados (`sub`). Los que no tienen ninguno quedan con `sub.id = NULL`, y el `WHERE` se queda
justo con ellos.

### Con NOT EXISTS

```sql
SELECT e.id, e.name
FROM employees AS e
WHERE NOT EXISTS (
    SELECT 1
    FROM employees AS sub
    WHERE sub.manager_id = e.id
)
ORDER BY e.id;
```

"Dame los empleados para los que **no existe** ningún subordinado." Lo verás a fondo en el capítulo de subconsultas. Las dos formas son
correctas y equivalentes; `NOT EXISTS` suele leerse más claro. Evita `NOT IN` con subconsultas que puedan tener `NULL` (el siguiente
capítulo explica por qué).

---

## 7. La trampa del WHERE en un LEFT JOIN

Quieres **todos** los clientes con sus pedidos **de 2025** (y los clientes sin pedidos en 2025 también deben aparecer). Esto parece
correcto, pero no lo es:

```sql
-- MAL: convierte el LEFT JOIN en un INNER JOIN
SELECT c.name, o.id
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.id
WHERE o.order_date >= '2025-01-01';
```

Los clientes sin pedidos tienen `o.order_date = NULL`, y `NULL >= '2025-01-01'` no es verdadero, así que el `WHERE` los **elimina**.
Acabas perdiendo justo las filas que querías conservar.

La solución es poner la condición sobre la tabla de la derecha **dentro del `ON`**:

```sql
-- BIEN
SELECT c.name, o.id
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer_id = c.id
      AND o.order_date >= '2025-01-01'
ORDER BY c.name, o.id;
```

Ahora la condición decide **qué pedidos se emparejan**, pero todos los clientes se conservan.

| En un LEFT JOIN, una condición sobre la tabla de la derecha... | Efecto |
|---|---|
| en el `ON` | Filtra qué filas de la derecha se emparejan; la izquierda se conserva entera |
| en el `WHERE` | Filtra el resultado final; elimina las filas sin pareja (como un INNER JOIN) |

La excepción es precisamente el anti-join: ahí **sí** quieres `WHERE derecha.id IS NULL` en el `WHERE`.

---

## 8. Self-join: una tabla consigo misma

Cuando una tabla se apunta a sí misma (como `employees.manager_id` → `employees.id`), se une **consigo misma** usando dos alias, como si
fueran dos tablas distintas. Empleados que ganan al menos el 75 % de lo que gana su jefe:

```sql
SELECT e.name   AS empleado,
       e.salary AS salario,
       j.name   AS jefe,
       j.salary AS salario_jefe
FROM employees AS e
JOIN employees AS j ON j.id = e.manager_id
WHERE e.salary >= 0.75 * j.salary;
```

`e` hace el papel de "empleado" y `j` el de "jefe". La condición `j.id = e.manager_id` empareja a cada empleado con su jefe. Como es un
`INNER JOIN`, quien no tiene jefe (`manager_id` es `NULL`) no aparece; si necesitaras incluirlo, usarías `LEFT JOIN`.

---

## 9. Otros tipos de JOIN

| JOIN | Qué conserva | Uso |
|---|---|---|
| `INNER JOIN` (o `JOIN`) | Solo las filas con pareja | El más común |
| `LEFT JOIN` | Todas las de la izquierda | "Todos los X, tengan o no Y" |
| `RIGHT JOIN` | Todas las de la derecha | Igual que LEFT con las tablas al revés; casi no se usa |
| `FULL OUTER JOIN` | Todas las de ambos lados | Comparar dos listas y ver qué falta en cada una |
| `CROSS JOIN` | Todas las combinaciones posibles | Generar combinaciones (cada producto con cada mes) |

Un `CROSS JOIN` (o un JOIN sin condición `ON` correcta) multiplica todas las filas por todas: 220 pedidos × 40 clientes = 8 800 filas. Si
tu resultado tiene muchísimas más filas de las esperadas, revisa las condiciones `ON`.

---

## 10. La trampa de sumar después de un JOIN

Quieres el importe total de pedidos y el número de clientes por país. Si unes `customers`, `orders` y `order_items` y haces
`COUNT(*)` para contar clientes, contarás **líneas de pedido**. Peor aún: si unes dos tablas "hijas" a la vez (por ejemplo, los pedidos de
un cliente y sus tickets de soporte), cada pedido se combina con cada ticket y las sumas salen **multiplicadas**.

Reglas para no equivocarte:

1. Pregúntate qué es una fila tras cada JOIN.
2. Para contar entidades, usa `COUNT(DISTINCT clave)`.
3. Si necesitas sumar datos de dos tablas hijas distintas, agrega cada una **por separado** (en subconsultas o CTE, siguiente capítulo) y
   une los resultados ya agregados.
4. Comprueba los totales con una consulta sencilla: si `SUM` de todas las líneas da X, tu desglose por país debe sumar X.

---

## 11. Cómo plantear una consulta con JOIN

1. **¿Qué tablas contienen los datos que necesito?** Márcalas en el diagrama.
2. **¿Cómo se llega de una a otra?** Sigue las claves; cada flecha es un `JOIN ... ON`.
3. **¿Necesito conservar elementos sin pareja?** Entonces `LEFT JOIN`, y cuidado con el `WHERE`.
4. **¿Qué es una fila tras los JOIN?** Decide si contar con `COUNT(*)` o `COUNT(DISTINCT ...)`.
5. Filtra, agrupa y ordena como siempre.

Ejemplo: *"Unidades vendidas por categoría en pedidos de la app"*. Tablas: `products` (categoría), `order_items` (unidades), `orders`
(canal). Camino: `orders → order_items → products`. Una fila tras los JOIN = una línea de pedido.

```sql
SELECT p.category, SUM(oi.quantity) AS unidades
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.id
JOIN products    AS p  ON p.id = oi.product_id
WHERE o.channel = 'app'
GROUP BY p.category
ORDER BY unidades DESC, p.category;
```

---

## 12. Errores típicos

| Síntoma | Causa | Solución |
|---|---|---|
| `column reference "id" is ambiguous` | Columna sin alias de tabla | Califica: `o.id`, `c.id` |
| Muchísimas más filas de las esperadas | Condición `ON` incorrecta o ausente | Revisa que cada `ON` siga una clave |
| Los conteos salen inflados | Contar filas tras un JOIN uno a muchos | `COUNT(DISTINCT clave)` |
| Faltan elementos sin pareja | `INNER JOIN` donde hacía falta `LEFT JOIN` | Usa `LEFT JOIN` |
| El LEFT JOIN se comporta como INNER | Condición de la tabla derecha en el `WHERE` | Muévela al `ON` |
| Clientes sin pedidos aparecen con 1 pedido | `COUNT(*)` en lugar de `COUNT(o.id)` | Cuenta una columna de la derecha |
| Las sumas salen multiplicadas | Unir dos tablas hijas a la vez | Agrega por separado y luego une |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Claves | La foránea de una tabla apunta a la primaria de otra; el JOIN sigue esa flecha |
| `INNER JOIN` | Solo filas con pareja; `ON` dice cómo emparejar |
| Alias | `FROM orders AS o`; califica todas las columnas |
| Uno a muchos | El JOIN multiplica filas; pregúntate qué es una fila |
| `LEFT JOIN` | Conserva toda la izquierda; sin pareja → `NULL`; cuenta con `COUNT(columna_derecha)` |
| Anti-join | `LEFT JOIN ... WHERE derecha.id IS NULL` o `NOT EXISTS` |
| `ON` frente a `WHERE` | En un LEFT JOIN, las condiciones de la derecha van en el `ON` |
| Self-join | Una tabla consigo misma con dos alias (empleado y jefe) |

## Autoevaluación final

1. ¿Qué filas devuelve un `INNER JOIN`?
2. Un cliente tiene 4 pedidos. ¿Cuántas veces aparece en `customers JOIN orders`?
3. ¿Qué valor tienen las columnas de la derecha en un `LEFT JOIN` cuando no hay pareja?
4. ¿Por qué al contar pedidos por cliente con LEFT JOIN se usa `COUNT(o.id)` y no `COUNT(*)`?
5. Escribe la idea del anti-join con LEFT JOIN.
6. ¿Qué pasa si en un LEFT JOIN pones `WHERE o.status = 'completado'`?
7. En un self-join de `employees`, ¿para qué sirven los dos alias?
8. Tras `orders JOIN order_items`, ¿qué cuenta `COUNT(*)`?

**Respuestas:** 1) Solo las que encuentran pareja según el `ON`. 2) Cuatro, una por pedido. 3) `NULL`. 4) Porque un cliente sin pedidos
tiene una fila con `o.id` en `NULL`: `COUNT(*)` la contaría como 1 y `COUNT(o.id)` la ignora. 5) `LEFT JOIN` con la otra tabla y
`WHERE otra.id IS NULL`. 6) Elimina los clientes sin pedidos (y los que solo tienen pedidos de otro estado): el LEFT JOIN actúa como un
INNER JOIN. 7) Para que la misma tabla haga dos papeles distintos (empleado y jefe) y poder distinguir sus columnas. 8) Líneas de pedido, no pedidos.
