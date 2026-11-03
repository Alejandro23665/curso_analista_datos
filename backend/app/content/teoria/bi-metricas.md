# Métricas, KPIs y dashboards

Todo negocio quiere saber si va bien. Pero "ir bien" no significa nada hasta que lo conviertes en **números bien definidos**, calculados
de la misma forma cada vez y presentados para que alguien pueda **tomar una decisión** con ellos. Ese es el trabajo de las métricas.

Te sirve en tres frentes: como analista o backend (calcular métricas con SQL es una tarea diaria), como freelance (un cliente valora
enormemente un panel que le diga qué está pasando en su negocio, y es lo que justifica una mensualidad) y como fundador (sin las métricas
correctas, no sabrás si tu startup funciona). Este capítulo cubre cómo definir una métrica, los KPIs más usados con su cálculo, los
errores que producen números engañosos y cómo diseñar un dashboard que se use.

---

## 1. Métrica, KPI y métrica de vanidad

- Una **métrica** es cualquier número medido: visitas, pedidos, ingresos.
- Un **KPI** (*Key Performance Indicator*) es una de las **pocas** métricas que indican si el negocio cumple sus objetivos. Un equipo
  tiene 3-5, no 40.
- Una **métrica de vanidad** es la que se ve bien pero **no ayuda a decidir nada**: descargas totales históricas, seguidores, páginas
  vistas. Casi siempre sube, no dice si el producto funciona y no indica qué hacer.

La prueba para distinguirlas: *"si este número cambia, ¿qué haría distinto?"*. Si no hay respuesta, es vanidad.

| Vanidad | Accionable |
|---|---|
| Descargas totales | % de usuarios nuevos que completan su primera compra en 7 días |
| Registros totales | % de registros que siguen activos a las 4 semanas |
| Páginas vistas | Conversión de visita a compra, por canal |
| Mensajes totales del chatbot | % de conversaciones resueltas sin pasar a una persona |

Las métricas accionables suelen ser **tasas o proporciones** (no totales acumulados), **acotadas en el tiempo** (en 7 días, este mes) y
**segmentables** (por canal, país, tipo de cliente).

## 2. Definir bien una métrica

"Ingresos del mes" parece claro hasta que preguntas: ¿con o sin impuestos? ¿cuentan los pedidos cancelados? ¿y los pendientes? ¿por fecha
del pedido o del pago? ¿en qué zona horaria acaba el mes? Dos personas calcularán números distintos, y la reunión se perderá discutiendo
cuál es el correcto.

Cada KPI necesita una **definición escrita**:

```
Nombre:       Ticket promedio
Definición:   Importe medio por pedido completado.
Cálculo:      SUM(importe de los pedidos completados) / COUNT(pedidos completados)
              importe de un pedido = SUM(quantity * unit_price) de sus líneas
Incluye:      Solo pedidos con status = 'completado'.
Periodo:      Por fecha del pedido (order_date), mes natural, hora de Caracas.
Fuente:       Tablas orders y order_items.
Responsable:  Equipo comercial.
```

Esto es lo que se llama una **capa semántica**: una única definición de cada métrica que usan todos los paneles e informes.

## 3. Los KPIs más usados

### Conversión

**Qué fracción de quienes empiezan un paso llegan al siguiente.**

```
conversión = quienes completaron / quienes empezaron
```

Se analiza como un **embudo** (visitas → producto → carrito → pago → compra) para ver dónde se pierde la gente. La pregunta siempre es:
¿en qué paso cae más, y en qué segmento?

Una variante muy usada es la **tasa** de un estado: qué porcentaje de pedidos terminan completados, cancelados o devueltos, por canal o
por mes. En SQL, el patrón es `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` dividido entre `COUNT(*)`, con `100.0` para evitar la división
entera (como viste en el capítulo de entrevistas).

### Ticket promedio (AOV, *Average Order Value*)

**Importe medio por pedido.** Tiene una trampa que casi todo el mundo pisa la primera vez: los importes están en las **líneas** del pedido
(`order_items`), así que hay que calcular primero **el total de cada pedido** y después promediar esos totales. Promediar directamente
las líneas da el importe medio **por línea**, que es otra cosa.

```sql
-- Ticket promedio por país, solo pedidos completados
WITH totales AS (                                       -- 1) un total por pedido
    SELECT o.id, c.country, SUM(oi.quantity * oi.unit_price) AS total
    FROM orders o
    JOIN customers c    ON c.id = o.customer_id
    JOIN order_items oi ON oi.order_id = o.id
    WHERE o.status = 'completado'
    GROUP BY o.id, c.country
)
SELECT country, COUNT(*) AS pedidos, ROUND(AVG(total), 2) AS ticket_promedio   -- 2) promedio de los totales
FROM totales
GROUP BY country
ORDER BY country;
```

| country | pedidos | ticket_promedio |
|---|---|---|
| Argentina | 21 | 792.15 |
| Chile | 26 | 906.35 |
| Colombia | 34 | 777.85 |
| Espana | 32 | 815.31 |
| Mexico | 32 | 780.76 |
| Venezuela | 10 | 895.34 |

Si promedias las líneas directamente (`AVG(oi.quantity * oi.unit_price)` sin la CTE), Chile sale con 362.54: menos de la mitad del ticket
real, porque cada pedido tiene varias líneas. Es un error silencioso: la consulta funciona y el número parece razonable.

Fíjate en el **nivel de agregación** como patrón general: muchas métricas necesitan dos pasos, primero agrupar al nivel de la entidad que
cuentas (el pedido, el cliente) y después al nivel del informe (el país, el mes).

### Retención

**De los clientes de un periodo, qué fracción vuelve en el siguiente.** Es probablemente la métrica más importante de un producto: si los
usuarios no vuelven, todo lo demás da igual.

```
retención (de marzo a abril) = |clientes de marzo que también compraron en abril| / |clientes de marzo|
```

Con conjuntos de Python, "los que están en los dos" es la **intersección** (`a & b`), y `len()` cuenta los elementos. Ejemplo con datos
inventados:

```python
marzo = {"ana", "luis", "eva", "jose"}
abril = {"luis", "jose", "carla"}

marzo & abril            # {'luis', 'jose'}
len(marzo & abril)       # 2  → 2 de 4 clientes de marzo volvieron
```

Detalles: la retención se calcula sobre los del **primer** periodo (Carla es nueva en abril: no cuenta como retenida), los duplicados no
deben contar dos veces (por eso los conjuntos), y hay que decidir qué devolver si el primer periodo no tiene clientes (no se puede dividir
entre cero).

En los datos del sandbox, de los 8 clientes con pedidos en marzo de 2025 solo 1 volvió a comprar en abril: una retención del 12,5 %.
Para una tienda, la retención mensual suele ser baja; para un producto de suscripción, es lo que decide si sobrevive.

La versión más completa es el **análisis de cohortes**: agrupar a los usuarios por su semana o mes de registro y ver qué fracción sigue
activa en cada periodo posterior. Lo verás en *Startup: del problema al MVP*.

### Churn (abandono)

**La fracción de clientes que se pierde en un periodo.** Es el complemento de la retención en productos de suscripción: si retienes el 95 %
cada mes, el churn mensual es del 5 %.

### LTV (*Lifetime Value*, valor de vida del cliente)

**Cuánto margen deja un cliente durante toda su relación con el negocio.** Una aproximación simple para suscripciones:

```
LTV ≈ ARPU × margen / churn
```

- **ARPU** (*Average Revenue Per User*): ingreso medio por usuario y periodo (por ejemplo, 20 USD al mes).
- **Margen**: la fracción del ingreso que queda tras los costos directos (0,7 = 70 %).
- **Churn**: la fracción que abandona por periodo (0,05 = 5 % mensual). `1 / churn` es la duración media de un cliente: con un 5 %
  mensual, unos 20 meses.

Ejemplo: 20 × 0,7 / 0,05 = **280 USD** de margen por cliente. Fíjate en que si el churn fuera 0 la fórmula dividiría entre cero (un
cliente "eterno"), y un churn negativo no tiene sentido: son entradas que una función debe rechazar.

### CAC y la relación LTV/CAC

**CAC** (*Customer Acquisition Cost*): cuánto cuesta conseguir un cliente (gasto en marketing y ventas / clientes nuevos). La regla
práctica: un negocio sano tiene un **LTV al menos 3 veces mayor que el CAC**, y recupera el CAC en menos de 12 meses. Si el CAC supera el
LTV, cada cliente nuevo hace perder dinero, y crecer empeora las cosas.

### Ingresos recurrentes: MRR

En productos de suscripción, el **MRR** (*Monthly Recurring Revenue*) es la suma de los ingresos mensuales de las suscripciones activas
(las anuales cuentan como su precio / 12). Lo verás en el capítulo de startup.

## 4. Errores que producen números engañosos

### Promedio de promedios

La conversión de tres países es 5 %, 10 % y 2 %. ¿La conversión global es (5 + 10 + 2) / 3 = 5,67 %? **No**, salvo que los tres tengan
el mismo número de visitas.

| País | Visitas | Compras | Conversión |
|---|---|---|---|
| A | 10 000 | 500 | 5 % |
| B | 1 000 | 100 | 10 % |
| C | 50 000 | 1 000 | 2 % |
| **Total** | **61 000** | **1 600** | **2,62 %** |

La conversión global real es 1 600 / 61 000 = **2,62 %**, no 5,67 %. El país C, con muchas más visitas, debe pesar más. La regla: **suma
los numeradores y los denominadores por separado y divide al final**. Por eso los paneles bien hechos guardan los componentes (compras y
visitas), no solo el porcentaje.

### La paradoja de Simpson

Una tendencia que aparece en cada grupo puede **invertirse** al juntar los grupos, si los grupos tienen tamaños muy distintos. Ejemplo:
una nueva versión de la web convierte mejor tanto en móvil como en escritorio, pero en total parece convertir peor, porque atrajo
muchos más usuarios de móvil, que convierten menos. Mira siempre los **segmentos** antes de concluir.

### Otros

- **Denominador equivocado**: "tasa de cancelación" sobre todos los pedidos o solo sobre los de los últimos 30 días; elegir uno y
  escribirlo en la definición.
- **Comparar periodos distintos**: un mes de 28 días con uno de 31; una semana con festivo con una normal. Compara con el mismo periodo
  del año anterior o normaliza por día.
- **Datos incompletos**: el día de hoy siempre parece malo porque aún no ha terminado; los pedidos de ayer pueden cambiar de estado.
- **Correlación no es causalidad**: que los usuarios que usan el chat compren más no significa que el chat cause las compras (quizá solo
  los más interesados lo usan). Para medir causas, un experimento: *Pruebas de hipótesis y A/B testing*.

## 5. Diseñar un dashboard que se use

Un mal dashboard tiene 25 gráficos, 10 filtros y nadie sabe qué mirar. Uno bueno responde a **unas pocas preguntas de una persona
concreta**.

### Antes de diseñar

1. **¿Para quién?** El dueño de la tienda, el equipo de soporte, el responsable de marketing. Cada uno necesita cosas distintas.
2. **¿Qué decisiones apoya?** "Dónde invertir en publicidad", "si hay que contratar más soporte".
3. **¿Cada cuánto lo mira?** Diario (operativo) o mensual (estratégico).

### Estructura

```
┌──────────────────────────────────────────────────────┐
│  KPI 1        KPI 2        KPI 3        KPI 4        │  ← 3-5 KPIs con la comparación
│  12 450 USD   2,6 %        815 USD      12,5 %       │    con el periodo anterior
│  ▲ 8 % vs     ▼ 0,3 pp     ▲ 2 %        ▼ 4 pp       │
│  mes anterior                                        │
├──────────────────────────────────────────────────────┤
│  Tendencia: ingresos por semana (línea)              │  ← cómo evoluciona
├──────────────────────────┬───────────────────────────┤
│  Por canal (barras)      │  Por país (barras)        │  ← dónde está la diferencia
└──────────────────────────┴───────────────────────────┘
   Filtros: periodo · canal · país   (máximo 3)
```

Principios:

- **Lo más importante, arriba a la izquierda**: ahí se mira primero.
- **Cada número con contexto**: un número solo ("12 450") no dice nada. Compáralo con el periodo anterior, con un objetivo o con el
  mismo periodo del año pasado.
- **El gráfico adecuado**: líneas para tendencias en el tiempo, barras para comparar categorías (ordenadas de mayor a menor), una tabla
  cuando hacen falta los valores exactos. Evita los gráficos circulares con más de 3-4 partes y los efectos 3D.
- **Pocos filtros** (máximo 3) y con valores por defecto razonables.
- **Definiciones accesibles**: un texto o un icono de información con la definición de cada KPI.
- **Diferencias porcentuales vs puntos porcentuales**: de 2,9 % a 2,6 % es una caída de 0,3 **puntos porcentuales** (pp), que es un 10 %
  relativo. Especifica cuál muestras.

### Herramientas

**Metabase** (código abierto, se conecta a PostgreSQL en minutos y es ideal para clientes pequeños), **Looker Studio** (gratuito, de
Google), **Power BI** (muy pedido en ofertas de analista). Para un panel dentro de tu propia aplicación: React con una librería de
gráficos como Recharts (la que usa esta plataforma).

La prueba final: enséñaselo a alguien que no lo ha visto. Si en un minuto no sabe decirte si el negocio va bien o mal, simplifica.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| KPI vs vanidad | ¿Si cambia, qué haría distinto? Tasas, acotadas en el tiempo, segmentables |
| Definición | Escrita: cálculo, qué incluye, periodo, fuente |
| Conversión | Completaron / empezaron; embudo por pasos y segmentos |
| Ticket promedio | Primero el total de cada pedido, después el promedio |
| Retención | Del primer periodo, cuántos vuelven: intersección / primer periodo |
| LTV | ARPU × margen / churn; churn debe ser positivo |
| LTV/CAC | Al menos 3 |
| Promedio de promedios | Sumar numeradores y denominadores y dividir al final |
| Dashboard | Para quién y qué decisión; 3-5 KPIs con contexto; tendencia y desglose; ≤ 3 filtros |

## Autoevaluación final

1. ¿Por qué "descargas totales" es una métrica de vanidad? Propón una alternativa accionable.
2. ¿Qué debe incluir la definición escrita de un KPI?
3. ¿Por qué `AVG(quantity * unit_price)` sobre las líneas no es el ticket promedio?
4. En enero compraron {1, 2, 3, 4, 5} y en febrero {2, 5, 6}. ¿Cuál es la retención de enero a febrero?
5. ARPU 30 USD/mes, margen 60 %, churn mensual 4 %. ¿Cuál es el LTV aproximado?
6. Dos tiendas convierten 4 % (10 000 visitas) y 8 % (1 000 visitas). ¿Cuál es la conversión conjunta?
7. ¿Qué diferencia hay entre una caída de 1 punto porcentual y una caída del 1 %?
8. ¿Cuál es la primera pregunta antes de diseñar un dashboard?

**Respuestas:** 1) Solo sube, no dice si el producto funciona ni qué hacer; por ejemplo, el % de usuarios nuevos que completan una acción
clave en 7 días. 2) Nombre, cálculo exacto, qué incluye y excluye, periodo y zona horaria, fuente y responsable. 3) Porque promedia
líneas, no pedidos; hay que sumar primero cada pedido y luego promediar esos totales. 4) 2 de 5 (los clientes 2 y 5): 0,4. El 6 es nuevo
y no cuenta. 5) 30 × 0,6 / 0,04 = 450 USD. 6) (400 + 80) / 11 000 = 4,36 %, no el 6 % del promedio simple. 7) De 10 % a 9 % es una caída
de 1 punto porcentual, que es un 10 % relativo; una caída del 1 % relativo sería de 10 % a 9,9 %. 8) ¿Para quién es y qué decisiones
debe ayudarle a tomar?
