# Inglés técnico para trabajar en remoto

El inglés es la habilidad que **más multiplica tus opciones**. Con el mismo nivel técnico, quien puede trabajar en inglés accede a muchas
más ofertas, a clientes de Estados Unidos y Europa en Upwork, y a salarios más altos. Y además, casi toda la documentación, los mensajes
de error, las librerías y las novedades de IA aparecen primero (o solo) en inglés.

Este capítulo no sustituye a la **vista de Inglés** de la plataforma, donde practicas escucha, vocabulario y conversación por niveles. Su
objetivo es otro: darte el **inglés específico de tu trabajo** (leer documentación, escribir en GitHub, hablar en reuniones y en
entrevistas), los errores típicos de los hispanohablantes y un plan realista para mejorar sin dejar de estudiar lo técnico.

---

## 1. Qué nivel hace falta para qué

No necesitas un inglés perfecto para empezar. Necesitas el nivel adecuado **para cada tarea**:

| Tarea | Nivel aproximado | Dificultad |
|---|---|---|
| Leer documentación y mensajes de error | A2-B1 (con ayuda del traductor) | La más fácil: vocabulario repetitivo, puedes ir a tu ritmo |
| Escribir commits, issues y mensajes de chat | B1 | Fácil: frases cortas, puedes revisarlas antes de enviar |
| Escribir propuestas y correos a clientes | B1 | Con plantillas y revisión, accesible pronto |
| Reuniones diarias del equipo | B1-B2 | Exige escuchar en tiempo real |
| Entrevistas en inglés | B2 | Lo más difícil: presión, tiempo real, preguntas abiertas |

La buena noticia: **leer y escribir** (lo que más harás en un trabajo remoto, porque casi todo es asíncrono: chat, tickets, revisiones de
código) se alcanza mucho antes que hablar con fluidez. Puedes empezar a trabajar en inglés escrito mientras mejoras la parte oral.

---

## 2. Leer documentación técnica

### Estrategia

- **Lee primero el código** de los ejemplos: muchas veces se entiende antes que el texto.
- **No traduzcas palabra por palabra**: busca la idea de cada párrafo.
- Usa el traductor para **frases concretas**, no para la página entera. Si traduces todo siempre, nunca aprenderás.
- Apunta las palabras que se repiten: en documentación técnica son pocas y vuelven una y otra vez.

### El vocabulario que más se repite

| Inglés | Significado | Ejemplo |
|---|---|---|
| *to deploy* | desplegar, publicar en un servidor | *We deploy every Friday.* |
| *to fetch* | obtener, traer (datos) | *Fetch the user data from the API.* |
| *to handle* | gestionar, manejar | *Handle the error gracefully.* |
| *to set up* | configurar, preparar | *Set up the database first.* |
| *to run* | ejecutar | *Run the tests before pushing.* |
| *to throw / to raise* | lanzar (una excepción) | *It raises a ValueError.* |
| *to override* | sobrescribir, reemplazar | *This option overrides the default.* |
| *default* | valor por defecto | *The default timeout is 30 seconds.* |
| *required / optional* | obligatorio / opcional | *This parameter is required.* |
| *deprecated* | obsoleto, que se eliminará | *This method is deprecated.* |
| *to return* | devolver | *The function returns a list.* |
| *payload* | los datos que se envían | *The request payload is JSON.* |
| *endpoint* | una ruta de la API | *Call the /users endpoint.* |
| *rate limit* | límite de peticiones | *You hit the rate limit.* |
| *timeout* | tiempo máximo de espera | *The request timed out.* |
| *issue* | problema; también un ticket en GitHub | *I opened an issue.* |
| *feature* | funcionalidad | *A new feature for the dashboard.* |
| *bug / fix* | error / corrección | *This fixes the login bug.* |
| *to merge* | fusionar (ramas) | *Merge it into main.* |
| *to roll back / to revert* | revertir | *We rolled back the release.* |

### Leer mensajes de error

Los mensajes de error siguen patrones fijos. Aprende a leerlos y la mitad de la depuración se vuelve más rápida:

| Mensaje | Qué significa |
|---|---|
| `KeyError: 'email'` | No existe la clave `email` en el diccionario |
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | Intentas sumar un número y un texto |
| `Connection refused` | No hay nada escuchando en esa dirección y puerto |
| `Permission denied` | No tienes permisos |
| `No such file or directory` | El archivo o carpeta no existe en esa ruta |
| `401 Unauthorized` / `403 Forbidden` | Falta autenticación / no tienes permiso |
| `Unexpected token` | El código o el JSON tiene un carácter que no se esperaba ahí |

---

## 3. Escribir en el trabajo

En un equipo remoto, **escribes mucho más de lo que hablas**. La ventaja: puedes revisar antes de enviar, usar plantillas y pedir ayuda a
un asistente de IA (pero entendiendo lo que envías).

### Commits

Se escriben en **imperativo**, cortos, describiendo lo que hace el cambio:

| Bien | Mal |
|---|---|
| `Add retry logic to the payment client` | `added stuff` |
| `Fix crash when the cart is empty` | `fixed bug` |
| `Update README with setup steps` | `cambios` |

Verbos más usados: *add, fix, update, remove, refactor, rename, improve, handle*.

### Pull requests e issues

Una plantilla sencilla para la descripción de un *pull request*:

```markdown
## What
Add streaming to the chat endpoint.

## Why
Users waited 10-15 seconds for long answers with no feedback.

## How
- The backend forwards the model stream as Server-Sent Events.
- The frontend appends each chunk to the last message.

## Testing
- Added tests for the SSE parser.
- Tested manually with long and short answers.
```

Y para reportar un error (*issue*): *Steps to reproduce* (pasos para reproducirlo), *Expected behavior* (lo que debería pasar), *Actual
behavior* (lo que pasa), *Environment* (versiones, sistema).

### Mensajes de chat (Slack, Teams)

Frases útiles que sirven en casi cualquier situación:

| Situación | Frase |
|---|---|
| Pedir ayuda | *Could you take a look at this when you have a moment?* |
| Avisar de un bloqueo | *I'm blocked on X because Y. Any ideas?* |
| Dar una actualización | *Quick update: the API is done, I'm working on the tests now.* |
| No entendiste | *Sorry, could you clarify what you mean by X?* |
| Confirmar | *Got it, thanks!* / *Sounds good.* |
| Proponer | *What do you think about...?* / *How about we...?* |
| Disculparse por un error | *My bad, I'll fix it right away.* |
| Avisar de un retraso | *Heads-up: this will take a bit longer than expected because...* |

En el mundo profesional en inglés se valora la **brevedad** y el tono amable pero directo. No hacen falta fórmulas largas de cortesía.

### Correo a un cliente (Upwork)

```
Hi Sarah,

Thanks for the details. I can build a WhatsApp assistant that answers questions
about your product catalog and hands off to your team when a customer wants to buy.

Here is a similar demo I built: [link]

Quick question: is your catalog in a spreadsheet or in your store platform?

Best,
Alejandro
```

Es la misma estructura de propuesta del capítulo de freelance: su problema, tu solución, una prueba, una pregunta.

---

## 4. Hablar: reuniones y *stand-ups*

La reunión diaria (*daily stand-up*) tiene una estructura fija, así que puedes prepararla:

> *Yesterday I finished the login page and fixed a bug in the search.*
> *Today I'm going to work on the streaming endpoint.*
> *No blockers.* / *I'm blocked on the API keys; I'm waiting for access.*

Frases para sobrevivir en una reunión cuando no entiendes todo:

- *Sorry, could you repeat that?*
- *Could you say that more slowly, please?*
- *Just to make sure I understood: you want me to...?* (Reformular es la técnica más útil: confirma y te da tiempo.)
- *Let me check and get back to you.* (Cuando no sabes la respuesta.)
- *Could you share that in the chat?* (Para tenerlo por escrito.)

Nadie espera que un hablante no nativo entienda todo a la primera. Pedir que repitan es **profesional**; fingir que entendiste y hacer
otra cosa no lo es.

---

## 5. Entrevistas en inglés

### Las frases que debes entender

| Te dicen | Significa |
|---|---|
| *Tell me about yourself.* | Preséntate (60 segundos, perfil profesional) |
| *Could you walk me through your project?* | Explícame tu proyecto paso a paso |
| *What was the most challenging part?* | ¿Qué fue lo más difícil? |
| *How would you approach...?* | ¿Cómo abordarías...? |
| *What would you do differently?* | ¿Qué harías distinto? |
| *Do you have any questions for us?* | ¿Tienes preguntas para nosotros? |
| *What are your salary expectations?* | ¿Cuánto esperas cobrar? |

### Prepara y practica tus respuestas

Escribe, corrige y **memoriza la estructura** (no palabra por palabra) de:

1. **Tu presentación** (*Tell me about yourself*):

> *I'm a web developer from Venezuela. I recently graduated and I've been focusing on backend development with Python and on applied AI.
> My main project is a customer support assistant that answers questions from a company's documents using retrieval-augmented
> generation. It's deployed, it shows the sources for each answer, and I evaluated it with a set of 40 questions. I'm looking for a role
> where I can build AI features for real products.*

2. **Tu proyecto** (problema, solución, el mayor reto, resultado, qué mejorarías).
3. **Tus historias STAR** más importantes.

Después **grábate** diciéndolas sin leer y escúchate. Es incómodo, y es la forma más rápida de mejorar. Un asistente de IA en modo de voz
también sirve para simular entrevistas.

### Si no entiendes una pregunta en la entrevista

> *Sorry, I didn't catch that. Could you rephrase the question?*

Es mucho mejor que responder a otra pregunta.

---

## 6. Errores típicos de los hispanohablantes

### Falsos amigos

Palabras que se parecen a una española pero significan otra cosa:

| Inglés | Significa | No significa |
|---|---|---|
| *actually* | en realidad, de hecho | actualmente (*currently*) |
| *eventually* | al final, con el tiempo | eventualmente / quizá (*possibly*) |
| *assist* | ayudar | asistir a un lugar (*attend*) |
| *library* | biblioteca (también de código) | librería, tienda (*bookstore*) |
| *carpet* | alfombra | carpeta (*folder*) |
| *realize* | darse cuenta | realizar (*carry out*, *do*) |
| *support* | dar soporte, apoyar | soportar, aguantar (*stand*, *tolerate*) |
| *sensible* | sensato | sensible (*sensitive*) |
| *exit* | salida | éxito (*success*) |
| *argument* | discusión; también un argumento de una función | — |

Ejemplo: *"Actually, the bug was in the frontend"* = "En realidad, el error estaba en el frontend". Y *"We will eventually migrate"* =
"Al final (con el tiempo) migraremos", con seguridad, no "quizá".

### Errores de gramática frecuentes

| Error | Correcto | Por qué |
|---|---|---|
| *I have 25 years.* | *I'm 25 (years old).* | La edad se dice con *to be* |
| *Explain me the problem.* | *Explain the problem to me.* | *Explain* no lleva la persona directamente |
| *I am agree.* | *I agree.* | *Agree* es un verbo |
| *It depends of...* | *It depends on...* | Preposición fija |
| *I work here since 2024.* | *I've worked here since 2024.* | Con *since/for* se usa el presente perfecto |
| *Is very important.* | *It's very important.* | En inglés el sujeto no se omite |
| *The people is...* | *People are...* | *People* es plural |
| *I want that you review it.* | *I want you to review it.* | Estructura *want + persona + to* |

### Pronunciación de palabras técnicas

Algunas que se suelen pronunciar mal: *data* (/déi-ta/), *cache* (/kásh/, como *cash*), *SQL* (/es-kiú-el/ o /síkuel/), *GUI* (/gúi/),
*Linux* (/líniks/), *nginx* (/éndyin-ex/), *Azure* (/ázhur/), *suite* (/suít/), *queue* (/kiú/), *width* (/uíth/). En caso de duda,
busca la palabra en un diccionario con audio.

---

## 7. Un plan realista

Mejorar el inglés es cuestión de **exposición diaria**, no de sesiones largas de vez en cuando. Una rutina que puedes mantener mientras
estudias lo técnico:

| Hábito | Tiempo | Cómo |
|---|---|---|
| Leer documentación en inglés | Lo que ya estudias | Cambia el idioma de la documentación por defecto |
| Escuchar contenido técnico | 20-30 min/día | Vídeos y podcasts técnicos con subtítulos **en inglés** (no en español) |
| Escribir | 10 min/día | Commits, README y apuntes en inglés |
| Vocabulario | 10 min/día | La vista de Inglés de la plataforma, con repaso espaciado |
| Hablar | 2-3 veces/semana | Grabarte, practicar con un asistente de voz, intercambios de idiomas |

**Cambia el entorno**: el sistema operativo, el editor y el móvil en inglés. Son cientos de palabras que verás cada día sin esfuerzo.

Y mide tu progreso: repite la prueba de nivel cada 2-3 meses. Pasar de A1 a B1 con constancia diaria es un objetivo realista en meses,
no en años.

---

## Resumen del capítulo

| Tema | Lo esencial |
|---|---|
| Niveles | Leer y escribir llegan antes que hablar; el trabajo remoto es sobre todo escrito |
| Documentación | Ideas por párrafo, código primero, traductor por frases |
| Escribir | Commits en imperativo; PR con *What/Why/How/Testing*; mensajes breves y directos |
| Reuniones | *Stand-up* con estructura fija; reformular para confirmar; pedir que repitan es profesional |
| Entrevistas | Presentación, proyecto y STAR escritos, practicados y grabados |
| Errores | Falsos amigos (*actually*, *eventually*), sujeto obligatorio, *depend on* |
| Plan | Exposición diaria, entorno en inglés, medir cada 2-3 meses |

## Autoevaluación final

1. Traduce: *"Actually, we will eventually deprecate this endpoint."*
2. Escribe un commit en inglés para un cambio que corrige un error cuando la lista de productos está vacía.
3. ¿Qué cuatro secciones tiene la plantilla de pull request del capítulo?
4. ¿Qué dices en un *stand-up* si estás bloqueado esperando unas credenciales?
5. ¿Qué significa *"Could you walk me through your project?"*?
6. Corrige: *"I am agree, is very important explain me the requirements."*
7. No entendiste una pregunta en una entrevista. ¿Qué dices?
8. ¿Por qué conviene usar subtítulos en inglés y no en español?

**Respuestas:** 1) "En realidad, al final dejaremos obsoleto este endpoint." 2) Por ejemplo: *Fix crash when the product list is empty*.
3) *What, Why, How, Testing*. 4) Algo como *I'm blocked on the credentials; I'm waiting for access.* 5) "Explícame tu proyecto paso a
paso." 6) *I agree; it's very important to explain the requirements to me.* 7) *Sorry, I didn't catch that. Could you rephrase the
question?* 8) Porque conectas el sonido con la palabra escrita en inglés; con subtítulos en español acabas leyendo en español y el oído no
se entrena.
