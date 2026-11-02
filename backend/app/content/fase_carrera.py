from ._helpers import checklist, py, quiz

TOPICS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "frontend-ia",
        "phase": "carrera",
        "title": "Interfaces para apps con IA: React, TypeScript y streaming",
        "summary": "Cómo conectar un frontend con tu backend de IA: chat con streaming, estados de carga y error, y dónde NO poner las claves.",
        "hours": 10,
        "theory": r"""
# Interfaces para apps con IA: React, TypeScript y streaming

Un cliente o un reclutador no abre tu repositorio: **abre un enlace y prueba**. Una demo con interfaz desplegada vale mucho más
que un endpoint perfecto. Ya conoces React por tu formación; aquí lo aplicas a lo específico de una app con IA.

## 1. La arquitectura correcta

```
Navegador (React)  →  Tu backend (FastAPI)  →  API del modelo (Claude, etc.)
```

- **La clave de la API vive solo en el backend** (variable de entorno). Todo lo que está en el frontend lo puede leer cualquiera
  con las herramientas del navegador, incluido un `VITE_API_KEY`.
- El backend también decide **qué** se envía al modelo (prompt del sistema, documentos del RAG, límites de tokens) y aplica
  autenticación y límite de peticiones por usuario. El frontend solo envía el mensaje y muestra la respuesta.

## 2. Streaming: que la respuesta aparezca mientras se genera

Una respuesta larga puede tardar 10-20 segundos. Si la muestras de golpe, parece que la app está colgada. Con **streaming**
el backend reenvía los fragmentos a medida que llegan, normalmente con *Server-Sent Events* (SSE): líneas de texto como

```
data: Hola
data: , ¿en qué
data:  te ayudo?
data: [DONE]
```

En FastAPI devuelves un `StreamingResponse` con `media_type="text/event-stream"`; en React lees el cuerpo con
`fetch` + `response.body.getReader()` y vas añadiendo cada fragmento al último mensaje del estado.

## 3. Los estados que siempre debe tener la interfaz

| Estado | Qué ve el usuario |
|---|---|
| Vacío | Ejemplos de preguntas para empezar |
| Cargando | Indicador y botón de enviar desactivado (evita peticiones duplicadas) |
| Respondiendo | Texto que crece + botón **Detener** (`AbortController`) |
| Error | Mensaje claro y opción de reintentar (el modelo puede fallar o saturarse) |
| Fuentes | En un RAG, las **citas** de los documentos usados: generan confianza |

## 4. TypeScript: tipa lo que viene del backend

```ts
type Mensaje = { rol: "usuario" | "asistente"; texto: string; fuentes?: string[] };
```

Tipar las respuestas de la API evita la mitad de los errores de interfaz y es lo que esperan las ofertas actuales
("React + TypeScript" aparece en la mayoría de las ofertas fullstack).

## 5. Despliegue y CORS

Frontend en Vercel o Netlify, backend en Railway, Render o una función de Vercel. Si están en dominios distintos, configura
**CORS** en el backend solo para el dominio del frontend (no `*` en producción).

## Cómo sabes que dominas este tema

- Tu demo tiene un enlace público, streaming, estados de carga y error, y la clave nunca llega al navegador.
- Sabes explicar en una entrevista por qué el frontend no llama directamente a la API del modelo.
""",
        "exercises": [
            py("fe-sse", "Leer un stream de eventos (SSE)", "Carrera: frontend para IA",
               "Escribe `leer_sse(lineas)` que reciba una lista de líneas de un stream SSE y devuelva el texto completo. "
               "Solo cuentan las líneas que empiezan por `data: ` (con el espacio); quita ese prefijo y concatena el resto **sin modificarlo**. "
               "Ignora las demás líneas (vacías, comentarios que empiezan por `:`) y **detente** al encontrar `data: [DONE]`.",
               starter="""
def leer_sse(lineas):
    texto = ""
    # recorre las líneas
    return texto
""",
               solution="""
def leer_sse(lineas):
    texto = ""
    for linea in lineas:
        if not linea.startswith("data: "):
            continue
        dato = linea[len("data: "):]
        if dato == "[DONE]":
            break
        texto += dato
    return texto
""",
               tests="""
assert leer_sse(["data: Hola", "", "data: , mundo", "data: [DONE]"]) == "Hola, mundo", "Concatena los fragmentos en orden"
assert leer_sse([": ping", "data: a", "event: x", "data:  b"]) == "a b", "Ignora lo que no es data y conserva los espacios del fragmento"
assert leer_sse(["data: uno", "data: [DONE]", "data: dos"]) == "uno", "Lo que viene despues de [DONE] no cuenta"
assert leer_sse([]) == "", "Sin lineas, texto vacio"
""",
               hint="`linea.startswith(\"data: \")` y luego `linea[6:]`. Usa `break` para detenerte en [DONE]."),
            quiz("fe-quiz-clave", "Dónde vive la clave del modelo", "Carrera: frontend para IA",
                 "Tu demo en React necesita llamar a la API de un LLM. ¿Dónde pones la clave?",
                 ["En una variable VITE_API_KEY del frontend", "En el código de React, ofuscada",
                  "Solo en el backend, como variable de entorno; el frontend llama a tu backend", "En localStorage del usuario"], 2,
                 "Todo lo que llega al navegador es público. La clave va en el backend, que además controla el prompt, los límites y la autenticación."),
            quiz("fe-quiz-streaming", "Por qué usar streaming", "Carrera: frontend para IA",
                 "¿Cuál es la principal ventaja de mostrar la respuesta del modelo con streaming?",
                 ["El modelo genera más rápido", "El usuario ve texto en uno o dos segundos en vez de esperar la respuesta completa",
                  "Se gastan menos tokens", "Evita tener que usar un backend"], 1,
                 "El tiempo total es el mismo, pero la percepción cambia por completo: el usuario ve progreso casi de inmediato y puede detener la respuesta."),
            checklist("fe-check-demo", "Interfaz de tu demo lista", "Carrera: frontend para IA",
                      "Revisa la interfaz de tu demo de chatbot antes de enseñarla.",
                      ["Tiene un enlace público que funciona", "La respuesta aparece con streaming y se puede detener",
                       "Muestra estados de carga y de error con opción de reintentar", "En el RAG se ven las fuentes citadas",
                       "La clave del modelo solo está en el backend", "CORS permite solo el dominio de mi frontend",
                       "Funciona bien en el móvil"]),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "freelance-clientes",
        "phase": "carrera",
        "title": "Freelance: propuestas, precios, alcance y cobros",
        "summary": "Cómo conseguir y llevar tus primeros clientes de chatbots y automatizaciones sin regalar tu trabajo.",
        "hours": 6,
        "theory": r"""
# Freelance: propuestas, precios, alcance y cobros

Saber construir un chatbot no basta: hay que **venderlo, delimitarlo y cobrarlo**. Además, cada cliente real es experiencia
que puedes poner en tu CV ("Desarrollé un asistente para X que responde Y consultas al día").

## 1. Dónde y cómo empezar

- **Plataformas:** Workana, Upwork, Malt, Fiverr. Al principio compites por reputación: acepta proyectos pequeños y bien
  delimitados para conseguir las primeras reseñas.
- **Agencias de marca blanca:** agencias de marketing o de desarrollo que venden chatbots y automatizaciones y subcontratan
  la parte técnica. Trabajo más estable y sin tener que buscar al cliente final.
- **Contacto directo:** negocios locales o conocidos con un problema claro (atención por WhatsApp, citas, pedidos, documentos).

## 2. Una propuesta que se lee (y se responde)

Los clientes reciben decenas de propuestas genéricas. La tuya debe tener, en pocas líneas:

1. **Que entendiste su problema**, con sus palabras ("necesitas que el bot responda dudas de envíos y pase a una persona los reclamos").
2. **Cómo lo resolverías**, en 2-3 pasos y sin jerga.
3. **Prueba:** enlace a tu demo o a un proyecto parecido.
4. **Una pregunta concreta** que demuestre criterio ("¿las respuestas deben salir de tu catálogo actual o de un documento de políticas?").

## 3. Precio y alcance

- **Estima en horas y añade un colchón** (25-40 %): siempre aparecen imprevistos (datos sucios, accesos que tardan, cambios de opinión).
- Prefiere **precio por proyecto con hitos** (por ejemplo 30 % al inicio, 40 % a mitad, 30 % al entregar) a precio por hora
  cuando el alcance está claro.
- Escribe el **alcance por escrito**: qué incluye, qué no, cuántas rondas de cambios y cuánto soporte después de entregar.
  Todo lo demás es un **cambio de alcance** y se presupuesta aparte.
- Ofrece **mantenimiento mensual** (monitoreo, ajustes del prompt, actualización de documentos): convierte proyectos en ingresos recurrentes.

## 4. Cobros y seguridad

- Dentro de una plataforma, **cobra siempre por la plataforma**: si un cliente te pide salir de ella antes de pagar, es una señal de alerta y además viola sus reglas.
- Comprueba antes de empezar **cómo retiras el dinero desde tu país**, qué comisiones hay y cuánto tarda; las opciones cambian con el tiempo.
- Nunca trabajes con las credenciales personales del cliente: pide accesos propios y guarda las claves fuera del código.

## 5. De clientes a startup

Lleva un registro de cada cliente: problema, sector, cuánto pagó, qué pidió que no ofrecías. Cuando el mismo problema
aparezca tres o cuatro veces, ahí hay un producto.

## Cómo sabes que dominas este tema

- Tienes una plantilla de propuesta, una forma de estimar y un documento de alcance reutilizable.
- Sabes responder sin ponerte nervioso cuando un cliente pide "un cambio pequeño" fuera de lo acordado.
""",
        "exercises": [
            py("fl-presupuesto", "Presupuesto con colchón y hitos", "Carrera: freelance",
               "Escribe `presupuesto(horas, tarifa, colchon=0.3)`. Calcula las horas con colchón redondeando **hacia arriba** "
               "(`math.ceil(horas * (1 + colchon))`), el total (`horas_con_colchon * tarifa`) y tres hitos de pago del 30 %, 40 % y 30 %, "
               "redondeados a 2 decimales; el **último hito** es lo que falta para llegar al total, así la suma siempre cuadra. "
               "Devuelve un diccionario `{\"horas\": ..., \"total\": ..., \"hitos\": [h1, h2, h3]}`. Lanza `ValueError` si las horas o la tarifa son menores o iguales a 0.",
               starter="""
import math

def presupuesto(horas, tarifa, colchon=0.3):
    # calcula horas, total e hitos
    return {}
""",
               solution="""
import math

def presupuesto(horas, tarifa, colchon=0.3):
    if horas <= 0 or tarifa <= 0:
        raise ValueError("Horas y tarifa deben ser positivas")
    horas_finales = math.ceil(horas * (1 + colchon))
    total = horas_finales * tarifa
    h1 = round(total * 0.3, 2)
    h2 = round(total * 0.4, 2)
    h3 = round(total - h1 - h2, 2)
    return {"horas": horas_finales, "total": total, "hitos": [h1, h2, h3]}
""",
               tests="""
p = presupuesto(20, 15)
assert p["horas"] == 26, "20 h + 30 % = 26 h"
assert p["total"] == 390, "26 h x 15 = 390"
assert p["hitos"] == [117.0, 156.0, 117.0], "30 %, 40 % y el resto"
q = presupuesto(7, 12.5, colchon=0.25)
assert q["horas"] == 9, "7 x 1.25 = 8.75, hacia arriba 9"
assert round(sum(q["hitos"]), 2) == q["total"], "Los hitos deben sumar el total"
for args in ((0, 10), (10, 0), (-5, 10)):
    try:
        presupuesto(*args)
    except ValueError:
        pass
    else:
        raise AssertionError("presupuesto%s debe lanzar ValueError" % (args,))
""",
               hint="Calcula h1 y h2 con round(..., 2) y deja que h3 sea total - h1 - h2."),
            quiz("fl-quiz-alcance", "Un \"cambio pequeño\"", "Carrera: freelance",
                 "Entregaste el chatbot acordado y el cliente pide que ahora también agende citas en su calendario \"ya que estás\". ¿Qué haces?",
                 ["Lo hago gratis para que deje una buena reseña", "Le explico que queda fuera del alcance acordado y le envío un presupuesto para esa ampliación",
                  "Lo ignoro", "Le digo que no se puede hacer"], 1,
                 "Con el alcance por escrito, la respuesta es fácil y profesional: es una ampliación con su propio precio y plazo. Así se convierte en otro ingreso."),
            quiz("fl-quiz-cobro", "Pagar fuera de la plataforma", "Carrera: freelance",
                 "Un cliente nuevo de Workana te propone pasar la conversación a WhatsApp y pagarte \"directamente\" al terminar. ¿Qué haces?",
                 ["Acepto, así me ahorro la comisión", "Sigo dentro de la plataforma, con el pago protegido y por hitos",
                  "Acepto si me paga el 10 % por adelantado", "Le pido mis datos bancarios para que pague"], 1,
                 "Fuera de la plataforma pierdes la protección de pago y puedes perder la cuenta. Es además un patrón frecuente de estafa."),
            checklist("fl-check-propuesta", "Tu kit de freelance", "Carrera: freelance",
                      "Prepara lo necesario para enviar propuestas con constancia.",
                      ["Tengo un perfil completo en al menos una plataforma, con foto y titular específico",
                       "Tengo una demo pública que puedo enlazar en cada propuesta", "Tengo una plantilla de propuesta de 5-8 líneas que adapto a cada cliente",
                       "Tengo una plantilla de alcance (incluye, no incluye, rondas de cambios, soporte)",
                       "Sé cómo retirar el dinero desde mi país y cuánto cuesta", "Envío al menos 5 propuestas a la semana y las registro"]),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "empleo-ia",
        "phase": "carrera",
        "title": "Tu primer empleo como desarrollador de IA o backend",
        "summary": "Qué puestos buscar, qué portafolio te diferencia, cómo conseguir respuestas y qué preguntan en las entrevistas de IA aplicada.",
        "hours": 8,
        "theory": r"""
# Tu primer empleo como desarrollador de IA o backend

Si casi nunca te responden, el problema está en el **primer filtro** (CV, portafolio, canal y tipo de oferta), no en tus conocimientos.
Esa es la parte más fácil de arreglar.

## 1. Qué puestos buscar

Busca por varios nombres, en español y en inglés: *AI engineer junior*, *AI developer*, *LLM engineer*, *Python developer*,
*backend developer junior*, *AI automation specialist*, *integraciones / automatizaciones*. Las **startups pequeñas y las agencias**
contratan juniors con más facilidad que las empresas grandes, y valoran más un proyecto real que los años de experiencia.

La demanda se está moviendo de especialistas a **perfiles híbridos**, que encajan con tu plan:

- **Product engineer:** construye funcionalidades completas (backend, frontend, datos) pensando en el usuario y en el negocio.
- **Forward Deployed Engineer (FDE):** trabaja de cara al cliente, entiende su problema e implementa la integración de IA en sus sistemas.
  Es casi lo mismo que harás como freelance: cada cliente es experiencia directa para este puesto.
- **AI engineer:** construye aplicaciones donde el modelo es una pieza central (RAG, agentes, evaluaciones).

## 2. Un portafolio que cuente tu historia (3 proyectos)

1. **Demo de chatbot con RAG**, desplegada, con fuentes citadas y una pequeña evaluación (cuántas preguntas responde bien).
2. **Automatización o procesamiento de documentos con IA**: extracción, validación y revisión humana, con métricas de costo y precisión.
3. **Un producto completo** (tu MVP o una plataforma como DataPath): autenticación, base de datos, despliegue y pruebas.

Cada repositorio con README (problema, arquitectura, resultados con números, cómo ejecutarlo), **enlace que funciona** y
**sin datos ni direcciones de clientes**. Un enlace roto o datos de un cliente en GitHub restan más de lo que suma el proyecto.

## 3. CV y perfiles

- Titular específico: "Desarrollador Python · APIs (FastAPI) · IA aplicada (LLMs, RAG, agentes)".
- **Enlaces arriba**: GitHub, LinkedIn y demo.
- Proyectos antes que estudios, con logros medibles. Solo las tecnologías que puedes defender en una entrevista.
- Versión en inglés para ofertas remotas.

## 4. Canales: el botón "postular" es el peor

- Escribe **directamente** a fundadores, CTOs o responsables de equipo de startups pequeñas: 3-4 líneas con quién eres, un proyecto
  relevante con enlace y por qué esa empresa. Responde mucha más gente de la que crees.
- Comunidades de desarrolladores (Discord, eventos, hackatones): una hackatón es experiencia y contactos a la vez.
- Publica en LinkedIn lo que construyes (un problema, cómo lo resolviste, un resultado). Atrae reclutadores.
- **Mide**: registra empresa, canal, fecha y respuesta. Con 20-30 postulaciones verás qué canal funciona.

## 5. Qué preguntan en una entrevista de IA aplicada

- **Conceptos:** tokens y ventana de contexto, temperatura, embeddings, cuándo usar RAG y cuándo *fine-tuning*.
- **Calidad:** cómo reduces alucinaciones (RAG con citas, instrucciones claras, validar la salida, decir "no lo sé") y **cómo lo mides** (evaluaciones).
- **Costo y latencia:** caché, modelo pequeño para tareas simples, *batching*, límites de tokens.
- **Seguridad:** *prompt injection*, datos personales, permisos de las herramientas de un agente.
- **Tu proyecto:** "Explícame la arquitectura", "¿qué harías distinto?", "¿qué falló y cómo lo resolviste?".
- Además: live coding (tema de algoritmos), SQL y una prueba para casa del tipo "construye esta API".

## 6. El formato nuevo: entrevistas asistidas por IA

Como los asistentes resuelven solos los problemas de algoritmos y las pruebas para casa, muchas **startups** están cambiando de formato:
te dan un problema realista y lo resuelves **usando un agente de IA delante del entrevistador**. No evalúan si escribes rápido,
sino tu **criterio**: cómo especificas la tarea, qué contexto le das, cómo revisas lo que genera y si detectas sus errores.
(Las empresas grandes siguen con algoritmos y diseño de sistemas, y algunas vuelven a la pizarra presencial.)

Preguntas que conviene llevar preparadas, con un ejemplo de tus proyectos:

| Pregunta | Qué buscan oír |
|---|---|
| ¿Cómo garantizas la calidad del código que genera la IA? | Tareas pequeñas, pruebas primero, leer cada diff, linter y revisión (también automática en CI) |
| ¿Cómo gestionas el contexto del agente? | Archivo de contexto del proyecto, especificación de la tarea, qué no debe tocar, empezar de cero cuando el contexto se ensucia |
| ¿Cómo reduces el consumo de tokens? | Contexto mínimo y relevante, modelo pequeño para tareas simples, caché, no reenviar archivos enteros |
| ¿Cómo minimizas las alucinaciones? | Contexto verificable (documentación, RAG), pedir que cite o que diga "no lo sé", validar con pruebas |
| Un cambio hecho por un agente rompió producción, ¿qué haces? | Revertir primero, reproducir con una prueba, corregir y añadir la prueba para que no vuelva a pasar |
| ¿Qué *guardrails* pondrías a un agente? | Permisos mínimos, confirmación humana para acciones irreversibles, sin acceso a secretos, límites de gasto |
| ¿Qué haces si te quedas sin tokens o el servicio cae a mitad de tarea? | Commits pequeños y frecuentes, poder seguir a mano: nunca depender de código que no entiendes |

Cómo practicarlo: graba o cronometra una sesión en la que resuelves una tarea de tu proyecto con un agente **explicando en voz alta**
qué le pides, por qué y qué revisas antes de aceptar.

## Cómo sabes que dominas este tema

- Tus 3 proyectos están publicados, funcionan y se entienden en 30 segundos.
- Respondes con ejemplos propios a las preguntas de la tabla de entrevistas asistidas por IA.
- Tienes un registro de postulaciones y un plan semanal, y sabes qué canal te da más respuestas.
""",
        "exercises": [
            py("emp-embudo", "Qué canal te da respuestas", "Carrera: búsqueda de empleo",
               "Escribe `tasa_por_canal(postulaciones)`. Recibe una lista de diccionarios con las claves `canal` y `respuesta` (True o False) "
               "y devuelve un diccionario `{canal: porcentaje}` con el porcentaje de postulaciones con respuesta, redondeado a 1 decimal.",
               starter="""
def tasa_por_canal(postulaciones):
    resultado = {}
    # cuenta envíos y respuestas por canal
    return resultado
""",
               solution="""
def tasa_por_canal(postulaciones):
    enviados = {}
    respuestas = {}
    for p in postulaciones:
        canal = p["canal"]
        enviados[canal] = enviados.get(canal, 0) + 1
        if p["respuesta"]:
            respuestas[canal] = respuestas.get(canal, 0) + 1
    return {canal: round(100 * respuestas.get(canal, 0) / n, 1) for canal, n in enviados.items()}
""",
               tests="""
datos = [
    {"canal": "linkedin", "respuesta": False}, {"canal": "linkedin", "respuesta": False},
    {"canal": "linkedin", "respuesta": True}, {"canal": "directo", "respuesta": True},
    {"canal": "directo", "respuesta": False}, {"canal": "portal", "respuesta": False},
]
r = tasa_por_canal(datos)
assert r == {"linkedin": 33.3, "directo": 50.0, "portal": 0.0}, "Resultado obtenido: %s" % r
assert tasa_por_canal([]) == {}, "Sin postulaciones, diccionario vacio"
""",
               hint="Usa dos diccionarios (enviados y respuestas) con .get(canal, 0) + 1."),
            quiz("emp-ia-quiz-portafolio", "El portafolio que más pesa", "Carrera: búsqueda de empleo",
                 "Para un puesto de AI engineer junior, ¿qué portafolio es más convincente?",
                 ["10 repositorios de cursos sin README", "Un chatbot RAG desplegado con fuentes citadas, README con arquitectura y una evaluación de 30 preguntas",
                  "Una lista de 15 certificados", "Un repositorio privado con el mejor código"], 1,
                 "Una demo que se puede probar, explicada y medida demuestra que ya haces el trabajo. Los certificados y repositorios de cursos no lo demuestran."),
            quiz("emp-ia-quiz-alucinaciones", "Pregunta de entrevista: alucinaciones", "Carrera: búsqueda de empleo",
                 "\"¿Cómo reducirías las alucinaciones del asistente de soporte de una empresa?\" ¿Qué respuesta es la más completa?",
                 ["Subiendo la temperatura", "Usando el modelo más grande disponible",
                  "RAG con los documentos de la empresa y citas, instrucciones para responder \"no lo sé\" sin contexto, y un conjunto de evaluación para medir la mejora",
                  "Pidiéndole al modelo que no invente"], 2,
                 "La clave es combinar contexto verificable (RAG con citas), instrucciones claras y medición: sin evaluación no sabes si mejoró."),
            quiz("emp-ia-quiz-mensaje", "Mensaje directo a una startup", "Carrera: búsqueda de empleo",
                 "¿Cuál mensaje a la fundadora de una startup tiene más probabilidad de respuesta?",
                 ["\"Hola, busco empleo, ¿tienen vacantes?\"", "Mi CV adjunto sin texto",
                  "\"Hola Ana, vi que automatizan facturas para pymes. Construí un sistema que extrae y valida facturas con IA (demo: enlace). ¿Podríamos hablar 15 minutos?\"",
                  "Un mensaje largo con toda mi historia académica"], 2,
                 "Corto, específico sobre su empresa, con una prueba de que puedes aportar y una petición pequeña y concreta."),
            quiz("emp-ia-quiz-asistida", "Entrevista asistida por IA", "Carrera: búsqueda de empleo",
                 "En una entrevista con un agente de IA, el agente genera en segundos una solución que parece funcionar. ¿Qué hace un buen candidato?",
                 ["La acepta enseguida para ahorrar tiempo", "Lee el diff explicando qué hace, pide o escribe pruebas para los casos borde y corrige lo que no entiende o está mal",
                  "Pide al agente que la vuelva a generar hasta que se vea más corta", "Dice que prefiere no usar IA"], 1,
                 "Lo que se evalúa es tu criterio: revisar, probar y poder explicar cada línea. Aceptar sin revisar es justo la señal que intentan detectar."),
            quiz("emp-ia-quiz-produccion", "Un agente rompió producción", "Carrera: búsqueda de empleo",
                 "Un cambio generado por un agente y fusionado ayer provoca errores en producción. ¿Cuál es el mejor primer paso?",
                 ["Pedirle al agente que lo arregle directamente en producción", "Revertir el cambio para restaurar el servicio y después reproducir el fallo con una prueba",
                  "Esperar a ver si se resuelve solo", "Borrar los registros de error"], 1,
                 "Primero se restaura el servicio (revertir es rápido y seguro). Después se reproduce con una prueba, se corrige y esa prueba evita que vuelva a pasar."),
            checklist("emp-ia-check-semana", "Tu semana de búsqueda", "Carrera: búsqueda de empleo",
                      "Un plan semanal sostenible mientras sigues estudiando.",
                      ["Envío 5-10 postulaciones adaptadas a la oferta", "Escribo 3-5 mensajes directos a startups o agencias",
                       "Publico o comparto algo que construí o aprendí", "Practico un problema de algoritmos y uno de SQL cronometrados",
                       "Actualizo mi registro de postulaciones y reviso qué canal funciona"]),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "algoritmos-entrevistas",
        "phase": "carrera",
        "title": "Algoritmos y estructuras de datos para entrevistas",
        "summary": "Big O, diccionarios, dos punteros, ventana deslizante, pilas y búsqueda binaria: los patrones del live coding.",
        "hours": 14,
        "theory": r"""
# Algoritmos y estructuras de datos para entrevistas

Las empresas grandes siguen filtrando con un ejercicio de programación en vivo (*live coding*); muchas startups lo están cambiando
por entrevistas asistidas por IA (ver el tema de empleo), pero los fundamentos siguen contando: los necesitas para **revisar** lo que
genera un agente y saber si es eficiente. Para un junior no piden algoritmos exóticos: piden **resolver un problema corto con claridad,
explicar lo que haces y saber cuánto cuesta tu solución**. La mayoría de los problemas se resuelven con unos pocos **patrones**.

## 1. Big O: cuánto crece el trabajo

| Notación | Ejemplo | Con 1 000 000 de datos |
|---|---|---|
| O(1) | buscar en un `dict` o `set` | instantáneo |
| O(log n) | búsqueda binaria | ~20 pasos |
| O(n) | recorrer una lista una vez | un millón de pasos |
| O(n log n) | `sorted()` | ~20 millones |
| O(n²) | dos bucles anidados | un billón: demasiado lento |

`x in lista` es O(n); `x in conjunto` es O(1). Cambiar una lista por un `set` o un `dict` es la optimización más común en entrevistas.

## 2. Los patrones

- **Diccionario como memoria** (*hash map*): guardar lo que ya viste para no buscarlo otra vez. Ejemplo: "dos números que suman X".
- **Contar con diccionarios** (`collections.Counter`): frecuencias, anagramas, el primer elemento no repetido.
- **Dos punteros:** un índice al inicio y otro al final de una lista ordenada que se acercan. Palíndromos, pares que suman X.
- **Ventana deslizante:** mantener la suma o el conteo de un tramo y moverlo un paso, en vez de recalcular todo. Máxima suma de k elementos seguidos.
- **Pila** (una lista con `append` y `pop`): lo último que entra es lo primero que sale. Paréntesis balanceados, deshacer, navegación.
- **Búsqueda binaria:** en datos **ordenados**, descarta la mitad en cada paso.

## 3. Cómo resolver un problema en vivo

1. **Repite el problema con tus palabras** y pregunta por los casos borde (¿lista vacía?, ¿negativos?, ¿duplicados?).
2. Propón primero la solución **simple** (aunque sea O(n²)) y di su costo.
3. Mejórala con un patrón y explica por qué es mejor.
4. Escribe código claro, con nombres que se entiendan, **pensando en voz alta**.
5. Pruébalo a mano con un ejemplo pequeño y con un caso borde.

El entrevistador evalúa tu **razonamiento y comunicación** tanto como el resultado. Callarse 10 minutos es peor que equivocarse en voz alta.

## 4. Cómo practicar

Un problema al día, cronometrado (20-30 minutos), primero en papel o sin autocompletado. Cuando no salga, estudia la solución,
identifica el patrón y repite el problema dos días después sin mirarla. Plataformas como NeetCode o LeetCode agrupan los problemas por patrón.

## Cómo sabes que dominas este tema

- Reconoces qué patrón usar en un problema nuevo y dices su Big O.
- Resuelves los ejercicios de abajo en menos de 20 minutos cada uno, explicándolos en voz alta.
""",
        "exercises": [
            py("alg-dos-suma", "Dos números que suman un objetivo", "Carrera: algoritmos",
               "Escribe `dos_suma(nums, objetivo)` que devuelva una tupla `(i, j)` con `i < j` tales que `nums[i] + nums[j] == objetivo`, "
               "o `None` si no existen. Debe ser **O(n)**: recorre la lista una sola vez guardando en un diccionario lo que ya viste.",
               starter="""
def dos_suma(nums, objetivo):
    vistos = {}  # valor -> índice
    # recorre nums una sola vez
    return None
""",
               solution="""
def dos_suma(nums, objetivo):
    vistos = {}
    for j, n in enumerate(nums):
        falta = objetivo - n
        if falta in vistos:
            return (vistos[falta], j)
        vistos[n] = j
    return None
""",
               tests="""
assert dos_suma([2, 7, 11, 15], 9) == (0, 1), "2 + 7 = 9"
assert dos_suma([3, 2, 4], 6) == (1, 2), "2 + 4 = 6 (no uses el mismo elemento dos veces)"
assert dos_suma([3, 3], 6) == (0, 1), "Valores repetidos"
assert dos_suma([1, 2, 3], 100) is None, "Sin solucion devuelve None"
grande = list(range(200000))
assert dos_suma(grande, 399997) == (199998, 199999), "Debe ser rapido con muchos datos"
""",
               hint="Para cada número calcula lo que le falta (objetivo - n) y pregunta si ya está en el diccionario."),
            py("alg-no-repetido", "Primer carácter no repetido", "Carrera: algoritmos",
               "Escribe `primer_unico(texto)` que devuelva el primer carácter que aparece **una sola vez** en el texto, o `None` si no hay ninguno. "
               "Cuenta primero las frecuencias y luego recorre el texto.",
               starter="""
def primer_unico(texto):
    # 1) cuenta cuántas veces aparece cada carácter
    # 2) devuelve el primero que aparece una vez
    return None
""",
               solution="""
from collections import Counter

def primer_unico(texto):
    conteo = Counter(texto)
    for c in texto:
        if conteo[c] == 1:
            return c
    return None
""",
               tests="""
assert primer_unico("programacion") == "p", "En 'programacion' la p aparece una vez"
assert primer_unico("aabbcdc") == "d", "a, b y c se repiten"
assert primer_unico("aabb") is None, "Todos se repiten"
assert primer_unico("") is None, "Texto vacio"
""",
               hint="collections.Counter(texto) te da las frecuencias en O(n)."),
            py("alg-parentesis", "Paréntesis balanceados", "Carrera: algoritmos",
               "Escribe `balanceado(s)` que devuelva `True` si los paréntesis `()`, corchetes `[]` y llaves `{}` de `s` están bien cerrados "
               "y en el orden correcto, y `False` si no. Ignora cualquier otro carácter. Usa una **pila**.",
               starter="""
def balanceado(s):
    pila = []
    pares = {")": "(", "]": "[", "}": "{"}
    # recorre s
    return None
""",
               solution="""
def balanceado(s):
    pila = []
    pares = {")": "(", "]": "[", "}": "{"}
    for c in s:
        if c in "([{":
            pila.append(c)
        elif c in pares:
            if not pila or pila.pop() != pares[c]:
                return False
    return not pila
""",
               tests="""
assert balanceado("print(lista[0]) {ok}") is True, "Bien cerrado"
assert balanceado("([)]") is False, "Orden incorrecto"
assert balanceado("((") is False, "Quedan abiertos"
assert balanceado("())") is False, "Cierre sin apertura"
assert balanceado("") is True, "Vacio esta balanceado"
""",
               hint="Al abrir, append. Al cerrar, la pila no puede estar vacía y el pop debe ser el par correspondiente. Al final, la pila debe quedar vacía."),
            py("alg-ventana", "Máxima suma de k elementos seguidos", "Carrera: algoritmos",
               "Escribe `max_suma_ventana(nums, k)` que devuelva la mayor suma de `k` elementos **consecutivos**, o `None` si `k` es menor que 1 "
               "o mayor que la longitud de la lista. Debe ser **O(n)**: calcula la primera ventana y luego, en cada paso, suma el que entra y resta el que sale.",
               starter="""
def max_suma_ventana(nums, k):
    # valida k, calcula la primera ventana y deslízala
    return None
""",
               solution="""
def max_suma_ventana(nums, k):
    if k < 1 or k > len(nums):
        return None
    actual = sum(nums[:k])
    mejor = actual
    for i in range(k, len(nums)):
        actual += nums[i] - nums[i - k]
        mejor = max(mejor, actual)
    return mejor
""",
               tests="""
assert max_suma_ventana([2, 1, 5, 1, 3, 2], 3) == 9, "5 + 1 + 3 = 9"
assert max_suma_ventana([-3, -1, -2], 2) == -3, "Con negativos: -1 + -2 = -3"
assert max_suma_ventana([4], 1) == 4, "Un solo elemento"
assert max_suma_ventana([1, 2], 3) is None, "k mayor que la lista"
assert max_suma_ventana([1, 2], 0) is None, "k menor que 1"
grande = list(range(300000))
assert max_suma_ventana(grande, 1000) == sum(range(299000, 300000)), "Debe ser rapido con muchos datos"
""",
               hint="actual += nums[i] - nums[i - k] mueve la ventana un paso sin volver a sumar todo."),
            py("alg-binaria", "Búsqueda binaria", "Carrera: algoritmos",
               "Escribe `busqueda_binaria(lista, x)` que devuelva el índice de `x` en una lista **ordenada**, o `-1` si no está. "
               "Debe ser O(log n): las pruebas cuentan cuántas veces lees la lista y no se aceptan más de 25 lecturas en un millón de elementos.",
               starter="""
def busqueda_binaria(lista, x):
    izq, der = 0, len(lista) - 1
    # mientras quede rango, mira el centro y descarta una mitad
    return None
""",
               solution="""
def busqueda_binaria(lista, x):
    izq, der = 0, len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        valor = lista[medio]
        if valor == x:
            return medio
        if valor < x:
            izq = medio + 1
        else:
            der = medio - 1
    return -1
""",
               tests="""
class Contada(list):
    lecturas = 0
    def __getitem__(self, i):
        Contada.lecturas += 1
        return list.__getitem__(self, i)

assert busqueda_binaria([1, 3, 5, 7, 9], 7) == 3, "7 esta en el indice 3"
assert busqueda_binaria([1, 3, 5, 7, 9], 4) == -1, "4 no esta"
assert busqueda_binaria([], 1) == -1, "Lista vacia"
datos = Contada(range(0, 2000000, 2))
assert busqueda_binaria(datos, 1234568) == 617284, "Indice incorrecto en la lista grande"
assert Contada.lecturas <= 25, "Demasiadas lecturas (%d): no es O(log n)" % Contada.lecturas
""",
               hint="medio = (izq + der) // 2. Si el valor del medio es menor que x, busca a la derecha (izq = medio + 1); si no, a la izquierda."),
            quiz("alg-quiz-bigo", "Elegir la estructura", "Carrera: algoritmos",
                 "Tienes que comprobar 100 000 veces si un correo está en una lista de 1 000 000 de correos bloqueados. ¿Qué haces?",
                 ["Uso `correo in lista` cada vez", "Ordeno la lista antes de cada comprobación",
                  "Convierto la lista en un `set` una vez y compruebo `correo in bloqueados`", "Recorro la lista con un for y un if"], 2,
                 "Crear el set cuesta O(n) una vez; después cada comprobación es O(1). Con la lista serían 100 000 × 1 000 000 operaciones."),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "ingles-tecnico",
        "phase": "carrera",
        "title": "Inglés técnico para trabajar en remoto",
        "summary": "Un plan práctico para leer, escribir y hablar de tu trabajo en inglés: la habilidad que más multiplica tus opciones.",
        "hours": 8,
        "theory": r"""
# Inglés técnico para trabajar en remoto

Desde Venezuela, el mercado más grande para ti es el remoto internacional, y ahí el inglés decide **antes** que cualquier tecnología:
una oferta en inglés suele pagar más y tener menos competencia hispanohablante. No necesitas un inglés perfecto; necesitas
**poder hacer tu trabajo en inglés**.

> La práctica diaria está en la sección **[Inglés](/ingles)** de la plataforma: prueba de nivel, unidades de entrevistas, clientes,
> trabajo en equipo e inglés técnico con escucha, dictado y ejercicios para hablar, y vocabulario con repaso espaciado.
> Este tema es el plan; esa sección, el gimnasio.

## 1. Las tres habilidades, por orden de prioridad

1. **Leer** documentación, issues y ofertas sin traductor. Ya lo haces a medias: lee la documentación oficial en inglés (FastAPI, React, Anthropic).
2. **Escribir** mensajes claros: un README, un mensaje en Slack, un commit, una propuesta. Frases cortas, sin miedo.
3. **Hablar** de tu trabajo: presentarte, explicar un proyecto y responder preguntas en una entrevista.

## 2. Un plan semanal realista (30-45 minutos al día)

- **Lectura:** la documentación de lo que estés estudiando, siempre en inglés.
- **Escucha:** charlas técnicas o podcasts en inglés con subtítulos en inglés (no en español).
- **Escritura:** escribe en inglés los README y los mensajes de commit de tus proyectos.
- **Habla:** grábate 2 minutos explicando un proyecto y escúchate. Practica la conversación con un asistente de IA o con otra persona
  y pide que te corrija.

## 3. Lo que tienes que poder decir de memoria

- **Tu presentación** (*elevator pitch*) en 30-60 segundos: quién eres, qué construyes, un proyecto y qué buscas.
- **Tu proyecto principal**: *"I built a document processing system that classifies invoices, extracts the data with an LLM and flags
  the ones that need human review. The main challenge was..."*
- **Frases útiles:** *"Could you repeat that, please?"*, *"Let me think out loud"*, *"Just to make sure I understand, you mean..."*,
  *"I haven't used that, but I've worked with something similar..."*.

## 4. Falsos amigos que confunden en el trabajo

| Inglés | Significa | No significa |
|---|---|---|
| *actually* | en realidad | actualmente (*currently*) |
| *eventually* | al final, con el tiempo | eventualmente (*occasionally*) |
| *library* | biblioteca (de código) | librería (*bookstore*) |
| *to realize* | darse cuenta | realizar (*to carry out*) |
| *issue* | problema, incidencia | edición (de una revista) |

## Cómo sabes que dominas este tema

- Lees la documentación en inglés sin traductor.
- Puedes presentarte y explicar tu proyecto principal durante 2 minutos, en inglés, sin leer.
""",
        "exercises": [
            quiz("en-quiz-actually", "Falso amigo: actually", "Carrera: inglés técnico",
                 "En una reunión dicen: *\"Actually, the bug was in the frontend.\"* ¿Qué significa?",
                 ["Actualmente, el error está en el frontend", "En realidad, el error estaba en el frontend",
                  "Eventualmente, el error estará en el frontend", "El error actual es del frontend"], 1,
                 "*Actually* = en realidad / de hecho. Para \"actualmente\" se dice *currently*."),
            quiz("en-quiz-eventually", "Falso amigo: eventually", "Carrera: inglés técnico",
                 "El cliente escribe: *\"We will eventually migrate to the new API.\"* ¿Qué quiere decir?",
                 ["Que quizá migren alguna vez, sin seguridad", "Que al final (con el tiempo) migrarán a la nueva API",
                  "Que migrarán de vez en cuando", "Que ya migraron"], 1,
                 "*Eventually* = al final, tarde o temprano. \"De vez en cuando\" sería *occasionally*."),
            quiz("en-quiz-walk", "Entender la pregunta", "Carrera: inglés técnico",
                 "En una entrevista te dicen: *\"Could you walk me through your project?\"* ¿Qué te piden?",
                 ["Que les enseñes la oficina", "Que expliques tu proyecto paso a paso",
                  "Que camines mientras hablas", "Que les envíes el proyecto por correo"], 1,
                 "*To walk someone through something* = explicarle algo paso a paso. Es de las preguntas más frecuentes: prepárala de memoria."),
            checklist("en-check-pitch", "Tu presentación en inglés", "Carrera: inglés técnico",
                      "Prepara y practica lo que vas a decir en cualquier entrevista en inglés.",
                      ["Escribí mi presentación de 30-60 segundos en inglés", "Escribí la explicación de mi proyecto principal (problema, solución, reto, resultado)",
                       "Me grabé diciéndolas sin leer y me escuché", "Practiqué 3 preguntas típicas de entrevista con alguien o con un asistente de IA",
                       "Mis README y commits están en inglés"]),
            checklist("en-check-rutina", "Tu rutina de inglés", "Carrera: inglés técnico",
                      "Hábitos semanales para mejorar sin dejar de estudiar lo técnico.",
                      ["Leo la documentación de lo que estudio en inglés", "Veo o escucho contenido técnico en inglés con subtítulos en inglés",
                       "Escribo algo en inglés cada día (commit, README, mensaje)", "Hablo en inglés al menos 2 veces por semana, aunque sea grabándome"]),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "leer-depurar-codigo",
        "phase": "producto",
        "title": "Leer, depurar y revisar código (también el generado por IA)",
        "summary": "Leer un traceback, reproducir un fallo, aislarlo y corregirlo, y revisar con criterio el código que escribe un asistente.",
        "hours": 8,
        "theory": r"""
# Leer, depurar y revisar código (también el generado por IA)

Escribir código es cada vez más barato: un asistente lo genera en segundos. Lo difícil, y lo que más se valora, es **leer** código que
no escribiste, **encontrar por qué falla** y **decidir si un cambio es correcto**. En tu primer empleo pasarás más tiempo leyendo y
depurando que escribiendo desde cero, y en una entrevista asistida por IA es exactamente lo que evalúan.

## 1. Leer un traceback (de abajo arriba)

```
Traceback (most recent call last):
  File "app.py", line 12, in <module>
    registrar(datos)
  File "app.py", line 5, in registrar
    correo = usuario["email"]
KeyError: 'email'
```

1. **La última línea** dice qué pasó: `KeyError: 'email'` → el diccionario no tiene esa clave.
2. **La línea anterior** dice dónde: `app.py`, línea 5, dentro de `registrar`.
3. **Hacia arriba** ves quién llamó a quién. El error suele estar en tu código, no en la librería: busca la última línea que sea tuya.

## 2. El método para depurar

1. **Reproduce** el fallo con el caso más pequeño posible. Si no lo reproduces, no sabes si lo arreglaste.
2. **Formula una hipótesis** ("la página empieza en 0 y no en 1") en vez de cambiar cosas al azar.
3. **Comprueba** con datos: `print()` de las variables clave, `breakpoint()` para pausar y explorar, o el depurador del editor.
4. **Aísla:** si no sabes dónde está, divide. Comenta la mitad, prueba con datos más simples o usa `git bisect` para encontrar el commit que lo rompió.
5. **Corrige y escribe una prueba** que habría detectado el error, para que no vuelva.

## 3. Errores clásicos que verás una y otra vez

| Error | Síntoma |
|---|---|
| Fuera por uno (*off-by-one*) | Falta o sobra el primer o el último elemento; la página 1 muestra la 2 |
| Argumento por defecto mutable (`def f(x, lista=[])`) | Los datos de una llamada "aparecen" en la siguiente |
| Modificar una lista mientras la recorres | Se saltan elementos sin ningún error |
| Casos borde no tratados | Falla con lista vacía, `0`, negativos, `None` o texto vacío |
| Errores de tipeo que son válidos | `total =+ p` (asigna `+p`) en vez de `total += p` |

## 4. Revisar código generado por IA

El código de un asistente **suele funcionar en el caso feliz** y fallar en los bordes. Revisa siempre:

- ¿Hace **exactamente** lo que se pidió? ¿Inventó requisitos o se saltó alguno?
- **Casos borde**: vacío, cero, negativos, duplicados, `None`, textos con espacios o mayúsculas.
- **Seguridad**: consultas SQL armadas con f-strings, secretos en el código, entradas sin validar.
- **Dependencias**: ¿existe de verdad ese paquete? ¿hacía falta?
- ¿Lo podrías **explicar** línea por línea? Si no, todavía no es tuyo.

## 5. Requisitos vagos

Muchos "bugs" son malentendidos. Ante un requisito vago ("que el reporte salga bien") pregunta por un ejemplo concreto de entrada y
salida esperada antes de escribir código.

## Cómo sabes que dominas este tema

- Encuentras la línea y la causa de un error leyendo su traceback.
- Corriges los ejercicios de abajo explicando qué estaba mal y qué prueba lo habría detectado.
""",
        "exercises": [
            py("dep-default", "El carrito que recuerda demasiado", "Sistemas: depuración y revisión",
               "Esta función debería crear un carrito nuevo en cada llamada si no se le pasa uno, pero los productos de una llamada aparecen en la siguiente. "
               "Encuentra el error y corrígelo sin cambiar cómo se usa la función.",
               starter="""
def agregar(producto, carrito=[]):
    carrito.append(producto)
    return carrito
""",
               solution="""
def agregar(producto, carrito=None):
    if carrito is None:
        carrito = []
    carrito.append(producto)
    return carrito
""",
               tests="""
a = agregar("pan")
b = agregar("leche")
assert a == ["pan"], "La primera llamada debe devolver solo ['pan']"
assert b == ["leche"], "Cada llamada sin carrito debe empezar vacia, obtuve %s" % b
assert agregar("cafe", ["azucar"]) == ["azucar", "cafe"], "Con un carrito dado, se agrega al final"
""",
               hint="El valor por defecto `[]` se crea una sola vez, al definir la función, y se comparte entre llamadas. Usa None como valor por defecto."),
            py("dep-ultimos", "Los últimos n elementos", "Sistemas: depuración y revisión",
               "`ultimos(lista, n)` debe devolver los últimos `n` elementos, y una lista vacía si `n` es 0 o negativo. Funciona casi siempre... "
               "Encuentra el caso que falla y corrígelo.",
               starter="""
def ultimos(lista, n):
    return lista[-n:]
""",
               solution="""
def ultimos(lista, n):
    if n <= 0:
        return []
    return lista[-n:]
""",
               tests="""
assert ultimos([1, 2, 3, 4], 2) == [3, 4], "Los dos ultimos"
assert ultimos([1, 2], 5) == [1, 2], "Si n es mayor que la lista, toda la lista"
assert ultimos([1, 2, 3], 0) == [], "Con n = 0 debe devolver [] (lista[-0:] es lista[0:], toda la lista)"
assert ultimos([1, 2, 3], -1) == [], "Con n negativo, []"
""",
               hint="Prueba a mano `[1, 2, 3][-0:]`. ¿Qué devuelve?"),
            py("dep-negativos", "Quitar negativos (sin saltarse ninguno)", "Sistemas: depuración y revisión",
               "`quitar_negativos(numeros)` debe devolver una lista **nueva** sin los negativos y **sin modificar** la original. "
               "Con dos negativos seguidos, uno se escapa. Corrígela.",
               starter="""
def quitar_negativos(numeros):
    for n in numeros:
        if n < 0:
            numeros.remove(n)
    return numeros
""",
               solution="""
def quitar_negativos(numeros):
    return [n for n in numeros if n >= 0]
""",
               tests="""
datos = [1, -2, -3, 4, -5]
r = quitar_negativos(datos)
assert r == [1, 4], "Resultado esperado [1, 4], obtuve %s" % r
assert datos == [1, -2, -3, 4, -5], "No debe modificar la lista original"
assert quitar_negativos([]) == [], "Lista vacia"
""",
               hint="Al borrar un elemento mientras recorres la lista, los siguientes se desplazan y el bucle se salta uno. Construye una lista nueva."),
            py("dep-paginar", "La paginación que escribió el asistente", "Sistemas: depuración y revisión",
               "Un asistente generó esta función. Según su documentación, `pagina` empieza en **1**, pero la página 1 muestra los elementos de la 2. "
               "Corrígela y haz que lance `ValueError` si `pagina` o `por_pagina` son menores que 1.",
               starter="""
def paginar(items, pagina, por_pagina):
    \"\"\"Devuelve los elementos de la página indicada. La primera página es la 1.\"\"\"
    inicio = pagina * por_pagina
    return items[inicio:inicio + por_pagina]
""",
               solution="""
def paginar(items, pagina, por_pagina):
    \"\"\"Devuelve los elementos de la página indicada. La primera página es la 1.\"\"\"
    if pagina < 1 or por_pagina < 1:
        raise ValueError("pagina y por_pagina deben ser 1 o mayores")
    inicio = (pagina - 1) * por_pagina
    return items[inicio:inicio + por_pagina]
""",
               tests="""
datos = list(range(10))
assert paginar(datos, 1, 3) == [0, 1, 2], "La pagina 1 debe empezar en el primer elemento"
assert paginar(datos, 4, 3) == [9], "La ultima pagina puede estar incompleta"
assert paginar(datos, 5, 3) == [], "Una pagina que no existe devuelve []"
for args in ((0, 3), (1, 0), (-1, 3)):
    try:
        paginar(datos, *args)
    except ValueError:
        pass
    else:
        raise AssertionError("paginar(datos, %s, %s) debe lanzar ValueError" % args)
""",
               hint="Si la primera página es la 1, su inicio debe ser 0."),
            py("dep-total", "Dos errores en el total", "Sistemas: depuración y revisión",
               "`total_con_descuento(precios, cupon=None)` suma los precios y, con el cupón `\"DESC10\"`, aplica un **10 % de descuento**. "
               "Tiene **dos** errores. Encuéntralos y corrígelos.",
               starter="""
def total_con_descuento(precios, cupon=None):
    total = 0
    for p in precios:
        total =+ p
    if cupon == "DESC10":
        total = total * 0.10
    return round(total, 2)
""",
               solution="""
def total_con_descuento(precios, cupon=None):
    total = 0
    for p in precios:
        total += p
    if cupon == "DESC10":
        total = total * 0.90
    return round(total, 2)
""",
               tests="""
assert total_con_descuento([10, 20, 5]) == 35, "Sin cupon: 10 + 20 + 5 = 35"
assert total_con_descuento([10, 20], "DESC10") == 27.0, "30 con 10 % de descuento = 27"
assert total_con_descuento([], "DESC10") == 0, "Sin productos, 0"
assert total_con_descuento([10], "OTRO") == 10, "Un cupon desconocido no cambia nada"
""",
               hint="Mira con lupa el operador dentro del bucle. Y un descuento del 10 % deja el 90 % del precio."),
            quiz("dep-quiz-traceback", "Leer un traceback", "Sistemas: depuración y revisión",
                 "Un traceback termina en `File \"pedidos.py\", line 18, in calcular_envio` / `peso = pedido[\"peso_kg\"]` / `KeyError: 'peso_kg'`. ¿Qué indica?",
                 ["Que Python no está bien instalado", "Que en la línea 18 de pedidos.py el diccionario `pedido` no tiene la clave 'peso_kg'",
                  "Que la variable peso no existe", "Que el error está en la primera línea del traceback"], 1,
                 "La última línea dice qué pasó (KeyError: falta la clave) y la anterior, dónde. Después, averigua por qué ese pedido llega sin peso."),
            quiz("dep-quiz-revision", "Revisar código de un asistente", "Sistemas: depuración y revisión",
                 "Un asistente propone `cur.execute(f\"SELECT * FROM usuarios WHERE email = '{email}'\")` y las pruebas pasan. ¿Qué haces?",
                 ["Lo acepto: las pruebas pasan", "Lo rechazo y pido una consulta parametrizada (`WHERE email = %s` con el valor aparte): permite inyección SQL",
                  "Solo cambio las comillas simples por dobles", "Añado un comentario explicando la consulta"], 1,
                 "Que las pruebas pasen no significa que sea seguro. Armar SQL con f-strings permite inyección: los valores siempre van como parámetros."),
            checklist("dep-check-metodo", "Tu método de depuración", "Sistemas: depuración y revisión",
                      "Aplícalo la próxima vez que algo falle en tus proyectos.",
                      ["Reproduje el fallo con el caso más pequeño posible", "Leí el traceback de abajo arriba y encontré la última línea de mi código",
                       "Formulé una hipótesis antes de cambiar nada", "Comprobé la hipótesis con print, breakpoint() o el depurador",
                       "Escribí una prueba que falla sin la corrección y pasa con ella", "Puedo explicar la causa en una frase"]),
        ],
    },
]
