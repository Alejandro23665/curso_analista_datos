from ._helpers import choice, dictation, fill, listen, speak, translate

UNITS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-int-1",
        "level": "A2",
        "focus": "entrevistas",
        "title": "Tell me about yourself",
        "summary": "Tu presentación de 60 segundos: quién eres, qué construyes y qué buscas.",
        "minutes": 30,
        "lesson": r"""
# Tell me about yourself

Es **la primera pregunta de casi todas las entrevistas** y la que mejor puedes llevar preparada. No te piden tu vida: te piden
un resumen profesional de 45-60 segundos con esta estructura:

1. **Presente:** quién eres y qué haces. *"I'm a Python developer focused on AI applications."*
2. **Pasado:** de dónde vienes, en una frase. *"I studied web development and worked on document automation."*
3. **Prueba:** un proyecto concreto. *"Recently, I built a system that reads invoices with an LLM."*
4. **Futuro:** qué buscas y por qué ahí. *"Now I'm looking for a role where I can build AI products."*

## La gramática que necesitas

- **Presente simple** para lo que haces normalmente: *I **work** with FastAPI. I **build** chatbots.*
  Con *he/she/it* se añade **-s**: *She **works** remotely.*
- **Presente continuo** para lo que haces estos días: *I'm **learning** about AI agents.*
- **Pasado simple** para lo que terminó: *I **studied**, I **built**, I **worked**.* (Verbos irregulares: build → built, make → made.)

## Errores típicos de hispanohablantes

| Incorrecto | Correcto |
|---|---|
| I have 24 years. | I'm 24 years old. |
| I am developer. | I'm **a** developer. |
| I work in Python since 2023. | I've worked with Python since 2023. |
| I'm agree. | I agree. |

## Pronunciación

*developer* se acentúa en la segunda sílaba: de-**VE**-lo-per. *Python* suena "PÁI-zon", y *data* se dice "DEI-ta" o "DA-ta".
""",
        "phrases": [
            ("I'm a Python developer focused on AI applications.", "Soy desarrollador Python enfocado en aplicaciones de IA."),
            ("I studied web development in Caracas.", "Estudié desarrollo web en Caracas."),
            ("Recently, I built a chatbot that answers questions about documents.", "Hace poco construí un chatbot que responde preguntas sobre documentos."),
            ("I'm currently learning about AI agents.", "Ahora mismo estoy aprendiendo sobre agentes de IA."),
            ("I'm looking for a role where I can build AI products.", "Busco un puesto donde pueda construir productos de IA."),
            ("I enjoy solving real problems for real users.", "Disfruto resolviendo problemas reales para usuarios reales."),
        ],
        "exercises": [
            listen("int1-listen-1",
                   "Hi, I'm Daniel. I'm a backend developer with two years of experience. I mostly work with Python and PostgreSQL, "
                   "and right now I'm learning how to build applications with language models.",
                   "¿Qué está aprendiendo Daniel ahora?",
                   ["PostgreSQL", "Desarrollo frontend", "A construir aplicaciones con modelos de lenguaje", "Python"], 2,
                   "*right now I'm learning how to build applications with language models*: el presente continuo indica lo que hace estos días."),
            fill("int1-fill-1", "I'm ___ developer focused on AI applications.", ["a"], "Soy desarrollador enfocado en aplicaciones de IA.",
                 "En inglés las profesiones llevan artículo: *I'm **a** developer*, *she's **an** engineer*."),
            fill("int1-fill-2", "She ___ remotely for a company in Canada.", ["works"], "Ella trabaja en remoto para una empresa de Canadá.",
                 "Presente simple con *she*: el verbo lleva **-s** → *works*."),
            choice("int1-choice-1", "¿Cuál es la forma correcta de decir tu edad?",
                   ["I have 24 years.", "I'm 24 years old.", "I have 24 years old.", "I'm 24 years."], 1,
                   "En inglés la edad se dice con *to be*: *I'm 24 (years old)*."),
            translate("int1-tr-1", "Hace poco construí un chatbot para una tienda.",
                      ["Recently, I built a chatbot for a store.", "Recently I built a chatbot for a shop.",
                       "I recently built a chatbot for a store.", "I recently built a chatbot for a shop."],
                      "*build* es irregular: build → **built**. *Recently* puede ir al principio o antes del verbo."),
            dictation("int1-dict-1", "I'm looking for a role where I can build AI products.",
                      "Busco un puesto donde pueda construir productos de IA."),
            speak("int1-speak-1", "Lee en voz alta esta frase de presentación.",
                  "I'm a Python developer focused on AI applications."),
            speak("int1-speak-2", "Di en inglés: «Ahora mismo estoy aprendiendo sobre agentes de IA».",
                  "I'm currently learning about AI agents.",
                  ["Right now I'm learning about AI agents.", "I'm learning about AI agents right now."], show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-int-2",
        "level": "B1",
        "focus": "entrevistas",
        "title": "Walk me through your project",
        "summary": "Explicar un proyecto paso a paso: problema, solución, reto principal y resultado.",
        "minutes": 40,
        "lesson": r"""
# Walk me through your project

*"Could you walk me through your project?"* significa **"explícame tu proyecto paso a paso"**. Es la pregunta donde más puedes brillar,
porque hablas de algo que conoces. Usa siempre la misma estructura:

1. **The problem:** *"The company was processing invoices by hand, and it took hours every day."*
2. **My solution:** *"I built a system that classifies the documents and extracts the data with an LLM."*
3. **The main challenge:** *"The main challenge was that many images were blurry."*
4. **How I solved it:** *"So I added a validation step and a human review screen."*
5. **The result:** *"As a result, ... / Now, ..."* (con un número si lo tienes).

## Conectores que ordenan tu historia

| Para | Usa |
|---|---|
| Empezar | *First, / To begin with,* |
| Continuar | *Then, / After that, / Next,* |
| Explicar una causa | *because / since* |
| Explicar una consecuencia | *so / as a result,* |
| Contrastar | *but / however,* |
| Terminar | *Finally, / In the end,* |

## Pasado simple: la base de la historia

Casi todo el relato va en **pasado simple**: *I **decided**, I **chose**, I **added**, it **worked***.
Irregulares que usarás mucho: *build → built, choose → chose, find → found, take → took, write → wrote, run → ran*.

## Frases para ganar tiempo (sin quedarte en silencio)

- *"That's a good question. Let me think about it for a second."*
- *"Let me give you some context first."*
- *"If I did it again, I would..."* (una de las frases que más gustan: demuestra criterio).
""",
        "phrases": [
            ("Let me give you some context first.", "Déjame darte algo de contexto primero."),
            ("The main challenge was that many images were blurry.", "El reto principal fue que muchas imágenes estaban borrosas."),
            ("So I added a validation step and a human review screen.", "Así que añadí un paso de validación y una pantalla de revisión humana."),
            ("As a result, the team saves about two hours every day.", "Como resultado, el equipo ahorra unas dos horas al día."),
            ("If I did it again, I would write the tests first.", "Si lo hiciera de nuevo, escribiría primero las pruebas."),
            ("That's a good question. Let me think about it for a second.", "Buena pregunta. Déjame pensarlo un segundo."),
        ],
        "exercises": [
            listen("int2-listen-1",
                   "The company was processing invoices by hand. First, I built a script to classify the documents. "
                   "Then, I used a language model to extract the data. The main challenge was the blurry images, "
                   "so I added a human review step. As a result, the team saves about two hours every day.",
                   "¿Cuál fue el reto principal del proyecto?",
                   ["El costo del modelo", "Las imágenes borrosas", "La falta de datos", "El tiempo de entrega"], 1,
                   "*The main challenge was the blurry images, so I added a human review step.*"),
            listen("int2-listen-2",
                   "If I did it again, I would write the tests first, because fixing the parser later took much longer than expected.",
                   "¿Qué haría distinto la persona?",
                   ["Usaría otro lenguaje", "Escribiría primero las pruebas", "Contrataría a alguien", "No usaría un parser"], 1,
                   "*If I did it again, I would...* es el segundo condicional: situaciones hipotéticas."),
            fill("int2-fill-1", "The main challenge was the blurry images, ___ I added a human review step.", ["so"],
                 "El reto principal fueron las imágenes borrosas, así que añadí una revisión humana.",
                 "*so* introduce una consecuencia (= así que)."),
            fill("int2-fill-2", "I ___ PostgreSQL because we needed transactions.", ["chose", "picked", "selected"],
                 "Elegí PostgreSQL porque necesitábamos transacciones.",
                 "Pasado de *choose* (irregular): **chose**."),
            choice("int2-choice-1", "El entrevistador dice *\"Could you walk me through your project?\"*. ¿Cómo empiezas mejor?",
                   ["Yes.", "My project is very good.", "Sure. Let me give you some context first: the company was processing invoices by hand.",
                    "I walk every day."], 2,
                   "Empieza por el contexto y el problema; luego la solución, el reto y el resultado."),
            translate("int2-tr-1", "Como resultado, el equipo ahorra dos horas al día.",
                      ["As a result, the team saves two hours a day.", "As a result, the team saves two hours every day.",
                       "As a result, the team saves two hours per day."],
                      "*As a result* = como resultado. *a day / every day / per day* son correctos."),
            dictation("int2-dict-1", "Then, I used a language model to extract the data.", "Después, usé un modelo de lenguaje para extraer los datos."),
            speak("int2-speak-1", "Lee en voz alta, con calma.", "If I did it again, I would write the tests first."),
            speak("int2-speak-2", "Di en inglés: «Déjame darte algo de contexto primero».", "Let me give you some context first.",
                  ["Let me give you a bit of context first."], show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-int-3",
        "level": "B2",
        "focus": "entrevistas",
        "title": "Behavioral questions and the STAR method",
        "summary": "Responder preguntas conductuales en inglés, pedir aclaraciones y decir \"no lo sé\" con elegancia.",
        "minutes": 45,
        "lesson": r"""
# Behavioral questions and the STAR method

Las preguntas conductuales empiezan casi siempre igual: *"Tell me about a time when..."* o *"Describe a situation where..."*.
Buscan **evidencia de cómo trabajas**, no teoría. Respóndelas con **STAR**:

- **Situation:** *"In my last job, we had a tight deadline for a client demo."*
- **Task:** *"I was responsible for the data extraction module."*
- **Action** (lo que **tú** hiciste, en primera persona): *"I split the work into small tasks and automated the tests."*
- **Result** (con números si puedes): *"We delivered on time, and the client signed a three-month contract."*

## Preguntas que conviene llevar preparadas

| Pregunta | Qué evalúan |
|---|---|
| *Tell me about a time you made a mistake.* | Honestidad y aprendizaje |
| *Tell me about a disagreement with a teammate.* | Comunicación y respeto |
| *Tell me about something you learned quickly.* | Capacidad de aprender |
| *What are you most proud of?* | Impacto real |

## Gramática que te hace sonar más natural

- **Pasado continuo** para el contexto: *"We **were preparing** a demo when the API stopped working."*
- **Present perfect** para experiencia sin fecha: *"I've **worked** with LLM APIs on three projects."*
- **Tercer condicional** para reflexionar: *"If I **had asked** earlier, we **would have saved** a day."*

## Cuando no entiendes o no sabes

- *"Sorry, could you repeat the question?"* / *"Could you rephrase that?"*
- *"Just to make sure I understand, you're asking about..."*
- *"I haven't used that tool, but I've worked with something similar: ..."*
- *"I'm not sure, but this is how I would find out: ..."*

Decir "no lo sé" bien, y explicar **cómo lo averiguarías**, suma puntos. Inventar resta.
""",
        "phrases": [
            ("Tell me about a time when you made a mistake.", "Háblame de una vez en que cometiste un error."),
            ("We were preparing a demo when the API stopped working.", "Estábamos preparando una demo cuando la API dejó de funcionar."),
            ("I was responsible for the data extraction module.", "Yo era responsable del módulo de extracción de datos."),
            ("If I had asked earlier, we would have saved a day.", "Si hubiera preguntado antes, habríamos ahorrado un día."),
            ("Just to make sure I understand, you're asking about testing?", "Para asegurarme de que entiendo, ¿preguntas por las pruebas?"),
            ("I haven't used that tool, but I've worked with something similar.", "No he usado esa herramienta, pero he trabajado con algo parecido."),
        ],
        "exercises": [
            listen("int3-listen-1",
                   "We were preparing a demo for a client when the language model API started returning errors. "
                   "I quickly added a fallback to a smaller model and a clear error message. "
                   "The demo went well, and afterwards we added monitoring so we would know about outages earlier.",
                   "¿Qué acción tomó la persona durante el problema?",
                   ["Canceló la demo", "Añadió un modelo alternativo más pequeño y un mensaje de error claro",
                    "Llamó al proveedor", "Cambió de cliente"], 1,
                   "*I quickly added a fallback to a smaller model and a clear error message.* Esa es la **Action** del STAR."),
            choice("int3-choice-1", "En el método STAR, ¿qué debe contar la parte de **Action**?",
                   ["Lo que hizo el equipo en general", "Lo que hiciste tú, en primera persona", "El resultado final", "El contexto de la empresa"], 1,
                   "El entrevistador quiere saber qué hiciste **tú**: *I decided, I wrote, I proposed...*"),
            fill("int3-fill-1", "If I had asked earlier, we would have ___ a day.", ["saved"],
                 "Si hubiera preguntado antes, habríamos ahorrado un día.",
                 "Tercer condicional: *if + had + participio, would have + participio* → *would have **saved***."),
            fill("int3-fill-2", "I ___ worked with LLM APIs on three projects.", ["have", "'ve"],
                 "He trabajado con APIs de LLM en tres proyectos.",
                 "Experiencia sin fecha concreta → *present perfect*: *I **have** worked*."),
            choice("int3-choice-2", "No entendiste bien la pregunta. ¿Qué dices?",
                   ["What?", "Repeat.", "Sorry, could you rephrase that?", "I don't speak English very well, sorry."], 2,
                   "Pedir que reformulen es normal y profesional. *Could you rephrase that?* o *Could you repeat the question?*"),
            translate("int3-tr-1", "No he usado esa herramienta, pero he trabajado con algo parecido.",
                      ["I haven't used that tool, but I've worked with something similar.",
                       "I have not used that tool, but I have worked with something similar."],
                      "Present perfect en las dos partes: experiencia sin fecha."),
            dictation("int3-dict-1", "We were preparing a demo when the API stopped working.",
                      "Estábamos preparando una demo cuando la API dejó de funcionar."),
            speak("int3-speak-1", "Lee en voz alta.", "Just to make sure I understand, you're asking about testing?"),
            speak("int3-speak-2", "Di en inglés: «No estoy seguro, pero así es como lo averiguaría».",
                  "I'm not sure, but this is how I would find out.",
                  ["I'm not sure, but this is how I'd find out.", "I'm not sure, but that's how I would find out."], show_target=False),
        ],
    },
]
