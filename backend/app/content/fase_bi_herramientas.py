from ._helpers import checklist, quiz

DESCARGAS = r"""
## Datos para practicar

Descarga los datos de la tienda de práctica (los mismos de los ejercicios SQL):

- [ventas.csv](/api/sandbox/csv/ventas): **una fila por línea de pedido** con fecha, estado, canal, cliente, país, segmento, producto, categoría, cantidad, precio e importe. Ideal para empezar.
- Tablas separadas para modelar: [orders.csv](/api/sandbox/csv/orders), [order_items.csv](/api/sandbox/csv/order_items),
  [customers.csv](/api/sandbox/csv/customers), [products.csv](/api/sandbox/csv/products) y [employees.csv](/api/sandbox/csv/employees).

Los archivos usan **coma** como separador y **punto** como decimal. Si tu Excel está en español, no los abras con doble clic (verías todo en una columna o decimales mal leídos):
impórtalos desde **Datos → Obtener datos → Desde archivo → Desde texto/CSV**, elige el delimitador *Coma* y, en *Transformar datos*, define la configuración regional *Inglés (Estados Unidos)*
para las columnas numéricas.
"""

TOPICS = [
    {
        "slug": "bi-excel",
        "phase": "bi",
        "title": "Excel para analistas",
        "summary": "Tablas, referencias, SUMAR.SI.CONJUNTO, BUSCARX, tablas dinámicas, Power Query y errores que conviene evitar.",
        "hours": 8,
        "theory": r"""
# Excel para analistas

Aunque domines SQL y Python, **Excel sigue presente en casi todos los equipos de negocio**, y muchas ofertas de analista lo piden.
Tu ventaja: piensas en datos como en SQL, así que vas a usar Excel de forma ordenada y reproducible.

> Los nombres de funciones cambian según el idioma. Aquí van en español con el inglés entre paréntesis. En Excel en español los argumentos se separan con **punto y coma** `;`.

## 1. Datos como tabla, no como "hoja"

Selecciona tus datos y pulsa **Ctrl + T** para convertirlos en una **tabla**. Ventajas: las fórmulas se extienden solas, los rangos crecen al añadir filas y
puedes referirte a columnas por nombre: `=[@cantidad]*[@precio_unitario]`.
Regla de oro: **una fila por registro, una columna por variable, sin celdas combinadas ni filas de totales en medio de los datos** (es la misma idea que una tabla SQL).

## 2. Referencias relativas y absolutas

- `A1` cambia al copiar la fórmula; `$A$1` no cambia; `A$1` y `$A1` fijan solo fila o solo columna.
- Pulsa **F4** para alternar. El error típico es arrastrar una fórmula que debía apuntar siempre a la celda de una tasa de cambio.

## 3. Funciones imprescindibles

| Necesitas | Función |
|---|---|
| Sumar con condiciones | `SUMAR.SI.CONJUNTO(suma; rango1; criterio1; ...)` (SUMIFS) |
| Contar con condiciones | `CONTAR.SI.CONJUNTO` (COUNTIFS) |
| Promedio con condiciones | `PROMEDIO.SI.CONJUNTO` (AVERAGEIFS) |
| Buscar un valor en otra tabla | `BUSCARX(valor; rango_búsqueda; rango_resultado; "no encontrado")` (XLOOKUP) |
| Condiciones | `SI`, `Y`, `O`, `SI.CONJUNTO` (IF, AND, OR, IFS) |
| Manejar errores | `SI.ERROR(fórmula; valor)` (IFERROR) |
| Texto | `ESPACIOS`, `MAYUSC`, `IZQUIERDA`, `TEXTO`, `CONCAT` (TRIM, UPPER, LEFT, TEXT, CONCAT) |
| Fechas | `AÑO`, `MES`, `FIN.MES`, `DIAS` (YEAR, MONTH, EOMONTH, DAYS) |
| Dinámicas (Excel 365) | `FILTRAR`, `UNICOS`, `ORDENAR` (FILTER, UNIQUE, SORT) |

Ejemplo, ingresos de la categoría Tecnología en pedidos completados:

```
=SUMAR.SI.CONJUNTO(Ventas[importe]; Ventas[categoria]; "Tecnologia"; Ventas[estado]; "completado")
```

`BUSCARX` reemplaza a `BUSCARV` (VLOOKUP): busca hacia la izquierda o la derecha y permite un valor "no encontrado". Es el equivalente a un `LEFT JOIN` de una columna.

## 4. Tablas dinámicas

**Insertar → Tabla dinámica**: arrastras campos a *Filas*, *Columnas*, *Valores* y *Filtros*. Es un `GROUP BY` con clics.
Trucos: en *Configuración de campo de valor* puedes mostrar "% del total de columnas"; agrupa fechas por mes o trimestre; añade **segmentaciones** (slicers) para filtrar.
Si cambian los datos, pulsa *Actualizar*.

## 5. Power Query: limpieza reproducible

**Datos → Obtener datos** abre Power Query. Cada paso de limpieza (quitar columnas, cambiar tipos, dividir texto, combinar tablas) queda **registrado**
y se repite al actualizar. Es el "ETL" de Excel y **es el mismo motor que usa Power BI**: lo que aprendas aquí lo reutilizas allí.

## 6. Buenas prácticas

- Separa en hojas: **datos** (crudos) → **cálculos** → **informe**. No escribas números a mano dentro de las fórmulas.
- Formato condicional con moderación para resaltar lo importante.
- Documenta supuestos en una hoja "Notas".
- Si el archivo supera unos cientos de miles de filas o necesitas automatizar, pasa a SQL, Python o Power BI.

## Cómo sabes que dominas este tema

- Conviertes datos en tabla y usas referencias estructuradas.
- Resuelves con `SUMAR.SI.CONJUNTO` y `BUSCARX` lo que harías con `GROUP BY` y `JOIN`.
- Construyes una tabla dinámica con segmentaciones en minutos.
""" + DESCARGAS,
        "exercises": [
            quiz("xl-quiz-absoluta", "Referencias absolutas", "Excel",
                 "En B2 escribes `=A2*D1`, donde D1 tiene la tasa de cambio, y arrastras la fórmula hacia abajo. En B3 obtienes un resultado incorrecto. ¿Qué pasó?",
                 ["Excel no permite multiplicar celdas", "La referencia D1 se movió a D2; debía ser absoluta: $D$1", "Hay que usar SUMA", "A3 está vacía"], 1,
                 "Las referencias relativas se desplazan al copiar. Para fijar la celda de la tasa se usa `$D$1` (pulsa F4)."),
            quiz("xl-quiz-sumifs", "Sumar con condiciones", "Excel",
                 "¿Qué fórmula suma el importe de las ventas de Colombia por el canal web?",
                 ["=SUMA(importe)", "=SUMAR.SI.CONJUNTO(Ventas[importe]; Ventas[pais]; \"Colombia\"; Ventas[canal]; \"web\")",
                  "=CONTAR.SI.CONJUNTO(Ventas[pais]; \"Colombia\")", "=BUSCARX(\"Colombia\"; Ventas[pais]; Ventas[importe])"], 1,
                 "SUMAR.SI.CONJUNTO recibe primero el rango a sumar y luego pares rango-criterio. BUSCARX solo devolvería la primera coincidencia."),
            quiz("xl-quiz-buscarx", "BUSCARX como JOIN", "Excel",
                 "Tienes una hoja de pedidos con `cliente_id` y otra de clientes con `id` y `segmento`. Quieres traer el segmento a cada pedido. ¿Qué usas?",
                 ["Una tabla dinámica", "BUSCARX(cliente_id; Clientes[id]; Clientes[segmento]; \"sin dato\")", "SUMAR.SI", "Copiar y pegar a mano"], 1,
                 "BUSCARX busca la clave en otra tabla y devuelve la columna que pidas: equivale a un LEFT JOIN de una columna."),
            quiz("xl-quiz-pivot", "Tabla dinámica", "Excel",
                 "En una tabla dinámica quieres ver, por mes, qué porcentaje de las ventas representa cada categoría. ¿Qué haces?",
                 ["Escribir los porcentajes a mano", "Poner meses en Filas, categoría en Columnas, importe en Valores y mostrar valores como '% del total de filas'",
                  "Crear una columna nueva por cada categoría", "No se puede con tablas dinámicas"], 1,
                 "La opción 'Mostrar valores como' calcula porcentajes sobre el total de fila, columna o general sin fórmulas adicionales."),
            quiz("xl-quiz-pq", "Power Query", "Excel",
                 "Cada lunes recibes el mismo CSV con columnas sucias y repites 15 pasos de limpieza a mano. ¿Qué es lo mejor?",
                 ["Seguir haciéndolo a mano con cuidado", "Grabar los pasos en Power Query y pulsar Actualizar cada semana",
                  "Pedir que dejen de enviarlo", "Copiarlo en una hoja nueva cada vez"], 1,
                 "Power Query registra cada transformación y la repite sobre los datos nuevos: limpieza reproducible, como un pipeline."),
            checklist("xl-check", "Práctica con ventas.csv", "Excel",
                      "Descarga ventas.csv (enlace en la teoría) e impórtalo con Power Query. Marca cada paso al terminarlo.",
                      ["Importé el CSV con Power Query con tipos y decimales correctos", "Convertí los datos en una tabla con nombre (Ventas)",
                       "Calculé con SUMAR.SI.CONJUNTO los ingresos completados de una categoría y lo comprobé contra mi consulta SQL",
                       "Usé BUSCARX para traer un dato de customers.csv", "Construí una tabla dinámica de ingresos por mes y categoría con segmentación por canal",
                       "Separé datos, cálculos e informe en hojas distintas"]),
        ],
    },
    {
        "slug": "bi-powerbi",
        "phase": "bi",
        "title": "Power BI: de los datos al dashboard",
        "summary": "Power Query, modelo en estrella, relaciones, medidas DAX, CALCULATE, tabla de fechas y diseño de informes.",
        "hours": 10,
        "theory": r"""
# Power BI: de los datos al dashboard

**Power BI** es la herramienta de BI que más se pide en ofertas de analista. **Power BI Desktop** es gratuito para Windows (descárgalo desde la
Microsoft Store). Lo que ya sabes de modelado dimensional, SQL y métricas se traslada casi directamente.

## 1. El flujo de trabajo

1. **Obtener datos:** CSV, Excel, bases de datos (PostgreSQL incluido), APIs.
2. **Transformar** en **Power Query** (el mismo de Excel): tipos, limpieza, columnas nuevas.
3. **Modelar:** tablas y relaciones (vista *Modelo*).
4. **Medir:** medidas en **DAX**.
5. **Visualizar** y diseñar el informe.
6. **Compartir:** publicar en el servicio de Power BI (normalmente requiere una cuenta de trabajo o estudiante) o exportar a PDF.

## 2. Modelo en estrella: la base de todo

Power BI funciona mejor con un **modelo en estrella**: una tabla de **hechos** (`order_items` u `orders`) rodeada de **dimensiones** (`customers`, `products`, `Calendario`).

- Relaciones **uno a varios** (1:*) desde la dimensión hacia el hecho (un cliente → muchos pedidos).
- Dirección de filtro **simple**, de la dimensión al hecho. Evita relaciones bidireccionales salvo que sepas por qué las necesitas.
- Evita tablas planas gigantes con todo mezclado: funcionan para empezar, pero complican las medidas.

## 3. Columnas calculadas vs medidas

- **Columna calculada:** se calcula **por fila** y se guarda en la tabla (por ejemplo `importe = order_items[quantity] * order_items[unit_price]`). Ocupa memoria.
- **Medida:** se calcula **al vuelo** según los filtros del visual (una tarjeta, una celda de una matriz). Es lo que usarás el 90 % de las veces para KPIs.

## 4. DAX esencial

```
Ventas = SUMX(order_items, order_items[quantity] * order_items[unit_price])
Pedidos = DISTINCTCOUNT(orders[id])
Ticket promedio = DIVIDE([Ventas], [Pedidos])
Ventas completadas = CALCULATE([Ventas], orders[status] = "completado")
% cancelación = DIVIDE(CALCULATE([Pedidos], orders[status] = "cancelado"), [Pedidos])
```

- `SUMX` recorre una tabla fila a fila y suma una expresión.
- `DIVIDE` evita errores al dividir entre cero (mejor que `/`).
- **`CALCULATE`** es la función más importante: evalúa una medida **cambiando el contexto de filtro**. Si entiendes `CALCULATE`, entiendes DAX.

**Contexto de filtro:** la misma medida `[Ventas]` da un número distinto en cada celda de una matriz porque cada celda filtra por su fila y columna
(por ejemplo, categoría *Hogar* y mes *marzo*). Es como si cada celda ejecutara un `WHERE` distinto.

## 5. Tabla de fechas (calendario)

Para comparar periodos crea una tabla de fechas continua, márcala como tabla de fechas y relaciónala con la fecha del hecho:

```
Calendario = CALENDAR(DATE(2024, 1, 1), DATE(2025, 12, 31))
Ventas año anterior = CALCULATE([Ventas], SAMEPERIODLASTYEAR(Calendario[Date]))
Variación interanual = DIVIDE([Ventas] - [Ventas año anterior], [Ventas año anterior])
```

## 6. Diseño del informe

Aplica lo que viste en métricas y storytelling: KPIs en tarjetas arriba, tendencia en el centro, desglose y detalle abajo, pocos filtros
(segmentaciones) y un título que diga la conclusión. Usa **una página por pregunta de negocio**.

## Cómo sabes que dominas este tema

- Construyes un modelo en estrella con relaciones 1:* correctas.
- Escribes medidas con `SUMX`, `DIVIDE`, `DISTINCTCOUNT` y `CALCULATE`.
- Explicas qué es el contexto de filtro con un ejemplo.
""" + DESCARGAS + r"""
Para practicar el modelado, importa por separado `orders`, `order_items`, `customers` y `products` y crea las relaciones tú mismo en la vista *Modelo*.
""",
        "exercises": [
            quiz("pbi-quiz-medida", "Medida o columna calculada", "Power BI y DAX",
                 "Quieres una tarjeta con el ticket promedio que cambie al filtrar por país y por mes. ¿Qué creas?",
                 ["Una columna calculada en la tabla orders", "Una medida: Ticket promedio = DIVIDE([Ventas], [Pedidos])",
                  "Una tabla nueva por cada país", "Un cálculo en Excel que pegas en el informe"], 1,
                 "Las medidas se recalculan según el contexto de filtro de cada visual. Una columna calculada se fija fila a fila al cargar los datos."),
            quiz("pbi-quiz-calculate", "CALCULATE", "Power BI y DAX",
                 "¿Qué hace `CALCULATE([Ventas], orders[status] = \"completado\")`?",
                 ["Crea una columna con el estado", "Calcula la medida Ventas aplicando además el filtro estado = completado",
                  "Borra los pedidos no completados del modelo", "Ordena las ventas por estado"], 1,
                 "CALCULATE evalúa una expresión modificando el contexto de filtro. Es la base de casi todas las medidas avanzadas."),
            quiz("pbi-quiz-relacion", "Relaciones", "Power BI y DAX",
                 "Relacionas `customers[id]` con `orders[customer_id]`. ¿Qué cardinalidad y dirección de filtro son las adecuadas?",
                 ["Varios a varios, bidireccional", "Uno a varios, filtrando de customers hacia orders",
                  "Uno a uno", "Varios a uno, filtrando de orders hacia customers"], 1,
                 "Un cliente tiene muchos pedidos (1:*), y la dimensión filtra al hecho. Es el patrón del modelo en estrella."),
            quiz("pbi-quiz-divide", "Dividir con seguridad", "Power BI y DAX",
                 "¿Por qué se recomienda `DIVIDE([Ventas], [Pedidos])` en lugar de `[Ventas] / [Pedidos]`?",
                 ["Es más rápido escribirlo", "Devuelve vacío (o un valor alternativo) cuando el denominador es 0, en lugar de un error",
                  "Redondea automáticamente", "No hay ninguna diferencia"], 1,
                 "Con filtros que dejan 0 pedidos, `/` produce errores o infinito; DIVIDE lo maneja de forma segura."),
            quiz("pbi-quiz-fechas", "Comparar con el año anterior", "Power BI y DAX",
                 "Para calcular las ventas del mismo periodo del año anterior con SAMEPERIODLASTYEAR, ¿qué necesitas en el modelo?",
                 ["Nada especial", "Una tabla de fechas continua, marcada como tabla de fechas y relacionada con la fecha del hecho",
                  "Una columna de texto con el año", "Dos archivos separados por año"], 1,
                 "Las funciones de inteligencia de tiempo de DAX necesitan una tabla de calendario sin huecos relacionada con los hechos."),
            checklist("pbi-check", "Construye tu primer modelo", "Power BI y DAX",
                      "Con los CSV de la teoría, en Power BI Desktop:",
                      ["Importé orders, order_items, customers y products y revisé los tipos en Power Query",
                       "Creé las relaciones 1:* desde customers y products hacia los hechos", "Creé una tabla Calendario y la marqué como tabla de fechas",
                       "Escribí las medidas Ventas, Pedidos, Ticket promedio y % cancelación", "Comprobé que [Ventas] completadas coincide con mi consulta SQL",
                       "Hice una página con 4 KPIs, una tendencia mensual y un desglose por categoría"]),
        ],
    },
    {
        "slug": "proyecto-dashboard",
        "phase": "bi",
        "title": "Proyecto 3: dashboard de negocio publicado",
        "summary": "Tu pieza de portafolio de BI: un dashboard en Power BI (o Looker Studio) que responde preguntas de negocio reales.",
        "hours": 10,
        "theory": r"""
# Proyecto 3: dashboard de negocio publicado

Con este proyecto tu portafolio cubre los tres perfiles: **análisis** (Proyecto 1), **ingeniería** (Proyecto 2) y **BI** (este).
Muchos reclutadores de analista miran primero un dashboard, porque se entiende en 30 segundos.

## 1. Elige el caso

Puedes usar los datos de la tienda de práctica para empezar, pero destacarás más con **un dataset propio o público** con fechas, categorías y métricas
(ventas de un comercio, datos abiertos de transporte, salud, educación o finanzas públicas de tu país). Si haces primero el Proyecto 2, conecta el dashboard a tu PostgreSQL.

## 2. Define antes de abrir Power BI

1. **Audiencia:** ¿quién lo usa? (gerente comercial, dirección, un equipo de operaciones).
2. **3 preguntas de negocio** que debe responder.
3. **4-6 KPIs** con su definición escrita (fórmula, filtros, granularidad).

## 3. Requisitos

- **Modelo en estrella** con relaciones correctas y tabla de fechas.
- **Medidas DAX** (no columnas) para todos los KPIs, con nombres claros.
- **Página ejecutiva:** KPIs con comparación (vs. periodo anterior o meta), tendencia y un desglose.
- **Página de detalle** para explorar (por segmento, producto o región).
- Títulos que dicen la conclusión, máximo 3 filtros y una paleta sobria.
- Una nota con **definiciones de KPIs** y la fecha de actualización de los datos.

## 4. Publicación

- Si tienes cuenta de trabajo o estudiante, publícalo en el servicio de Power BI.
- Si no, exporta a **PDF** y graba un **video corto (1-2 min)** recorriendo el dashboard. También puedes rehacerlo en **Looker Studio**, que permite compartir con un enlace público.
- En GitHub: el archivo `.pbix` (si los datos son públicos), capturas, el PDF y un README con las preguntas, los KPIs, el modelo (captura de la vista *Modelo*) y las conclusiones.

## 5. Plan de trabajo (≈ 10 horas)

| Horas | Tarea |
|---|---|
| 1,5 | Caso, audiencia, preguntas y KPIs por escrito |
| 2 | Power Query y modelo |
| 2,5 | Medidas DAX y validación contra SQL |
| 2,5 | Diseño de las páginas |
| 1,5 | Publicación, README y post en LinkedIn |

## 6. Errores comunes

- Dashboards con 20 gráficos y ninguna conclusión.
- KPIs sin definición (cada persona lo interpreta distinto).
- Medidas que no se validaron contra la fuente.
- Colores por todas partes y gráficos de pastel con muchas porciones.
""",
        "exercises": [
            quiz("dash-quiz-1", "Por dónde empezar", "Proyecto: dashboard",
                 "¿Qué haces primero al empezar un dashboard?",
                 ["Elegir los colores y el logo", "Definir la audiencia, las preguntas de negocio y los KPIs por escrito",
                  "Poner todos los gráficos posibles y luego borrar", "Publicarlo vacío para reservar el enlace"], 1,
                 "Sin audiencia ni preguntas no hay criterio para elegir qué mostrar. El diseño viene después."),
            checklist("dash-entregables", "Entregables del proyecto", "Proyecto: dashboard",
                      "Marca cada punto cuando esté listo.",
                      ["Escribí la audiencia, 3 preguntas de negocio y 4-6 KPIs con su definición", "El modelo está en estrella con tabla de fechas",
                       "Todos los KPIs son medidas DAX validadas contra SQL", "Tiene una página ejecutiva y una de detalle",
                       "Cada página tiene un título-conclusión y máximo 3 filtros", "Lo publiqué (servicio de Power BI, PDF + video, o Looker Studio)",
                       "El repositorio tiene README con preguntas, KPIs, modelo y conclusiones", "Escribí un post en LinkedIn con una captura y el hallazgo principal"]),
        ],
    },
]
