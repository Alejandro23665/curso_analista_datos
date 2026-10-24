from ._helpers import checklist, py, quiz, sql
from .fase_bi_herramientas import TOPICS as _HERRAMIENTAS

TOPICS = [
    {
        "slug": "bi-metricas",
        "phase": "bi",
        "title": "Métricas, KPIs y dashboards",
        "summary": "Definir bien una métrica, calcular KPIs típicos (conversión, retención, ticket, LTV) y diseñar un dashboard útil.",
        "hours": 10,
        "theory": r"""
# Métricas, KPIs y dashboards

Un analista de datos aporta valor cuando convierte datos en **decisiones**. Eso empieza por medir lo correcto.

## 1. Qué es una buena métrica

- **Definida sin ambigüedad:** "cliente activo = compró al menos una vez en los últimos 30 días". Si dos personas calculan números distintos, la métrica no sirve.
- **Accionable:** si sube o baja, sabes qué hacer. Las **métricas de vanidad** (descargas totales, visitas) impresionan pero no guían decisiones.
- **Comparable en el tiempo y entre grupos** (misma definición, mismos filtros).
- **Con granularidad explícita:** por pedido, por cliente, por día...

## 2. KPIs que verás en casi todos los negocios

| KPI | Cálculo |
|---|---|
| **Tasa de conversión** | usuarios que completan la acción / usuarios que llegaron |
| **Ticket promedio (AOV)** | ingresos / número de pedidos |
| **Retención** | clientes de un periodo que siguen activos en el siguiente / clientes del periodo inicial |
| **Churn (abandono)** | 1 − retención |
| **ARPU** | ingresos / usuarios activos |
| **LTV simple** | ARPU × margen / churn |
| **CAC** | gasto de adquisición / clientes nuevos |

Una regla frecuente de negocios con suscripción: **LTV / CAC ≥ 3**.

## 3. Diseño de un dashboard que se usa

1. **Empieza por la audiencia y las decisiones**: ¿quién lo mira y qué decide con él?
2. **Arriba, lo importante:** 3-5 KPIs con su comparación (vs. mes anterior o vs. meta).
3. **En medio, el porqué:** tendencia en el tiempo y desglose por segmentos.
4. **Abajo, el detalle:** tablas para explorar.
5. **Filtros mínimos** (fecha, región, canal). Cada filtro extra es una forma de equivocarse.
6. Un dashboard que nadie abre es un fracaso aunque esté bonito: **pregunta qué decisión cambió**.

## 4. Herramientas

Power BI, Tableau, Looker Studio, Metabase, Superset. Los conceptos son los mismos: **modelo de datos limpio →
medidas bien definidas → visuales simples**. Empieza con una gratuita (Metabase o Looker Studio) conectada a tu PostgreSQL.

## 5. Trampas

- **Promedios de promedios:** calcula siempre desde los datos base, no promediando ratios ya calculados.
- **Comparar periodos incompletos** (mes en curso vs. mes completo).
- **Denominadores que cambian** sin avisar.
- **Mezclar métricas de distinta granularidad** en el mismo gráfico.

## Cómo sabes que dominas este tema

- Escribes la definición exacta de cada KPI de tu proyecto.
- Calculas conversión, retención y ticket con SQL y con pandas.
- Puedes explicar a quién sirve cada gráfico de tu dashboard.
""",
        "exercises": [
            sql("bi-sql-1", "Tasa de pedidos completados por canal", "BI: cálculo de KPIs",
                "Para cada `channel` muestra `pedidos` (total), `completados` (con estado `completado`) y `tasa` = porcentaje de completados "
                "redondeado a 1 decimal. Ordena por channel.",
                "SELECT channel, COUNT(*) AS pedidos, SUM(CASE WHEN status = 'completado' THEN 1 ELSE 0 END) AS completados, "
                "ROUND(100.0 * SUM(CASE WHEN status = 'completado' THEN 1 ELSE 0 END) / COUNT(*), 1) AS tasa "
                "FROM orders GROUP BY channel ORDER BY channel",
                starter="SELECT channel,\n       COUNT(*) AS pedidos,\nFROM orders\n", ordered=True,
                hint="SUM(CASE WHEN status = 'completado' THEN 1 ELSE 0 END)"),
            sql("bi-sql-2", "Ticket promedio por segmento", "BI: cálculo de KPIs",
                "Calcula el **ticket promedio** por segmento de cliente, solo con pedidos completados. Primero obtén el total de cada pedido "
                "(`SUM(quantity * unit_price)`), luego agrupa por `segment`. Devuelve `segment`, `pedidos` y `ticket_promedio` (2 decimales). Ordena por segment.",
                """WITH totales AS (
  SELECT o.id, o.customer_id, SUM(oi.quantity * oi.unit_price) AS total
  FROM orders o JOIN order_items oi ON oi.order_id = o.id
  WHERE o.status = 'completado'
  GROUP BY o.id, o.customer_id
)
SELECT c.segment, COUNT(*) AS pedidos, ROUND(AVG(t.total), 2) AS ticket_promedio
FROM totales t JOIN customers c ON c.id = t.customer_id
GROUP BY c.segment
ORDER BY c.segment""",
                starter="WITH totales AS (\n  -- total por pedido completado\n)\nSELECT c.segment\nFROM totales t\n", ordered=True,
                hint="Promediar el total por PEDIDO, no por línea de pedido."),
            py("bi-py-retencion", "Retención entre dos meses", "BI: cálculo de KPIs",
               "Escribe `retencion(clientes_mes1, clientes_mes2)` que reciba dos colecciones de ids de cliente y devuelva la **retención**: "
               "la fracción de clientes del mes 1 que también aparecen en el mes 2. Si el mes 1 está vacío, devuelve `0.0`.",
               starter="""
def retencion(clientes_mes1, clientes_mes2):
    # tu código aquí
    pass
""",
               solution="""
def retencion(clientes_mes1, clientes_mes2):
    base = set(clientes_mes1)
    if not base:
        return 0.0
    return len(base & set(clientes_mes2)) / len(base)
""",
               tests="""
assert retencion([1, 2, 3, 4], [2, 4, 9]) == 0.5, "Se quedan 2 de 4 clientes -> 0.5"
assert retencion([1, 1, 2], [1]) == 0.5, "Los clientes repetidos cuentan una sola vez (1 de 2)"
assert retencion([], [1, 2]) == 0.0, "Sin clientes en el mes 1 la retencion es 0.0"
"""),
            py("bi-py-ltv", "LTV simple", "BI: cálculo de KPIs",
               "Escribe `ltv_simple(arpu, margen, churn)` que devuelva `arpu * margen / churn`. "
               "Si `churn` es 0 o negativo, lanza `ValueError`.",
               starter="""
def ltv_simple(arpu, margen, churn):
    # tu código aquí
    pass
""",
               solution="""
def ltv_simple(arpu, margen, churn):
    if churn <= 0:
        raise ValueError("El churn debe ser mayor que 0")
    return arpu * margen / churn
""",
               tests="""
assert abs(ltv_simple(20, 0.5, 0.05) - 200.0) < 1e-9, "20 * 0.5 / 0.05 = 200"
try:
    ltv_simple(10, 0.4, 0)
except ValueError:
    pass
else:
    raise AssertionError("Con churn = 0 debe lanzar ValueError")
"""),
            quiz("bi-quiz-vanidad", "Métrica de vanidad", "BI: definición de métricas",
                 "¿Cuál de estas es la métrica **más accionable** para un equipo de producto?",
                 ["Descargas totales históricas de la app", "Porcentaje de usuarios nuevos que completan su primera compra en 7 días",
                  "Número de páginas vistas del sitio", "Seguidores en redes sociales"], 1,
                 "Es específica, está acotada en el tiempo y, si baja, el equipo sabe dónde investigar (onboarding, precios, confianza...)."),
            quiz("bi-quiz-promedios", "Promedio de promedios", "BI: definición de métricas",
                 "Tienes la conversión de cada país (0,05, 0,10 y 0,02). ¿Es correcto promediar esas tres cifras para obtener la conversión global?",
                 ["Sí, siempre", "No: hay que sumar conversiones y visitas y dividir, porque los países tienen distinto tamaño",
                  "Sí, si usas la mediana", "Solo si son más de tres países"], 1,
                 "Un promedio de ratios ignora el peso de cada grupo. El cálculo correcto parte de los totales (conversiones totales / visitas totales)."),
            checklist("bi-check", "Diseña tu dashboard", "BI: diseño de dashboards",
                      "Aplica esta lista a un dashboard de tu proyecto (Metabase, Looker Studio o Power BI).",
                      ["Definí por escrito a quién sirve y qué decisiones apoya", "Los 3-5 KPIs principales están arriba, con comparación contra el periodo anterior",
                       "Cada KPI tiene una definición escrita", "Hay una vista de tendencia y un desglose por segmento",
                       "Máximo 3 filtros", "Un compañero entendió el dashboard sin explicación"]),
        ],
    },
    {
        "slug": "data-storytelling",
        "phase": "bi",
        "title": "Storytelling con datos",
        "summary": "Cómo estructurar un análisis para que la audiencia entienda, confíe y actúe.",
        "hours": 6,
        "theory": r"""
# Storytelling con datos

Puedes hacer el mejor análisis del mundo y que **nadie lo use** porque no supiste contarlo. Esta habilidad te distingue
de otros candidatos técnicos.

## 1. Empieza por la audiencia

Antes de abrir el notebook, responde:

- ¿Quién va a leerlo? (director, equipo técnico, cliente)
- ¿Qué **decisión** tiene que tomar?
- ¿Cuánto tiempo tiene? (un correo de 3 líneas vs. una presentación de 20 minutos)

Un directivo quiere la **respuesta y la recomendación primero**. Un colega técnico quiere además el método.

## 2. Estructura de pirámide (principio de Minto)

1. **Conclusión / recomendación** en la primera frase.
2. **2-3 argumentos** que la sostienen, cada uno con un dato o gráfico.
3. **Detalle y método** en un anexo.

Ejemplo de resumen ejecutivo:

> *Recomendamos reforzar el canal app: tiene la menor tasa de cancelación (8 % vs. 15 % en web) y el ticket promedio
> más alto. Con el mismo presupuesto, desplazar 20 % de la inversión de web a app añadiría ≈ 12 000 USD/mes.
> Limitación: los datos cubren solo 6 meses.*

## 3. Del hallazgo al mensaje: la pregunta "¿y qué?"

Para cada gráfico pregúntate "¿y qué?" hasta llegar a una **acción**.
"Las ventas del martes son bajas" → ¿y qué? → "Una promoción los martes podría equilibrar la demanda."

## 4. Honestidad con la incertidumbre

- Indica el **periodo y el tamaño de muestra**.
- Distingue **correlación** de **causalidad** ("se asocia con", no "causa").
- Menciona **limitaciones** y qué harías con más datos. Genera confianza, no la resta.

## 5. Estructura narrativa

**Contexto** (qué pasaba) → **Tensión** (el problema o la pregunta) → **Resolución** (lo que encontraste) → **Siguiente paso**.

## 6. Consejos de presentación

- Una idea por diapositiva y un título que sea la conclusión.
- Resalta lo importante con color; atenúa el resto.
- Practica la versión de 30 segundos ("elevator pitch") de cada proyecto: la usarás en entrevistas.

## Cómo sabes que dominas este tema

- Tus informes empiezan por la conclusión.
- Cada gráfico tiene un mensaje y una acción asociada.
- Tienes una versión de 30 segundos de cada proyecto de tu portafolio.
""",
        "exercises": [
            quiz("story-quiz-orden", "Por dónde empezar un informe ejecutivo", "Storytelling con datos",
                 "Vas a presentar un análisis a la directora comercial. ¿Cómo empiezas?",
                 ["Explicando cómo limpiaste los datos paso a paso", "Con la recomendación principal y el impacto esperado",
                  "Mostrando todos los gráficos exploratorios", "Con la lista de librerías usadas"], 1,
                 "Los directivos deciden con la conclusión y la acción propuesta. El método va después o en un anexo."),
            quiz("story-quiz-causa", "Correlación y causalidad", "Storytelling con datos",
                 "Los clientes que usan la función X compran más. ¿Qué redacción es más honesta?",
                 ["La función X hace que los clientes compren más", "Usar la función X se asocia con mayores compras; falta probar si es causal",
                  "Hay que eliminar la función X", "Los datos no sirven"], 1,
                 "Los clientes más comprometidos pueden usar más funciones y comprar más, sin que una cause la otra. Un experimento A/B ayudaría a probar causalidad."),
            checklist("story-check", "Tu resumen ejecutivo", "Storytelling con datos",
                      "Escribe un resumen ejecutivo de 5 líneas para tu Proyecto 1 y comprueba esta lista.",
                      ["Empieza con la conclusión o recomendación", "Incluye al menos un número concreto de impacto",
                       "Menciona una limitación del análisis", "Propone un siguiente paso claro",
                       "Lo puedo contar en 30 segundos sin mirar notas"]),
        ],
    },
]

# Orden final de la fase: conceptos -> herramientas -> comunicación -> proyecto
_POR_SLUG = {t["slug"]: t for t in TOPICS + _HERRAMIENTAS}
TOPICS = [_POR_SLUG[s] for s in ("bi-metricas", "bi-excel", "bi-powerbi", "data-storytelling", "proyecto-dashboard")]
