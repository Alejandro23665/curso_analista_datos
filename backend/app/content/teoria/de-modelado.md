# Modelado de datos y data warehouse

Cuando diseñas las tablas de una aplicación, tomas decisiones que te acompañarán durante años: qué tabla guarda qué, cómo se relacionan,
qué se repite y qué no. Y cuando el negocio quiere **analizar** esos datos (ventas por mes, clientes por segmento, productos estrella),
descubres que las tablas pensadas para que la app funcione no son las mejores para analizar.

Este capítulo cubre las dos caras del modelado: **normalizar** para las aplicaciones (OLTP) y **modelar en estrella** para el análisis
(OLAP), con los conceptos que aparecen en cualquier conversación sobre datos: tablas de hechos y dimensiones, granularidad y dimensiones
que cambian con el tiempo. Te sirve tanto para diseñar la base de tu MVP como para construir el panel de métricas de un cliente.

---

## 1. Entidades, relaciones y claves

Modelar empieza por identificar las **entidades** (las "cosas" del negocio: cliente, producto, pedido) y sus **relaciones**:

| Relación | Ejemplo | Cómo se implementa |
|---|---|---|
| Uno a muchos (1:N) | Un cliente tiene muchos pedidos | Clave foránea en el lado "muchos": `orders.customer_id` |
| Muchos a muchos (N:M) | Un pedido tiene muchos productos y un producto está en muchos pedidos | **Tabla intermedia**: `order_items(order_id, product_id, ...)` |
| Uno a uno (1:1) | Un usuario y su perfil | Clave foránea única, o la misma tabla |

Las tablas del sandbox siguen exactamente este esquema:

```
customers (1) ──< orders (1) ──< order_items >── (1) products
   id              id               order_id           id
   name            customer_id      product_id         name
   country         order_date       quantity           category
   segment         status           unit_price         price
   signup_date     channel
```

- **Clave primaria** (*primary key*): identifica cada fila de forma única (`id`).
- **Clave foránea** (*foreign key*): apunta a la clave primaria de otra tabla y la base de datos garantiza que exista (no puede haber un
  pedido de un cliente inexistente).
- **Clave natural vs clave sustituta**: una clave natural tiene significado de negocio (un correo, un número de documento); una
  **sustituta** es un número sin significado (`id` autoincremental). Las sustitutas son más estables: el correo de un cliente puede
  cambiar, su `id` no.

Fíjate en un detalle de diseño de `order_items`: guarda `unit_price` aunque el producto ya tenga `price`. ¿Por qué? Porque el precio del
producto **cambia con el tiempo**, y el pedido debe recordar el precio **al que se vendió**. Es una decisión de modelado deliberada, no una
repetición.

---

## 2. Normalización: cada dato en un solo lugar

Imagina guardar los pedidos en una sola tabla gigante (datos inventados):

| pedido | fecha | cliente | país_cliente | producto | categoría | cantidad |
|---|---|---|---|---|---|---|
| 1 | 2024-07-19 | Luisa Perez | Venezuela | Aspiradora | Hogar | 1 |
| 1 | 2024-07-19 | Luisa Perez | Venezuela | Lámpara | Hogar | 5 |
| 2 | 2024-07-20 | Luisa Perez | Venezuela | Laptop 14 | Tecnologia | 1 |

Problemas (*anomalías*):

- **Actualización**: si Luisa se muda a Chile, hay que cambiar todas sus filas; si olvidas una, los datos se contradicen.
- **Inserción**: no puedes registrar un cliente nuevo hasta que haga un pedido.
- **Borrado**: si borras el único pedido de un cliente, pierdes también al cliente.
- **Espacio**: el nombre y el país se repiten en cada fila.

**Normalizar** es dividir los datos en tablas para que **cada dato esté en un solo lugar**. Las formas normales, en versión práctica:

| Forma normal | Regla | Ejemplo de violación |
|---|---|---|
| **1FN** | Cada celda tiene un solo valor; sin grupos repetidos | Una columna `productos` con "Aspiradora, Lámpara" |
| **2FN** | Cada columna depende de **toda** la clave | En `order_items(order_id, product_id, nombre_producto)`, el nombre depende solo de `product_id` |
| **3FN** | Las columnas dependen **solo** de la clave, no de otras columnas | En `orders`, guardar el `país_cliente` (depende del cliente, no del pedido) |

La frase que resume las tres: *cada columna debe depender de la clave, de toda la clave y de nada más que la clave*.

Para las aplicaciones (OLTP), **normaliza hasta 3FN** por defecto. Desnormaliza solo con un motivo claro y medido (rendimiento de una
consulta concreta, o guardar un valor histórico como el `unit_price`).

---

## 3. OLTP y OLAP: dos usos, dos diseños

| | OLTP (transaccional) | OLAP (analítico) |
|---|---|---|
| Para qué | Que la aplicación funcione | Analizar el negocio |
| Operaciones | Muchas pequeñas: insertar un pedido, leer un cliente | Pocas y enormes: sumar todas las ventas de 3 años |
| Usuarios | La app, miles de peticiones por segundo | Analistas, paneles, informes |
| Diseño | Normalizado (3FN) | Desnormalizado: **esquema en estrella** |
| Datos | El estado actual | Historia completa |
| Ejemplos | PostgreSQL, MySQL | BigQuery, Snowflake, Redshift, ClickHouse, DuckDB |

### Por qué no analizar sobre la base de producción

Si el equipo de análisis lanza consultas pesadas (sumar millones de filas con varios `JOIN`) sobre la base de producción, **compiten con
la aplicación** por CPU, memoria y disco: la tienda se vuelve lenta para los clientes. La solución estándar es **copiar los datos** a un
almacén analítico (*data warehouse*) y consultar allí:

```
Base de producción (OLTP)  ──►  Proceso ETL/ELT (periódico)  ──►  Data warehouse (OLAP)  ──►  Paneles, informes, análisis
```

- **ETL**: extraer, **transformar** (limpiar, modelar) y cargar.
- **ELT**: extraer, cargar los datos crudos en el warehouse y transformarlos **allí** con SQL. Es el enfoque moderno (con herramientas
  como **dbt**), porque los warehouses son muy potentes.

Para proyectos pequeños, una **réplica de lectura** de la base, o una tabla resumen que se recalcula cada noche, puede bastar.

---

## 4. El esquema en estrella

El modelo estándar para análisis tiene dos tipos de tablas:

- **Tabla de hechos** (*fact table*): los **eventos medibles** del negocio, con sus **métricas** numéricas (cantidades, importes) y
  claves hacia las dimensiones. Es larga (millones de filas) y estrecha.
- **Tablas de dimensiones**: el **contexto** de los hechos (quién, qué, cuándo, dónde, cómo), con atributos descriptivos por los que se
  filtra y agrupa. Son cortas y anchas.

```
                    dim_fecha
                  (fecha, día, mes,
                  trimestre, año, festivo)
                        │
dim_cliente ─── fact_ventas ─── dim_producto
(nombre, país,   (fecha_key, cliente_key,     (nombre, categoría,
 segmento)        producto_key, canal_key,      marca)
                  unidades, ingresos)
                        │
                    dim_canal
                  (web, app, tienda)
```

Por qué funciona tan bien para analizar:

- Cualquier pregunta del negocio es "**métrica** por **dimensiones**": ingresos por mes y categoría, unidades por país y canal.
- Las consultas son siempre iguales: la tabla de hechos con `JOIN` a las dimensiones que necesitas, `GROUP BY` y `SUM`.
- Las dimensiones están **desnormalizadas** a propósito (la categoría dentro de `dim_producto`, el país dentro de `dim_cliente`): menos
  `JOIN`, consultas más simples y rápidas.

### La dimensión de fecha

Casi todo warehouse tiene una `dim_fecha` con una fila por día y columnas como día de la semana, mes, trimestre, año, si es festivo o fin
de semana. Permite agrupar y filtrar por cualquier atributo del calendario sin cálculos repetidos ("ventas en festivos", "por trimestre
fiscal").

---

## 5. Granularidad: la decisión más importante

La **granularidad** (*grain*) de una tabla de hechos es **qué representa una fila**. Es la primera decisión, y la más difícil de cambiar.

| Granularidad | Una fila es... | Puedes responder | No puedes responder |
|---|---|---|---|
| Línea de pedido | Un producto dentro de un pedido | Todo: por producto, pedido, cliente, día... | — |
| Pedido | Un pedido completo | Por cliente, día, canal | Por producto o categoría |
| Día y categoría | La suma de un día en una categoría | Por día y categoría | Por cliente, canal o producto |
| Mes | El total de un mes | Por mes | Casi nada más |

La regla: **elige la granularidad más fina disponible** (la línea de pedido, en una tienda). Desde el detalle siempre puedes **agregar**
hacia arriba (sumar por día, por mes); desde un agregado **nunca** puedes volver al detalle. Si hoy te piden "totales por día" pero mañana
preguntan "¿y por producto?", con una tabla diaria tendrías que rehacerlo todo.

Las **tablas agregadas** (por día y categoría, por ejemplo) se construyen **además** de la tabla de detalle, para que los paneles sean
rápidos. Construir una es un ejercicio típico de SQL: unir las tablas necesarias, filtrar los eventos que cuentan y agrupar por las
dimensiones del agregado.

```sql
-- Agregado mensual por país, solo pedidos completados, segundo trimestre de 2025 (PostgreSQL)
SELECT TO_CHAR(o.order_date, 'YYYY-MM') AS mes,
       c.country                       AS pais,
       COUNT(DISTINCT o.id)            AS pedidos,
       SUM(oi.quantity)                AS unidades,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS ingresos
FROM orders o
JOIN customers c    ON c.id = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
WHERE o.status = 'completado'
  AND o.order_date >= '2025-04-01' AND o.order_date < '2025-07-01'
GROUP BY TO_CHAR(o.order_date, 'YYYY-MM'), c.country
ORDER BY mes, pais;
```

Primeras filas del resultado:

| mes | pais | pedidos | unidades | ingresos |
|---|---|---|---|---|
| 2025-04 | Argentina | 2 | 10 | 2001.00 |
| 2025-04 | Chile | 2 | 10 | 647.00 |
| 2025-04 | Colombia | 3 | 19 | 1986.98 |
| 2025-04 | Espana | 3 | 40 | 4042.96 |
| 2025-04 | Mexico | 1 | 1 | 79.00 |

Detalles a observar:

- Los **ingresos** se calculan a partir de la línea (`quantity * unit_price`), no del precio actual del producto.
- `COUNT(DISTINCT o.id)`: después del `JOIN` con `order_items`, cada pedido aparece una vez **por línea**; sin `DISTINCT` contarías líneas,
  no pedidos. Es el error clásico de "el `JOIN` multiplicó las filas".
- El rango de fechas con `>=` el primer día y `<` el primer día del periodo siguiente funciona igual con fechas y con fechas con hora.
- El filtro de estado va en el `WHERE`, **antes** de agrupar.

### Métricas aditivas y no aditivas

- **Aditivas**: se pueden sumar por cualquier dimensión (unidades, ingresos).
- **No aditivas**: no se pueden sumar (precios unitarios, porcentajes, promedios). El ticket medio de un mes **no** es el promedio de los
  tickets medios diarios: se recalcula como ingresos totales / pedidos totales. Por eso las tablas de hechos guardan los **componentes**
  (ingresos y pedidos), no el cociente.

---

## 6. Dimensiones que cambian: SCD

Un cliente pasa del segmento "Pyme" a "Corporativo". ¿Qué hacemos con su fila en `dim_cliente`? Depende de qué necesite el análisis. Las
técnicas se llaman **SCD** (*Slowly Changing Dimensions*, dimensiones que cambian lentamente):

### Tipo 1: sobrescribir

Se actualiza el valor. Simple, pero **se pierde la historia**: todas sus ventas, también las de hace dos años, aparecerán como
"Corporativo". Adecuado para correcciones (un nombre mal escrito) o cuando la historia no importa.

### Tipo 2: nueva fila con fechas de vigencia

Se **cierra** la fila antigua y se crea una nueva:

| cliente_key | cliente_id | nombre | segmento | valido_desde | valido_hasta | actual |
|---|---|---|---|---|---|---|
| 101 | 7 | Luisa Perez | Pyme | 2023-01-10 | 2025-03-31 | no |
| 245 | 7 | Luisa Perez | Corporativo | 2025-04-01 | 9999-12-31 | sí |

- Cada fila tiene su propia **clave sustituta** (`cliente_key`), y los hechos apuntan a la versión **vigente en la fecha del hecho**: una
  venta de 2024 apunta a la fila 101 (Pyme); una de mayo de 2025, a la 245 (Corporativo).
- Así, las ventas de 2024 **siguen contando como Pyme**, que es lo correcto para analizar la historia.
- Es la técnica más usada cuando la historia importa.

### Tipo 3: columna con el valor anterior

Se añade una columna `segmento_anterior`. Solo guarda **un** cambio; se usa poco.

| Tipo | Historia | Complejidad | Cuándo |
|---|---|---|---|
| 1 | Se pierde | Baja | Correcciones; la historia no importa |
| 2 | Completa | Media | Hay que analizar el pasado con los valores de entonces |
| 3 | Solo el valor anterior | Baja | Comparar "antes y después" de un único cambio |

---

## 7. Del modelo a la práctica

### Herramientas que verás en las ofertas

- **dbt**: escribir las transformaciones del warehouse como consultas `SELECT` versionadas en Git, con pruebas (únicos, no nulos,
  relaciones) y documentación. Es el estándar actual de la "ingeniería analítica".
- **Warehouses**: BigQuery, Snowflake, Redshift; para proyectos pequeños, **DuckDB** (un warehouse en un archivo, perfecto para practicar)
  o el mismo PostgreSQL.
- **Orquestadores**: Airflow, Dagster, Prefect, para ejecutar los procesos en orden y a su hora.
- **BI**: Metabase, Looker Studio, Power BI, que se conectan al warehouse.

### Para tus proyectos

- **En tu MVP o la app de un cliente**: diseña la base normalizada (3FN), con claves foráneas y restricciones. Guarda los valores
  históricos que importan (precio en la venta, estado con fecha).
- **Para el panel de métricas de un cliente**: una tabla de hechos con la granularidad más fina, unas pocas dimensiones y, si hace falta
  velocidad, tablas agregadas que se recalculan cada noche. Muchas veces bastan unas **vistas** de SQL sobre una réplica de la base.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Relaciones | 1:N con clave foránea; N:M con tabla intermedia |
| Claves | Primaria, foránea; sustituta (estable) vs natural |
| Normalización | Cada dato en un solo lugar; 3FN para aplicaciones |
| OLTP vs OLAP | Operaciones pequeñas vs análisis masivo; separar con un warehouse |
| ETL / ELT | Transformar antes o después de cargar; ELT + dbt es lo moderno |
| Esquema en estrella | Hechos (métricas) + dimensiones (contexto) desnormalizadas |
| Granularidad | Qué es una fila; la más fina disponible; agregar siempre es posible, desagregar no |
| Métricas | Aditivas se suman; las no aditivas se recalculan desde sus componentes |
| SCD | Tipo 1 sobrescribe; tipo 2 versiona con fechas; tipo 3 guarda el anterior |

## Autoevaluación final

1. ¿Cómo se implementa una relación muchos a muchos entre estudiantes y cursos?
2. ¿Por qué `order_items` guarda `unit_price` si `products` ya tiene `price`?
3. Una tabla `orders` tiene la columna `pais_cliente`. ¿Qué forma normal viola y qué problema causa?
4. ¿Por qué no conviene que los analistas consulten directamente la base de producción?
5. ¿Qué diferencia hay entre una tabla de hechos y una de dimensiones?
6. Hoy te piden ventas por día, pero podrían pedir por producto. ¿Qué granularidad eliges y por qué?
7. Después de unir `orders` con `order_items`, ¿por qué `COUNT(*)` no cuenta pedidos?
8. ¿Por qué no se puede promediar el ticket medio de cada día para obtener el del mes?
9. Un cliente cambia de segmento y las ventas pasadas deben seguir mostrando el segmento antiguo. ¿Qué tipo de SCD usas?

**Respuestas:** 1) Con una tabla intermedia `inscripciones(estudiante_id, curso_id, ...)`. 2) Porque el precio cambia con el tiempo y el
pedido debe recordar el precio al que se vendió. 3) La 3FN (el país depende del cliente, no del pedido); si el cliente se muda, hay que
actualizar muchas filas y pueden quedar contradicciones. 4) Porque sus consultas pesadas compiten por recursos con la aplicación y la
vuelven lenta. 5) La de hechos guarda eventos con métricas numéricas y claves; las dimensiones guardan el contexto descriptivo para
filtrar y agrupar. 6) La línea de pedido: la más fina, desde la que se puede agregar a cualquier nivel. 7) Porque cada pedido aparece una
vez por línea; se usa `COUNT(DISTINCT o.id)`. 8) Porque es una métrica no aditiva: los días con más pedidos deben pesar más; se calcula
como ingresos totales / pedidos totales. 9) SCD tipo 2.
