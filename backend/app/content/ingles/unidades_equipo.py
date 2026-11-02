from ._helpers import choice, dictation, fill, listen, speak, translate

UNITS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-team-1",
        "level": "A2",
        "focus": "equipo",
        "title": "The daily standup",
        "summary": "Contar en 30 segundos qué hiciste ayer, qué harás hoy y qué te bloquea.",
        "minutes": 30,
        "lesson": r"""
# The daily standup

En muchos equipos remotos hay una reunión corta cada mañana (*standup*). Cada persona responde tres preguntas en 30-60 segundos.
Es la situación de inglés **más repetida** de tu futuro trabajo, así que conviene dominarla de memoria.

## Las tres partes

| Pregunta | Tiempo verbal | Ejemplo |
|---|---|---|
| ¿Qué hiciste ayer? | Pasado simple | *Yesterday I **finished** the login page and **fixed** a bug in the API.* |
| ¿Qué harás hoy? | *going to* | *Today I'm **going to** write the tests for the payment endpoint.* |
| ¿Algo te bloquea? | *blocked by / need* | *I'm **blocked by** the database access. I **need** the credentials.* |

Si no hay bloqueos: *"No blockers."* o *"Nothing blocking me right now."*

## Pasado simple: regulares e irregulares

- Regulares terminan en **-ed**: *fixed, finished, updated, deployed, tested*.
- Irregulares frecuentes en el trabajo: *write → wrote, build → built, make → made, do → did, have → had, meet → met*.

## Pronunciación del -ed

- Suena **/t/** después de sonidos sordos: *fixed* ("fikst"), *finished*, *pushed*.
- Suena **/d/** en la mayoría: *deployed, called, reviewed*.
- Suena **/id/** solo después de **t** o **d**: *tested* ("TES-tid"), *updated*, *added*.

## Frases útiles

- *"I'm still working on..."* (sigo trabajando en...)
- *"It's taking longer than expected."*
- *"Could someone help me with...?"*
""",
        "phrases": [
            ("Yesterday I finished the login page and fixed a bug in the API.", "Ayer terminé la página de inicio de sesión y arreglé un error en la API."),
            ("Today I'm going to write the tests for the payment endpoint.", "Hoy voy a escribir las pruebas del endpoint de pagos."),
            ("I'm blocked by the database access. I need the credentials.", "Estoy bloqueado por el acceso a la base de datos. Necesito las credenciales."),
            ("No blockers.", "Sin bloqueos."),
            ("I'm still working on the dashboard. It's taking longer than expected.", "Sigo trabajando en el dashboard. Está tardando más de lo esperado."),
            ("Could someone help me with the deployment?", "¿Alguien podría ayudarme con el despliegue?"),
        ],
        "exercises": [
            listen("team1-listen-1",
                   "Yesterday I updated the user model and reviewed Ana's pull request. "
                   "Today I'm going to work on the email notifications. No blockers.",
                   "¿Qué va a hacer hoy esta persona?",
                   ["Revisar un pull request", "Trabajar en las notificaciones por correo", "Actualizar el modelo de usuario", "Nada, está bloqueada"], 1,
                   "*Today I'm going to work on the email notifications.*"),
            listen("team1-listen-2",
                   "I'm still working on the report. It's taking longer than expected because the data has a lot of duplicates. "
                   "I'm blocked by the access to the production database.",
                   "¿Qué bloquea a esta persona?",
                   ["Los duplicados", "El acceso a la base de datos de producción", "El informe", "Una reunión"], 1,
                   "*I'm blocked by...* = estoy bloqueado por..."),
            fill("team1-fill-1", "Yesterday I ___ a bug in the payment API.", ["fixed", "solved"],
                 "Ayer arreglé un error en la API de pagos.",
                 "Pasado simple regular: *fix → fixed*."),
            fill("team1-fill-2", "Today I'm ___ to write the tests.", ["going"],
                 "Hoy voy a escribir las pruebas.", "*be going to + verbo* = planes: *I'm going to write*."),
            choice("team1-choice-1", "¿Cuál es el pasado de *write*?", ["writed", "wrote", "written", "writing"], 1,
                   "*write → wrote → written*. En el standup: *Yesterday I wrote the documentation.*"),
            translate("team1-tr-1", "Sigo trabajando en el dashboard.",
                      ["I'm still working on the dashboard.", "I am still working on the dashboard."],
                      "*still* (todavía/sigo) va entre *am* y el verbo en -ing."),
            dictation("team1-dict-1", "Today I'm going to write the tests for the payment endpoint.",
                      "Hoy voy a escribir las pruebas del endpoint de pagos."),
            speak("team1-speak-1", "Lee en voz alta (cuida el sonido de *finished* y *fixed*).",
                  "Yesterday I finished the login page and fixed a bug in the API."),
            speak("team1-speak-2", "Di en inglés: «Está tardando más de lo esperado».", "It's taking longer than expected.",
                  ["It is taking longer than I expected."], show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-team-2",
        "level": "B1",
        "focus": "equipo",
        "title": "Slack and async messages",
        "summary": "Mensajes escritos claros: actualizar el estado, pedir ayuda bien y entender las abreviaturas del equipo.",
        "minutes": 35,
        "lesson": r"""
# Slack and async messages

En un equipo remoto, **escribes mucho más de lo que hablas**. Un buen mensaje se entiende sin contexto y sin una reunión.

## Pedir ayuda bien (sin hacer perder tiempo)

Malo: *"Hi"* ... (y esperar respuesta). Bueno, todo en un mensaje:

> *Hi Tom, quick question about the payments API. I'm getting a 401 error when I call `/refunds` from staging.
> I already checked the API key and the headers. Do you know if staging needs a different token? Thanks!*

Estructura: **contexto → qué pasa → qué ya probaste → pregunta concreta**.

## Actualizar el estado

> *Heads up: the deployment is delayed. The migration failed on staging. I'm looking into it, ETA 3 pm.*

## Abreviaturas que verás a diario

| Abreviatura | Significa |
|---|---|
| FYI | *For your information* — para tu información |
| ETA | *Estimated time of arrival* — hora estimada |
| ASAP | *As soon as possible* — lo antes posible |
| PTAL | *Please take a look* — échale un vistazo |
| WFH / OOO | *Working from home / Out of office* |
| LGTM | *Looks good to me* — me parece bien (aprobar un cambio) |

## Expresiones naturales

- *Heads up:* aviso de algo importante.
- *Quick question:* pregunta corta.
- *I'm looking into it.* Lo estoy investigando.
- *I'll get back to you.* Te respondo más tarde.
- *No worries.* No pasa nada.

## Gramática: *already / yet / still*

- *I've **already** checked the logs.* (ya, antes de lo esperado)
- *I haven't deployed it **yet**.* (todavía no, en negativas y preguntas)
- *I'm **still** waiting for access.* (todavía, algo que continúa)
""",
        "phrases": [
            ("Quick question about the payments API.", "Una pregunta rápida sobre la API de pagos."),
            ("I already checked the API key and the headers.", "Ya revisé la clave de la API y las cabeceras."),
            ("Heads up: the deployment is delayed.", "Aviso: el despliegue va con retraso."),
            ("I'm looking into it. I'll get back to you in an hour.", "Lo estoy investigando. Te respondo en una hora."),
            ("I haven't deployed it yet.", "Todavía no lo he desplegado."),
            ("Please take a look when you have a moment.", "Échale un vistazo cuando tengas un momento."),
        ],
        "exercises": [
            listen("team2-listen-1",
                   "Heads up: the deployment is delayed. The database migration failed on staging. "
                   "I'm looking into it, and I'll post an update by three p.m.",
                   "¿Qué falló?",
                   ["El servidor de producción", "La migración de la base de datos en staging", "Las pruebas unitarias", "El inicio de sesión"], 1,
                   "*The database migration failed on staging.*"),
            choice("team2-choice-1", "¿Qué significa *LGTM* en un pull request?",
                   ["Let's go to the meeting", "Looks good to me (lo apruebo)", "Last good test merged", "Let's get the money"], 1,
                   "Se escribe al aprobar un cambio: *LGTM, thanks!*"),
            choice("team2-choice-2", "¿Cuál es la mejor forma de pedir ayuda por Slack?",
                   ["Hi", "Can I ask you something?",
                    "Hi Tom, quick question: I'm getting a 401 on /refunds from staging. I already checked the API key. Does staging need a different token?",
                    "HELP!!! NOTHING WORKS"], 2,
                   "Todo en un mensaje: contexto, qué pasa, qué probaste y una pregunta concreta."),
            fill("team2-fill-1", "I haven't deployed it ___.", ["yet"],
                 "Todavía no lo he desplegado.", "*yet* va al final de frases negativas: *I haven't ... yet*."),
            fill("team2-fill-2", "I've ___ checked the logs, but I can't find the error.", ["already"],
                 "Ya revisé los registros, pero no encuentro el error.", "*already* va entre *have* y el participio."),
            translate("team2-tr-1", "Lo estoy investigando. Te respondo en una hora.",
                      ["I'm looking into it. I'll get back to you in an hour.", "I am looking into it. I will get back to you in an hour.",
                       "I'm looking into it. I'll get back to you in one hour."],
                      "*look into* = investigar. *get back to someone* = responder más tarde."),
            dictation("team2-dict-1", "Heads up: the deployment is delayed.", "Aviso: el despliegue va con retraso."),
            speak("team2-speak-1", "Lee en voz alta.", "Please take a look when you have a moment."),
            speak("team2-speak-2", "Di en inglés: «Todavía estoy esperando el acceso».", "I'm still waiting for access.",
                  ["I'm still waiting for the access.", "I am still waiting for access."], show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-team-3",
        "level": "B2",
        "focus": "equipo",
        "title": "Pull requests and code review",
        "summary": "Escribir descripciones de pull requests y dar o recibir comentarios de revisión con tacto.",
        "minutes": 40,
        "lesson": r"""
# Pull requests and code review

La revisión de código es **comunicación escrita entre colegas**. Un comentario técnicamente correcto pero brusco
genera fricción; uno claro y amable acelera al equipo.

## La descripción de un pull request

```
## What
Adds rate limiting to the /chat endpoint.

## Why
Some users were sending hundreds of requests per minute, which increased our LLM costs.

## How
Uses a token bucket per user (20 requests/minute). Returns 429 when the limit is exceeded.

## Testing
Added unit tests for the limiter and tested manually on staging.
```

## Comentar con tacto

| Brusco | Con tacto |
|---|---|
| This is wrong. | I think this might fail when the list is empty. What do you think? |
| Change this. | **Could we** move this logic to the service layer? |
| Why did you do this? | **I'm curious** about this approach. Could you explain the reasoning? |
| Bad name. | **Nit:** maybe `user_count` would be clearer than `n`. |

- **Nit:** = detalle menor, no bloquea la aprobación.
- *Suggestion:* / *Optional:* = propuesta que el autor puede ignorar.
- *Blocking:* = hay que resolverlo antes de aprobar.

## Recibir comentarios

- *Good catch, thanks! Fixed in the latest commit.*
- *I see what you mean. I went with this approach because..., but I'm open to changing it.*
- *Let's discuss it in a quick call; it might be faster.*

## Vocabulario de revisión

*to merge* (fusionar), *to approve*, *to request changes*, *a conflict*, *to rebase*, *a regression* (algo que funcionaba y dejó de funcionar),
*edge case* (caso borde), *backwards compatible*.
""",
        "phrases": [
            ("This pull request adds rate limiting to the chat endpoint.", "Este pull request añade un límite de peticiones al endpoint del chat."),
            ("I think this might fail when the list is empty. What do you think?", "Creo que esto podría fallar con la lista vacía. ¿Qué opinas?"),
            ("Could we move this logic to the service layer?", "¿Podríamos mover esta lógica a la capa de servicios?"),
            ("Nit: maybe user count would be a clearer name.", "Detalle menor: quizá user count sería un nombre más claro."),
            ("Good catch, thanks! Fixed in the latest commit.", "¡Bien visto, gracias! Corregido en el último commit."),
            ("I went with this approach because it's easier to test.", "Elegí este enfoque porque es más fácil de probar."),
        ],
        "exercises": [
            listen("team3-listen-1",
                   "This looks good overall. I left two comments. The first one is blocking: the endpoint doesn't validate the input. "
                   "The second one is just a nit about a variable name.",
                   "¿Qué comentario hay que resolver antes de aprobar?",
                   ["El nombre de la variable", "La falta de validación de la entrada en el endpoint", "Ninguno", "Los dos son detalles menores"], 1,
                   "*blocking* = bloquea la aprobación. *nit* = detalle menor."),
            choice("team3-choice-1", "¿Qué comentario de revisión es el más adecuado?",
                   ["This is wrong.", "Bad code, rewrite it.",
                    "I think this might fail when the list is empty. Could we add a check?", "Why would anyone do this?"], 2,
                   "Señala el problema concreto, en tono de hipótesis, y propone una solución."),
            choice("team3-choice-2", "Un compañero escribe *\"Nit: rename n to user_count\"*. ¿Qué significa *Nit*?",
                   ["Que es un error grave", "Que es un detalle menor que no bloquea", "Que no le gusta tu código", "Que hay que borrar la variable"], 1,
                   "*Nit* viene de *nitpick* (detalle quisquilloso)."),
            fill("team3-fill-1", "___ we move this logic to the service layer?", ["could", "can", "should", "shall"],
                 "¿Podríamos mover esta lógica a la capa de servicios?",
                 "Las sugerencias en forma de pregunta (*Could we...?*) suenan colaborativas."),
            fill("team3-fill-2", "Good ___, thanks! Fixed in the latest commit.", ["catch"],
                 "¡Bien visto, gracias! Corregido en el último commit.", "*Good catch* = bien visto (cuando alguien encuentra un error)."),
            translate("team3-tr-1", "Elegí este enfoque porque es más fácil de probar.",
                      ["I went with this approach because it's easier to test.", "I chose this approach because it's easier to test.",
                       "I chose this approach because it is easier to test.", "I went with this approach because it is easier to test."],
                      "*go with* = elegir/quedarse con. *easier to test* = más fácil de probar."),
            dictation("team3-dict-1", "I think this might fail when the list is empty.", "Creo que esto podría fallar cuando la lista está vacía."),
            speak("team3-speak-1", "Lee en voz alta.", "Good catch, thanks! Fixed in the latest commit."),
            speak("team3-speak-2", "Di en inglés: «Tengo curiosidad por este enfoque. ¿Podrías explicar el razonamiento?»",
                  "I'm curious about this approach. Could you explain the reasoning?",
                  ["I'm curious about this approach. Can you explain the reasoning?"], show_target=False),
        ],
    },
]
