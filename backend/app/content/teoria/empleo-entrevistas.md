# Entrevistas técnicas y casos de negocio

Una entrevista técnica no es un examen de memoria: es una simulación de cómo trabajarías. El entrevistador quiere ver **cómo piensas**
ante un problema que no conoces, cómo te comunicas y si eres alguien con quien le gustaría trabajar. Por eso dos candidatos con el mismo
nivel técnico obtienen resultados muy distintos según cómo lo cuentan.

Este capítulo cubre los cuatro tipos de preguntas que encontrarás: **SQL**, **Python**, **casos de negocio** y **preguntas de
comportamiento** (con el método STAR). Para cada uno verás los patrones que se repiten y cómo responder.

---

## 1. Antes de la entrevista

- **Investiga la empresa**: qué hace, quiénes son sus clientes, qué producto usarías tú. Prepara una o dos preguntas sobre su trabajo.
- **Relee la oferta** y prepara un ejemplo de tus proyectos para cada requisito importante.
- **Prepara tu presentación de 60 segundos**: quién eres, qué construyes y qué buscas. Termínala con algo concreto ("mi último proyecto es
  un asistente con RAG que...").
- **Prueba la técnica** si es en línea: cámara, micrófono, conexión, la herramienta de código compartido. Ten agua y papel.
- **Prepara tus historias STAR** (sección 6) por escrito y practícalas en voz alta.

---

## 2. Cómo comportarte durante una prueba técnica

Las mismas reglas valen para SQL, Python o cualquier problema:

1. **Aclara antes de escribir.** Repite el problema con tus palabras y pregunta lo ambiguo: ¿qué hago con los empates? ¿cuentan los pedidos
   cancelados? ¿y los valores nulos? Muchas preguntas de entrevista **están diseñadas** para tener una ambigüedad, y preguntar por ella es
   parte de la respuesta correcta.
2. **Piensa en voz alta.** El silencio no deja ver tu razonamiento; si te equivocas de camino pero se ve cómo piensas, el entrevistador
   puede ayudarte.
3. **Empieza simple y mejora.** Una solución correcta y sencilla primero; luego, optimizar.
4. **Comprueba tu resultado** con un ejemplo pequeño y con los casos borde.
5. **Si no sabes algo, dilo** y explica cómo lo averiguarías. Inventar se nota y resta mucho más.

---

## 3. Preguntas de SQL: los patrones que se repiten

Las preguntas de SQL de entrevista se repiten muchísimo. Si dominas estos cinco patrones, resolverás la mayoría. Los ejemplos usan las
tablas del sandbox de la plataforma.

### Patrón 1: el N-ésimo (o los N primeros) de cada grupo

"El segundo salario más alto", "los 3 productos más vendidos de cada categoría", "el último pedido de cada cliente". La herramienta es
una **función de ventana** con `PARTITION BY` (el grupo) y `ORDER BY` (el criterio), en una CTE, y un filtro fuera:

```sql
-- Los dos precios más altos de cada categoría
WITH ranking AS (
    SELECT category, name, price,
           DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC) AS puesto
    FROM products
)
SELECT category, name, price, puesto
FROM ranking
WHERE puesto <= 2
ORDER BY category, puesto, name;
```

| category | name | price | puesto |
|---|---|---|---|
| Deportes | Bicicleta urbana | 420 | 1 |
| Deportes | Zapatillas running | 110 | 2 |
| Hogar | Silla ergonomica | 249 | 1 |
| Hogar | Aspiradora | 159 | 2 |
| Libros | Atlas del mundo | 48 | 1 |
| Libros | Guia de Python | 44 | 2 |
| Tecnologia | Laptop 14 | 899 | 1 |
| Tecnologia | Monitor 24 | 189 | 2 |

¿Por qué una CTE? Porque **no se puede filtrar por una función de ventana en el `WHERE`** de la misma consulta: las ventanas se calculan
después del `WHERE`.

**La pregunta clave: ¿qué pasa con los empates?** Imagina salarios 5000, 5000, 4000:

| salario | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
|---|---|---|---|
| 5000 | 1 | 1 | 1 |
| 5000 | 2 | 1 | 1 |
| 4000 | 3 | 3 | 2 |

- Si preguntan por "el segundo **salario** más alto" (el segundo **valor** distinto), es 4000: `DENSE_RANK = 2`.
- Con `ROW_NUMBER`, el puesto 2 sería uno de los empatados a 5000, elegido arbitrariamente.
- Con `RANK`, no existe el puesto 2.

Para "**uno** por grupo" con un criterio de desempate, usa `ROW_NUMBER` y añade el desempate al `ORDER BY` de la ventana:

```sql
-- El producto más caro de cada categoría; si hay empate de precio, el de menor nombre
WITH r AS (
    SELECT category, name, price,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC, name) AS rn
    FROM products
)
SELECT category, name, price FROM r WHERE rn = 1 ORDER BY category;
```

Cuando el criterio es una **métrica agregada** (unidades vendidas, ingresos), primero agregas en una CTE (con `GROUP BY` y los `JOIN`
necesarios) y después aplicas la ventana sobre ese resultado. Son dos pasos encadenados.

Y "al menos dos valores distintos en el grupo" se puede comprobar con `COUNT(DISTINCT columna)` agrupando por el grupo, o simplemente
observando que, si un grupo solo tiene un valor, ninguna fila tendrá `DENSE_RANK = 2`.

### Patrón 2: porcentaje de un subgrupo

"¿Qué porcentaje de clientes...?", "tasa de cancelación por canal". La técnica: `CASE WHEN` dentro de `SUM` (o `AVG`) para contar los que
cumplen, dividido entre el total, con `100.0` para forzar decimales.

```sql
-- Tasa de cancelación por canal
SELECT channel,
       COUNT(*) AS pedidos,
       ROUND(100.0 * SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_cancelados
FROM orders
GROUP BY channel
ORDER BY channel;
```

| channel | pedidos | pct_cancelados |
|---|---|---|
| app | 68 | 30.9 |
| tienda | 69 | 13.0 |
| web | 83 | 21.7 |

Cuando la pregunta es sobre **clientes** (no sobre pedidos), necesitas dos niveles: primero una fila por cliente con su dato, y después
el porcentaje sobre esas filas.

```sql
-- ¿Qué porcentaje de los clientes con pedidos ha cancelado al menos uno?
WITH por_cliente AS (
    SELECT customer_id,
           SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) AS cancelados
    FROM orders
    GROUP BY customer_id
)
SELECT ROUND(100.0 * SUM(CASE WHEN cancelados >= 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_con_cancelacion
FROM por_cliente;
-- 79.4  (27 de 34 clientes)
```

Las trampas de este patrón: la **división entera** (`27 / 34` da 0 en PostgreSQL si ambos son enteros: por eso el `100.0`), y definir
bien el **denominador**. ¿Todos los clientes o solo los que tienen pedidos? ¿Todos los pedidos o solo los completados? Pregúntalo y
filtra en el lugar correcto (un `WHERE` antes de agrupar cambia tanto el numerador como el denominador).

### Patrón 3: cumple A y también B

"Clientes que compraron por la web y también en tienda", "usuarios activos en enero y en febrero". Un error típico es escribir
`WHERE channel = 'web' AND channel = 'tienda'`: ninguna fila puede tener dos valores a la vez, así que no devuelve nada. Las condiciones
están en **filas distintas** del mismo cliente. Tres formas correctas:

```sql
-- A) Agrupar y comprobar cada condición con CASE en el HAVING
SELECT c.id, c.name
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name
HAVING SUM(CASE WHEN o.channel = 'web' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN o.channel = 'tienda' THEN 1 ELSE 0 END) > 0
ORDER BY c.id;

-- B) Intersección de conjuntos
SELECT customer_id FROM orders WHERE channel = 'web'
INTERSECT
SELECT customer_id FROM orders WHERE channel = 'tienda';

-- C) EXISTS (útil cuando quieres las columnas de customers sin agrupar)
SELECT c.id, c.name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.channel = 'web')
  AND EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.channel = 'tienda')
ORDER BY c.id;
```

Las tres devuelven los mismos 26 clientes. La condición puede ser cualquier cosa: un canal, un año (extrayéndolo de la fecha, como viste
en el capítulo de agregaciones), un estado.

### Patrón 4: lo que no tiene pareja

"Clientes sin pedidos", "productos que nunca se vendieron". `LEFT JOIN` + `WHERE ... IS NULL`, o `NOT EXISTS`. Cuidado con `NOT IN` si la
subconsulta puede devolver `NULL`: entonces no devuelve ninguna fila.

### Patrón 5: comparar con la fila anterior o con el total

"Crecimiento respecto al mes anterior" (`LAG`), "acumulado" (`SUM(...) OVER (ORDER BY ...)`), "porcentaje del total"
(`valor / SUM(valor) OVER ()`). Lo viste en el capítulo de funciones de ventana.

### Al terminar una consulta, comprueba

- ¿El número de filas tiene sentido? (¿Un `JOIN` duplicó filas?)
- ¿Los empates y los nulos se tratan como pide el enunciado?
- ¿El orden es el pedido?
- ¿Cuadra con un caso que puedas calcular a mano?

---

## 4. Preguntas de Python

Las preguntas de Python para puestos junior suelen ser problemas pequeños de estructuras de datos (pares que suman un objetivo, el primer
elemento que cumple algo, frecuencias, paréntesis balanceados). Los patrones (diccionario de lo visto, contar y luego recorrer, pila,
ventana, búsqueda binaria) están explicados a fondo en *Algoritmos y estructuras de datos para entrevistas*.

Además, para puestos de datos y backend es frecuente:

- **Manipular datos**: agrupar una lista de diccionarios, limpiar textos, leer un CSV o un JSON.
- **Preguntas conceptuales**: diferencia entre lista y tupla (mutable o no), entre lista y conjunto (orden y duplicados vs pertenencia en
  O(1)), qué es una excepción y cómo se maneja, qué es un generador, qué hace `with`.
- **Leer código**: "¿qué imprime esto?" o "¿qué error tiene?". Lee línea a línea siguiendo las variables, como en el capítulo de leer y
  depurar código.
- **Escribir pruebas**: "¿cómo probarías esta función?" Casos normales, casos borde (vacío, un elemento, nulos, duplicados) y casos de
  error.

---

## 5. Casos de negocio

En puestos de datos, producto y cada vez más en IA aplicada te harán preguntas abiertas: "las ventas bajaron un 10 %, ¿qué haces?",
"¿cómo medirías si el nuevo chatbot funciona?". No hay una respuesta única: evalúan tu **estructura de pensamiento**.

### La estructura para cualquier caso

1. **Aclarar**: ¿qué métrica exactamente? ¿comparado con qué periodo? ¿en todos los mercados?
2. **Verificar los datos**: antes de buscar causas de negocio, comprueba que no sea un error de datos (un día sin cargar, un cambio en
   cómo se registra, un filtro distinto). Pasa muchísimo más de lo que parece.
3. **Descomponer la métrica** en sus factores.
4. **Segmentar**: ¿en qué segmento está la caída? (canal, país, tipo de cliente, producto, dispositivo, nuevos vs recurrentes).
5. **Hipótesis y cómo comprobarlas**, internas (un cambio en la web, un precio, un error) y externas (estacionalidad, competencia, un
   festivo).
6. **Recomendación** con el siguiente paso concreto.

### Descomponer una métrica

```
Ventas = visitas × tasa de conversión × ticket medio
```

Si las ventas cayeron un 10 %, ¿qué factor cambió?

| Factor | Mes anterior | Este mes | Cambio |
|---|---|---|---|
| Visitas | 50 000 | 49 500 | −1 % |
| Conversión | 2,0 % | 1,8 % | −10 % |
| Ticket medio | 40 | 40,4 | +1 % |

La caída está en la **conversión**: la gente sigue llegando, pero compra menos. Ahora segmentas la conversión: si la caída es solo en
móvil y empezó el día que se publicó una nueva versión de la web, tienes una hipótesis muy fuerte (un error en el proceso de pago en
móvil). Comprobarla es rápido; lanzar una promoción habría sido inútil.

Otras descomposiciones útiles:

- **Ingresos** = clientes × pedidos por cliente × ticket medio.
- **Clientes activos** = clientes que se mantienen + nuevos − los que se van.
- **Costo de un chatbot** = conversaciones × mensajes por conversación × tokens por mensaje × precio por token.

### "¿Cómo medirías si el nuevo chatbot funciona?"

Una buena respuesta define métricas a varios niveles:

- **Objetivo de negocio**: menos tickets que llegan al equipo humano, menor tiempo de respuesta, mayor satisfacción.
- **Calidad**: porcentaje de respuestas correctas en un conjunto de evaluación; porcentaje de conversaciones resueltas sin derivar a una
  persona; valoraciones de los usuarios.
- **Salvaguardas** (*guardrails*): que no empeoren otras cosas, como las quejas, las derivaciones tardías o el costo por conversación.
- **Cómo compararlo**: idealmente, un experimento (una parte de los usuarios con chatbot y otra sin él), lo que verás en *Pruebas A/B*.

---

## 6. Preguntas de comportamiento: el método STAR

"Cuéntame de una vez que cometiste un error", "¿cómo resuelves un desacuerdo?". Estas preguntas evalúan cómo trabajas con otros, y se
responden con **historias reales**, no con opiniones ("yo siempre me comunico bien").

**STAR** es una estructura para contar esas historias de forma clara en 1-2 minutos:

| Letra | Qué cuentas | Peso |
|---|---|---|
| **S**ituación | El contexto, en una o dos frases | Breve |
| **T**area | Cuál era tu responsabilidad o el reto | Breve |
| **A**cción | Qué hiciste **tú** (en primera persona), paso a paso | **La parte principal** |
| **R**esultado | Qué pasó, con un número si puedes, y qué aprendiste | Concreto |

### Ejemplo: "Cuéntame de un error que cometiste"

> **S:** En el proyecto final de la carrera, desarrollábamos una aplicación web en un equipo de cuatro personas.
> **T:** Yo era responsable de la base de datos y de la API.
> **A:** Hice un cambio en el modelo de datos sin avisar al equipo, y la parte del frontend dejó de funcionar dos días antes de una
> entrega. Lo detecté cuando un compañero me escribió. Primero revertí mi cambio para que todos pudieran seguir trabajando; después
> propuse que cualquier cambio en la API se anunciara en el grupo con un ejemplo de la respuesta nueva, y escribí pruebas para los
> endpoints principales.
> **R:** Entregamos a tiempo y no volvimos a tener ese problema. Aprendí que un cambio en un contrato compartido no es solo mío, y desde
> entonces escribo pruebas antes de modificar una API.

Fíjate en lo que hace buena la historia: un error **real** (no un falso defecto como "soy demasiado perfeccionista"), una acción
concreta de **tú** (no "el equipo"), un resultado y un **aprendizaje** que se nota en tu forma de trabajar hoy.

### Las historias que conviene tener preparadas

1. Un **error** y lo que aprendiste.
2. Un **desacuerdo** y cómo lo resolviste.
3. Algo que **aprendiste rápido** por necesidad.
4. Un **proyecto del que estás orgulloso**, con un resultado medible.
5. Trabajo **bajo presión** o con un plazo ajustado.

Con 5-6 historias bien preparadas puedes responder casi cualquier pregunta de comportamiento, adaptándolas. Sin experiencia laboral, usa
proyectos de la universidad, freelance, proyectos personales o voluntariado: valen igual si son reales.

### Preguntas frecuentes y qué buscan

| Pregunta | Qué evalúan |
|---|---|
| "Háblame de ti" | Claridad y foco: 60 segundos sobre tu perfil y lo que buscas, no tu biografía |
| "¿Por qué esta empresa?" | Que investigaste; conecta su producto con lo que te interesa |
| "¿Cuál es tu mayor debilidad?" | Autoconocimiento: una debilidad real y lo que haces para mejorarla |
| "¿Dónde te ves en 3 años?" | Ambición y encaje; habla de crecer en habilidades, no de irte |
| "¿Tienes preguntas para nosotros?" | Interés: siempre ten 2-3 (sobre el equipo, el producto, cómo es el primer mes) |

---

## 7. Después de la entrevista

- Envía un **mensaje breve de agradecimiento** el mismo día, mencionando algo concreto de la conversación.
- **Anota** las preguntas que te hicieron y lo que respondiste mal: es tu material de estudio para la siguiente.
- Si te descartan, **pide comentarios** con educación. No siempre responden, pero cuando lo hacen es oro.
- Cada entrevista, aunque no salga, es práctica. La segunda siempre sale mejor que la primera, y la décima mucho mejor.

---

## Resumen del capítulo

| Tema | Lo esencial |
|---|---|
| Actitud | Aclarar, pensar en voz alta, empezar simple, comprobar, admitir lo que no sabes |
| N-ésimo por grupo | Ventana con `PARTITION BY` en una CTE; `DENSE_RANK` para valores distintos; `ROW_NUMBER` + desempate para uno |
| Porcentajes | `SUM(CASE ...)` / `COUNT(*)` con `100.0`; dos niveles si es por cliente; cuidado con el denominador |
| A y también B | `HAVING` con dos `CASE`, `INTERSECT` o dos `EXISTS`; nunca `col = A AND col = B` |
| Casos de negocio | Aclarar, verificar datos, descomponer, segmentar, hipótesis, recomendación |
| Descomposición | Ventas = visitas × conversión × ticket |
| STAR | Situación, Tarea, **Acción**, Resultado; historias reales en primera persona |

## Autoevaluación final

1. Los salarios de un departamento son 7000, 7000, 6000 y 5000. ¿Qué valor tiene el "segundo salario más alto"? ¿Qué función de ventana
   lo encuentra con `= 2`?
2. ¿Por qué no se puede escribir `WHERE DENSE_RANK() OVER (...) = 2`?
3. ¿Por qué `WHERE channel = 'web' AND channel = 'app'` no devuelve nada? Escribe la idea de una alternativa.
4. En un porcentaje, ¿qué problema evita multiplicar por `100.0` en lugar de `100`?
5. Las ventas cayeron un 10 %. ¿Cuáles son tus dos primeros pasos?
6. Visitas estables, ticket estable, ventas abajo. ¿Qué factor cambió y qué harías a continuación?
7. ¿Qué parte de una historia STAR debe ocupar más tiempo y por qué?
8. ¿Por qué "soy demasiado perfeccionista" es una mala respuesta a "¿cuál es tu mayor debilidad?"?

**Respuestas:** 1) 6000; `DENSE_RANK`. 2) Porque las funciones de ventana se calculan después del `WHERE`; se calcula en una CTE o
subconsulta y se filtra fuera. 3) Porque una fila no puede tener dos valores en la misma columna; las condiciones están en filas distintas
del mismo cliente: agrupar por cliente y comprobar cada una con `SUM(CASE ...) > 0` en el `HAVING` (o `INTERSECT`, o dos `EXISTS`).
4) La división entera, que daría 0 o un número truncado. 5) Aclarar la métrica y el periodo, y verificar que los datos son correctos.
6) La conversión; segmentarla (dispositivo, canal, tipo de cliente) y buscar qué cambió cuando empezó la caída. 7) La Acción: es lo que
demuestra cómo trabajas tú. 8) Porque no es una debilidad real y suena preparada; muestra poco autoconocimiento.
