# Explaining an AI system

En una entrevista de AI engineer, en una llamada con un cliente o en el README de tu demo, tendrás que explicar **cómo funciona tu
sistema**, paso a paso y con claridad. No hace falta un vocabulario complicado: hace falta **orden** y una herramienta gramatical que
hace que las explicaciones técnicas suenen naturales, la **voz pasiva**.

> Lectura de la pronunciación: la **tilde** marca la sílaba fuerte, **j** es la h inglesa, **y** es la j inglesa de *job*, **ii/uu**
> son vocales largas, **z** es la th con la lengua entre los dientes, **er** es una vocal relajada con r suave.

---

## 1. La voz pasiva: lo importante es el proceso

En una explicación técnica, normalmente importa **lo que le pasa a los datos**, no quién lo hace. Por eso se usa la **voz pasiva**:

| Activa (quién lo hace) | Pasiva (qué pasa) |
|---|---|
| We split the documents into chunks. | The documents **are split** into chunks. |
| The model generates the answer. | The answer **is generated** by the model. |
| We stored the embeddings in PostgreSQL. | The embeddings **were stored** in PostgreSQL. |
| The system will send a notification. | A notification **will be sent**. |

### Cómo se forma

**to be (en el tiempo que necesites) + participio**

| Tiempo | Estructura | Ejemplo |
|---|---|---|
| Presente | is / are + participio | *The data **is stored** in a database.* |
| Pasado | was / were + participio | *The model **was tested** with 40 questions.* |
| Futuro | will be + participio | *The results **will be shown** to the user.* |
| Con *can* | can be + participio | *The answer **can be streamed**.* |
| Presente perfecto | has / have been + participio | *The bug **has been fixed**.* |

Si quieres decir quién lo hace, se añade **by**: *The answer is generated **by** the model.*

En español, la pasiva se traduce casi siempre con **«se»**: *The documents are split* = Los documentos **se** dividen.

### Participios que más usarás

| Verbo | Participio | Se pronuncia |
|---|---|---|
| split | split | split |
| store | stored | stord |
| send | sent | sent |
| retrieve | retrieved | ritríivd |
| convert | converted | konvértid |
| generate | generated | yénereitid |
| use | used | iuusd |
| show | shown | shoun |
| build | built | bilt |
| train | trained | treind |
| write | written | ríten |
| choose | chosen | chóusen |

---

## 2. Un RAG explicado en inglés

Este es el tipo de explicación que te pedirán en una entrevista de IA aplicada. Fíjate en los conectores (*first, then, when, finally*)
y en la pasiva:

> *"First, the documents **are split** into small chunks. Each chunk **is converted** into an embedding, which is a vector that represents
> its meaning, and **stored** in a vector database. When a user asks a question, the question **is** also **converted** into an embedding,
> and the most similar chunks **are retrieved**. Then, those chunks **are sent** to the model together with the question. The model
> answers using only that context, and finally, the sources **are shown** to the user."*

Pronunciación de las partes difíciles:

- *the documents are split into small chunks* → de dókiuments ar split íntu smol chanks
- *Each chunk is converted into an embedding* → iich chank is konvértid íntu an imbéding
- *a vector that represents its meaning* → a véktor dat reprisénts its míining
- *the most similar chunks are retrieved* → de moust símilar chanks ar ritríivd
- *together with the question* → tuguéder uid de kuéschon
- *the sources are shown to the user* → de sórsis ar shoun tu de iúser

### La versión corta (para una conversación)

> *"It's a retrieval system. It finds the relevant parts of the documents and gives them to the model, so the answers are based on real
> information, with sources."*

Ten **las dos versiones**: una de 15 segundos para no técnicos (un cliente) y una de 1 minuto para técnicos (una entrevista).

---

## 3. Explicar un agente

> *"The agent works in a loop. The model receives the user's request and a list of tools. If it needs information, it asks to call a
> tool, for example, to check the order status. **The tool is executed** by our code, not by the model, and the result **is sent back**
> to the model. This **is repeated** until the model has enough information to answer. For actions like refunds, a human confirmation
> **is required**."*

Pronunciación:

- *The agent works in a loop* → di éiyent uerks in a luup
- *a list of tools* → a list ov tuuls
- *The tool is executed by our code* → de tuul is éksekiutid bai áuer koud
- *until the model has enough information* → antíl de módel jas ináf informéishon
- *a human confirmation is required* → a jiúman konferméishon is rikuáird

***enough*** se pronuncia *ináf*: la *gh* suena *f*. Lo mismo en *tough* (*taf*) y *rough* (*raf*).

---

## 4. Vocabulario de IA aplicada

| Inglés | Se pronuncia | Español |
|---|---|---|
| large language model (LLM) | larch lánguich módel (el-el-ém) | modelo de lenguaje grande |
| prompt | prompt | instrucción, mensaje al modelo |
| token | tóuken | unidad de texto del modelo |
| chunk | chank | fragmento |
| embedding | imbéding | vector que representa el significado |
| vector database | véktor déitabeis | base de datos vectorial |
| to retrieve | tu ritríiv | recuperar |
| retrieval | ritríival | recuperación |
| context window | kóntekst uíndou | ventana de contexto |
| hallucination | jalusinéishon | alucinación (respuesta inventada) |
| latency | léitensi | latencia |
| accuracy | ákiurasi | precisión, exactitud |
| tool call | tuul kol | llamada a una herramienta |
| agent | éiyent | agente |
| evaluation set | ivaliuéishon set | conjunto de evaluación |
| fine-tuning | fáin-tiúning | ajuste fino |
| guardrails | gárdreils | salvaguardas, barreras |
| prompt injection | prompt inyékshon | inyección de instrucciones |
| citation | saitéishon | cita (de una fuente) |
| streaming | stríiming | envío en tiempo real |

### Las palabras más difíciles de pronunciar

| Palabra | Se pronuncia | Trampa |
|---|---|---|
| retrieve | ritríiv | La *ie* suena *ii* larga |
| accuracy | ákiurasi | La fuerza al principio; la *cc* suena *k* |
| latency | léitensi | La *a* suena *ei* |
| hallucination | jalusinéishon | La *h* suena (aire) y la fuerza en *nei* |
| data | déita | La *a* suena *ei* |
| model | módel | La *o* corta |
| vector | véktor | La *v* con los dientes sobre el labio |
| algorithm | álgoridem | La *th* suave |
| cache | kash | Como *cash*, una sílaba |
| query | kuíri | La *u* suena *u* rápida |

---

## 5. Hablar de resultados y métricas

| Inglés | Se pronuncia | Español |
|---|---|---|
| We measured the accuracy with... | ui méshurd di ákiurasi uid | Medimos la precisión con... |
| It answers correctly 85% of the time. | it ánsers koréktli éiti-faiv persént ov de taim | Responde bien el 85 % de las veces. |
| The latency went down from 4 to 2 seconds. | de léitensi uent daun from for tu tuu sékonds | La latencia bajó de 4 a 2 segundos. |
| It improved by 20%. | it imprúuvd bai tuénti persént | Mejoró un 20 %. |
| It costs about one cent per question. | it kosts abáut uan sent per kuéschon | Cuesta un centavo por pregunta. |

Fíjate en ***by*** para la cantidad de un cambio: *It improved **by** 20%* (mejoró un 20 %), *It went down **by** half* (bajó a la
mitad).

---

## 6. Explicar a un cliente no técnico

Con un cliente, evita la jerga y habla de **lo que hace por él**:

| Técnico (para una entrevista) | Para un cliente |
|---|---|
| *The documents are split into chunks and converted into embeddings.* | *The assistant reads your documents and finds the right information for each question.* |
| *We reduced hallucinations with citations and an "I don't know" instruction.* | *It only answers with your information, shows where it comes from, and says when it doesn't know.* |
| *The p95 latency is two seconds.* | *It answers in about two seconds.* |

---

## 7. Errores típicos de hispanohablantes

| Incorrecto | Correcto | Por qué |
|---|---|---|
| The documents are splitted. | The documents are **split**. | *split* es irregular: igual en los tres tiempos |
| The answer is generate by the model. | The answer is **generated** by the model. | Pasiva = *be* + **participio** |
| Se envían los chunks → The chunks send to the model. | The chunks **are sent** to the model. | Falta *are*: sin él, los chunks «envían» |
| The datas are stored. | The data **is** stored. | *data* suele tratarse como incontable |
| It improved in 20%. | It improved **by** 20%. | Preposición |
| The model hallucinates less with citations. (pronunciado «aluci...») | *jalusinéits* | La *h* se pronuncia |

---

## 8. Consejos para esta unidad

- **Escribe la explicación de tu demo** en inglés, en dos versiones (15 segundos y 1 minuto), y ponla en el README. Así la practicas y
  la tienes preparada para la entrevista.
- **Dibuja mientras explicas.** En una entrevista por vídeo puedes compartir pantalla con un diagrama simple. Un dibujo reduce mucho las
  palabras que necesitas.
- **Comprueba que te siguen:** *Does that make sense?* (¿Se entiende?) al terminar cada parte.

---

## Comprueba que entendiste

1. Pasa a pasiva: *We store the embeddings in PostgreSQL.*
2. ¿Por qué se usa tanto la voz pasiva en las explicaciones técnicas?
3. ¿Cuál es el participio de *split*? ¿Y de *choose*?
4. ¿Cómo se pronuncian *retrieve* y *accuracy*?
5. Corrige: *The answer is generate by the model.*
6. ¿Cómo dices «Mejoró un 30 %»?

**Respuestas:** 1) *The embeddings are stored in PostgreSQL.* 2) Porque lo importante es el proceso (lo que les pasa a los datos), no
quién lo hace. 3) *split* y *chosen*. 4) *ritríiv* y *ákiurasi*. 5) *The answer is generated by the model.* 6) *It improved by 30%.*
