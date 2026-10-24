from ._helpers import checklist, py, quiz, sql

TOPICS = [
    {
        "slug": "empleo-portafolio",
        "phase": "empleo",
        "title": "Portafolio, CV, LinkedIn y búsqueda de empleo",
        "summary": "Cómo presentar tu trabajo, dónde buscar (también remoto) y cómo destacar siendo junior.",
        "hours": 8,
        "theory": r"""
# Portafolio, CV, LinkedIn y búsqueda de empleo

Con menos ofertas junior, **cómo te presentas pesa tanto como lo que sabes**. La idea: que quien te vea en 30 segundos piense
"esta persona ya hace el trabajo".

## 1. Portafolio: 3 proyectos que cuenten una historia

1. **Análisis** (Proyecto 1): preguntas de negocio, limpieza, gráficos y conclusiones.
2. **Pipeline** (Proyecto 2): ingeniería de datos de punta a punta, con Docker y pruebas.
3. **IA aplicada o dashboard:** un asistente RAG, un dashboard publicado, o un modelo con evaluación honesta.

Cada repositorio debe tener un **README** con: problema, datos, arquitectura/diagrama, resultados, cómo ejecutarlo y qué aprendiste.
Fija (pin) los 3 mejores en tu perfil de GitHub y escribe una biografía clara.

## 2. CV de una página

- **Titular claro:** "Analista de datos / Ingeniero de datos junior · SQL · Python · PostgreSQL · Docker".
- **Proyectos arriba** (con enlace), antes que estudios si no tienes experiencia.
- **Logros con números**, no tareas:

| Débil | Fuerte |
|---|---|
| "Trabajé con datos de ventas" | "Construí un pipeline diario en Python/PostgreSQL que procesa 200 000 filas y reduce el tiempo de reporte de 2 h a 5 min" |
| "Hice dashboards" | "Diseñé un dashboard de 5 KPIs que usan 3 áreas para decidir promociones" |

- Palabras clave de la oferta (los filtros automáticos las buscan), sin mentir.
- Un solo formato limpio, en PDF, con tu correo y enlaces (LinkedIn, GitHub).

## 3. LinkedIn

Foto profesional, titular con tu especialidad (no "buscando oportunidades"), extracto en primera persona con tus proyectos y tecnologías,
y publica de vez en cuando lo que aprendes. Un post sobre un problema real que resolviste te genera más contactos que cien solicitudes.

## 4. Dónde y cómo buscar

- **Portales:** LinkedIn, Indeed, Computrabajo, GetOnBoard, WeWorkRemotely, RemoteOK, Torre; busca "data analyst", "analista de datos", "BI", "data engineer junior".
- **Remoto internacional:** amplía mucho tus opciones; revisa idioma y zona horaria requeridos, y la forma de contratación y pago.
- **Referidos:** escribe a personas del área con un mensaje corto y específico ("vi tu proyecto X, me gustaría preguntarte...").
- **Pasantías, voluntariados y proyectos freelance pequeños** cuentan como experiencia.
- **Sé constante:** aplica a pocas ofertas bien personalizadas en lugar de 100 genéricas, y lleva un registro (empresa, fecha, estado).

## 5. Idiomas y habilidades blandas

El inglés técnico (leer documentación y comunicarte por escrito) es un multiplicador enorme. Practica explicando tus proyectos en inglés.

## 6. Cuidado con las estafas

Desconfía de ofertas que piden **pagar** por el puesto o por materiales, dan **datos bancarios** antes de un contrato o prometen sueldos irreales. Verifica la empresa y el reclutador.

## Cómo sabes que dominas este tema

- Cualquier persona entiende en 30 segundos qué haces y qué proyectos tienes.
- Tu CV muestra logros medibles.
- Tienes un registro de postulaciones y un plan semanal de búsqueda.
""",
        "exercises": [
            quiz("emp-quiz-cv", "Mejorar una viñeta del CV", "Empleo: portafolio y CV",
                 "¿Cuál de estas viñetas de CV es la más sólida?",
                 ["Responsable de reportes de ventas", "Automaticé el reporte semanal de ventas con Python y SQL, pasando de 3 h a 10 min",
                  "Experiencia con datos y herramientas varias", "Conocimientos de Excel, Python, SQL, Power BI, R, Java y C++"], 1,
                 "Una buena viñeta empieza con un verbo de acción, indica **qué hiciste, con qué** y el **resultado medible**."),
            quiz("emp-quiz-estafa", "Señales de alerta", "Empleo: portafolio y CV",
                 "Un reclutador te ofrece un puesto remoto muy bien pagado sin entrevista y te pide un depósito 'para el equipo de trabajo'. ¿Qué haces?",
                 ["Pago para no perder la oportunidad", "No pago; es una señal clásica de estafa", "Doy mis datos bancarios para verificar", "Pago solo la mitad"], 1,
                 "Una empresa real nunca te cobra por contratarte. Verifica la empresa y al reclutador por canales oficiales."),
            checklist("emp-check-github", "Tu GitHub listo", "Empleo: portafolio y CV",
                      "Revisa tu perfil de GitHub.",
                      ["Tengo 3 proyectos fijados con README completo", "Cada README tiene problema, arquitectura, resultados y cómo ejecutarlo",
                       "No hay credenciales ni datos privados en los repositorios", "Mi perfil tiene foto y una biografía clara",
                       "Mis commits tienen mensajes descriptivos"]),
            checklist("emp-check-cv", "Tu CV y LinkedIn listos", "Empleo: portafolio y CV",
                      "Revisa tu CV y tu perfil de LinkedIn.",
                      ["Mi CV cabe en una página y está en PDF", "Mis proyectos aparecen arriba, con enlaces", "Cada logro tiene un número o resultado medible",
                       "Mi titular de LinkedIn indica mi especialidad y tecnologías", "Pedí a una persona que revisara mi CV",
                       "Tengo una hoja de seguimiento de postulaciones"]),
        ],
    },
    {
        "slug": "empleo-entrevistas",
        "phase": "empleo",
        "title": "Entrevistas técnicas y casos de negocio",
        "summary": "Practica las preguntas clásicas de SQL y Python, casos de negocio y entrevistas conductuales con el método STAR.",
        "hours": 12,
        "theory": r"""
# Entrevistas técnicas y casos de negocio

Un proceso típico para analista o ingeniero de datos junior tiene 3-5 etapas:

1. **Screening con recursos humanos:** motivación, expectativas, inglés, disponibilidad.
2. **Prueba técnica:** SQL y Python (en vivo o como tarea para casa).
3. **Caso de negocio o de datos:** analizas un problema y explicas tu razonamiento.
4. **Entrevista conductual:** cómo trabajas en equipo, cómo manejas errores y desacuerdos.
5. **Conversación final** con el responsable y negociación.

## 1. Prueba técnica de SQL (la más común)

Temas que **siempre** aparecen: `JOIN` (y anti-joins), `GROUP BY`/`HAVING`, funciones de ventana (top N por grupo, segundo valor más alto, acumulados, variación periodo a periodo), CTE, fechas, duplicados y NULL.

Cómo abordarla:

1. **Repite la pregunta** y aclara el grano (¿una fila por qué?), el tratamiento de NULL y los empates.
2. Escribe primero una versión simple y **piensa en voz alta**.
3. **Prueba con un ejemplo pequeño** mentalmente.
4. Menciona alternativas y rendimiento ("podría usar un índice en...").

## 2. Prueba técnica de Python

Estructuras de datos (diccionarios, conjuntos), manipulación de texto, pandas y problemas cortos de lógica. No suelen pedir algoritmos complejos para roles de datos, pero sí **claridad y casos borde** (listas vacías, nulos, duplicados).

## 3. Casos de negocio: un marco de 5 pasos

1. **Aclara el objetivo:** "¿Qué decisión se tomará con el resultado?"
2. **Define las métricas** y su denominador ("¿conversión sobre visitas o sobre usuarios únicos?").
3. **Segmenta:** canal, producto, país, nuevos vs. recurrentes... buscando dónde está el cambio.
4. **Formula hipótesis** y qué datos las confirmarían o descartarían.
5. **Recomienda** una acción y explica cómo medirías su efecto (¿un experimento A/B?).

Ejemplo: "Las ventas bajaron 10 % este mes, ¿qué harías?" → descompón (visitas × conversión × ticket), segmenta, comprueba datos (¿un fallo de registro?), estacionalidad, y propone acciones.

## 4. Entrevista conductual: método STAR

Cuenta cada historia con **S**ituación → **T**area → **A**cción (lo que *tú* hiciste) → **R**esultado (con números si es posible).
Prepara 5 historias: un error y qué aprendiste, un desacuerdo, algo que aprendiste rápido, un proyecto del que estás orgulloso, trabajo bajo presión.

## 5. Preguntas que debes hacer tú

"¿Cómo es el día a día del equipo?", "¿Qué herramientas y datos usan?", "¿Cómo medirán mi éxito en los primeros 6 meses?", "¿Qué oportunidades de aprendizaje hay?".

## 6. Negociación y primera oferta

Investiga rangos del mercado (portales y comunidades), considera el paquete completo (salario, moneda, beneficios, formación, remoto) y no aceptes ni rechaces en el acto: **pide tiempo** para evaluar la oferta.

## 7. Cómo prepararte con esta plataforma

Haz los ejercicios de abajo **cronometrados** (15 minutos cada uno) y explícalos en voz alta, como si hablaras con el entrevistador.

## Cómo sabes que dominas este tema

- Resuelves los 4 ejercicios SQL de abajo sin pistas y los explicas.
- Tienes 5 historias STAR escritas.
- Sigues un marco para cualquier caso de negocio.
""",
        "exercises": [
            sql("int-sql-1", "Segundo salario más alto por departamento", "Entrevistas: SQL clásico",
                "Para cada departamento con al menos dos salarios distintos, muestra el `department`, el `name` y el `salary` de quien tiene el **segundo salario más alto** "
                "(si hay empate en ese salario, muestra a todos). Usa `DENSE_RANK`. Ordena por departamento y nombre.",
                """SELECT department, name, salary FROM (
  SELECT department, name, salary,
         DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS r
  FROM employees
) t
WHERE r = 2
ORDER BY department, name""",
                starter="SELECT department, name, salary FROM (\n  SELECT department, name, salary,\n         DENSE_RANK() OVER (\n           -- completa\n         ) AS r\n  FROM employees\n) t\nWHERE r = 2\n",
                ordered=True),
            sql("int-sql-2", "Producto estrella de cada categoría", "Entrevistas: SQL clásico",
                "Para cada categoría, encuentra el producto con **más unidades vendidas** (`SUM(quantity)` en `order_items`). Devuelve `category`, `name` y `unidades`. "
                "Si hay empate, elige el de menor nombre alfabéticamente. Ordena por categoría.",
                """WITH ventas AS (
  SELECT p.category, p.name, SUM(oi.quantity) AS unidades
  FROM order_items oi JOIN products p ON p.id = oi.product_id
  GROUP BY p.category, p.name
),
ranking AS (
  SELECT category, name, unidades,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY unidades DESC, name) AS rn
  FROM ventas
)
SELECT category, name, unidades FROM ranking WHERE rn = 1 ORDER BY category""",
                starter="WITH ventas AS (\n  -- unidades por producto\n),\nranking AS (\n  -- numera dentro de cada categoría\n)\nSELECT category, name, unidades\nFROM ranking\nWHERE rn = 1\nORDER BY category",
                ordered=True),
            sql("int-sql-3", "Clientes que repiten compra", "Entrevistas: SQL clásico",
                "¿Qué porcentaje de los clientes con al menos un pedido **completado** tiene 2 o más pedidos completados? "
                "Devuelve una sola columna `pct_repetidores` redondeada a 1 decimal.",
                """WITH por_cliente AS (
  SELECT customer_id, COUNT(*) AS n
  FROM orders
  WHERE status = 'completado'
  GROUP BY customer_id
)
SELECT ROUND(100.0 * SUM(CASE WHEN n >= 2 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_repetidores
FROM por_cliente""",
                starter="WITH por_cliente AS (\n  -- pedidos completados por cliente\n)\nSELECT\nFROM por_cliente\n"),
            sql("int-sql-4", "Clientes con pedidos en 2024 y en 2025", "Entrevistas: SQL clásico",
                "Lista `id` y `name` de los clientes que hicieron **al menos un pedido en 2024 y al menos uno en 2025** (cualquier estado). Ordena por id.",
                """SELECT c.id, c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.order_date BETWEEN '2024-01-01' AND '2024-12-31')
  AND EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.order_date BETWEEN '2025-01-01' AND '2025-12-31')
ORDER BY c.id""",
                starter="SELECT c.id, c.name\nFROM customers c\nWHERE EXISTS (\n  -- pedido en 2024\n)\n  AND EXISTS (\n  -- pedido en 2025\n)\nORDER BY c.id", ordered=True),
            py("int-py-dos-sumas", "Dos números que suman el objetivo", "Entrevistas: Python clásico",
               "Escribe `dos_sumas(nums, objetivo)` que devuelva una tupla `(i, j)` con `i < j` tal que `nums[i] + nums[j] == objetivo`, o `None` si no existe. "
               "Intenta resolverlo en una sola pasada usando un diccionario.",
               starter="""
def dos_sumas(nums, objetivo):
    # tu código aquí
    pass
""",
               solution="""
def dos_sumas(nums, objetivo):
    vistos = {}
    for j, n in enumerate(nums):
        complemento = objetivo - n
        if complemento in vistos:
            return (vistos[complemento], j)
        vistos[n] = j
    return None
""",
               tests="""
assert dos_sumas([2, 7, 11, 15], 9) == (0, 1)
assert dos_sumas([3, 2, 4], 6) == (1, 2)
assert dos_sumas([1, 2, 3], 100) is None, "Si no existe, devuelve None"
assert dos_sumas([], 5) is None
""",
               hint="Guarda en un diccionario cada número visto con su posición y busca el complemento."),
            py("int-py-no-repetido", "Primer carácter no repetido", "Entrevistas: Python clásico",
               "Escribe `primer_no_repetido(texto)` que devuelva el primer carácter que aparece **una sola vez** en `texto`, o `None` si no hay ninguno.",
               starter="""
def primer_no_repetido(texto):
    # tu código aquí
    pass
""",
               solution="""
def primer_no_repetido(texto):
    conteo = {}
    for caracter in texto:
        conteo[caracter] = conteo.get(caracter, 0) + 1
    for caracter in texto:
        if conteo[caracter] == 1:
            return caracter
    return None
""",
               tests="""
assert primer_no_repetido("aabbcd") == "c"
assert primer_no_repetido("aabb") is None
assert primer_no_repetido("") is None
assert primer_no_repetido("xyzx") == "y"
"""),
            quiz("int-quiz-caso", "Caso de negocio", "Entrevistas: casos de negocio",
                 "Te dicen: 'Las ventas bajaron un 10 % este mes. ¿Qué haces primero?'",
                 ["Proponer una gran promoción de inmediato", "Verificar que los datos son correctos y descomponer la métrica (visitas × conversión × ticket) por segmentos",
                  "Despedir al equipo comercial", "Esperar al mes siguiente"], 1,
                 "Primero valida los datos (¿es un fallo de registro?) y descompón la caída para localizar dónde ocurre. Solo después proponen acciones."),
            checklist("int-check-star", "Prepara tus historias STAR", "Entrevistas: casos de negocio",
                      "Escribe cada historia con Situación, Tarea, Acción y Resultado.",
                      ["Un error que cometí y lo que aprendí", "Un desacuerdo y cómo lo resolví", "Algo que aprendí rápido por necesidad",
                       "Un proyecto del que estoy orgulloso (con resultado medible)", "Trabajo bajo presión o con plazo ajustado",
                       "Practiqué contarlas en voz alta en menos de 2 minutos cada una"]),
        ],
    },
]
