# SELECT, filtros y orden

SQL es el idioma con el que se habla con las bases de datos, y es **la habilidad técnica más pedida** en ofertas de datos y de backend.
Casi todas las aplicaciones guardan su información en una base de datos relacional (PostgreSQL, MySQL, SQL Server, SQLite), y casi todas
las pruebas técnicas incluyen al menos una pregunta de SQL.

La buena noticia: SQL es un lenguaje pequeño y muy legible. Con lo de este capítulo ya puedes responder una gran parte de las preguntas
que se le hacen a una base de datos.

Todos los ejemplos usan las **tablas de práctica** de la plataforma, así que puedes escribirlos en cualquier ejercicio de SQL y pulsar
**Ejecutar** para ver el resultado real. En la práctica tienes a mano el esquema de las tablas.

---

## 1. Qué es una base de datos relacional

Una base de datos relacional guarda la información en **tablas**, parecidas a hojas de cálculo:

- Cada **fila** (o registro) es un elemento: un cliente, un pedido.
- Cada **columna** (o campo) es un dato de ese elemento: el nombre, el país. Cada columna tiene un **tipo** fijo (número, texto, fecha).
- Casi todas las tablas tienen una **clave primaria** (*primary key*): una columna, normalmente `id`, cuyo valor identifica cada fila sin
  repetirse.
- Las tablas se **relacionan** entre sí mediante **claves foráneas** (*foreign keys*): la columna `customer_id` de `orders` guarda el `id`
  del cliente que hizo el pedido. Así no se repiten los datos del cliente en cada pedido.

### Las tablas de práctica

| Tabla | Qué guarda | Columnas |
|---|---|---|
| `customers` | 40 clientes | `id`, `name`, `country`, `segment`, `signup_date` |
| `products` | 24 productos | `id`, `name`, `category`, `price` |
| `orders` | 220 pedidos | `id`, `customer_id`, `order_date`, `status`, `channel` |
| `order_items` | Las líneas de cada pedido | `id`, `order_id`, `product_id`, `quantity`, `unit_price` |
| `employees` | 24 empleados | `id`, `name`, `department`, `title`, `salary`, `hire_date`, `manager_id` |

Valores que conviene conocer (sin tildes, para que no tengas que escribirlas):

- `orders.status`: `completado`, `cancelado`, `pendiente`.
- `orders.channel`: `web`, `app`, `tienda`.
- `products.category`: `Tecnologia`, `Hogar`, `Deportes`, `Libros`.
- `customers.country`: `Argentina`, `Chile`, `Colombia`, `Espana`, `Mexico`, `Venezuela`.
- `customers.segment`: `Consumidor`, `Corporativo`, `Pyme`.
- Las fechas van de 2024 a mediados de 2025.

---

## 2. SELECT: elegir qué columnas ver

La consulta más simple tiene dos partes: **qué columnas** (`SELECT`) y **de qué tabla** (`FROM`):

```sql
SELECT name, price
FROM products;
```

Devuelve el nombre y el precio de los 24 productos.

- Las columnas se separan con comas. **No pongas coma después de la última**: `SELECT name, price, FROM products` es un error de sintaxis
  (es de los más frecuentes).
- El `;` final marca el fin de la consulta. En la plataforma es opcional.
- SQL no distingue mayúsculas en las palabras clave: `select` y `SELECT` son lo mismo. Por convención, se escriben en mayúsculas para
  distinguirlas de los nombres de tablas y columnas.
- Los saltos de línea y la indentación son libres: úsalos para que la consulta se lea bien.

### Todas las columnas: `*`

```sql
SELECT *
FROM customers;
```

Útil para **explorar** una tabla, pero evítalo en el código de una aplicación: trae columnas que no necesitas y, si alguien añade columnas
a la tabla, tu código recibe datos inesperados.

### Columnas calculadas y alias

En el `SELECT` puedes calcular valores y ponerles nombre con `AS`:

```sql
SELECT name,
       price,
       price * 1.16 AS precio_con_iva,
       ROUND(price * 0.9, 2) AS precio_oferta
FROM products;
```

El **alias** (`AS precio_con_iva`) es el nombre que tendrá esa columna en el resultado. Sin él, la columna se llamaría algo como
`price * 1.16`. En las pruebas técnicas te pedirán a menudo nombres de columna concretos: usa exactamente el alias que te digan.

---

## 3. WHERE: filtrar filas

`WHERE` se queda solo con las filas que cumplen una condición:

```sql
SELECT name, department, salary
FROM employees
WHERE salary > 5000;
```

### Operadores de comparación

| Operador | Significado | Ejemplo |
|---|---|---|
| `=` | igual (¡un solo signo, no `==`!) | `country = 'Chile'` |
| `<>` o `!=` | distinto | `status <> 'cancelado'` |
| `<`, `>`, `<=`, `>=` | menor, mayor... | `price >= 100` |

### Texto y fechas van entre comillas simples

```sql
SELECT id, order_date, channel
FROM orders
WHERE status = 'pendiente';
```

- Los textos se escriben con **comillas simples** `'...'`. Las comillas dobles en SQL significan otra cosa (nombres de columnas) y
  provocan errores raros.
- Las comparaciones de texto **distinguen mayúsculas**: `'Chile'` no es igual a `'chile'`.
- Las fechas se escriben como texto en formato **`'AAAA-MM-DD'`** y se comparan con normalidad:
  `WHERE order_date >= '2025-01-01'`.

### Combinar condiciones: `AND`, `OR`, `NOT`

```sql
SELECT id, order_date, status
FROM orders
WHERE channel = 'app'
  AND status = 'cancelado'
  AND order_date >= '2025-01-01';
```

**La trampa de `AND` y `OR`:** `AND` se evalúa antes que `OR` (como la multiplicación antes que la suma). Mira esta consulta, que
pretende "pedidos de la app o de la web, pero solo los cancelados":

```sql
-- MAL
SELECT id, channel, status
FROM orders
WHERE channel = 'app' OR channel = 'web' AND status = 'cancelado';
```

SQL la interpreta como `channel = 'app' OR (channel = 'web' AND status = 'cancelado')`: devuelve **todos** los pedidos de la app (de
cualquier estado) más los cancelados de la web. La versión correcta lleva paréntesis:

```sql
-- BIEN
SELECT id, channel, status
FROM orders
WHERE (channel = 'app' OR channel = 'web')
  AND status = 'cancelado';
```

**Regla: siempre que mezcles `AND` y `OR`, pon paréntesis.**

### Comprueba que entendiste

**Pregunta:** ¿qué devuelve `SELECT name FROM products WHERE category = 'Libros' AND price < 20`?

**Respuesta:** los nombres de los libros que cuestan menos de 20. Las dos condiciones deben cumplirse.

---

## 4. IN, BETWEEN y LIKE

### `IN`: una lista de valores posibles

En lugar de encadenar varios `OR` sobre la misma columna:

```sql
SELECT name, category, price
FROM products
WHERE category IN ('Hogar', 'Deportes');
```

Equivale a `category = 'Hogar' OR category = 'Deportes'`, pero es más corto y no tiene el problema de los paréntesis. `NOT IN (...)`
excluye esos valores.

### `BETWEEN`: un rango, incluidos los extremos

```sql
SELECT name, salary
FROM employees
WHERE salary BETWEEN 3000 AND 4000;
```

Incluye **los dos extremos**: un salario de exactamente 3000 o 4000 aparece. Equivale a `salary >= 3000 AND salary <= 4000`.

Con fechas es muy útil:

```sql
SELECT id, order_date
FROM orders
WHERE order_date BETWEEN '2025-02-01' AND '2025-02-28';
```

Cuidado: si una columna guarda fecha **y hora** (por ejemplo `'2025-02-28 15:30'`), `BETWEEN ... AND '2025-02-28'` excluiría ese pedido,
porque `'2025-02-28'` equivale a la medianoche del inicio del día. Con columnas de fecha y hora es más seguro escribir
`order_date >= '2025-02-01' AND order_date < '2025-03-01'`. En nuestras tablas las fechas no tienen hora, así que `BETWEEN` funciona bien.

### `LIKE`: buscar patrones en texto

| Comodín | Significa | Ejemplo | Encuentra |
|---|---|---|---|
| `%` | cualquier cantidad de caracteres (incluso ninguno) | `'%de%'` | "Juego de sabanas", "Guia de Python" |
| `_` | exactamente un carácter | `'_a%'` | textos cuya segunda letra es "a" |

```sql
SELECT name
FROM customers
WHERE name LIKE '%ez';          -- nombres que TERMINAN en "ez"
```

```sql
SELECT name
FROM products
WHERE name LIKE '%de%';         -- nombres que CONTIENEN "de"
```

Detalles:

- Dónde va el `%` cambia todo: `'M%'` empieza por M, `'%m'` termina en m, `'%m%'` contiene una m.
- `LIKE` **distingue mayúsculas** en PostgreSQL: `'a%'` no encuentra "Ana". PostgreSQL tiene `ILIKE` para buscar sin distinguir
  mayúsculas (`name ILIKE 'a%'`).

---

## 5. NULL: la ausencia de valor

`NULL` significa **"no hay valor"** o "desconocido". No es cero ni texto vacío: es la ausencia de dato. En la tabla `employees`, la
directora general tiene `manager_id` en `NULL` porque no tiene jefe.

### No se compara con `=`

Como `NULL` es "desconocido", cualquier comparación con él da también "desconocido", que `WHERE` trata como falso:

```sql
-- MAL: no devuelve ninguna fila, aunque haya NULLs
SELECT name FROM employees WHERE manager_id = NULL;
```

Para preguntar por `NULL` se usan operadores especiales:

```sql
SELECT name FROM employees WHERE manager_id IS NULL;        -- sin jefe
SELECT name FROM employees WHERE manager_id IS NOT NULL;    -- con jefe
```

### `COALESCE`: un valor de reemplazo

`COALESCE(a, b, ...)` devuelve el primer valor que no sea `NULL`. Sirve para mostrar algo en lugar de un hueco:

```sql
SELECT name, COALESCE(manager_id, 0) AS jefe
FROM employees;
```

### Las trampas de NULL

- `NULL = NULL` **no** es verdadero (es desconocido). Dos valores desconocidos no tienen por qué ser iguales.
- Cualquier operación con `NULL` da `NULL`: `salary + NULL` es `NULL`.
- `NOT IN` con una lista que contiene un `NULL` no devuelve **ninguna** fila. Es un error famoso en entrevistas; lo verás con
  subconsultas.
- Las funciones de agregación (`SUM`, `AVG`, `COUNT(columna)`) **ignoran** los `NULL` (siguiente capítulo).

---

## 6. ORDER BY: ordenar el resultado

Sin `ORDER BY`, **el orden de las filas no está garantizado**. Puede parecer ordenado por `id`, pero no tiene por qué serlo y puede
cambiar. Si el orden importa, indícalo siempre:

```sql
SELECT name, price
FROM products
ORDER BY price DESC;
```

- `ASC` (ascendente, de menor a mayor) es el valor por defecto; `DESC` es descendente.
- Los textos se ordenan alfabéticamente y las fechas cronológicamente.

### Ordenar por varias columnas: el desempate

```sql
SELECT name, department, salary
FROM employees
ORDER BY department ASC, salary DESC;
```

Ordena por departamento y, **dentro de cada departamento**, por salario de mayor a menor. La segunda columna solo se usa para desempatar
filas con el mismo valor en la primera.

Esto importa mucho en las pruebas técnicas (y en los ejercicios de esta plataforma): si piden "ordena por fecha y luego por id", es
porque hay fechas repetidas y el resultado solo es único con el desempate. **Cuando ordenes por algo que se puede repetir, añade una
columna de desempate**, normalmente `id`.

Puedes ordenar por un alias o por una columna calculada:

```sql
SELECT name, price * 1.16 AS precio_con_iva
FROM products
ORDER BY precio_con_iva DESC;
```

---

## 7. LIMIT y OFFSET: los N primeros

```sql
SELECT name, price
FROM products
ORDER BY price DESC
LIMIT 3;                 -- los 3 productos más caros
```

`LIMIT` sin `ORDER BY` devuelve 3 filas **cualesquiera**: casi siempre es un error. "Los N mayores" siempre es `ORDER BY ... DESC LIMIT
N`.

`OFFSET` salta filas. Es la base de la **paginación**:

```sql
SELECT id, order_date
FROM orders
ORDER BY order_date, id
LIMIT 10 OFFSET 20;      -- la página 3, de 10 en 10 (salta las 20 primeras)
```

Para la página `p` (empezando en 1) con `n` filas por página: `LIMIT n OFFSET (p - 1) * n`. Otra vez el famoso "fuera por uno".

---

## 8. DISTINCT: valores sin repetir

```sql
SELECT DISTINCT segment
FROM customers
ORDER BY segment;
```

Devuelve cada segmento una sola vez. Con varias columnas, elimina las **combinaciones** repetidas:

```sql
SELECT DISTINCT country, segment
FROM customers
ORDER BY country, segment;
```

Esto devuelve cada par (país, segmento) que existe, una vez.

`DISTINCT` no es para "arreglar" resultados duplicados que no entiendes. Si una consulta te devuelve duplicados inesperados (pasará con
los JOIN), averigua por qué antes de añadir `DISTINCT`.

---

## 9. El orden en que SQL ejecuta una consulta

Escribes las cláusulas en un orden, pero la base de datos las **ejecuta en otro**. Entenderlo explica muchos errores:

| Orden de escritura | Orden de ejecución |
|---|---|
| `SELECT` columnas | 1. `FROM` (de qué tabla) |
| `FROM` tabla | 2. `WHERE` (qué filas) |
| `WHERE` condición | 3. `SELECT` (qué columnas y cálculos) |
| `ORDER BY` columnas | 4. `DISTINCT` |
| `LIMIT` n | 5. `ORDER BY` |
| | 6. `LIMIT` / `OFFSET` |

Consecuencia práctica: **no puedes usar en `WHERE` un alias definido en `SELECT`**, porque cuando se ejecuta el `WHERE` el alias todavía
no existe:

```sql
-- MAL: column "precio_con_iva" does not exist
SELECT name, price * 1.16 AS precio_con_iva
FROM products
WHERE precio_con_iva > 100;

-- BIEN: repite la expresión
SELECT name, price * 1.16 AS precio_con_iva
FROM products
WHERE price * 1.16 > 100;
```

En cambio, **sí** puedes usar el alias en `ORDER BY`, porque se ejecuta después del `SELECT`.

---

## 10. Cómo plantear una consulta

Ante cualquier enunciado:

1. **¿De qué tabla salen los datos?** → `FROM`.
2. **¿Qué filas me interesan?** → `WHERE`. Traduce cada condición del enunciado.
3. **¿Qué columnas devuelvo y con qué nombres?** → `SELECT` con alias.
4. **¿En qué orden?** → `ORDER BY`, con desempate si hace falta.
5. **¿Todas o solo algunas?** → `LIMIT`.

Ejemplo: *"Nombre y salario de los empleados de Ingenieria o Datos que ganan al menos 4000, del que más gana al que menos"*:

```sql
SELECT name, salary
FROM employees
WHERE department IN ('Ingenieria', 'Datos')
  AND salary >= 4000
ORDER BY salary DESC, name;
```

---

## 11. Errores típicos

| Error | Causa | Solución |
|---|---|---|
| `syntax error at or near "FROM"` | Coma después de la última columna del `SELECT` | Quita la coma |
| `column "chile" does not exist` | Texto con comillas dobles (o sin comillas) | Texto entre comillas simples: `'Chile'` |
| La consulta no devuelve filas | Mayúsculas distintas (`'chile'`), o `= NULL` | Revisa los valores reales; usa `IS NULL` |
| Devuelve demasiadas filas | `AND` y `OR` mezclados sin paréntesis | Agrupa con paréntesis |
| `column "alias" does not exist` en `WHERE` | Usaste un alias del `SELECT` en el `WHERE` | Repite la expresión |
| El orden cambia entre ejecuciones | Falta `ORDER BY` o falta desempate | Ordena siempre explícitamente |
| `LIMIT` devuelve filas al azar | `LIMIT` sin `ORDER BY` | Ordena antes de limitar |

---

## Resumen del capítulo

| Cláusula | Para qué | Recuerda |
|---|---|---|
| `SELECT` | Elegir y calcular columnas | Alias con `AS`; sin coma final |
| `FROM` | De qué tabla | |
| `WHERE` | Filtrar filas | `=`, `<>`, `AND`, `OR` (con paréntesis), texto entre comillas simples |
| `IN` / `BETWEEN` / `LIKE` | Listas, rangos (incluye extremos), patrones (`%`, `_`) | `LIKE` distingue mayúsculas; `ILIKE` no |
| `IS NULL` | Ausencia de valor | Nunca `= NULL`; `COALESCE` para reemplazar |
| `ORDER BY` | Ordenar | `DESC`; desempate con una segunda columna |
| `LIMIT` / `OFFSET` | Top N y paginación | Siempre con `ORDER BY` |
| `DISTINCT` | Quitar repetidos | No lo uses para tapar duplicados que no entiendes |

## Autoevaluación final

1. ¿Qué diferencia hay entre `'Chile'` y `"Chile"` en SQL?
2. ¿Qué devuelve `WHERE channel = 'app' OR channel = 'web' AND status = 'cancelado'`?
3. ¿Incluye `BETWEEN 10 AND 20` el valor 20?
4. ¿Qué patrón de `LIKE` encuentra los nombres que contienen "ar"?
5. ¿Por qué `WHERE manager_id = NULL` no devuelve nada?
6. ¿Cómo obtienes los 5 pedidos más recientes?
7. ¿Por qué no puedes usar en `WHERE` un alias del `SELECT`?
8. Tu enunciado dice "ordena por precio y luego por nombre". ¿Por qué hace falta lo segundo?

**Respuestas:** 1) `'Chile'` es un texto; `"Chile"` es el nombre de una columna. 2) Todos los pedidos de la app más los cancelados de la
web, porque `AND` va antes que `OR`. 3) Sí, `BETWEEN` incluye los dos extremos. 4) `LIKE '%ar%'`. 5) Porque cualquier comparación con
`NULL` da "desconocido"; se usa `IS NULL`. 6) `ORDER BY order_date DESC, id DESC LIMIT 5`. 7) Porque `WHERE` se ejecuta antes que
`SELECT` y el alias todavía no existe. 8) Porque puede haber productos con el mismo precio, y sin desempate su orden no está definido.
