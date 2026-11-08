"""Segunda parte del bloque B (crear tendencia, carruseles, construir en público, producir, comunidad) y bloque A completo."""
from ..._helpers import checklist, py, quiz

SK_REDES = "Marketing: redes sociales"
SK_CONTENIDO = "Marketing: contenido"
SK_METRICAS = "Marketing: métricas"
SK_COMUNICAR = "Marketing: comunicación"

_PENDIENTE = "Capítulo en preparación. " * 60

TOPICS = [
    # ------------------------------------------------------------------------------------------ bloque B, segunda parte
    {
        "slug": "mk-crear-tendencia",
        "title": "Crear tendencia y formatos propios",
        "summary": "Lo que se puede controlar de la viralidad: series reconocibles, ser el primero en explicar algo, retos y colaboraciones.",
        "hours": 3,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mkc-formato", "¿Insistir o abandonar un formato?", SK_METRICAS,
                "Escribe `evaluar_formato(vistas, media_cuenta, minimo=3)`. `vistas` tiene las visualizaciones de los vídeos de un formato "
                "(una serie) y `media_cuenta`, la media de tu cuenta. Devuelve:\n\n"
                "- `'seguir probando'` si hay menos de `minimo` vídeos,\n"
                "- `'insistir'` si la media del formato es al menos un 20 % mayor que la de la cuenta,\n"
                "- `'abandonar'` si es al menos un 20 % menor,\n"
                "- `'neutro'` en otro caso.",
                """
def evaluar_formato(vistas, media_cuenta, minimo=3):
    pass
""",
                """
def evaluar_formato(vistas, media_cuenta, minimo=3):
    if len(vistas) < minimo:
        return "seguir probando"
    media = sum(vistas) / len(vistas)
    if media >= media_cuenta * 1.2:
        return "insistir"
    if media <= media_cuenta * 0.8:
        return "abandonar"
    return "neutro"
""",
                """
assert evaluar_formato([1500, 900], 1000) == "seguir probando", "con 2 vídeos todavía no se puede saber"
assert evaluar_formato([1500, 1200, 1300], 1000) == "insistir", "media 1333: más de un 20 % por encima"
assert evaluar_formato([700, 800, 900], 1000) == "abandonar", "media 800: justo un 20 % por debajo"
assert evaluar_formato([1100, 950, 1000], 1000) == "neutro"
assert evaluar_formato([1200, 1200, 1200], 1000) == "insistir", "exactamente un 20 % más cuenta como insistir"
""",
            ),
            quiz(
                "mkc-quiz-viral", "Qué se puede controlar", SK_REDES,
                "¿Qué afirmación sobre crear tendencias es realista?",
                [
                    "Con la fórmula correcta, cualquier vídeo se hace viral",
                    "La viralidad no se controla, pero puedes crear formatos reconocibles, llegar primero a los temas y facilitar que otros participen, "
                    "lo que aumenta las probabilidades",
                    "Solo las cuentas con más de 100 000 seguidores crean tendencias",
                    "Las tendencias las decide la plataforma a mano",
                ],
                1,
                "Hay mucha suerte y momento en lo viral. Lo que depende de ti es la calidad, la constancia, los formatos propios y la rapidez.",
            ),
            quiz(
                "mkc-quiz-serie", "Una serie que funciona", SK_CONTENIDO,
                "¿Qué hace que una serie (un formato que repites) crezca?",
                [
                    "Cambiar de nombre y de estructura en cada episodio",
                    "Un nombre fijo, una estructura reconocible y una promesa clara que el público aprende a esperar (por ejemplo, «IA en 30 segundos»)",
                    "Publicarla solo una vez",
                    "Que cada episodio dure el doble que el anterior",
                ],
                1,
                "Una serie funciona por repetición: el público reconoce el formato, sabe qué va a recibir y vuelve a buscarlo.",
            ),
            quiz(
                "mkc-quiz-reto", "Un reto que invita a participar", SK_REDES,
                "¿Qué propuesta tiene más posibilidades de que tu audiencia participe y se extienda?",
                [
                    "«Sígueme y comparte»",
                    "«Prueba este prompt con una foto de tu negocio y enséñame el resultado en tu historia mencionándome»",
                    "«Escribe un ensayo sobre la IA»",
                    "«Dame like si te gustó»",
                ],
                1,
                "Funciona lo que es fácil, rápido, tiene un resultado que la gente quiere enseñar y se conecta contigo (la mención).",
            ),
            checklist(
                "mkc-check-serie", "Diseña tu propia serie", SK_CONTENIDO,
                "Diseña en Apuntes una serie para tu cuenta y publica los tres primeros episodios.",
                [
                    "Tiene un nombre corto y memorable",
                    "Tiene una estructura fija (mismo gancho, mismas partes, misma duración aproximada)",
                    "Tiene un elemento visual reconocible (portada, color o frase de inicio)",
                    "Escribí una lista de al menos 10 episodios posibles",
                    "Publiqué 3 episodios y comparé sus visualizaciones con la media de mi cuenta",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-carruseles",
        "title": "Carruseles educativos",
        "summary": "El formato que más se guarda en Instagram: portada que detiene el dedo, una idea por diapositiva, datos con fuente y cierre con acción.",
        "hours": 3,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mkr-revisar", "Revisor de carruseles", SK_CONTENIDO,
                "Escribe `revisar_carrusel(diapositivas)` que reciba una lista de textos (una diapositiva cada uno) y devuelva una lista con "
                "los problemas encontrados, en este orden:\n\n"
                "1. `'pocas diapositivas'` si hay menos de 3, o `'demasiadas diapositivas'` si hay más de 10.\n"
                "2. `'portada larga'` si la primera tiene más de 8 palabras.\n"
                "3. `'diapositiva densa: N'` por cada diapositiva (numeradas desde 1) con más de 40 palabras.\n"
                "4. `'sin llamada a la accion'` si la última no contiene ninguna de estas palabras (sin distinguir mayúsculas): "
                "`guarda`, `comparte`, `comenta`, `sigue`.",
                """
def revisar_carrusel(diapositivas):
    problemas = []
    return problemas
""",
                """
def revisar_carrusel(diapositivas):
    problemas = []
    if len(diapositivas) < 3:
        problemas.append("pocas diapositivas")
    elif len(diapositivas) > 10:
        problemas.append("demasiadas diapositivas")
    if diapositivas and len(diapositivas[0].split()) > 8:
        problemas.append("portada larga")
    for i, texto in enumerate(diapositivas, start=1):
        if len(texto.split()) > 40:
            problemas.append("diapositiva densa: %d" % i)
    if diapositivas:
        ultima = diapositivas[-1].lower()
        if not any(p in ultima for p in ("guarda", "comparte", "comenta", "sigue")):
            problemas.append("sin llamada a la accion")
    return problemas
""",
                """
bueno = ["3 errores al usar IA en tu negocio", "1. Creer que sabe todo", "2. No darle contexto", "Guarda este carrusel para tu próximo proyecto"]
assert revisar_carrusel(bueno) == []
assert revisar_carrusel(["Hola", "Adiós"]) == ["pocas diapositivas", "sin llamada a la accion"]
largo = ["Esta es una portada con demasiadas palabras para leerse rápido", "texto", "Comenta si te sirvió"]
assert revisar_carrusel(largo) == ["portada larga"]
denso = ["Portada", "palabra " * 45, "Sigue para más"]
assert revisar_carrusel(denso) == ["diapositiva densa: 2"]
assert revisar_carrusel([]) == ["pocas diapositivas"]
""",
            ),
            quiz(
                "mkr-quiz-portada", "La portada", SK_CONTENIDO,
                "¿Qué portada de carrusel hace más probable que alguien deslice?",
                [
                    "«Inteligencia artificial: conceptos, aplicaciones y perspectivas de futuro para empresas»",
                    "«5 cosas que ChatGPT hace con tus datos (y nadie te cuenta)» en letra grande, con una palabra resaltada",
                    "Una foto sin texto",
                    "Tu logo grande",
                ],
                1,
                "La portada es el gancho del carrusel: pocas palabras, una promesa concreta y legible en miniatura.",
            ),
            quiz(
                "mkr-quiz-dato", "Un dato en un carrusel", SK_CONTENIDO,
                "Vas a poner en una diapositiva «el 70 % de las pymes ya usa IA». ¿Qué haces?",
                [
                    "Ponerlo, suena convincente",
                    "Buscar la fuente original, comprobar qué mide exactamente y citarla en pequeño en la diapositiva",
                    "Redondearlo al 80 % para que impacte más",
                    "Quitar el porcentaje y decir «todas»",
                ],
                1,
                "Un dato sin fuente (o malinterpretado) en el nicho de la IA se detecta rápido en los comentarios. La fuente da credibilidad.",
            ),
            quiz(
                "mkr-quiz-guardado", "Por qué los carruseles se guardan", SK_REDES,
                "¿Por qué el carrusel educativo suele acumular muchos guardados?",
                [
                    "Porque la plataforma lo obliga",
                    "Porque condensa información útil que la gente quiere consultar después, a su ritmo",
                    "Porque es el formato más corto",
                    "Porque no se puede compartir",
                ],
                1,
                "Un carrusel bien hecho es una pequeña guía: se guarda para releerlo, y el guardado es una de las señales que más pesan.",
            ),
            checklist(
                "mkr-check-carrusel", "Tu primer carrusel", SK_CONTENIDO,
                "Crea un carrusel en Canva con tu plantilla sobre un concepto de IA y revísalo antes de publicarlo.",
                [
                    "La portada tiene 8 palabras o menos y se lee en miniatura",
                    "Cada diapositiva tiene una sola idea y poco texto",
                    "Hay un ejemplo concreto o un dato con su fuente",
                    "Usé mi tipografía y mis colores, y resalté las palabras clave",
                    "La última diapositiva invita a guardar, comentar o seguir",
                    "Escribí una descripción con las palabras que mi público buscaría",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-en-publico",
        "title": "Construir en público",
        "summary": "Contar el camino de tu startup y tu aprendizaje de IA: qué compartir, qué no, cómo contar los fracasos y por qué atrae al público correcto.",
        "hours": 2,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mkp-crecimiento", "Crecimiento semana a semana", SK_METRICAS,
                "Al construir en público se comparten números. Escribe `crecimiento_semanal(valores)` que devuelva una lista con el "
                "crecimiento porcentual de cada semana respecto a la anterior, redondeado a 1 decimal. Si el valor anterior es 0, pon `None` "
                "en esa posición. Con menos de 2 valores, devuelve `[]`.",
                """
def crecimiento_semanal(valores):
    pass
""",
                """
def crecimiento_semanal(valores):
    resultado = []
    for anterior, actual in zip(valores, valores[1:]):
        if anterior == 0:
            resultado.append(None)
        else:
            resultado.append(round((actual - anterior) / anterior * 100, 1))
    return resultado
""",
                """
assert crecimiento_semanal([10, 15, 12, 24]) == [50.0, -20.0, 100.0]
assert crecimiento_semanal([0, 5, 5]) == [None, 0.0]
assert crecimiento_semanal([7]) == []
assert crecimiento_semanal([]) == []
""",
            ),
            quiz(
                "mkp-quiz-que", "Qué no compartir", SK_CONTENIDO,
                "Al construir en público, ¿qué NO deberías publicar?",
                [
                    "Lo que aprendiste esta semana",
                    "Datos de tus clientes o usuarios, claves o información de terceros sin permiso",
                    "Tus errores y lo que cambiaste",
                    "El número de usuarios de tu MVP",
                ],
                1,
                "Puedes compartir tu proceso y tus números, pero nunca datos personales de otros ni información confidencial.",
            ),
            quiz(
                "mkp-quiz-fracaso", "Contar un fracaso", SK_CONTENIDO,
                "Lanzaste tu MVP y en dos semanas solo se registraron 4 personas. ¿Cómo lo cuentas?",
                [
                    "No lo cuentas: solo se publican los éxitos",
                    "Lo cuentas con honestidad: qué esperabas, qué pasó, qué crees que falló y qué vas a probar ahora",
                    "Dices que se registraron 400",
                    "Culpas a la plataforma",
                ],
                1,
                "Los fracasos contados con aprendizaje generan mucha conexión y credibilidad. Exagerar los números destruye la confianza.",
            ),
            quiz(
                "mkp-quiz-equilibrio", "Equilibrio con la divulgación", SK_CONTENIDO,
                "Tu idea principal es divulgar conceptos de IA. ¿Qué papel tiene construir en público?",
                [
                    "Debe ser todo tu contenido",
                    "Un complemento (por ejemplo, 1 de cada 4 publicaciones) que te diferencia y demuestra que aplicas lo que explicas",
                    "Ninguno",
                    "Solo cuando la startup tenga éxito",
                ],
                1,
                "La divulgación atrae; el diario del fundador da prueba y personalidad. Juntos forman tu propuesta.",
            ),
            checklist(
                "mkp-check-diario", "Tu primer diario del fundador", SK_CONTENIDO,
                "Publica una actualización de tu proyecto (startup, demo o aprendizaje).",
                [
                    "Cuenta qué hice esta semana en una frase",
                    "Incluye un número real (usuarios, horas, conversaciones, errores corregidos)",
                    "Cuenta un problema o un error y qué aprendí",
                    "Dice qué voy a hacer la semana que viene",
                    "No incluye datos de terceros ni información confidencial",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-produccion",
        "title": "Producir sin agotarte",
        "summary": "Banco de ideas, producción por lotes, reutilizar cada idea en varios formatos y un calendario sostenible mientras estudias.",
        "hours": 2,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mko-lotes", "Cuánto ahorras produciendo por lotes", SK_CONTENIDO,
                "Escribe `minutos_semana(videos, guion, grabar, editar, preparar, por_lotes)`. Cada vídeo necesita `guion + grabar + editar` "
                "minutos. Además, cada **sesión de grabación** necesita `preparar` minutos (luz, micrófono, ropa). Si `por_lotes` es `True`, "
                "hay una sola sesión para todos los vídeos; si es `False`, una por vídeo. Con 0 vídeos, devuelve 0.",
                """
def minutos_semana(videos, guion, grabar, editar, preparar, por_lotes):
    pass
""",
                """
def minutos_semana(videos, guion, grabar, editar, preparar, por_lotes):
    if videos == 0:
        return 0
    sesiones = 1 if por_lotes else videos
    return videos * (guion + grabar + editar) + sesiones * preparar
""",
                """
assert minutos_semana(4, 20, 10, 30, 25, por_lotes=False) == 340, "4 x 60 + 4 x 25"
assert minutos_semana(4, 20, 10, 30, 25, por_lotes=True) == 265, "4 x 60 + 1 x 25"
assert minutos_semana(0, 20, 10, 30, 25, por_lotes=True) == 0
assert minutos_semana(1, 10, 10, 10, 5, por_lotes=True) == 35
""",
            ),
            quiz(
                "mko-quiz-ritmo", "Un ritmo sostenible", SK_CONTENIDO,
                "Estudias a tiempo completo. ¿Qué plan de publicación es más probable que mantengas durante 6 meses?",
                [
                    "Dos vídeos al día desde mañana",
                    "3 piezas a la semana, grabadas en una o dos sesiones por lotes, con un banco de ideas y una revisión semanal",
                    "Publicar solo cuando tengas inspiración",
                    "Un vídeo perfecto al mes",
                ],
                1,
                "Crecer depende de la constancia durante meses. Un ritmo que puedes mantener gana a uno intenso que abandonas en dos semanas.",
            ),
            quiz(
                "mko-quiz-reutilizar", "Una idea, varios formatos", SK_CONTENIDO,
                "Hiciste un buen vídeo explicando qué es un agente de IA. ¿Cómo lo aprovechas más?",
                [
                    "Lo publicas una vez y pasas a otra cosa",
                    "Lo publicas en TikTok e Instagram, lo conviertes en un carrusel, sacas una frase para una historia y lo adaptas a una "
                    "publicación de LinkedIn",
                    "Lo subes 10 veces seguidas",
                    "Lo borras al cabo de una semana",
                ],
                1,
                "Reutilizar una idea en varios formatos multiplica su alcance con poco esfuerzo extra: el trabajo difícil (entender y explicar) ya está hecho.",
            ),
            quiz(
                "mko-quiz-ia", "Usar IA para producir", SK_CONTENIDO,
                "¿Cuál es un buen uso de la IA para producir tu contenido?",
                [
                    "Que la IA escriba todos tus guiones y publicarlos sin leerlos",
                    "Usarla para generar ideas, ordenar un borrador, crear subtítulos o proponer ganchos, y revisar tú el contenido y los datos",
                    "Inventar datos con ella",
                    "No usarla nunca",
                ],
                1,
                "La IA acelera las partes mecánicas; tu criterio, tu voz y la comprobación de los datos son lo que te diferencia.",
            ),
            checklist(
                "mko-check-sistema", "Tu sistema de producción", SK_CONTENIDO,
                "Monta tu sistema y úsalo durante dos semanas.",
                [
                    "Tengo un banco de ideas (nota o tablero) con al menos 20 ideas",
                    "Elegí cuántas piezas publicaré por semana y qué días",
                    "Escribo los guiones de la semana en un solo bloque de tiempo",
                    "Grabo por lotes, en una o dos sesiones a la semana",
                    "Reutilizo cada buena idea en al menos dos formatos",
                    "Reviso las estadísticas una vez por semana, no cada hora",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-comunidad",
        "title": "Comunidad, comentarios y automatización",
        "summary": "Convertir espectadores en comunidad: responder, conversar, colaborar, y la mecánica de «comenta X y te envío Y» con mensajes automáticos.",
        "hours": 3,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mku-palabra", "Responder a una palabra clave", SK_REDES,
                "Las herramientas de mensajes automáticos responden cuando alguien comenta una palabra clave. Escribe "
                "`respuesta(comentario, reglas)`: `reglas` es una lista de tuplas `(palabra, mensaje)`. Devuelve el mensaje de la **primera** "
                "regla cuya palabra aparezca en el comentario como **palabra completa** (sin distinguir mayúsculas e ignorando la puntuación "
                "de alrededor), o `None`. «GUIA!» coincide con `guia`; «guiaremos» no.",
                """
import re

def respuesta(comentario, reglas):
    pass
""",
                """
import re

def respuesta(comentario, reglas):
    palabras = re.findall(r"\\w+", comentario.lower())
    for palabra, mensaje in reglas:
        if palabra.lower() in palabras:
            return mensaje
    return None
""",
                """
reglas = [("guia", "Aquí tienes la guía: enlace"), ("demo", "Te envío la demo: enlace")]
assert respuesta("¡GUIA! por favor", reglas) == "Aquí tienes la guía: enlace"
assert respuesta("quiero la demo y la guia", reglas) == "Aquí tienes la guía: enlace", "gana la primera regla de la lista"
assert respuesta("Nos guiaremos por esto", reglas) is None, "guiaremos no es la palabra guia"
assert respuesta("Demo", reglas) == "Te envío la demo: enlace"
assert respuesta("", reglas) is None
""",
                hint="re.findall(r\"\\w+\", texto.lower()) devuelve la lista de palabras sin la puntuación.",
            ),
            quiz(
                "mku-quiz-comentarios", "La primera hora de comentarios", SK_REDES,
                "Tu vídeo empieza a recibir comentarios y preguntas. ¿Qué haces?",
                [
                    "Ignorarlos: el algoritmo solo mira las visualizaciones",
                    "Responder pronto, con respuestas que inviten a seguir conversando, y apuntar las preguntas como ideas de vídeos",
                    "Responder a todos con un emoji",
                    "Borrar los que no te gustan",
                ],
                1,
                "Responder genera más conversación (una señal positiva), crea relación con tu audiencia y te da ideas de contenido.",
            ),
            quiz(
                "mku-quiz-colab", "Una buena colaboración", SK_REDES,
                "¿Qué colaboración tiene más sentido para tu cuenta de IA y startups?",
                [
                    "Con una cuenta muy grande de cualquier tema",
                    "Con un creador de un nicho cercano (emprendimiento, productividad, programación) y tamaño parecido, con un formato que aporte "
                    "a las dos audiencias",
                    "Con cuentas que venden seguidores",
                    "Con nadie: colaborar resta seguidores",
                ],
                1,
                "La colaboración funciona cuando las audiencias se interesan por los dos temas y ambos creadores aportan algo.",
            ),
            quiz(
                "mku-quiz-automatizar", "Automatizar con ética", SK_REDES,
                "Usas una herramienta de mensajes automáticos. ¿Qué es correcto?",
                [
                    "Enviar mensajes masivos a personas que no te han escrito",
                    "Responder automáticamente solo a quien pidió algo (por ejemplo, comentó la palabra clave), cumpliendo lo prometido y dejando "
                    "claro cómo hablar con una persona",
                    "Pedir contraseñas por mensaje",
                    "Prometer un recurso y no enviarlo para generar comentarios",
                ],
                1,
                "La automatización debe responder a quien la pidió y cumplir lo prometido. Los mensajes no solicitados son spam y las plataformas "
                "los penalizan.",
            ),
            checklist(
                "mku-check-embudo", "Tu primera automatización de comentarios", SK_REDES,
                "Monta una mecánica «comenta X y te envío Y» con un recurso útil.",
                [
                    "Preparé un recurso que de verdad aporta (una guía en PDF, una lista de prompts, un enlace a mi demo)",
                    "Elegí una palabra clave corta y fácil de escribir",
                    "Configuré la respuesta automática con una herramienta oficial o autorizada por la plataforma",
                    "Probé el flujo con otra cuenta antes de publicar",
                    "El mensaje automático entrega lo prometido y dice cómo hablar conmigo directamente",
                    "Anoté cuántas personas comentaron y cuántas abrieron el recurso",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------ bloque A
    {
        "slug": "mk-escribir",
        "title": "Escribir para que te lean",
        "summary": "Lo más importante primero, frases cortas, palabras concretas y textos pensados para el móvil: descripciones, carruseles, mensajes y propuestas.",
        "hours": 2,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mke-promedio", "Longitud media de las frases", SK_COMUNICAR,
                "Escribe `palabras_por_frase(texto)` que devuelva el número medio de palabras por frase, redondeado a 1 decimal. Las frases se "
                "separan por `.`, `?` o `!`; ignora las vacías. Si no hay frases, devuelve `0.0`.",
                """
import re

def palabras_por_frase(texto):
    pass
""",
                """
import re

def palabras_por_frase(texto):
    frases = [f for f in re.split(r"[.?!]", texto) if f.strip()]
    if not frases:
        return 0.0
    return round(sum(len(f.split()) for f in frases) / len(frases), 1)
""",
                """
assert palabras_por_frase("La IA predice. No piensa. Úsala bien.") == 2.3, "7 palabras en 3 frases"
assert palabras_por_frase("¿Qué es un agente? Una IA que usa herramientas para hacer tareas.") == 6.0, "4 + 8 palabras en 2 frases"
assert palabras_por_frase("") == 0.0
assert palabras_por_frase("...") == 0.0
""",
            ),
            quiz(
                "mke-quiz-primero", "Lo importante primero", SK_COMUNICAR,
                "Escribes a un posible cliente. ¿Qué inicio es mejor?",
                [
                    "«Hola, espero que estés bien. Me llamo Alejandro, estudié desarrollo web y desde hace un tiempo me interesa la IA...»",
                    "«Puedo hacer que tu tienda responda los mensajes de WhatsApp en segundos con IA. Te cuento cómo en 3 líneas.»",
                    "«Te escribo para comentarte algunas cosas»",
                    "«¿Tienes un minuto?»",
                ],
                1,
                "En el móvil la gente decide en la primera línea si sigue leyendo. Lo que le importa al lector va primero; tu presentación, después.",
            ),
            quiz(
                "mke-quiz-concreto", "Concreto frente a vago", SK_COMUNICAR,
                "¿Qué frase comunica mejor?",
                [
                    "«Optimizamos procesos empresariales mediante soluciones innovadoras de IA»",
                    "«Un asistente que responde las preguntas de tus clientes a las 3 de la mañana, con la información de tu tienda»",
                    "«Transformación digital inteligente»",
                    "«Sinergias de alto impacto»",
                ],
                1,
                "Las palabras concretas crean una imagen y se entienden al instante. Las abstractas suenan bien y no dicen nada.",
            ),
            quiz(
                "mke-quiz-recortar", "Recortar", SK_COMUNICAR,
                "¿Cuál es la versión más clara de «Es importante tener en cuenta que, a la hora de utilizar herramientas de IA, es fundamental "
                "revisar la información que se genera»?",
                ["La original", "«Revisa siempre lo que genera la IA.»", "«Es fundamental tener en cuenta la revisión»", "«La IA genera información»"],
                1,
                "Quitar las muletillas («es importante tener en cuenta que», «a la hora de») y usar un verbo directo deja la idea en 6 palabras.",
            ),
            checklist(
                "mke-check-texto", "Revisa un texto tuyo", SK_COMUNICAR,
                "Elige un texto real (la descripción de un vídeo, una propuesta o tu biografía) y revísalo.",
                [
                    "La primera frase dice lo más importante para el lector",
                    "Las frases tienen menos de 20 palabras de media",
                    "Quité muletillas y relleno («es importante destacar que», «a la hora de»)",
                    "Cambié palabras abstractas por ejemplos concretos",
                    "Lo leí en el móvil: hay párrafos cortos y se entiende de un vistazo",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-storytelling",
        "title": "Storytelling y propuesta de valor",
        "summary": "Contar historias que enganchan (situación, conflicto, resolución), beneficios frente a características y tu propuesta en una frase.",
        "hours": 2,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mks-propuesta", "Tu propuesta en una frase", SK_COMUNICAR,
                "Escribe `propuesta(publico, resultado, obstaculo)` que devuelva la frase `'Ayudo a {publico} a {resultado} sin {obstaculo}.'`, "
                "quitando los espacios sobrantes de cada parte. Si alguna parte queda vacía, lanza `ValueError`. Si el texto final tiene más de "
                "20 palabras, lanza también `ValueError` (una propuesta debe ser corta).",
                """
def propuesta(publico, resultado, obstaculo):
    pass
""",
                """
def propuesta(publico, resultado, obstaculo):
    partes = [publico.strip(), resultado.strip(), obstaculo.strip()]
    if not all(partes):
        raise ValueError("faltan partes de la propuesta")
    frase = "Ayudo a %s a %s sin %s." % tuple(partes)
    if len(frase.split()) > 20:
        raise ValueError("la propuesta es demasiado larga")
    return frase
""",
                """
assert propuesta(" pequeñas tiendas ", "responder a sus clientes al instante", "contratar más personal") == \\
    "Ayudo a pequeñas tiendas a responder a sus clientes al instante sin contratar más personal."
for malo in [("", "x", "y"), ("a", "   ", "y")]:
    try:
        propuesta(*malo)
        raise AssertionError("debía lanzar ValueError")
    except ValueError:
        pass
try:
    propuesta("dueños de pequeños y medianos negocios de toda Latinoamérica", "automatizar absolutamente todas sus tareas repetitivas diarias", "saber programar nada")
    raise AssertionError("debía lanzar ValueError por ser demasiado larga")
except ValueError:
    pass
""",
            ),
            quiz(
                "mks-quiz-beneficio", "Beneficio frente a característica", SK_COMUNICAR,
                "¿Cuál es un **beneficio** (y no una característica) de un chatbot con RAG para una clínica?",
                [
                    "«Usa embeddings y una base de datos vectorial»",
                    "«Responde 24 horas las dudas de los pacientes sobre horarios y preparación, y libera a la recepción»",
                    "«Está hecho con FastAPI»",
                    "«Tiene 4 000 líneas de código»",
                ],
                1,
                "La característica dice qué es; el beneficio, qué gana el cliente. Se vende con beneficios; las características son la prueba.",
            ),
            quiz(
                "mks-quiz-conflicto", "La parte que engancha", SK_COMUNICAR,
                "En una historia (situación, conflicto, resolución), ¿qué parte mantiene la atención?",
                [
                    "La situación inicial, cuanto más larga mejor",
                    "El conflicto: el problema, la dificultad o la tensión que quieres ver resuelta",
                    "La lista de herramientas usadas",
                    "Los agradecimientos",
                ],
                1,
                "Sin conflicto no hay historia. Es lo que hace que quieras saber cómo termina.",
            ),
            quiz(
                "mks-quiz-historia", "Contar un caso", SK_COMUNICAR,
                "¿Qué inicio de un vídeo sobre un proyecto engancha más?",
                [
                    "«En este proyecto usé Python, FastAPI y PostgreSQL»",
                    "«La dueña de esta tienda pasaba 3 horas al día respondiendo las mismas 10 preguntas. Un día perdió una venta grande por no "
                    "contestar a tiempo.»",
                    "«Hoy os enseño un proyecto»",
                    "«Primero, un poco de contexto sobre mí»",
                ],
                1,
                "Empieza por una persona con un problema concreto: el público se identifica y quiere saber la solución.",
            ),
            checklist(
                "mks-check-historia", "Tu historia y tu propuesta", SK_COMUNICAR,
                "Escribe en Apuntes tu propuesta de valor y una historia corta de un proyecto (real o de tu demo).",
                [
                    "Mi propuesta cabe en una frase: a quién ayudo, a qué y sin qué",
                    "La historia tiene un protagonista concreto (un cliente, un usuario o yo)",
                    "Tiene un conflicto claro y un resultado, con un número si es posible",
                    "Hablé de beneficios y usé las características solo como prueba",
                    "La conté en voz alta en menos de un minuto",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "mk-hablar",
        "title": "Hablar a cámara y en videollamadas",
        "summary": "Voz, ritmo, pausas y nervios; lenguaje corporal en cámara; y cómo presentar una demo o responder objeciones en una llamada con un cliente.",
        "hours": 2,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mkh-ritmo", "Tu velocidad al hablar", SK_COMUNICAR,
                "Escribe `ritmo(palabras, segundos)` que devuelva una tupla `(palabras_por_minuto, etiqueta)`. Las palabras por minuto se "
                "redondean al entero más cercano. La etiqueta es `'lento'` por debajo de 130, `'rapido'` por encima de 170 y `'normal'` en otro "
                "caso. Si `segundos` es 0 o menos, lanza `ValueError`.",
                """
def ritmo(palabras, segundos):
    pass
""",
                """
def ritmo(palabras, segundos):
    if segundos <= 0:
        raise ValueError("la duración debe ser positiva")
    ppm = round(palabras / segundos * 60)
    if ppm < 130:
        etiqueta = "lento"
    elif ppm > 170:
        etiqueta = "rapido"
    else:
        etiqueta = "normal"
    return ppm, etiqueta
""",
                """
assert ritmo(150, 60) == (150, "normal")
assert ritmo(100, 60) == (100, "lento")
assert ritmo(120, 40) == (180, "rapido")
assert ritmo(130, 60) == (130, "normal"), "130 justo es normal"
try:
    ritmo(10, 0)
    raise AssertionError("debía lanzar ValueError")
except ValueError:
    pass
""",
            ),
            quiz(
                "mkh-quiz-nervios", "Los nervios", SK_COMUNICAR,
                "Te pones nervioso al grabarte y suenas acelerado. ¿Qué ayuda más?",
                [
                    "Grabar todo de una sola toma sin guion",
                    "Preparar la estructura, grabar frase por frase, hacer pausas a propósito y practicar con varios vídeos: los nervios bajan con la repetición",
                    "Hablar todavía más rápido para terminar antes",
                    "No grabar nunca tu cara",
                ],
                1,
                "La preparación y la repetición reducen los nervios. Las pausas, además, dan claridad y te hacen sonar seguro.",
            ),
            quiz(
                "mkh-quiz-demo", "Presentar una demo", SK_COMUNICAR,
                "Vas a enseñar tu chatbot a un posible cliente en una videollamada. ¿Cómo lo estructuras?",
                [
                    "Explicar primero toda la arquitectura técnica",
                    "Recordar su problema, enseñar la demo resolviendo un caso suyo, mostrar el resultado y preguntar qué le parece",
                    "Leer el código en voz alta",
                    "Enseñar todas las funciones posibles, aunque no le importen",
                ],
                1,
                "Una demo convence cuando el cliente ve su problema resuelto. La técnica, solo si la pregunta.",
            ),
            quiz(
                "mkh-quiz-objecion", "Responder una objeción", SK_COMUNICAR,
                "El cliente dice: «¿Y si la IA responde algo incorrecto a mis clientes?». ¿Qué respondes?",
                [
                    "«Eso nunca pasa»",
                    "«Es una preocupación lógica. Por eso responde solo con tu información, cita la fuente y, si no sabe algo, lo pasa a una persona. "
                    "Además, revisamos las conversaciones las primeras semanas.»",
                    "«Bueno, ya veremos»",
                    "Cambiar de tema",
                ],
                1,
                "Valida la preocupación, explica cómo se controla el riesgo y da un plan concreto. Negar el riesgo destruye la confianza.",
            ),
            checklist(
                "mkh-check-practica", "Practica tu presentación", SK_COMUNICAR,
                "Grábate presentándote y explicando tu demo (2 minutos) y revisa la grabación.",
                [
                    "Miré al objetivo de la cámara la mayor parte del tiempo",
                    "Mi ritmo está entre 130 y 170 palabras por minuto",
                    "Hice pausas después de las ideas importantes",
                    "Eliminé muletillas repetidas («eh», «o sea», «básicamente»)",
                    "Empecé por el problema del cliente y terminé con una pregunta o un siguiente paso",
                ],
            ),
        ],
    },
]
