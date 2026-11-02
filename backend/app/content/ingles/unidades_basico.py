"""Bloque A1: las bases (to be, presente simple, preguntas, números, fechas y pasado simple), siempre en contexto de trabajo."""
from ._helpers import choice, dictation, fill, listen, speak, translate

UNITS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-a1-1",
        "level": "A1",
        "focus": "entrevistas",
        "title": "Hello, I'm a developer",
        "summary": "El verbo to be (am, is, are), a/an y cómo decir quién eres, de dónde eres y a qué te dedicas.",
        "minutes": 35,
        "lesson": r"""
# Hello, I'm a developer

El verbo **to be** (ser / estar) es el más importante del inglés. Con él dices quién eres, de dónde eres y a qué te dedicas.
En español cambia mucho (soy, eres, es, somos...); en inglés solo tiene **tres formas en presente: am, is, are**.

## To be en presente

| Sujeto | Completo | Contraído (lo normal al hablar) |
|---|---|---|
| I (yo) | I **am** | I**'m** |
| you (tú / ustedes) | you **are** | you**'re** |
| he / she / it (él / ella / eso) | he **is** | he**'s** |
| we (nosotros) | we **are** | we**'re** |
| they (ellos) | they **are** | they**'re** |

- **Negativo:** añade *not* → *I'm **not** a designer. She **isn't** here. They **aren't** ready.*
- **Pregunta:** pon el verbo delante → ***Are** you a developer? **Is** she from Mexico?*
- **Respuesta corta:** *Yes, I am. / No, I'm not.*

## En inglés el sujeto es obligatorio

En español decimos «Soy desarrollador». En inglés **siempre** hay sujeto: ***I** am a developer.* (nunca ~~Am a developer~~).
Para cosas se usa **it**: *It **is** a good project.*

## A / an con las profesiones

En inglés la profesión lleva artículo: *I'm **a** developer.* Se usa **an** si la palabra siguiente **suena** a vocal:
*an engineer, an analyst, an AI project* (AI suena «ei-ai»).

## Frases para presentarte

- *Hello, my name is ... / Hi, I'm ...*
- *I'm **from** Venezuela. I live **in** Caracas.*
- *I'm a web developer.*
- *Where are you from?* (¿De dónde eres?) — *What do you do?* (¿A qué te dedicas?)

**Consejo:** escucha cada frase clave en modo 🐢, repítela en voz alta tres veces y después a velocidad normal.
""",
        "phrases": [
            ("Hello, my name is Alex. I'm a web developer.", "Hola, me llamo Alex. Soy desarrollador web."),
            ("I'm from Venezuela. I live in Caracas.", "Soy de Venezuela. Vivo en Caracas."),
            ("Where are you from?", "¿De dónde eres?"),
            ("What do you do? I'm an engineer.", "¿A qué te dedicas? Soy ingeniero."),
            ("She isn't here today.", "Ella no está hoy."),
            ("Are you ready? Yes, I am.", "¿Estás listo? Sí, lo estoy."),
        ],
        "exercises": [
            choice("a11-choice-1", "She ___ a designer.", ["am", "is", "are", "be"], 1,
                   "Con *he / she / it* se usa **is**: *She **is** a designer.*"),
            fill("a11-fill-1", "I ___ from Venezuela.", ["am", "'m"], "Soy de Venezuela.",
                 "Con *I* siempre **am**: *I **am** (I'm) from Venezuela.*"),
            fill("a11-fill-2", "They ___ developers.", ["are", "'re"], "Ellos son desarrolladores.",
                 "Con *we / you / they* se usa **are**."),
            choice("a11-choice-2", "I'm ___ engineer.", ["a", "an", "the", "—"], 1,
                   "*engineer* empieza con sonido de vocal, así que va **an**."),
            choice("a11-choice-3", "¿Cuál es correcta?", ["Am a developer.", "I am developer.", "I am a developer.", "I a developer."], 2,
                   "Necesitas sujeto (*I*), verbo (*am*) y artículo (*a*)."),
            listen("a11-listen-1", "Hello, my name is Ana. I am from Mexico. I am a data analyst.",
                   "¿De dónde es Ana?", ["De Venezuela", "De México", "De España", "De Colombia"], 1,
                   "*I am from Mexico.*"),
            translate("a11-tr-1", "Soy desarrollador web.",
                      ["I am a web developer.", "I'm a web developer."],
                      "Sujeto + *am* + *a* + profesión."),
            dictation("a11-dict-1", "I am a developer from Venezuela.", "Soy un desarrollador de Venezuela."),
            speak("a11-speak-1", "Lee en voz alta (primero escucha el modelo en 🐢).", "Hello, I'm a web developer from Venezuela."),
            speak("a11-speak-2", "Di en inglés: «¿De dónde eres?»", "Where are you from?", show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-a1-2",
        "level": "A1",
        "focus": "equipo",
        "title": "My work day",
        "summary": "El presente simple (I work, she works, do / does, don't), los días de la semana y las horas.",
        "minutes": 40,
        "lesson": r"""
# My work day

El **presente simple** sirve para hablar de rutinas y cosas que haces normalmente: *I **work** from home. We **have** a meeting every Monday.*

## Afirmativo: la -s de he / she / it

| Sujeto | Verbo |
|---|---|
| I / you / we / they | **work**, **start**, **have** |
| he / she / it | work**s**, start**s**, **has** (irregular) |

*I write code every day. → She write**s** code every day.*

## Negativo y preguntas: do / does

- **Negativo:** *I **don't** work on Sundays. He **doesn't** use Windows.*
- **Pregunta:** ***Do** you work from home? **Does** she speak English?*
- **Respuesta corta:** *Yes, I do. / No, I don't. — Yes, she does. / No, she doesn't.*

Ojo: con *does / doesn't* el verbo **pierde la -s**: *Does she **work**...?* (no ~~Does she works~~).

## Días y horas

- **Días** (siempre con mayúscula y con **on**): *on Monday, on Tuesday, on Wednesday, on Thursday, on Friday, on Saturday, on Sunday.*
- **Horas** (con **at**): *at nine o'clock (9:00), at nine thirty (9:30), at five p.m.*
- **Partes del día** (con **in**): *in the morning, in the afternoon, in the evening.*

## Verbos de un día de trabajo

*start work* (empezar a trabajar) · *check my email* (revisar el correo) · *have a meeting* (tener una reunión) ·
*write code* (escribir código) · *have lunch* (almorzar) · *finish work* (terminar de trabajar)

**Consejo:** describe tu propio día en voz alta con estas frases. Es la base del *standup* de la unidad siguiente.
""",
        "phrases": [
            ("I start work at nine o'clock.", "Empiezo a trabajar a las nueve."),
            ("I check my email in the morning.", "Reviso mi correo por la mañana."),
            ("We have a meeting on Monday.", "Tenemos una reunión el lunes."),
            ("She works from home.", "Ella trabaja desde casa."),
            ("I don't work on Sundays.", "No trabajo los domingos."),
            ("Do you work from home? Yes, I do.", "¿Trabajas desde casa? Sí."),
        ],
        "exercises": [
            fill("a12-fill-1", "I ___ work at nine o'clock.", ["start", "begin"], "Empiezo a trabajar a las nueve.",
                 "Con *I* el verbo va sin -s: *I **start***."),
            fill("a12-fill-2", "He ___ code every day.", ["writes"], "Él escribe código todos los días.",
                 "Con *he / she / it* el verbo lleva **-s**: *write → writes*."),
            choice("a12-choice-1", "Do you work on Saturday?", ["No, I don't.", "No, I not.", "No, I doesn't.", "No, I am not work."], 0,
                   "Respuesta corta con *do*: *Yes, I do. / No, I don't.*"),
            choice("a12-choice-2", "___ she speak English?", ["Do", "Does", "Is", "Are"], 1,
                   "Pregunta en presente simple con *she* → **Does**."),
            choice("a12-choice-3", "¿Qué día va después de *Tuesday*?", ["Monday", "Thursday", "Wednesday", "Friday"], 2,
                   "Monday, Tuesday, **Wednesday**, Thursday, Friday, Saturday, Sunday."),
            listen("a12-listen-1", "I start work at eight thirty. I have a meeting with my team at ten. I finish at five.",
                   "¿A qué hora es la reunión?", ["A las 8:30", "A las 10:00", "A las 5:00", "A las 2:00"], 1,
                   "*I have a meeting with my team at ten.*"),
            translate("a12-tr-1", "No trabajo los domingos.",
                      ["I don't work on Sundays.", "I do not work on Sundays.", "I don't work on Sunday."],
                      "Negativo con *don't* + verbo. Los días llevan *on* y mayúscula."),
            dictation("a12-dict-1", "We have a meeting on Monday morning.", "Tenemos una reunión el lunes por la mañana."),
            speak("a12-speak-1", "Lee en voz alta.", "I start work at nine and I finish at five."),
            speak("a12-speak-2", "Di en inglés: «Ella trabaja desde casa».", "She works from home.", show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-a1-3",
        "level": "A1",
        "focus": "freelance",
        "title": "Questions, numbers and dates",
        "summary": "Hacer preguntas (what, when, how much...), decir precios y números, y hablar de fechas y plazos.",
        "minutes": 40,
        "lesson": r"""
# Questions, numbers and dates

Con un cliente necesitas preguntar y entender **precios, cantidades y fechas**. Con estas palabras ya puedes mantener una conversación básica.

## Palabras para preguntar

| Inglés | Español | Ejemplo |
|---|---|---|
| What | qué / cuál | *What do you need?* |
| When | cuándo | *When is the deadline?* |
| Where | dónde | *Where is the file?* |
| Who | quién | *Who is the project manager?* |
| Why | por qué | *Why do you need a chatbot?* |
| How | cómo | *How does it work?* |
| How much | cuánto (precio, sin contar) | *How much is it?* |
| How many | cuántos (cosas que se cuentan) | *How many users do you have?* |

## Pedir algo: Can you...?

*Can you send me the file? — Can we have a call on Thursday?* La respuesta: *Yes, sure. / Sorry, I can't.*

## Números y precios

- *13 thirteen* y *30 thirty* suenan parecido: en *thir**TEEN*** el acento va al final; en ***THIR**ty*, al principio.
- *100 one hundred · 250 two hundred **and** fifty · 1,000 one thousand · 1,500 one thousand five hundred*.
- *$400* se dice *four hundred dollars* (el símbolo va delante, pero se dice al final).

## Fechas

- **Meses** (con mayúscula): *January, February, March, April, May, June, July, August, September, October, November, December.*
- **Días del mes** con ordinales: *first (1st), second (2nd), third (3rd), fifth (5th), fifteenth (15th), twentieth (20th)*.
  *The deadline is **on** March 15th* («March fifteenth»).
- **Plazos:** *by Friday* (para el viernes, como muy tarde) · *next week* (la semana que viene) · *in two days* (en dos días).
""",
        "phrases": [
            ("How much is it?", "¿Cuánto cuesta?"),
            ("When is the deadline?", "¿Cuándo es la fecha límite?"),
            ("How many users do you have?", "¿Cuántos usuarios tienes?"),
            ("Can you send me the file?", "¿Puedes enviarme el archivo?"),
            ("The project costs four hundred dollars.", "El proyecto cuesta cuatrocientos dólares."),
            ("I can finish it by Friday.", "Puedo terminarlo para el viernes."),
        ],
        "exercises": [
            choice("a13-choice-1", "Quieres preguntar el precio. ___ is it?", ["How many", "How much", "What time", "Where"], 1,
                   "El precio se pregunta con **How much**."),
            fill("a13-fill-1", "___ is the deadline? — On Friday.", ["when"], "¿Cuándo es la fecha límite? — El viernes.",
                 "Para preguntar por un momento: **When**."),
            fill("a13-fill-2", "How ___ hours do you need?", ["many"], "¿Cuántas horas necesitas?",
                 "*hours* se pueden contar → **How many**."),
            choice("a13-choice-2", "¿Cómo se dice *$250*?", ["two hundred fifty dollar", "two hundred and fifty dollars", "dollars two hundred fifty", "two fifty hundred dollars"], 1,
                   "*two hundred **and** fifty dollars* (en plural)."),
            listen("a13-listen-1", "The project costs four hundred dollars, and the deadline is March fifteenth.",
                   "¿Cuánto cuesta el proyecto?", ["$140", "$400", "$415", "$40"], 1, "*four hundred dollars* = $400."),
            listen("a13-listen-2", "Can we have a call on Thursday at two p.m.?",
                   "¿Cuándo propone la llamada?", ["El martes a las 2 p. m.", "El jueves a las 2 p. m.", "El jueves a las 12", "El sábado a las 2 p. m."], 1,
                   "*Thursday* = jueves (no confundir con *Tuesday*, martes)."),
            translate("a13-tr-1", "¿Cuánto cuesta?", ["How much is it?", "How much does it cost?"],
                      "Las dos formas son correctas y muy comunes."),
            dictation("a13-dict-1", "The deadline is on Friday.", "La fecha límite es el viernes."),
            speak("a13-speak-1", "Lee en voz alta.", "How many hours do you need?"),
            speak("a13-speak-2", "Di en inglés: «¿Puedes enviarme el archivo?»", "Can you send me the file?",
                  ["Could you send me the file?"], show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-a1-4",
        "level": "A1",
        "focus": "tecnico",
        "title": "Yesterday at work",
        "summary": "El pasado simple (was / were, -ed, did / didn't) y los verbos más usados en el trabajo con software.",
        "minutes": 40,
        "lesson": r"""
# Yesterday at work

Para contar lo que hiciste (en el *standup*, en una entrevista o a un cliente) necesitas el **pasado simple**.
La buena noticia: en inglés **es igual para todas las personas** (I, you, she, they...).

## Was / were (pasado de to be)

*I / he / she / it **was** — you / we / they **were***
*The server **was** down yesterday. We **were** busy last week.*

## Verbos regulares: + -ed

| Presente | Pasado |
|---|---|
| work | work**ed** |
| fix | fix**ed** |
| test | test**ed** |
| deploy | deploy**ed** |
| update | updat**ed** |

## Irregulares que más usarás (apréndelos de memoria)

| Presente | Pasado | Español |
|---|---|---|
| write | **wrote** | escribir |
| send | **sent** | enviar |
| build | **built** | construir |
| make | **made** | hacer, crear |
| do | **did** | hacer |
| have | **had** | tener |
| go | **went** | ir |

## Negativo y preguntas: did / didn't

- *I **didn't** deploy the new version.* (con *didn't* el verbo vuelve a la forma base: no ~~didn't deployed~~)
- ***Did** you send the file? — Yes, I did. / No, I didn't.*

## Palabras de tiempo

*yesterday* (ayer) · *last week* (la semana pasada) · *two days ago* (hace dos días) · *this morning* (esta mañana)

## Vocabulario básico de software

*a bug / an error* (error) · *a file* (archivo) · *a folder* (carpeta) · *the screen* (pantalla) · *to save* (guardar) ·
*to download* (descargar) · *to update* (actualizar) · *a password* (contraseña)
""",
        "phrases": [
            ("Yesterday I fixed a bug.", "Ayer arreglé un error."),
            ("I sent the email this morning.", "Envié el correo esta mañana."),
            ("We built a new website last month.", "Construimos un sitio web nuevo el mes pasado."),
            ("The server was down yesterday.", "El servidor estuvo caído ayer."),
            ("I didn't deploy the new version.", "No desplegué la nueva versión."),
            ("Did you save the file? Yes, I did.", "¿Guardaste el archivo? Sí."),
        ],
        "exercises": [
            fill("a14-fill-1", "Yesterday I ___ a bug.", ["fixed", "found"], "Ayer arreglé un error.",
                 "Verbo regular en pasado: *fix → fix**ed***."),
            fill("a14-fill-2", "I ___ the email this morning.", ["sent", "wrote", "read"], "Envié el correo esta mañana.",
                 "*send* es irregular: *send → **sent***."),
            choice("a14-choice-1", "I didn't ___ the tests.", ["run", "ran", "runs", "running"], 0,
                   "Después de *didn't* el verbo va en forma base: *didn't **run***."),
            choice("a14-choice-2", "The server ___ down yesterday.", ["was", "were", "is", "be"], 0,
                   "*The server* = *it* → **was**."),
            choice("a14-choice-3", "¿Cuál es el pasado de *build*?", ["builded", "built", "build", "builted"], 1,
                   "*build → **built*** es irregular."),
            listen("a14-listen-1", "Yesterday I fixed two bugs and I wrote the documentation. I didn't deploy the new version.",
                   "¿Qué NO hizo ayer?", ["Arreglar errores", "Escribir la documentación", "Desplegar la nueva versión", "Nada, lo hizo todo"], 2,
                   "*I didn't deploy the new version.*"),
            translate("a14-tr-1", "Ayer arreglé un error.",
                      ["Yesterday I fixed a bug.", "I fixed a bug yesterday.", "Yesterday I fixed an error.", "I fixed an error yesterday."],
                      "*yesterday* puede ir al principio o al final."),
            dictation("a14-dict-1", "I didn't deploy the new version.", "No desplegué la nueva versión."),
            speak("a14-speak-1", "Lee en voz alta.", "Yesterday I fixed a bug and I tested the app."),
            speak("a14-speak-2", "Di en inglés: «¿Enviaste el archivo?»", "Did you send the file?", show_target=False),
        ],
    },
]
