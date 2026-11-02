from ._helpers import choice, dictation, fill, listen, speak, translate

UNITS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-fl-1",
        "level": "A2",
        "focus": "freelance",
        "title": "Your first message to a client",
        "summary": "Escribir una propuesta corta y amable en inglés: saludo, entender el problema, ofrecer ayuda y una pregunta.",
        "minutes": 30,
        "lesson": r"""
# Your first message to a client

En Upwork y en las agencias internacionales, tu primer mensaje decide si te responden. Debe ser **corto, claro y específico**.
Estructura de 5 líneas:

1. **Greeting:** *Hi Sarah,*
2. **Show you understand:** *I read your post. You need a chatbot that answers customer questions on WhatsApp.*
3. **Offer + proof:** *I can help you with that. I recently built a similar assistant: [link].*
4. **One smart question:** *Do the answers need to come from your product catalog?*
5. **Closing:** *Best regards, Alejandro*

## Peticiones educadas: *can / could / would*

| Directo (suena brusco) | Educado |
|---|---|
| Send me the file. | **Could you** send me the file? |
| I want to know your budget. | **Would you** mind sharing your budget? |
| Tell me when. | **Can you** let me know when it works for you? |

*Could* y *would* son más formales que *can*. En un primer mensaje, úsalos.

## Palabras de cliente que verás mucho

*budget* (presupuesto), *deadline* (fecha límite), *quote* (cotización), *milestone* (hito), *deliverable* (entregable),
*hourly rate* (tarifa por hora), *fixed price* (precio cerrado).

## Errores típicos

| Incorrecto | Correcto |
|---|---|
| I can help you with this **proyect**. | I can help you with this **project**. |
| I have **experience in** chatbots. | I have experience **building** chatbots. |
| **Dear Sir**, (a todo el mundo) | **Hi + nombre**, es lo normal en plataformas |
""",
        "phrases": [
            ("I read your post, and I can help you with that.", "Leí tu publicación y puedo ayudarte con eso."),
            ("I recently built a similar assistant for an online store.", "Hace poco construí un asistente parecido para una tienda en línea."),
            ("Could you share a few examples of the questions your customers ask?", "¿Podrías compartir algunos ejemplos de las preguntas que hacen tus clientes?"),
            ("Would you mind sharing your budget?", "¿Te importaría compartir tu presupuesto?"),
            ("Can you let me know when it works for you?", "¿Puedes decirme cuándo te viene bien?"),
            ("Best regards,", "Saludos cordiales,"),
        ],
        "exercises": [
            listen("fl1-listen-1",
                   "Hi Sarah, I read your post. You need a chatbot that answers customer questions on WhatsApp. "
                   "I recently built a similar assistant for an online store. Do the answers need to come from your product catalog?",
                   "¿Qué pregunta hace el freelancer al final?",
                   ["Cuál es el presupuesto", "Si las respuestas deben salir del catálogo de productos",
                    "Cuándo es la fecha límite", "Si puede usar otra plataforma"], 1,
                   "Una pregunta concreta al final demuestra que entendiste el problema."),
            fill("fl1-fill-1", "___ you send me a few examples of customer questions?", ["could", "can", "would"],
                 "¿Podrías enviarme algunos ejemplos de preguntas de clientes?",
                 "Peticiones educadas: *Could you...? / Can you...? / Would you...?*"),
            fill("fl1-fill-2", "I have experience ___ chatbots for small businesses.", ["building", "creating", "developing"],
                 "Tengo experiencia construyendo chatbots para pequeños negocios.",
                 "Después de *experience* va un verbo en **-ing**: *experience building*."),
            choice("fl1-choice-1", "¿Qué significa *quote* en un mensaje de un cliente?",
                   ["Una cita textual", "Una cotización o presupuesto", "Una reunión", "Una factura pagada"], 1,
                   "*Could you send me a quote?* = ¿Podrías enviarme una cotización?"),
            choice("fl1-choice-2", "¿Cuál es el saludo más natural para un cliente en Upwork que se llama Mark?",
                   ["Dear Sir,", "Hi Mark,", "Hello Mr. Client,", "Hey bro,"], 1,
                   "En plataformas y startups lo normal es *Hi + nombre*. Es amable y profesional."),
            translate("fl1-tr-1", "Leí tu publicación y puedo ayudarte con eso.",
                      ["I read your post, and I can help you with that.", "I read your post and I can help you with that.",
                       "I read your post and can help you with that."],
                      "*read* en pasado se escribe igual, pero se pronuncia «red»."),
            dictation("fl1-dict-1", "Would you mind sharing your budget?", "¿Te importaría compartir tu presupuesto?"),
            speak("fl1-speak-1", "Lee en voz alta.", "I recently built a similar assistant for an online store."),
            speak("fl1-speak-2", "Di en inglés: «¿Puedes decirme cuándo te viene bien?»", "Can you let me know when it works for you?",
                  ["Could you let me know when it works for you?"], show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-fl-2",
        "level": "B1",
        "focus": "freelance",
        "title": "The discovery call",
        "summary": "La primera llamada con un cliente: preguntas para entender el problema, el proceso actual y cómo medirán el éxito.",
        "minutes": 40,
        "lesson": r"""
# The discovery call

En la primera llamada (*discovery call*) tu objetivo no es venderte, sino **entender el problema mejor que nadie**.
Quien hace buenas preguntas parece (y es) más experto. Prepara preguntas en cuatro bloques:

## 1. El problema
- *What problem are you trying to solve?*
- *What happens today when a customer asks a question?*

## 2. El proceso actual
- *How do you **currently** handle this?*
- *How many requests do you get **per day**?*
- *Which tools does your team **use**?* (WhatsApp, Shopify, Google Sheets...)

## 3. El éxito
- *What would success look like in three months?*
- *How will you measure it?*

## 4. Las restricciones
- *Do you have a deadline?*  *Is there a budget range you have in mind?*
- *Who else needs to approve this?*

## Gramática: preguntas con *do / does*

En presente simple, las preguntas llevan **do** (o **does** con *he/she/it*) y el verbo en forma base:
*How many messages **do** you **get**?* — *How **does** your team **handle** returns?*
Error típico: ~~How many messages you get?~~

## Confirmar lo que entendiste

*"So, if I understand correctly, you want ... Is that right?"* Resumir al final de la llamada evita malentendidos
y le demuestra al cliente que le escuchaste.
""",
        "phrases": [
            ("What problem are you trying to solve?", "¿Qué problema intentas resolver?"),
            ("How do you currently handle customer questions?", "¿Cómo gestionáis actualmente las preguntas de los clientes?"),
            ("How many requests do you get per day?", "¿Cuántas solicitudes recibís al día?"),
            ("What would success look like in three months?", "¿Cómo sería el éxito dentro de tres meses?"),
            ("So, if I understand correctly, you want to reduce response time. Is that right?", "Entonces, si entiendo bien, queréis reducir el tiempo de respuesta. ¿Es así?"),
            ("Who else needs to approve this project?", "¿Quién más tiene que aprobar este proyecto?"),
        ],
        "exercises": [
            listen("fl2-listen-1",
                   "Right now, two people answer all the messages by hand. We get around one hundred and fifty questions a day, "
                   "and most of them are about shipping times and returns.",
                   "¿Sobre qué tratan la mayoría de las preguntas?",
                   ["Precios y descuentos", "Tiempos de envío y devoluciones", "Problemas técnicos", "Horarios de la tienda"], 1,
                   "*most of them are about shipping times and returns*"),
            listen("fl2-listen-2",
                   "Success for us would be answering at least seventy percent of the questions automatically, "
                   "without making customers angry.",
                   "¿Cómo define el cliente el éxito?",
                   ["Despedir al equipo", "Responder automáticamente al menos el 70 % de las preguntas sin enfadar a los clientes",
                    "Vender un 70 % más", "Responder en menos de un minuto"], 1, ""),
            fill("fl2-fill-1", "How many messages ___ you get per day?", ["do"],
                 "¿Cuántos mensajes recibís al día?",
                 "Pregunta en presente simple: *How many ... **do** you get?*"),
            fill("fl2-fill-2", "How ___ your team handle returns today?", ["does"],
                 "¿Cómo gestiona tu equipo las devoluciones hoy?",
                 "*your team* = *it* → **does**, y el verbo queda en forma base (*handle*)."),
            choice("fl2-choice-1", "¿Cuál es la pregunta correcta?",
                   ["How many requests you get per day?", "How many requests do you get per day?",
                    "How many requests are you get per day?", "How many requests you are getting per day?"], 1,
                   "Las preguntas en presente simple necesitan *do/does*."),
            translate("fl2-tr-1", "¿Cómo sería el éxito dentro de tres meses?",
                      ["What would success look like in three months?", "What would success look like three months from now?"],
                      "*What would success look like...?* es una expresión muy usada para hablar de objetivos."),
            dictation("fl2-dict-1", "So, if I understand correctly, you want to reduce response time.",
                      "Entonces, si entiendo bien, queréis reducir el tiempo de respuesta."),
            speak("fl2-speak-1", "Lee en voz alta.", "How do you currently handle customer questions?"),
            speak("fl2-speak-2", "Di en inglés: «¿Quién más tiene que aprobar este proyecto?»", "Who else needs to approve this project?",
                  ["Who else has to approve this project?"], show_target=False),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "en-fl-3",
        "level": "B2",
        "focus": "freelance",
        "title": "Scope, price and saying no politely",
        "summary": "Presentar un precio con confianza, defender el alcance y negociar sin perder al cliente.",
        "minutes": 45,
        "lesson": r"""
# Scope, price and saying no politely

Con clientes internacionales, cómo dices las cosas importa tanto como lo que dices. La regla: **firme en el fondo, amable en la forma**.

## Presentar el precio con confianza

- *"Based on what you described, the project would take about three weeks. The price is $1,200, split into three milestones."*
- No te disculpes por tu precio (~~"Sorry, it's a bit expensive..."~~). Explica **qué incluye**.

## Defender el alcance (*scope*)

Cuando piden algo extra "ya que estás":
- *"That's a great idea. It's outside the current scope, but I'd be happy to send you a quote for it."*
- *"We can include it, but it would push the delivery date by a week. Would that work for you?"*

## Decir que no, sin decir "no"

| Brusco | Profesional |
|---|---|
| No, I can't do that. | I'm afraid that won't be possible within this budget. |
| That's not my problem. | That falls outside what we agreed, but here's what I can do... |
| You're wrong. | I see your point. However, ... |

## Gramática: condicionales para negociar

- **Primer condicional** (posibilidad real): *If you **approve** the quote today, I **can start** on Monday.*
- **Segundo condicional** (opción hipotética, más suave): *If we **removed** the dashboard, the price **would be** lower.*

## *I'm afraid*

*I'm afraid...* no significa "tengo miedo" en este contexto: suaviza una mala noticia (= "me temo que...").
""",
        "phrases": [
            ("It's outside the current scope, but I'd be happy to send you a quote for it.", "Está fuera del alcance actual, pero con gusto te envío una cotización."),
            ("The price is twelve hundred dollars, split into three milestones.", "El precio es de mil doscientos dólares, dividido en tres hitos."),
            ("If you approve the quote today, I can start on Monday.", "Si apruebas la cotización hoy, puedo empezar el lunes."),
            ("I'm afraid that won't be possible within this budget.", "Me temo que eso no será posible con este presupuesto."),
            ("We can include it, but it would push the delivery date by a week.", "Podemos incluirlo, pero retrasaría la entrega una semana."),
            ("I see your point. However, the tests are part of the delivery.", "Entiendo tu punto. Sin embargo, las pruebas son parte de la entrega."),
        ],
        "exercises": [
            listen("fl3-listen-1",
                   "That's a great idea. It's outside the current scope, but I'd be happy to send you a quote for it. "
                   "If you'd like, we can add it as a second phase after the launch.",
                   "¿Qué propone el freelancer?",
                   ["Hacerlo gratis", "Rechazarlo sin más", "Enviar una cotización y hacerlo como segunda fase tras el lanzamiento",
                    "Cancelar el proyecto"], 2,
                   "Convierte el pedido extra en una oportunidad: cotización aparte y segunda fase."),
            choice("fl3-choice-1", "El cliente pide reducir el precio a la mitad. ¿Qué respuesta es más profesional?",
                   ["No way.", "OK, no problem.",
                    "I'm afraid that won't be possible for the full scope. If we removed the dashboard, the price would be lower.",
                    "You're wrong, my price is fair."], 2,
                   "Mantienes el valor y ofreces una alternativa reduciendo el alcance."),
            fill("fl3-fill-1", "If you approve the quote today, I ___ start on Monday.", ["can", "will", "could"],
                 "Si apruebas la cotización hoy, puedo empezar el lunes.",
                 "Primer condicional: *If + presente, can/will + verbo*."),
            fill("fl3-fill-2", "If we removed the dashboard, the price ___ be lower.", ["would"],
                 "Si quitáramos el dashboard, el precio sería más bajo.",
                 "Segundo condicional: *If + pasado, **would** + verbo*."),
            choice("fl3-choice-2", "En *\"I'm afraid we can't deliver by Friday\"*, *I'm afraid* significa:",
                   ["Tengo miedo", "Me temo que (suaviza una mala noticia)", "Estoy preocupado por ti", "No estoy seguro"], 1,
                   "Es una fórmula de cortesía muy común en el trabajo."),
            translate("fl3-tr-1", "Podemos incluirlo, pero retrasaría la entrega una semana.",
                      ["We can include it, but it would push the delivery date by a week.",
                       "We can include it, but it would delay the delivery by a week.",
                       "We can include it, but it would delay delivery by one week.",
                       "We can include it, but it would push the delivery by a week."],
                      "*push (back) / delay* = retrasar."),
            dictation("fl3-dict-1", "I'm afraid that won't be possible within this budget.",
                      "Me temo que eso no será posible con este presupuesto."),
            speak("fl3-speak-1", "Lee en voz alta, con tono amable y seguro.",
                  "It's outside the current scope, but I'd be happy to send you a quote for it."),
            speak("fl3-speak-2", "Di en inglés: «Entiendo tu punto. Sin embargo, las pruebas son parte de la entrega».",
                  "I see your point. However, the tests are part of the delivery.",
                  ["I understand your point. However, the tests are part of the delivery."], show_target=False),
        ],
    },
]
