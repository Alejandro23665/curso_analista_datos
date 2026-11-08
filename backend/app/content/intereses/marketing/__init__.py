"""Área de interés: Comunicación y marketing moderno.

Bloques A (comunicar con claridad) y B (crecer en Instagram y TikTok divulgando IA y startups) completos. Pendientes: los bloques C
(de la audiencia a los clientes) y D (medir y el reto de 30 días). Los temas del bloque A están al final de TOPICS.
"""
from ..._helpers import checklist, py, quiz

SK_REDES = "Marketing: redes sociales"
SK_CONTENIDO = "Marketing: contenido"
SK_DIVULGAR = "Marketing: divulgación"
SK_METRICAS = "Marketing: métricas"

_PENDIENTE = "Capítulo en preparación. " * 60

AREA = {
    "slug": "marketing",
    "title": "Comunicación y marketing moderno",
    "order": 2,
    "description": "Crecer en Instagram y TikTok divulgando IA y startups, y convertir esa audiencia en clientes, usuarios y "
                   "oportunidades. Inspirado en perfiles como @crece30x y @andresbilbao, adaptado a quien empieza sin una trayectoria famosa.",
    "notice": "**Tu autoridad** saldrá de la **claridad** (explicar mejor que nadie), las **pruebas** (enseñar que lo que dices funciona) "
              "y las **fuentes** (citar datos). Los ejercicios de cálculo usan métricas inventadas pero realistas; las listas de "
              "comprobación se aplican a tus propios vídeos y publicaciones.",
    "blocks": [
        {
            "label": "A",
            "title": "Comunicar con claridad",
            "description": "La base de todo lo demás: escribir para que te lean, contar historias y una propuesta de valor clara, y hablar "
                           "a cámara y en videollamadas con naturalidad.",
            "topics": ["mk-escribir", "mk-storytelling", "mk-hablar"],
        },
        {
            "label": "B",
            "title": "Crecer en Instagram y TikTok",
            "description": "Cómo deciden las plataformas, tu nicho, divulgar conceptos de IA, ganchos, tendencias, grabar a cámara, crear "
                           "formatos propios, carruseles, construir en público, producir sin agotarte y comunidad.",
            "topics": ["mk-algoritmos", "mk-nicho", "mk-divulgar-ia", "mk-ganchos", "mk-tendencias", "mk-video",
                       "mk-crear-tendencia", "mk-carruseles", "mk-en-publico", "mk-produccion", "mk-comunidad"],
        },
    ],
}

TOPICS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-algoritmos",
        "title": "Cómo deciden las plataformas qué mostrar",
        "summary": "Las señales que miran TikTok e Instagram (retención, vistas completas, compartidos, guardados) y cómo leerlas en tus estadísticas.",
        "hours": 3,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mka-interaccion", "Tasa de interacción", SK_METRICAS,
                "Escribe `tasa_interaccion(me_gusta, comentarios, compartidos, guardados, alcance)` que devuelva el **porcentaje** de "
                "interacciones sobre el alcance (cuentas que vieron el contenido), redondeado a 2 decimales. Si el alcance es 0, devuelve `0.0`.",
                """
def tasa_interaccion(me_gusta, comentarios, compartidos, guardados, alcance):
    pass
""",
                """
def tasa_interaccion(me_gusta, comentarios, compartidos, guardados, alcance):
    if alcance == 0:
        return 0.0
    return round((me_gusta + comentarios + compartidos + guardados) / alcance * 100, 2)
""",
                """
assert tasa_interaccion(300, 20, 50, 30, 10000) == 4.0
assert tasa_interaccion(0, 0, 0, 0, 0) == 0.0, "sin alcance no se puede dividir"
assert tasa_interaccion(10, 1, 2, 3, 777) == 2.06
""",
            ),
            py(
                "mka-completas", "Vistas completas y retención media", SK_METRICAS,
                "Escribe `retencion(segundos_vistos, duracion)`. `segundos_vistos` tiene cuántos segundos vio cada persona un vídeo de "
                "`duracion` segundos (nadie supera la duración). Devuelve una tupla `(pct_completas, retencion_media)`: el porcentaje de "
                "vistas que llegaron al final y el porcentaje medio del vídeo que se vio, ambos redondeados a 1 decimal. Sin vistas, `(0.0, 0.0)`.",
                """
def retencion(segundos_vistos, duracion):
    pass
""",
                """
def retencion(segundos_vistos, duracion):
    if not segundos_vistos:
        return (0.0, 0.0)
    completas = sum(1 for s in segundos_vistos if s >= duracion)
    pct_completas = round(completas / len(segundos_vistos) * 100, 1)
    media = round(sum(s / duracion for s in segundos_vistos) / len(segundos_vistos) * 100, 1)
    return (pct_completas, media)
""",
                """
assert retencion([30, 30, 15, 3], 30) == (50.0, 65.0), "2 de 4 completas; media de 100 %, 100 %, 50 % y 10 %"
assert retencion([], 30) == (0.0, 0.0)
assert retencion([2, 2, 2], 20) == (0.0, 10.0), "todos se van a los 2 segundos: el gancho falla"
""",
            ),
            quiz(
                "mka-quiz-senal", "La señal más fuerte", SK_REDES,
                "Dos vídeos tienen el mismo número de «me gusta». El A se ve completo el 15 % de las veces y casi nadie lo comparte; el B se "
                "ve completo el 55 % de las veces y muchos lo guardan y lo envían por mensaje. ¿Cuál es más probable que la plataforma muestre "
                "a más gente?",
                ["El A", "El B: retener, guardar y compartir pesan más que un «me gusta»", "Los dos igual", "Depende solo de los hashtags"],
                1,
                "Un «me gusta» cuesta poco. Que la gente vea el vídeo entero, lo guarde para después o lo envíe a alguien indica que de verdad le "
                "aportó algo, y las plataformas lo usan para decidir si se lo enseñan a más personas.",
            ),
            quiz(
                "mka-quiz-prueba", "Las primeras horas", SK_REDES,
                "Publicas un vídeo y en la primera hora tiene 200 visualizaciones con una retención muy baja. ¿Qué es lo más razonable?",
                [
                    "Borrarlo y volver a subirlo idéntico muchas veces",
                    "Analizar en qué segundo se va la gente, aprender para el siguiente vídeo y no obsesionarse con uno solo",
                    "Comprar visualizaciones",
                    "Dejar de publicar una semana",
                ],
                1,
                "Las plataformas suelen probar un contenido con un grupo pequeño y amplían si responde bien. Un vídeo que no funciona es "
                "información: la curva de retención te dice qué cambiar en el siguiente.",
            ),
            quiz(
                "mka-quiz-seguidores", "Seguidores frente a recomendación", SK_REDES,
                "Tienes 300 seguidores. ¿Puede un vídeo tuyo llegar a 50 000 personas?",
                [
                    "No: solo lo ven tus seguidores",
                    "Sí: TikTok e Instagram recomiendan contenido a gente que no te sigue si retiene e interesa",
                    "Solo si pagas publicidad",
                    "Solo si usas 30 hashtags",
                ],
                1,
                "La mayor parte del alcance de un Reel o un TikTok viene de la recomendación (la página Para ti o Explorar), no de los "
                "seguidores. Por eso una cuenta pequeña puede tener un vídeo que funcione muy bien.",
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-nicho",
        "title": "Tu nicho, tu perfil y tu estilo visual",
        "summary": "Elegir un ángulo propio dentro de la IA, un perfil que explique en 3 segundos qué ganas siguiéndote y una identidad visual constante.",
        "hours": 3,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mkn-elegir", "Elegir nicho con criterios", SK_CONTENIDO,
                "Escribe `mejor_nicho(opciones)`. Cada opción es un diccionario con `nombre` y puntuaciones del 1 al 5 en `interes` (cuánto te "
                "gusta), `conocimiento`, `demanda` (cuánta gente lo busca) y `competencia` (5 = muchísima). La puntuación total es "
                "`interes + conocimiento + demanda + (6 - competencia)`. Devuelve el `nombre` con mayor total; en caso de empate, el primero "
                "de la lista. Con una lista vacía, `None`.",
                """
def mejor_nicho(opciones):
    pass
""",
                """
def mejor_nicho(opciones):
    mejor, mejor_total = None, None
    for o in opciones:
        total = o["interes"] + o["conocimiento"] + o["demanda"] + (6 - o["competencia"])
        if mejor_total is None or total > mejor_total:
            mejor, mejor_total = o["nombre"], total
    return mejor
""",
                """
ops = [
    {"nombre": "Noticias de IA", "interes": 4, "conocimiento": 3, "demanda": 5, "competencia": 5},
    {"nombre": "IA para pymes en LATAM", "interes": 5, "conocimiento": 4, "demanda": 4, "competencia": 2},
    {"nombre": "Prompts graciosos", "interes": 2, "conocimiento": 3, "demanda": 4, "competencia": 4},
]
assert mejor_nicho(ops) == "IA para pymes en LATAM", "17 frente a 13 y 11: la competencia baja suma"
assert mejor_nicho([]) is None
empate = [{"nombre": "A", "interes": 3, "conocimiento": 3, "demanda": 3, "competencia": 3},
          {"nombre": "B", "interes": 3, "conocimiento": 3, "demanda": 3, "competencia": 3}]
assert mejor_nicho(empate) == "A", "con empate gana el primero"
""",
            ),
            quiz(
                "mkn-quiz-bio", "La mejor biografía", SK_CONTENIDO,
                "¿Qué biografía hace más probable que alguien interesado en IA te siga?",
                [
                    "«Apasionado por la tecnología | Soñador | Venezuela 🇻🇪»",
                    "«Te explico la IA en 60 segundos para que la uses en tu negocio | Construyendo una startup de IA en público»",
                    "«Desarrollador web. Me gusta el café.»",
                    "«Sígueme para más contenido»",
                ],
                1,
                "Una buena biografía dice qué ganas siguiéndote y sobre qué tema, en una línea. Las demás no explican qué contenido vas a encontrar.",
            ),
            quiz(
                "mkn-quiz-nicho", "Nicho estrecho o amplio", SK_CONTENIDO,
                "Empiezas desde cero. ¿Qué enfoque suele crecer más rápido?",
                [
                    "Hablar de todo (IA, viajes, deporte, motivación) para atraer a más gente",
                    "Un tema claro (IA práctica para negocios, en español) que la plataforma pueda asociar a un público concreto",
                    "Cambiar de tema cada semana según lo que esté de moda",
                    "Solo noticias de famosos",
                ],
                1,
                "Si siempre hablas de lo mismo, la plataforma aprende a quién mostrar tu contenido y quien te sigue sabe qué va a recibir. Puedes "
                "ampliar el tema más adelante.",
            ),
            quiz(
                "mkn-quiz-visual", "Por qué un estilo visual constante", SK_CONTENIDO,
                "Los perfiles como @crece30x usan siempre la misma tipografía, colores y estructura en sus portadas. ¿Para qué?",
                [
                    "Por casualidad",
                    "Para que, al ver la portada en el feed, se reconozca la cuenta antes de leer el nombre, y para producir más rápido con plantillas",
                    "Porque la plataforma lo exige",
                    "Para ocupar menos espacio",
                ],
                1,
                "La constancia visual crea reconocimiento (una marca) y, con plantillas, hace que cada publicación cueste menos esfuerzo.",
            ),
            checklist(
                "mkn-check-perfil", "Tu perfil, listo", SK_CONTENIDO,
                "Revisa tu perfil de Instagram y de TikTok con esta lista.",
                [
                    "El nombre o el título incluye de qué hablo (por ejemplo, «IA para negocios»)",
                    "La biografía dice en una línea qué gana quien me sigue",
                    "La foto es mi cara, bien iluminada, reconocible en pequeño",
                    "El enlace lleva a un sitio útil (lista de espera, demo o formulario de contacto)",
                    "Elegí 2 tipografías y 2-3 colores y creé plantillas en Canva para portadas y carruseles",
                    "Las 3 primeras publicaciones (o fijadas) explican quién soy y qué contenido encontrarán",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-divulgar-ia",
        "title": "Divulgar conceptos de IA",
        "summary": "Explicar un LLM, un agente o un RAG en 60 segundos, con analogías correctas, sin jerga y sin exagerar.",
        "hours": 4,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mkd-frases-largas", "Detectar frases demasiado largas", SK_DIVULGAR,
                "En un guion para vídeo, las frases largas cuestan de seguir. Escribe `frases_largas(texto, maximo)` que separe el texto en "
                "frases (por `.`, `?` o `!`), ignore las vacías y devuelva la lista de las que tienen **más** de `maximo` palabras, sin espacios "
                "a los lados.",
                """
import re

def frases_largas(texto, maximo):
    pass
""",
                """
import re

def frases_largas(texto, maximo):
    frases = [f.strip() for f in re.split(r"[.?!]", texto)]
    return [f for f in frases if f and len(f.split()) > maximo]
""",
                """
guion = "Un LLM predice la siguiente palabra. Lo entrenaron con muchísimo texto de internet, libros y código durante meses en miles de ordenadores. ¿Sabe cosas? No exactamente."
assert frases_largas(guion, 10) == ["Lo entrenaron con muchísimo texto de internet, libros y código durante meses en miles de ordenadores"]
assert frases_largas(guion, 20) == []
assert frases_largas("", 5) == []
""",
                hint="re.split(r\"[.?!]\", texto) separa por cualquiera de los tres signos.",
            ),
            quiz(
                "mkd-quiz-analogia", "Una analogía que no engaña", SK_DIVULGAR,
                "¿Cuál es la mejor analogía para explicar qué hace un modelo de lenguaje (LLM)?",
                [
                    "Es un cerebro digital que piensa y siente como una persona",
                    "Es como el autocompletado del móvil, pero entrenado con muchísimo texto: predice qué palabra viene después, y por eso a veces "
                    "se equivoca con mucha seguridad",
                    "Es una base de datos que busca la respuesta exacta en internet",
                    "Es un programa con todas las respuestas escritas a mano",
                ],
                1,
                "La analogía del autocompletado es simple y además explica una limitación real (las alucinaciones). Las demás son falsas: no "
                "siente, no consulta una base de datos de respuestas y nadie escribió las respuestas.",
            ),
            quiz(
                "mkd-quiz-exagerar", "Divulgar sin exagerar", SK_DIVULGAR,
                "¿Qué frase es responsable para un vídeo sobre agentes de IA?",
                [
                    "«Con esta IA ya no necesitas empleados»",
                    "«Un agente puede encadenar tareas usando herramientas, como consultar tu agenda y enviar un correo; todavía comete errores, así "
                    "que conviene revisar lo importante»",
                    "«Esta IA es consciente»",
                    "«Gana 10 000 dólares al mes con IA sin hacer nada»",
                ],
                1,
                "Explica qué hace y su límite real. Las promesas exageradas atraen visualizaciones a corto plazo, pero destruyen la credibilidad, "
                "que es tu principal activo en un nicho saturado.",
            ),
            quiz(
                "mkd-quiz-jerga", "Quitar la jerga", SK_DIVULGAR,
                "Quieres explicar RAG a dueños de negocios. ¿Qué empiezo es mejor?",
                [
                    "«RAG combina recuperación vectorial por similitud coseno con generación condicionada»",
                    "«¿Tu chatbot inventa respuestas? Hay una forma de que conteste solo con la información de tu empresa: primero busca en tus "
                    "documentos y después responde»",
                    "«Hoy hablamos de embeddings»",
                    "«RAG significa Retrieval-Augmented Generation»",
                ],
                1,
                "Empieza por el problema que tiene tu público y explica la idea con palabras comunes. Los términos técnicos pueden aparecer "
                "después, ya explicados.",
            ),
            checklist(
                "mkd-check-explicacion", "Tu primera explicación de un concepto", SK_DIVULGAR,
                "Escribe en Apuntes el guion de un vídeo de 60 segundos que explique un concepto de IA (LLM, token, alucinación, agente o RAG) y "
                "revísalo con esta lista.",
                [
                    "Empieza con el problema o la pregunta de la audiencia, no con la definición",
                    "Usa una analogía que no sea falsa y digo dónde se rompe",
                    "No tiene ninguna palabra técnica sin explicar",
                    "Incluye un ejemplo concreto (un negocio, una tarea real)",
                    "Menciona una limitación real del concepto",
                    "Se lo leí a alguien no técnico y supo repetirlo con sus palabras",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-ganchos",
        "title": "Ganchos, opinión y polémica responsable",
        "summary": "Los primeros segundos deciden todo: tipos de gancho, cómo dar opiniones fuertes con argumentos y dónde está la línea.",
        "hours": 3,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mkg-caida", "¿Dónde se va la gente?", SK_METRICAS,
                "La curva de retención indica qué porcentaje de espectadores sigue viendo en cada segundo. Escribe `mayor_caida(curva)` que "
                "devuelva el **segundo** en el que se produce la mayor caída respecto al segundo anterior (el índice del segundo de llegada). "
                "Si hay empate, el primero. Con menos de 2 valores, `None`.",
                """
def mayor_caida(curva):
    pass
""",
                """
def mayor_caida(curva):
    if len(curva) < 2:
        return None
    mejor, mayor = None, None
    for i in range(1, len(curva)):
        caida = curva[i - 1] - curva[i]
        if mayor is None or caida > mayor:
            mejor, mayor = i, caida
    return mejor
""",
                """
assert mayor_caida([100, 62, 55, 50, 48, 30, 28]) == 1, "de 100 a 62 en el segundo 1: el gancho no funciona"
assert mayor_caida([100, 95, 92, 90, 60, 58]) == 4, "el gancho funciona; algo pasa en el segundo 4"
assert mayor_caida([100]) is None
assert mayor_caida([100, 80, 60]) == 1, "empate: el primero"
""",
            ),
            quiz(
                "mkg-quiz-gancho", "El mejor gancho", SK_CONTENIDO,
                "Vídeo sobre cómo una pequeña tienda puede responder WhatsApp con IA. ¿Qué primeros segundos funcionan mejor?",
                [
                    "«Hola a todos, bienvenidos a mi canal, hoy vamos a hablar de un tema muy interesante...»",
                    "«Esta tienda respondía 200 mensajes al día a mano. Ahora los responde una IA en segundos, y así lo hicimos.»",
                    "«La inteligencia artificial es una rama de la informática...»",
                    "Diez segundos de música con el logo",
                ],
                1,
                "El buen gancho promete un resultado concreto y despierta curiosidad desde la primera frase. Los saludos y las definiciones hacen "
                "que la gente se vaya antes de llegar a lo interesante.",
            ),
            quiz(
                "mkg-quiz-opinion", "Opinión fuerte y responsable", SK_CONTENIDO,
                "Quieres un vídeo de opinión del estilo «3 carreras que no estudiaría en 2026». ¿Qué hace que sea responsable?",
                [
                    "Afirmarlo con mucha seguridad, sin datos, para generar polémica",
                    "Dar tu opinión con argumentos y algún dato verificable, decir que es tu opinión y reconocer los matices",
                    "Inventar una estadística que suene convincente",
                    "Atacar a las personas que estudian esas carreras",
                ],
                1,
                "La opinión fuerte genera conversación, pero sin argumentos ni datos destruye la credibilidad. Y una estadística inventada en el "
                "nicho de la IA, donde el público es crítico, se detecta rápido.",
            ),
            quiz(
                "mkg-quiz-promesa", "Cumplir la promesa del gancho", SK_CONTENIDO,
                "Tu gancho dice «el truco de IA que nadie te cuenta», pero el vídeo explica algo muy conocido. ¿Qué pasa?",
                [
                    "Nada, lo importante es que lo vean",
                    "La gente se siente engañada: se va, no vuelve a confiar y la retención y los comentarios lo reflejan",
                    "Gana más seguidores",
                    "La plataforma premia el contenido conocido",
                ],
                1,
                "Un gancho es una promesa. Si el contenido no la cumple, pierdes la confianza, que vale más que una visualización.",
            ),
            checklist(
                "mkg-check-ganchos", "Cinco ganchos para tu próximo vídeo", SK_CONTENIDO,
                "Elige un tema de IA y escribe en Apuntes cinco ganchos distintos para el mismo vídeo. Después revísalos.",
                [
                    "Escribí un gancho de resultado («así pasó de X a Y»)",
                    "Escribí un gancho de error común («el error que cometen todos al usar ChatGPT»)",
                    "Escribí un gancho de contraste («no es X, es Y»)",
                    "Escribí un gancho de lista («3 cosas que...»)",
                    "Escribí un gancho de pregunta que mi público se hace de verdad",
                    "Comprobé que el vídeo cumple lo que promete cada gancho y elegí el mejor",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-tendencias",
        "title": "Descubrir tendencias",
        "summary": "Dónde encontrar lo que está creciendo (en la plataforma y en el mundo de la IA), cómo filtrarlo y cómo llegar a tiempo.",
        "hours": 3,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mkt-acelera", "¿Está acelerando?", SK_METRICAS,
                "Escribe `crecimiento(serie, ventana)` que compare la suma de los **últimos** `ventana` valores de una serie semanal (por ejemplo, "
                "búsquedas de un término) con la de los `ventana` **anteriores**, y devuelva el crecimiento en porcentaje redondeado a 1 "
                "decimal. Si no hay `2 * ventana` valores o la suma anterior es 0, devuelve `None`.",
                """
def crecimiento(serie, ventana):
    pass
""",
                """
def crecimiento(serie, ventana):
    if len(serie) < 2 * ventana:
        return None
    reciente = sum(serie[-ventana:])
    anterior = sum(serie[-2 * ventana:-ventana])
    if anterior == 0:
        return None
    return round((reciente - anterior) / anterior * 100, 1)
""",
                """
assert crecimiento([10, 12, 11, 15, 30, 45], 2) == 188.5, "anterior 11 + 15 = 26; reciente 30 + 45 = 75"
assert crecimiento([50, 48, 40, 30], 2) == -28.6
assert crecimiento([1, 2, 3], 2) is None
assert crecimiento([0, 0, 5, 8], 2) is None
""",
            ),
            quiz(
                "mkt-quiz-a-tiempo", "Llegar a tiempo", SK_REDES,
                "Una empresa de IA lanza hoy un modelo nuevo muy comentado. ¿Qué haces si quieres aprovecharlo?",
                [
                    "Esperar dos semanas para hacer un análisis perfecto",
                    "Probarlo y publicar pronto (en uno o dos días) una explicación clara de qué cambia y para quién, sin exagerar",
                    "Copiar el vídeo de otro creador",
                    "Ignorarlo: las noticias no sirven",
                ],
                1,
                "En las noticias de IA, los primeros días concentran el interés. Llegar pronto con una explicación clara (y probada) te da "
                "alcance y te posiciona como referencia.",
            ),
            quiz(
                "mkt-quiz-filtro", "Filtrar una tendencia", SK_REDES,
                "Un audio de baile está de moda en TikTok. ¿Cuándo tiene sentido usarlo en tu cuenta de IA?",
                [
                    "Siempre: todo lo que está de moda sirve",
                    "Si puedo adaptarlo a mi tema con algo propio (por ejemplo, un formato de humor sobre lo que la gente cree que hace la IA)",
                    "Nunca: las tendencias son para cuentas de entretenimiento",
                    "Solo si bailo bien",
                ],
                1,
                "Una tendencia te sirve si encaja con tu nicho y puedes aportar algo tuyo. Si no tiene relación con tu tema, atrae a un público "
                "que después no se queda.",
            ),
            quiz(
                "mkt-quiz-fuentes", "Dónde mirar", SK_REDES,
                "¿Qué combinación te ayuda más a descubrir tendencias para una cuenta de IA?",
                [
                    "Solo la página de inicio de TikTok",
                    "Tendencias de la plataforma (TikTok Creative Center, audios en tendencia de Instagram) más fuentes del tema (lanzamientos de "
                    "IA, Google Trends, foros y newsletters)",
                    "Solo los periódicos generalistas",
                    "Preguntarle a tus amigos",
                ],
                1,
                "Necesitas las dos miradas: qué formatos y audios están creciendo en la plataforma y de qué se está hablando en tu tema.",
            ),
            checklist(
                "mkt-check-sistema", "Tu sistema de vigilancia de tendencias", SK_REDES,
                "Monta tu sistema y úsalo durante una semana.",
                [
                    "Guardé en marcadores el TikTok Creative Center y Google Trends con mis términos de IA",
                    "Me suscribí a 2-3 fuentes de noticias de IA (newsletters o cuentas de los laboratorios)",
                    "Tengo una nota de ideas donde apunto cada tendencia con la fecha y una idea de cómo adaptarla",
                    "Dedico 15 minutos al día, a una hora fija, a revisar tendencias (y no más)",
                    "Esta semana publiqué al menos un contenido basado en una tendencia que encajaba con mi nicho",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-video",
        "title": "Vídeo a cámara y formatos de Reels y TikTok",
        "summary": "Grabar hablando a cámara con el móvil, guion, texto en pantalla y subtítulos, ritmo, y tutoriales con grabación de pantalla.",
        "hours": 4,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mkv-duracion", "¿Cuánto dura tu guion?", SK_CONTENIDO,
                "Escribe `duracion_segundos(guion, palabras_por_minuto=150)` que estime cuántos segundos dura un guion leído en voz alta, "
                "redondeando **hacia arriba** (`math.ceil`). Las palabras se separan por espacios.",
                """
import math

def duracion_segundos(guion, palabras_por_minuto=150):
    pass
""",
                """
import math

def duracion_segundos(guion, palabras_por_minuto=150):
    palabras = len(guion.split())
    return math.ceil(palabras / palabras_por_minuto * 60)
""",
                """
assert duracion_segundos("hola " * 150) == 60
assert duracion_segundos("uno dos tres") == 2, "3 palabras = 1.2 s -> 2"
assert duracion_segundos("") == 0
assert duracion_segundos("a " * 100, palabras_por_minuto=200) == 30
""",
            ),
            py(
                "mkv-subtitulos", "Partir subtítulos", SK_CONTENIDO,
                "Escribe `subtitulos(texto, maximo)` que reparta el texto en líneas de **como mucho** `maximo` caracteres **sin partir "
                "palabras** (las palabras se separan con un espacio). Si una palabra sola es más larga que `maximo`, va en su propia línea.",
                """
def subtitulos(texto, maximo):
    pass
""",
                """
def subtitulos(texto, maximo):
    lineas, actual = [], ""
    for palabra in texto.split():
        candidata = palabra if not actual else actual + " " + palabra
        if len(candidata) <= maximo:
            actual = candidata
        else:
            if actual:
                lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas
""",
                """
assert subtitulos("la IA no piensa como tú", 12) == ["la IA no", "piensa como", "tú"]
assert subtitulos("hola", 10) == ["hola"]
assert subtitulos("", 10) == []
assert subtitulos("supercalifragilístico ok", 8) == ["supercalifragilístico", "ok"]
""",
            ),
            quiz(
                "mkv-quiz-subtitulos", "¿Subtítulos?", SK_CONTENIDO,
                "¿Por qué casi todos los vídeos de divulgación llevan subtítulos o texto en pantalla?",
                [
                    "Porque la plataforma los exige",
                    "Porque mucha gente ve los vídeos sin sonido, y el texto ayuda a seguir la explicación y a retener",
                    "Para ocupar la pantalla",
                    "No hacen falta nunca",
                ],
                1,
                "Muchos ven vídeos en silencio (en el transporte, en el trabajo). Los subtítulos además refuerzan los conceptos clave y mejoran "
                "la retención.",
            ),
            quiz(
                "mkv-quiz-pantalla", "Enseñar una herramienta", SK_CONTENIDO,
                "Vas a enseñar cómo crear un chatbot. ¿Qué formato funciona mejor en vertical?",
                [
                    "Grabar la pantalla completa del ordenador sin zoom",
                    "Tu cara al principio con el gancho, y después la pantalla con zoom en lo importante, texto grande y cortes rápidos",
                    "Una presentación con diapositivas llenas de texto",
                    "Una imagen fija con voz",
                ],
                1,
                "En el móvil, la pantalla de un ordenador sin zoom es ilegible. Tu cara crea conexión en el gancho; el zoom y el texto grande "
                "hacen que se entienda.",
            ),
            checklist(
                "mkv-check-grabacion", "Tu primer vídeo a cámara", SK_CONTENIDO,
                "Graba un vídeo de 30-60 segundos explicando un concepto de IA y revisa cada punto antes de publicarlo.",
                [
                    "Escribí el guion y lo leí en voz alta: dura menos de 60 segundos",
                    "Grabé con luz de frente (una ventana o un aro de luz), el móvil a la altura de los ojos y en vertical",
                    "El sonido se entiende bien (micrófono o una habitación sin eco)",
                    "La primera frase es el gancho, sin saludo",
                    "Corté silencios y repeticiones y añadí subtítulos",
                    "Lo vi entero en el móvil, sin sonido, y se entiende",
                ],
            ),
        ],
    },
]

# Segunda parte del bloque B y bloque A
from .temas_extra import TOPICS as _MAS  # noqa: E402

TOPICS = TOPICS + _MAS
