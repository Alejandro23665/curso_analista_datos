# Funciones de ventana

Las funciones de ventana son la herramienta de SQL que más separa a un perfil junior de uno que "sabe SQL de verdad", y por eso son la
**pregunta estrella de las entrevistas**: el segundo salario más alto de cada departamento, el último pedido de cada cliente, la variación
mes a mes, el total acumulado. Todas se resuelven con lo que vas a aprender aquí.

Necesitas dominar `GROUP BY` y las CTE de los capítulos anteriores. Si alguno de los dos te genera dudas, repásalo antes.

---

## 1. El problema que resuelven

`GROUP BY` resume, pero **colapsa las filas**: si agrupas los empleados por departamento, pierdes a cada empleado y te queda una fila por
departamento. ¿Y si quieres **cada empleado** junto al promedio de **su** departamento, para compararlos?

```
name           department  salary  promedio_depto
Felipe Cruz    Datos        4800    4550.00
Nicolas Pardo  Datos        3800    4550.00
Monica Reyes   Ingenieria   4500    4980.00
...
```

Con lo que sabes, necesitarías una subconsulta correlacionada o un JOIN con una CTE agregada. Con una función de ventana es una línea:

```sql
SELECT name,
       department,
       salary,
       ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS promedio_depto
FROM employees
ORDER BY department, salary DESC;
```

Una **función de ventana** calcula un valor para **cada fila** mirando un conjunto de filas relacionadas (su "ventana"), **sin colapsar
nada**. El resultado tiene tantas filas como la tabla original.

---

## 2. La sintaxis: OVER

Todo lo que lleva `OVER (...)` es una función de ventana:

```
FUNCIÓN(...) OVER (PARTITION BY columnas   ORDER BY columnas   marco)
                   ─────────────────────   ─────────────────   ─────
                   qué filas forman         en qué orden se     (opcional) qué parte
                   el grupo de cada fila    recorren            de la ventana usar
```

- **`PARTITION BY`**: divide las filas en grupos, como `GROUP BY`, **pero sin colapsarlas**. Cada fila ve solo las filas de su
  partición. Sin `PARTITION BY`, la ventana es toda la tabla.
- **`ORDER BY`** (dentro del `OVER`): el orden dentro de cada partición. Es imprescindible para los rankings, para "el anterior" y para
  los acumulados.

### Agregaciones como ventana

Cualquier función de agregación (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`) se convierte en función de ventana al añadirle `OVER`:

```sql
SELECT name,
       department,
       salary,
       COUNT(*)    OVER (PARTITION BY department) AS personas_depto,
       MAX(salary) OVER (PARTITION BY department) AS maximo_depto,
       SUM(salary) OVER ()                        AS nomina_empresa
FROM employees
ORDER BY department, name;
```

`OVER ()` vacío significa "toda la tabla es la ventana".

Con esto puedes comparar cada fila con su grupo directamente:

```sql
SELECT name, department, salary,
       salary - AVG(salary) OVER (PARTITION BY department) AS diferencia
FROM employees
ORDER BY department, diferencia DESC;
```

---

## 3. Funciones de ranking

Para numerar o clasificar filas dentro de cada partición, en el orden que indique el `ORDER BY` del `OVER`:

| Función | Qué hace con los empates |
|---|---|
| `ROW_NUMBER()` | Numera 1, 2, 3, 4... **siempre distinto**, aunque haya empate (el orden entre empatados es arbitrario si no desempatas) |
| `RANK()` | Los empatados reciben el mismo número y **se salta** los siguientes: 1, 2, 2, 4 |
| `DENSE_RANK()` | Los empatados reciben el mismo número y **no se salta** ninguno: 1, 2, 2, 3 |

Con los salarios de un departamento ordenados de mayor a menor:

| salario | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
|---|---|---|---|
| 5100 | 1 | 1 | 1 |
| 4800 | 2 | 2 | 2 |
| 3800 | 3 | 3 | 3 |
| 3800 | 4 | 3 | 3 |
| 3400 | 5 | 5 | 4 |

Elegir la correcta depende de la pregunta:

- "**Un** elemento por grupo" (el último pedido, el producto más caro): `ROW_NUMBER`, con un desempate en el `ORDER BY` para que el
  resultado sea determinista.
- "El puesto en una clasificación, como en una competición": `RANK`.
- "El segundo **valor** más alto" (si dos empatan en el primero, el segundo es el siguiente valor distinto): `DENSE_RANK`.

Ranking de productos por precio dentro de cada categoría:

```sql
SELECT category,
       name,
       price,
       RANK() OVER (PARTITION BY category ORDER BY price DESC) AS puesto
FROM products
ORDER BY category, puesto, name;
```

---

## 4. El patrón "el primero de cada grupo"

Es probablemente **la** pregunta de entrevista de SQL: "el producto más caro de cada categoría", "el último pedido de cada cliente", "el
empleado más antiguo de cada departamento". El patrón tiene dos pasos:

1. Numerar las filas de cada grupo en el orden adecuado.
2. Quedarse con las que tienen el número 1.

```sql
WITH numerados AS (
    SELECT category,
           name,
           price,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC, name) AS rn
    FROM products
)
SELECT category, name, price
FROM numerados
WHERE rn = 1
ORDER BY category;
```

¿Por qué hace falta la CTE? Porque **no puedes filtrar una función de ventana en el `WHERE`** de la misma consulta: las ventanas se
calculan **después** del `WHERE`. Primero calculas el número en una CTE (o subconsulta) y filtras fuera.

Fíjate en `ORDER BY price DESC, name` dentro del `OVER`: si dos productos tienen el mismo precio, el nombre decide cuál es el número 1.
Sin desempate, el resultado podría cambiar entre ejecuciones.

Variantes del mismo patrón:

- "Los **3** mejores de cada grupo": `WHERE rn <= 3`.
- "El **segundo** mayor valor": `DENSE_RANK()` y `WHERE puesto = 2`.
- "El **último**": ordena en sentido contrario (`DESC` en lugar de `ASC`, o al revés) y quédate con el 1.

---

## 5. LAG y LEAD: mirar la fila anterior o la siguiente

`LAG(columna)` devuelve el valor de esa columna en la **fila anterior** (según el `ORDER BY` del `OVER`); `LEAD(columna)`, el de la
**siguiente**. Son la herramienta para comparar periodos: este mes con el anterior, cada pedido con el pedido previo del mismo cliente.

Días transcurridos entre contrataciones consecutivas:

```sql
SELECT name,
       hire_date,
       LAG(hire_date) OVER (ORDER BY hire_date) AS contratacion_anterior
FROM employees
ORDER BY hire_date;
```

La primera fila no tiene anterior: `LAG` devuelve `NULL`. Puedes dar un valor por defecto como tercer argumento: `LAG(columna, 1, 0)` (el
`1` es "una fila atrás").

### Variación entre periodos

El patrón típico: primero agregar por periodo (en una CTE) y luego aplicar `LAG` sobre ese resultado. Pedidos por canal y año, con la
variación respecto al año anterior del mismo canal:

```sql
WITH por_anio AS (
    SELECT channel,
           SUBSTR(CAST(order_date AS TEXT), 1, 4) AS anio,
           COUNT(*) AS pedidos
    FROM orders
    GROUP BY channel, anio
)
SELECT channel,
       anio,
       pedidos,
       pedidos - LAG(pedidos) OVER (PARTITION BY channel ORDER BY anio) AS variacion
FROM por_anio
ORDER BY channel, anio;
```

Fíjate en el `PARTITION BY channel`: sin él, el primer año de "tienda" se compararía con el último año de "app". La partición hace que
`LAG` solo mire dentro de cada canal.

Sobre las fechas: `SUBSTR(CAST(order_date AS TEXT), 1, 4)` toma los 4 primeros caracteres de la fecha (el año), y con `1, 7` obtendrías
`'AAAA-MM'` (el mes). Funciona tanto en SQLite como en PostgreSQL. En PostgreSQL también existe `DATE_TRUNC('month', order_date)`.

---

## 6. Totales acumulados

`SUM(...) OVER (ORDER BY ...)` suma desde la primera fila **hasta la actual**: un total acumulado (*running total*).

Pedidos por mes de 2025 y su acumulado en el año:

```sql
WITH por_mes AS (
    SELECT SUBSTR(CAST(order_date AS TEXT), 1, 7) AS mes,
           COUNT(*) AS pedidos
    FROM orders
    WHERE order_date >= '2025-01-01'
    GROUP BY mes
)
SELECT mes,
       pedidos,
       SUM(pedidos) OVER (ORDER BY mes) AS acumulado
FROM por_mes
ORDER BY mes;
```

| mes | pedidos | acumulado |
|---|---|---|
| 2025-01 | 6 | 6 |
| 2025-02 | 15 | 21 |
| 2025-03 | 10 | 31 |
| ... | ... | ... |

La regla clave: **con `ORDER BY` dentro del `OVER`, la ventana va del principio hasta la fila actual**. Sin `ORDER BY`, la ventana es la
partición entera y obtendrías el total en todas las filas.

### Marcos: controlar exactamente qué filas entran

Puedes indicar explícitamente qué filas forman la ventana con un **marco** (`ROWS BETWEEN ...`). Una media móvil de 3 meses:

```sql
AVG(pedidos) OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
```

"El promedio de esta fila y las dos anteriores". Útil para suavizar series con mucho ruido.

Un detalle que causa sorpresas: con `ORDER BY` y sin marco explícito, si hay **valores repetidos** en la columna de orden (dos filas del
mismo día), el acumulado los suma **juntos** a las dos. Si necesitas un acumulado fila a fila, añade `ROWS BETWEEN UNBOUNDED PRECEDING
AND CURRENT ROW` o un desempate. Cuando agregas primero por día o por mes (una fila por periodo), este problema no existe.

---

## 7. Porcentaje sobre el total del grupo

Combinar el valor de la fila con el total de su partición:

```sql
SELECT category,
       name,
       price,
       ROUND(100.0 * price / SUM(price) OVER (PARTITION BY category), 1) AS pct_de_su_categoria
FROM products
ORDER BY category, pct_de_su_categoria DESC;
```

`SUM(price) OVER (PARTITION BY category)` es la suma de precios de la categoría de esa fila. Dividir y multiplicar por `100.0` (recuerda
la división entera) da el porcentaje.

### Ventanas sobre un resultado agregado

Puedes aplicar una ventana **sobre una agregación** en la misma consulta, porque las ventanas se calculan después del `GROUP BY`. Cuota de
pedidos de cada canal sobre el total:

```sql
SELECT channel,
       COUNT(*) AS pedidos,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM orders
GROUP BY channel
ORDER BY pct DESC;
```

`SUM(COUNT(*)) OVER ()` suena raro, pero se lee así: "la suma, sobre todas las filas del resultado, de los conteos de cada grupo", es decir,
el total de pedidos.

---

## 8. Otras funciones útiles

| Función | Qué hace |
|---|---|
| `FIRST_VALUE(col)` / `LAST_VALUE(col)` | El primer / último valor de la ventana |
| `NTILE(n)` | Reparte las filas en `n` grupos de tamaño parecido (cuartiles: `NTILE(4)`) |
| `PERCENT_RANK()` | Posición relativa entre 0 y 1 |

`NTILE(4) OVER (ORDER BY salary)` asigna a cada empleado su cuartil salarial: útil para segmentar clientes en "top 25 %", etc.

---

## 9. Dónde encajan en el orden de ejecución

```
FROM → WHERE → GROUP BY → HAVING → funciones de ventana → SELECT → ORDER BY → LIMIT
```

Consecuencias:

- Las ventanas **ven las filas que dejaron `WHERE` y `GROUP BY`**. Si filtras en el `WHERE`, el ranking se calcula solo sobre las filas
  que quedan.
- **No puedes usar una función de ventana en `WHERE`, `GROUP BY` ni `HAVING`**: todavía no se ha calculado. Para filtrar por ella,
  calcula en una CTE y filtra fuera.
- **Sí** puedes usarla en `ORDER BY`.
- Puedes aplicar ventanas sobre agregaciones (`SUM(COUNT(*)) OVER ()`), porque `GROUP BY` ya se ejecutó.

---

## 10. Cómo reconocer qué función usar

| La pregunta dice... | Herramienta |
|---|---|
| "...de cada X" y quieres conservar el detalle | Agregación con `OVER (PARTITION BY X)` |
| "el primero / el último / el más ... de cada X" | `ROW_NUMBER()` + CTE + `WHERE rn = 1` |
| "el segundo valor más alto" | `DENSE_RANK()` + `WHERE puesto = 2` |
| "posición en el ranking" | `RANK()` |
| "respecto al anterior / variación / crecimiento" | `LAG()` |
| "acumulado / hasta la fecha" | `SUM() OVER (ORDER BY ...)` |
| "porcentaje sobre el total del grupo" | `valor / SUM(valor) OVER (PARTITION BY ...)` |
| "media móvil" | `AVG() OVER (ORDER BY ... ROWS BETWEEN n PRECEDING AND CURRENT ROW)` |

---

## 11. Errores típicos

| Error | Causa | Solución |
|---|---|---|
| `window functions are not allowed in WHERE` | Filtrar por `ROW_NUMBER()` en el mismo nivel | Calcula en una CTE y filtra fuera |
| El "primero de cada grupo" cambia entre ejecuciones | `ROW_NUMBER` sin desempate | Añade una columna de desempate al `ORDER BY` del `OVER` |
| El acumulado muestra el total en todas las filas | Falta `ORDER BY` dentro del `OVER` | `SUM(x) OVER (ORDER BY fecha)` |
| `LAG` compara con otro grupo | Falta `PARTITION BY` | Particiona por la entidad |
| El ranking salta números | Usaste `RANK` y querías `DENSE_RANK` | Elige según la pregunta |
| Porcentajes en 0 | División entera | `100.0 * ...` |
| Acumulados que suman dos filas a la vez | Valores repetidos en el `ORDER BY` | Marco `ROWS` o agregar por periodo antes |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Ventana | Calcula por fila mirando filas relacionadas, sin colapsar |
| `OVER (PARTITION BY ...)` | El grupo de cada fila; como `GROUP BY` sin perder filas |
| `OVER (ORDER BY ...)` | El orden dentro del grupo; necesario para rankings, `LAG` y acumulados |
| `ROW_NUMBER` / `RANK` / `DENSE_RANK` | Siempre distinto / empates con salto / empates sin salto |
| Primero de cada grupo | `ROW_NUMBER` en una CTE, `WHERE rn = 1` fuera |
| `LAG` / `LEAD` | Fila anterior / siguiente; variaciones entre periodos |
| Acumulado | `SUM() OVER (ORDER BY ...)` |
| Porcentaje del grupo | `valor / SUM(valor) OVER (PARTITION BY ...)` |
| Orden de ejecución | Después de `GROUP BY`/`HAVING`, antes de `ORDER BY`; nunca en `WHERE` |

## Autoevaluación final

1. ¿Qué diferencia hay entre `AVG(salary)` con `GROUP BY department` y `AVG(salary) OVER (PARTITION BY department)`?
2. Con los valores 90, 80, 80, 70 ordenados de mayor a menor, ¿qué da `RANK()` y qué da `DENSE_RANK()` para el 70?
3. ¿Por qué no se puede escribir `WHERE ROW_NUMBER() OVER (...) = 1`?
4. ¿Para qué sirve el desempate dentro del `ORDER BY` del `OVER`?
5. ¿Qué devuelve `LAG(x)` en la primera fila de una partición?
6. ¿Qué cambia entre `SUM(x) OVER ()` y `SUM(x) OVER (ORDER BY fecha)`?
7. ¿Por qué hace falta `PARTITION BY channel` al calcular la variación mensual por canal?
8. ¿Cómo calculas el porcentaje que representa cada fila sobre el total de su grupo?

**Respuestas:** 1) Con `GROUP BY` obtienes una fila por departamento; con `OVER` conservas cada empleado y le añades el promedio de su
departamento. 2) `RANK()` da 4 y `DENSE_RANK()` da 3. 3) Porque las ventanas se calculan después del `WHERE`; hay que calcularla en una CTE
y filtrar fuera. 4) Para que el orden entre filas empatadas sea siempre el mismo y el resultado sea determinista. 5) `NULL` (o el valor
por defecto que indiques). 6) `OVER ()` da el total de todas las filas en cada fila; con `ORDER BY` da el acumulado hasta la fila actual.
7) Para que `LAG` compare cada mes con el anterior **del mismo canal** y no con otro canal. 8) `100.0 * valor / SUM(valor) OVER (PARTITION
BY grupo)`.
