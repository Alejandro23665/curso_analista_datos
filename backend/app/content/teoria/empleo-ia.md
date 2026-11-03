# Tu primer empleo como desarrollador de IA o backend

Conseguir el primer empleo en tecnología es, para la mayoría, **más difícil que conseguir el segundo**. No tienes experiencia
profesional que enseñar, compites con cientos de candidatos por cada oferta junior y muchas postulaciones no reciben respuesta. Si te ha
pasado, no es una señal de que no sirvas: es como funciona el proceso, y se puede mejorar con método.

Este capítulo trata la búsqueda como lo que es: **un embudo que se mide y se optimiza**. Verás qué puestos buscar, qué portafolio te
diferencia, cómo conseguir respuestas, cómo son las entrevistas de IA aplicada (incluidas las que se hacen con agentes de IA) y qué
responder a las preguntas típicas.

---

## 1. El embudo: dónde se pierden los candidatos

```
Postulaciones enviadas      100
  ↓ alguien te responde       5-10    ← aquí se pierde la mayoría
Primera llamada (RR. HH.)     4-8
  ↓
Entrevista técnica            2-4
  ↓
Entrevista final              1-2
  ↓
Oferta                        0-1
```

Las cifras varían mucho, pero la forma es siempre esta. La consecuencia práctica: **si casi nadie te responde, el problema está en la
primera etapa** (qué puestos eliges, tu CV, tu portafolio, el canal), no en tus entrevistas. Si te entrevistan a menudo pero no avanzas,
el problema está en la preparación técnica. Cada etapa tiene soluciones distintas, y la única forma de saber dónde estás fallando es
**medir**.

### Lleva un registro

Una hoja de cálculo con una fila por postulación: fecha, empresa, puesto, **canal** (portal de empleo, LinkedIn, mensaje directo,
referido), si adaptaste el CV, si hubo respuesta y hasta qué etapa llegaste. Con 30-50 filas podrás calcular, por ejemplo, el **porcentaje
de postulaciones con respuesta de cada canal** y dedicar más tiempo al que funciona. Es el mismo análisis que harías con los datos de una
empresa: agrupar por una categoría y calcular una proporción.

---

## 2. Qué puestos buscar

El título "AI Engineer junior" existe, pero hay pocos y muy disputados. Amplía el radio a puestos donde tu combinación (desarrollo web +
Python + SQL + IA aplicada) es una ventaja:

| Puesto | Por qué encaja | Qué destacar |
|---|---|---|
| **Backend developer junior (Python)** | La base de casi toda app de IA | FastAPI, SQL, APIs, pruebas, Docker |
| **AI / LLM engineer junior** | Tu objetivo directo | Demo RAG desplegada, evaluación, agentes |
| **Full-stack developer** | Tu formación web + backend | React + FastAPI + una funcionalidad con IA |
| **Automation engineer** / integraciones | Muy demandado en pymes y agencias | n8n/Make, APIs, webhooks, scripts de Python |
| **Solutions / support engineer** | Técnico + trato con clientes | Comunicación, depuración, documentación |
| **Data analyst junior** | Usa tu SQL y Python | Consultas, métricas, un análisis publicado |
| **Evaluación de código para entrenar IA** (*AI trainer*) | Trabajo remoto accesible; buen ingreso puente | Lectura de código, rigor, inglés escrito |

**Las startups pequeñas y las agencias** suelen ser más accesibles que las grandes empresas para un primer empleo: procesos más cortos,
menos filtros automáticos y más valor a quien "sabe construir cosas", aunque no tenga experiencia formal.

### Lee las ofertas como un analista

Una oferta pide 12 requisitos; ninguna persona los cumple todos. Separa los **imprescindibles** (normalmente los 3-4 primeros, o los que
se repiten) de los deseables. Si cumples el 60-70 % de lo importante, postula. Y fíjate en las palabras que se repiten en muchas ofertas:
son las que deben aparecer en tu CV y tu portafolio (si de verdad las sabes usar).

---

## 3. El portafolio que te diferencia

Para un junior sin experiencia, el portafolio **es** la experiencia. Pero no cualquier portafolio:

| Débil | Fuerte |
|---|---|
| 10 repositorios de cursos sin README | 1-3 proyectos completos, desplegados, con README |
| Un clon de un tutorial | Un problema real, con datos reales |
| "Funciona en mi máquina" | Un enlace público que cualquiera puede probar |
| Código sin pruebas | Pruebas automáticas y una evaluación medida |
| Una lista de certificados | Proyectos que demuestran lo que dicen los certificados |

### El proyecto estrella: tu asistente con RAG

El proyecto de esta ruta (la demo de chatbot) cubre casi todo lo que buscan en un puesto de IA aplicada:

- **Desplegado**, con un enlace en la primera línea del README.
- **RAG con fuentes citadas** sobre un conjunto de documentos real.
- **Streaming**, estados de carga y error.
- **Evaluación**: un conjunto de 30-50 preguntas con resultados medidos ("la recuperación pasó del 70 % al 88 % al cambiar el chunking").
  Esto es lo que casi nadie hace y lo que más impresiona.
- **Seguridad básica**: claves en el backend, límite de peticiones, defensa contra la inyección de instrucciones.
- **README** con: qué problema resuelve, una captura o GIF, la arquitectura (un diagrama simple), las decisiones que tomaste y por qué,
  los resultados de la evaluación, cómo ejecutarlo en local y qué mejorarías.

Un segundo proyecto útil: una **automatización** que resuelva un problema concreto de negocio (extraer datos de facturas, clasificar
correos), y un tercero opcional de **datos** (un análisis con SQL y Python con conclusiones claras).

### GitHub, CV y LinkedIn

- **GitHub**: fija (*pin*) tus mejores proyectos; un README de perfil breve; commits con mensajes claros. Nadie mira 40 repositorios: mira
  los fijados.
- **CV**: una página, sin foto ni datos personales innecesarios, con el enlace a la demo arriba. Los proyectos se describen como
  experiencia: qué construiste, con qué y **qué resultado** ("asistente RAG con FastAPI y pgvector; 88 % de recuperación en una evaluación
  de 40 preguntas"). Adapta el orden y las palabras a cada tipo de puesto.
- **LinkedIn**: un titular específico ("Backend Python · IA aplicada (RAG, agentes) · FastAPI") en vez de "Estudiante" o "Buscando
  oportunidades"; la demo en la sección destacada; publica de vez en cuando lo que construyes.

---

## 4. Conseguir respuestas: canales

| Canal | Tasa de respuesta típica | Notas |
|---|---|---|
| Postulación en un portal (LinkedIn Easy Apply, portales) | Baja | Mucho volumen y filtros automáticos; útil pero no suficiente |
| Portales especializados en tecnología y remoto para Latinoamérica | Media | Menos competencia y ofertas más relevantes |
| **Mensaje directo** a fundadores, responsables técnicos o reclutadores | Media-alta si es bueno | El canal infrautilizado |
| **Referidos** (alguien de dentro te recomienda) | La más alta | Se construye con comunidad y contactos |
| Comunidades (Discord, meetups, open source) | Indirecta | Generan referidos y oportunidades no publicadas |

### El mensaje directo que recibe respuesta

Igual que en las propuestas de freelance: corto, concreto y con prueba.

> Hola, Marta. Vi que en [empresa] están construyendo un asistente para conciliar pagos de pymes. Construí un sistema parecido que
> extrae y valida datos de facturas con IA y lo evalué con 50 facturas reales (demo: [enlace]). Me encantaría aportar en algo así:
> ¿podríamos hablar 15 minutos esta semana?

Personalizado (demuestra que miraste qué hace la empresa), con una prueba relacionada con **su** problema y una petición pequeña. Un
mensaje genérico ("busco empleo, ¿tienen vacantes?") o un CV sin texto casi nunca recibe respuesta.

### Una semana sostenible

La búsqueda es una maratón, no un sprint. Un plan semanal que puedes mantener mientras estudias:

- 5-10 postulaciones **adaptadas** (mejor pocas buenas que 50 genéricas).
- 3-5 mensajes directos.
- Publicar o compartir algo que construiste o aprendiste.
- Practicar un problema de algoritmos y uno de SQL, cronometrados.
- Actualizar el registro y revisar qué canal funciona.

---

## 5. Las etapas de la entrevista

1. **Llamada con reclutamiento** (15-30 min): motivación, disponibilidad, expectativas salariales, inglés. Prepara un resumen de 60
   segundos de quién eres y qué construyes, y una cifra salarial investigada.
2. **Prueba técnica**: puede ser *live coding* (algoritmos o un problema práctico), una prueba para casa (*take-home*), una revisión de
   código o, cada vez más, **una tarea con un agente de IA**.
3. **Entrevista técnica en profundidad**: hablar de tus proyectos, diseño de sistemas sencillo, preguntas conceptuales.
4. **Entrevista de cultura o comportamiento**: trabajo en equipo, conflictos, cómo aprendes (capítulo de entrevistas).
5. **Oferta**.

### Entrevistas con agentes de IA

Muchas empresas ya permiten (o exigen) usar asistentes de código en la entrevista, porque así se trabaja. Lo que evalúan **no** es si el
agente genera código, sino **tu criterio**:

- **Entender antes de pedir**: reformula el problema y los casos borde antes de escribir el prompt.
- **Leer el resultado**: recorre el código generado explicando en voz alta qué hace. Si no entiendes una parte, dilo y averígualo.
- **Verificar**: pide o escribe pruebas para los casos borde (lista vacía, valores nulos, duplicados), ejecútalas.
- **Corregir**: el agente a menudo produce algo que "parece funcionar". Encontrar lo que está mal es lo que demuestra nivel.
- **Explicar las decisiones**: por qué aceptaste o rechazaste una sugerencia.

Aceptar sin leer lo que genera el agente es la forma más rápida de suspender. Y si en tu trabajo un cambio generado por un agente rompe
producción, lo profesional es lo mismo que con cualquier otro cambio: primero **restaurar el servicio** (revertir el cambio), después
reproducir el fallo con una prueba, corregir y explicar qué falló en el proceso de revisión.

---

## 6. Preguntas de entrevista de IA aplicada

Preguntas que salen a menudo, con lo que debería contener una buena respuesta. No las memorices: entiéndelas, porque te pedirán ejemplos
de tus proyectos.

**"Explícame cómo funciona un LLM a alguien no técnico."**
Predice el siguiente fragmento de texto a partir de lo anterior, entrenado con muchísimo texto; no consulta una base de datos de hechos,
por eso puede equivocarse con seguridad.

**"¿Qué es RAG y cuándo lo usarías?"**
Recuperar fragmentos relevantes de los documentos propios y dárselos al modelo con la pregunta. Para conocimiento privado o que cambia;
frente al fine-tuning, que sirve más para el comportamiento o el estilo.

**"¿Cómo reducirías las alucinaciones de un asistente de soporte?"**
Una respuesta completa combina varias medidas: RAG con los documentos de la empresa y **citas**; instrucciones explícitas para responder
"no lo sé" cuando la información no está; limitar el asistente a su dominio; y, sobre todo, **un conjunto de evaluación** para medir si
cada cambio mejora o empeora. Respuestas como "usar el modelo más grande" o "pedirle que no invente" son incompletas: pueden ayudar, pero
no se pueden comprobar sin medir.

**"¿Cómo evaluarías un sistema con LLM?"**
Un conjunto de casos realistas con la respuesta esperada; métricas automáticas donde se pueda (recuperación, formato, exactitud) y
revisión humana o un LLM como juez para la calidad; medir antes y después de cada cambio.

**"¿Cómo controlas el costo?"**
Tokens de entrada y salida; elegir el modelo adecuado por tarea; caché de prompts; limitar la longitud del historial y de la respuesta;
medir el costo por conversación.

**"¿Qué riesgos de seguridad tiene una app con LLM?"**
Inyección de instrucciones (directa e indirecta), filtración de datos, claves expuestas, acciones peligrosas de agentes; defensas por
capas: permisos mínimos, confirmación humana para acciones sensibles, tratar el contenido externo como datos.

**"Háblame de un proyecto del que estés orgulloso."**
Usa una estructura: el problema, tu solución, **una decisión difícil** y por qué la tomaste, el resultado medido y qué harías distinto.
Es la pregunta más importante para un junior: prepara bien la respuesta sobre tu demo.

### Preguntas de backend que también salen

Diferencia entre `GET` y `POST`; códigos de estado (200, 201, 400, 401, 403, 404, 500); qué es un índice en una base de datos;
`INNER JOIN` vs `LEFT JOIN`; cómo guardar contraseñas; qué es la inyección SQL; qué hace Docker; cómo escribirías pruebas para una
función. Todas están en los capítulos de esta ruta.

---

## 7. Errores frecuentes en la búsqueda

| Error | Alternativa |
|---|---|
| Postular solo a ofertas que piden 3 años de experiencia, o solo a "AI Engineer" | Ampliar a backend, automatización, full-stack, startups |
| El mismo CV para todo | Adaptar el orden y las palabras a cada tipo de puesto |
| Portafolio de ejercicios de cursos | 1-3 proyectos reales, desplegados, con README y evaluación |
| Solo postular por portales | Mensajes directos, comunidades, referidos |
| No medir | Registro de postulaciones y análisis por canal |
| Esperar a "estar listo" para postular | Postular mientras aprendes: las entrevistas también enseñan |
| Desaparecer tras una entrevista | Un mensaje breve de agradecimiento; pedir comentarios si te descartan |

### Sobre el inglés

El mercado remoto internacional paga más y tiene más ofertas, pero casi siempre exige inglés para comunicarte con el equipo. No necesitas
un nivel perfecto para empezar a postular a empresas de Latinoamérica o en español, pero cada mejora en tu inglés **multiplica** las
ofertas a las que puedes aspirar. Por eso la plataforma tiene una vista de inglés aparte: avanza en paralelo.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Embudo | Si nadie responde, el problema está en la primera etapa; mide cada etapa |
| Registro | Una fila por postulación; tasa de respuesta por canal |
| Puestos | Backend Python, IA aplicada, full-stack, automatización, soporte técnico, datos, evaluación de código |
| Portafolio | 1-3 proyectos desplegados, con README, pruebas y evaluación medida |
| Canales | Mensajes directos y referidos, además de portales |
| Entrevistas con IA | Entender, leer, verificar con pruebas, corregir, explicar |
| Preguntas de IA | RAG, alucinaciones, evaluación, costo, seguridad, tu proyecto |
| Constancia | Un plan semanal sostenible y revisado con datos |

## Autoevaluación final

1. Has enviado 80 postulaciones y solo has tenido una entrevista. ¿En qué etapa del embudo está el problema y qué cambiarías?
2. Nombra tres puestos, además de "AI Engineer", donde tu perfil es competitivo.
3. ¿Qué hace que un proyecto de portafolio sea "fuerte"?
4. Escribe la estructura de un buen mensaje directo a una startup.
5. En una entrevista con un agente de IA, el agente genera una solución en segundos. ¿Qué haces?
6. ¿Qué elementos tiene una respuesta completa a "¿cómo reducirías las alucinaciones?"?
7. Un cambio generado por un agente rompe producción. ¿Cuál es el primer paso?
8. ¿Qué datos registrarías de cada postulación y qué calcularías con ellos?

**Respuestas:** 1) En la primera etapa (conseguir respuesta): revisar los puestos elegidos, adaptar el CV, mejorar el portafolio y
añadir mensajes directos y referidos. 2) Por ejemplo: backend Python junior, automatización/integraciones, full-stack, soporte o
solutions engineer, data analyst, evaluación de código para IA. 3) Resuelve un problema real, está desplegado, tiene README con
arquitectura y decisiones, pruebas y una evaluación con resultados medidos. 4) Algo concreto de su empresa, una prueba relacionada
(demo), una petición pequeña (15 minutos). 5) Leerla explicando qué hace, probar los casos borde, corregir lo que esté mal y explicar las
decisiones. 6) RAG con citas, instrucciones de "no lo sé", limitar el dominio y un conjunto de evaluación para medir. 7) Revertir el
cambio para restaurar el servicio; después reproducir el fallo con una prueba y corregir. 8) Fecha, empresa, puesto, canal, CV adaptado,
respuesta y etapa alcanzada; la tasa de respuesta por canal y por tipo de puesto.
