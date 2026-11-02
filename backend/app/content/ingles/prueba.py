"""Prueba de nivel: 6 preguntas por nivel (A2, B1, B2). Las de tipo listen se escuchan con la voz del navegador."""
from ._helpers import choice, listen


def _q(level, exercise):
    return dict(exercise, level=level)


PLACEMENT = [
    # --- A2 ---------------------------------------------------------------------------------
    _q("A2", choice("pl-a2-1", "I ___ a web developer from Venezuela.", ["am", "is", "are", "be"], 0, "")),
    _q("A2", choice("pl-a2-2", "She ___ Python every day at work.", ["use", "uses", "using", "is use"], 1, "")),
    _q("A2", choice("pl-a2-3", "Yesterday we ___ the new version of the app.", ["deploy", "deploys", "deployed", "are deploying"], 2, "")),
    _q("A2", choice("pl-a2-4", "___ you send me the file, please?", ["Can", "Do", "Are", "Have"], 0, "")),
    _q("A2", listen("pl-a2-5", "Hi, my name is Laura. I work as a backend developer in a small company.",
                    "¿Qué trabajo tiene Laura?", ["Diseñadora", "Desarrolladora backend", "Gerente de ventas", "Profesora"], 1)),
    _q("A2", listen("pl-a2-6", "The meeting is at three o'clock tomorrow, not today.",
                    "¿Cuándo es la reunión?", ["Hoy a las tres", "Mañana a las tres", "Mañana a las dos", "Hoy a las dos"], 1)),
    # --- B1 ---------------------------------------------------------------------------------
    _q("B1", choice("pl-b1-1", "I have been working on this project ___ March.", ["for", "since", "during", "from"], 1, "")),
    _q("B1", choice("pl-b1-2", "If the tests ___, we will deploy on Friday.", ["pass", "passed", "will pass", "would pass"], 0, "")),
    _q("B1", choice("pl-b1-3", "This API is ___ than the old one.", ["more fast", "faster", "fastest", "most fast"], 1, "")),
    _q("B1", choice("pl-b1-4", "\"Could you walk me through your project?\" means:",
                    ["¿Podrías caminar conmigo hasta el proyecto?", "¿Podrías explicarme tu proyecto paso a paso?",
                     "¿Podrías enviarme tu proyecto?", "¿Podrías terminar tu proyecto?"], 1, "")),
    _q("B1", listen("pl-b1-5", "We decided to use PostgreSQL because we needed transactions, and the team already knew SQL.",
                    "¿Por qué eligieron PostgreSQL?",
                    ["Porque era gratis y rápido", "Porque necesitaban transacciones y el equipo ya sabía SQL",
                     "Porque el cliente lo exigía", "Porque no necesitaban un esquema"], 1)),
    _q("B1", listen("pl-b1-6", "I'm a bit behind on the dashboard, so I'll need two more days to finish it.",
                    "¿Qué dice la persona?",
                    ["Ya terminó el dashboard", "Va un poco atrasada y necesita dos días más",
                     "Necesita ayuda con el diseño", "El dashboard se canceló"], 1)),
    # --- B2 ---------------------------------------------------------------------------------
    _q("B2", choice("pl-b2-1", "If we had added monitoring earlier, we ___ the problem much sooner.",
                    ["would notice", "will notice", "would have noticed", "had noticed"], 2, "")),
    _q("B2", choice("pl-b2-2", "The results ___ by the evaluation script every night.",
                    ["generate", "are generated", "are generating", "have generate"], 1, "")),
    _q("B2", choice("pl-b2-3", "Which sentence is the most appropriate way to push back on a client request?",
                    ["No, that's impossible.", "I can't do that, sorry.",
                     "That's outside the current scope, but I'd be happy to send you a quote for it.", "You didn't ask for that before."], 2, "")),
    _q("B2", choice("pl-b2-4", "\"We should eventually migrate to the new service\" means that we should migrate:",
                    ["de vez en cuando", "al final, con el tiempo", "inmediatamente", "eventualmente, quizá nunca"], 1, "")),
    _q("B2", listen("pl-b2-5",
                    "The root cause was a misconfigured environment variable. We rolled back within ten minutes, "
                    "and we've since added a check to the deployment pipeline.",
                    "¿Qué hicieron después del incidente?",
                    ["Cambiaron de proveedor", "Añadieron una comprobación al pipeline de despliegue",
                     "Despidieron al responsable", "Desactivaron las variables de entorno"], 1)),
    _q("B2", listen("pl-b2-6",
                    "While retrieval improved the accuracy, it also increased latency, so we added a cache for the most frequent questions.",
                    "¿Qué problema causó la recuperación de documentos y cómo lo resolvieron?",
                    ["Bajó la precisión; cambiaron de modelo", "Aumentó la latencia; añadieron una caché",
                     "Aumentó el costo; redujeron los documentos", "Generó alucinaciones; añadieron citas"], 1)),
]
