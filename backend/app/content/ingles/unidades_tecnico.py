from ._helpers import choice, dictation, fill, listen, speak, translate

UNITS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-tech-1",
        "level": "A2",
        "focus": "tecnico",
        "title": "Reading documentation",
        "summary": "Las palabras y estructuras que se repiten en toda documentación técnica: instalar, ejecutar, parámetros y valores de retorno.",
        "minutes": 30,
        "lesson": r"""
# Reading documentation

La documentación en inglés usa un vocabulario **pequeño y muy repetitivo**. Si dominas estas palabras, puedes leer la documentación
de FastAPI, React o de cualquier API de IA sin traductor.

## El imperativo: instrucciones directas

La documentación da órdenes con el verbo en forma base, sin sujeto:
*"**Install** the package. **Run** the server. **Set** the environment variable. **Make sure** the port is free."*

## Vocabulario esencial

| Inglés | Español |
|---|---|
| *install / run / set up* | instalar / ejecutar / configurar |
| *required / optional* | obligatorio / opcional |
| *default (value)* | (valor) por defecto |
| *returns* | devuelve |
| *raises (an error)* | lanza (un error) |
| *deprecated* | obsoleto (dejará de existir) |
| *argument / parameter* | argumento / parámetro |
| *request / response* | petición / respuesta |
| *endpoint* | ruta de una API |
| *rate limit* | límite de peticiones |
| *note / warning* | nota / advertencia |

## Una frase típica, desmontada

> *"`max_tokens` (integer, **required**): the maximum number of tokens to generate **before stopping**."*

- *integer, required* → número entero, obligatorio.
- *the maximum number of...* → el número máximo de...
- *before stopping* → antes de detenerse (después de *before/after* el verbo va en **-ing**).

## Falsos amigos frecuentes

*library* = biblioteca (de código), no librería · *actually* = en realidad · *eventually* = al final, con el tiempo ·
*to support* = ser compatible con (*"This version supports Python 3.12"*), no "soportar".
""",
        "phrases": [
            ("Install the package and run the server.", "Instala el paquete y ejecuta el servidor."),
            ("This parameter is optional. The default value is ten.", "Este parámetro es opcional. El valor por defecto es diez."),
            ("The function returns a list of results.", "La función devuelve una lista de resultados."),
            ("This method is deprecated and will be removed in the next version.", "Este método está obsoleto y se eliminará en la próxima versión."),
            ("Make sure the environment variable is set.", "Asegúrate de que la variable de entorno esté configurada."),
            ("This version supports Python three point twelve.", "Esta versión es compatible con Python 3.12."),
        ],
        "exercises": [
            listen("tech1-listen-1",
                   "To get started, install the package and set your API key as an environment variable. "
                   "Never write the key directly in your code.",
                   "¿Qué advierte la documentación?",
                   ["Instalar la versión más reciente", "Nunca escribir la clave directamente en el código", "Usar otro lenguaje", "Pagar antes de empezar"], 1,
                   "*Never write the key directly in your code.*"),
            choice("tech1-choice-1", "La documentación dice que un método es *deprecated*. ¿Qué significa?",
                   ["Que es el más rápido", "Que está obsoleto y dejará de existir", "Que es obligatorio", "Que es gratuito"], 1,
                   "Si algo es *deprecated*, busca la alternativa recomendada."),
            choice("tech1-choice-2", "*\"This library supports async requests.\"* ¿Qué quiere decir?",
                   ["Que la librería aguanta peticiones", "Que la biblioteca es compatible con peticiones asíncronas",
                    "Que la biblioteca necesita soporte técnico", "Que no admite peticiones"], 1,
                   "*to support* = ser compatible con / admitir. *library* = biblioteca de código."),
            fill("tech1-fill-1", "The function ___ a list of results.", ["returns"],
                 "La función devuelve una lista de resultados.", "*returns* = devuelve (con *it*, lleva -s)."),
            fill("tech1-fill-2", "This parameter is optional. The ___ value is 10.", ["default"],
                 "Este parámetro es opcional. El valor por defecto es 10.", "*default* = por defecto."),
            translate("tech1-tr-1", "Instala el paquete y ejecuta el servidor.",
                      ["Install the package and run the server.", "Install the package and start the server."],
                      "Imperativo: verbo en forma base y sin sujeto."),
            dictation("tech1-dict-1", "Make sure the environment variable is set.",
                      "Asegúrate de que la variable de entorno esté configurada."),
            speak("tech1-speak-1", "Lee en voz alta.", "This method is deprecated and will be removed in the next version."),
            speak("tech1-speak-2", "Di en inglés: «Este parámetro es obligatorio».", "This parameter is required.",
                  ["This parameter is mandatory."], show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-tech-2",
        "level": "B1",
        "focus": "tecnico",
        "title": "Explaining an AI system",
        "summary": "Explicar en inglés cómo funciona un RAG o un agente: la voz pasiva y el vocabulario de IA aplicada.",
        "minutes": 40,
        "lesson": r"""
# Explaining an AI system

En una entrevista de AI engineer o en una llamada con un cliente tendrás que explicar **cómo funciona tu sistema**, paso a paso.
La herramienta gramatical clave es la **voz pasiva**: lo importante es el proceso, no quién lo hace.

## Voz pasiva: *be + participio*

| Activa | Pasiva |
|---|---|
| We split the documents into chunks. | The documents **are split** into chunks. |
| The model generates the answer. | The answer **is generated** by the model. |
| We stored the embeddings in PostgreSQL. | The embeddings **were stored** in PostgreSQL. |

## Un RAG explicado en inglés

> *"First, the documents **are split** into small chunks. Each chunk **is converted** into an embedding and **stored** in a vector database.
> When a user asks a question, the most similar chunks **are retrieved** and **sent** to the model together with the question.
> The model answers using only that context, and the sources **are shown** to the user."*

## Vocabulario de IA aplicada

| Inglés | Español |
|---|---|
| *chunk* | fragmento |
| *embedding* | vector que representa el significado |
| *to retrieve* | recuperar |
| *context window* | ventana de contexto |
| *hallucination* | alucinación (respuesta inventada) |
| *latency* | latencia |
| *accuracy* | precisión, exactitud |
| *tool call* | llamada a una herramienta |
| *evaluation set* | conjunto de evaluación |

## Pronunciación

*retrieve* = ri-**TRIIV** · *accuracy* = **Á**-kiu-ra-si · *latency* = **LEI**-ten-si · *hallucination* = ha-lu-si-**NEI**-shon
""",
        "phrases": [
            ("The documents are split into small chunks.", "Los documentos se dividen en fragmentos pequeños."),
            ("Each chunk is converted into an embedding.", "Cada fragmento se convierte en un embedding."),
            ("The most similar chunks are retrieved and sent to the model.", "Los fragmentos más parecidos se recuperan y se envían al modelo."),
            ("The model answers using only that context.", "El modelo responde usando solo ese contexto."),
            ("We measured the accuracy with an evaluation set of fifty questions.", "Medimos la precisión con un conjunto de evaluación de cincuenta preguntas."),
            ("Citations reduce hallucinations and build trust.", "Las citas reducen las alucinaciones y generan confianza."),
        ],
        "exercises": [
            listen("tech2-listen-1",
                   "When a user asks a question, the most similar chunks are retrieved from the vector database "
                   "and sent to the model together with the question. The sources are shown below the answer.",
                   "¿Qué se envía al modelo junto con la pregunta?",
                   ["Todo el documento", "Los fragmentos más parecidos", "El historial completo del usuario", "Nada más"], 1,
                   "*the most similar chunks are retrieved ... and sent to the model together with the question*"),
            listen("tech2-listen-2",
                   "Our first version was accurate, but the latency was too high, around eight seconds. "
                   "We reduced it to two seconds by using a smaller model for simple questions.",
                   "¿Cómo redujeron la latencia?",
                   ["Con más servidores", "Usando un modelo más pequeño para preguntas simples", "Quitando las citas", "Reduciendo los documentos"], 1, ""),
            fill("tech2-fill-1", "The documents are ___ into small chunks.", ["split", "divided"],
                 "Los documentos se dividen en fragmentos pequeños.",
                 "Pasiva: *are + participio*. *split* es irregular: split → split → split."),
            fill("tech2-fill-2", "The answer is ___ by the model.", ["generated", "produced", "written"],
                 "La respuesta la genera el modelo.", "Pasiva en presente: *is + participio*."),
            choice("tech2-choice-1", "¿Qué es una *hallucination* en un sistema con LLMs?",
                   ["Un error de red", "Una respuesta inventada que parece correcta", "Una respuesta lenta", "Un ataque informático"], 1,
                   "Se reduce con contexto verificable (RAG con citas) y se mide con evaluaciones."),
            translate("tech2-tr-1", "Los fragmentos más parecidos se envían al modelo.",
                      ["The most similar chunks are sent to the model."],
                      "Pasiva: *are sent*. *the most similar* = los más parecidos."),
            dictation("tech2-dict-1", "Each chunk is converted into an embedding.", "Cada fragmento se convierte en un embedding."),
            speak("tech2-speak-1", "Lee en voz alta (cuida *retrieved* y *similar*).",
                  "The most similar chunks are retrieved and sent to the model."),
            speak("tech2-speak-2", "Di en inglés: «Las citas reducen las alucinaciones».", "Citations reduce hallucinations.",
                  ["Citations reduce the hallucinations."], show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-tech-3",
        "level": "B2",
        "focus": "tecnico",
        "title": "Trade-offs and incidents",
        "summary": "Comparar opciones técnicas, justificar decisiones y contar un incidente de producción en inglés.",
        "minutes": 45,
        "lesson": r"""
# Trade-offs and incidents

Lo que distingue a un buen ingeniero en una entrevista o en una reunión es **explicar decisiones**: qué opciones había, qué ganas,
qué pierdes y por qué elegiste una. Y cuando algo falla, contarlo con claridad y sin culpas.

## Hablar de trade-offs

- *"Option A is **faster**, but it's **more expensive**."*
- *"**On the one hand**, a bigger model is more accurate. **On the other hand**, it increases latency and cost."*
- *"**It depends on** the volume. For a few hundred requests a day, a single server is enough."*
- *"I'd go with PostgreSQL **because** we need transactions, **even though** a NoSQL database would scale writes more easily."*

### Comparativos

| Corto (1 sílaba) | Largo |
|---|---|
| fast → **faster** → the **fastest** | expensive → **more** expensive → the **most** expensive |
| cheap → **cheaper** | reliable → **more** reliable |
| Irregulares: good → **better** → the **best** · bad → **worse** → the **worst** |

Error típico: ~~more faster~~ → *faster*.

## Contar un incidente (*postmortem*)

> *"On Tuesday at 10 a.m., users **started getting** errors when they uploaded files. **The root cause was** a missing environment variable
> after a deployment. We **rolled back** within ten minutes, so the impact was limited. **Since then**, we've **added** a check to the pipeline
> **so that** it can't happen again."*

| Expresión | Significado |
|---|---|
| *root cause* | causa raíz |
| *to roll back* | revertir un despliegue |
| *to mitigate* | mitigar, reducir el impacto |
| *outage / downtime* | caída / tiempo sin servicio |
| *blameless* | sin buscar culpables |
""",
        "phrases": [
            ("On the one hand, a bigger model is more accurate. On the other hand, it's slower.", "Por un lado, un modelo más grande es más preciso. Por otro, es más lento."),
            ("It depends on the volume of requests.", "Depende del volumen de peticiones."),
            ("I'd go with PostgreSQL because we need transactions.", "Me quedaría con PostgreSQL porque necesitamos transacciones."),
            ("The root cause was a missing environment variable.", "La causa raíz fue una variable de entorno que faltaba."),
            ("We rolled back within ten minutes.", "Revertimos el cambio en menos de diez minutos."),
            ("Since then, we've added a check to the pipeline.", "Desde entonces, hemos añadido una comprobación al pipeline."),
        ],
        "exercises": [
            listen("tech3-listen-1",
                   "On Tuesday morning, users started getting errors when they uploaded files. The root cause was a missing environment variable "
                   "after a deployment. We rolled back within ten minutes, and since then we've added a check to the pipeline.",
                   "¿Cuál fue la causa raíz del incidente?",
                   ["Un ataque", "Una variable de entorno que faltaba tras un despliegue", "Archivos demasiado grandes", "Un fallo del proveedor"], 1,
                   "*The root cause was a missing environment variable after a deployment.*"),
            listen("tech3-listen-2",
                   "On the one hand, the bigger model gives better answers. On the other hand, it costs five times more. "
                   "For our volume, I'd use the smaller model and send only the hard questions to the bigger one.",
                   "¿Qué propone la persona?",
                   ["Usar siempre el modelo grande", "Usar el modelo pequeño y enviar solo las preguntas difíciles al grande",
                    "Usar siempre el modelo pequeño", "No usar modelos"], 1, ""),
            fill("tech3-fill-1", "The smaller model is ___ than the bigger one.", ["cheaper", "faster"],
                 "El modelo pequeño es más barato (o rápido) que el grande.", "Comparativo de adjetivo corto: *-er + than*."),
            fill("tech3-fill-2", "The root ___ was a missing environment variable.", ["cause"],
                 "La causa raíz fue una variable de entorno que faltaba.", "*root cause* = causa raíz."),
            choice("tech3-choice-1", "¿Cuál es correcta?",
                   ["This option is more faster.", "This option is fastest than the other.", "This option is faster than the other.",
                    "This option is more fast than the other."], 2,
                   "Adjetivo corto: *faster than*. Nunca *more faster*."),
            choice("tech3-choice-2", "*\"We rolled back the deployment.\"* ¿Qué hicieron?",
                   ["Desplegaron de nuevo más rápido", "Revirtieron el despliegue a la versión anterior", "Borraron la base de datos",
                    "Movieron el servidor"], 1, "*to roll back* = volver a la versión anterior."),
            translate("tech3-tr-1", "Depende del volumen de peticiones.",
                      ["It depends on the volume of requests.", "It depends on the number of requests."],
                      "En inglés es *depend **on*** (no *depend of*)."),
            dictation("tech3-dict-1", "Since then, we've added a check to the pipeline.",
                      "Desde entonces, hemos añadido una comprobación al pipeline."),
            speak("tech3-speak-1", "Lee en voz alta.", "I'd go with PostgreSQL because we need transactions."),
            speak("tech3-speak-2", "Di en inglés: «Revertimos el cambio en menos de diez minutos».", "We rolled back within ten minutes.",
                  ["We rolled back the change within ten minutes.", "We rolled back in less than ten minutes."], show_target=False),
        ],
    },
]
