# Cómo funcionan los LLMs por dentro

Para construir productos con IA de forma profesional no basta con llamar a una API. Necesitas un **modelo mental correcto** de lo que
hace el modelo, para entender:

- **Por qué falla** (y cómo evitarlo).
- **Cuánto cuesta** y cuánto tarda cada llamada.
- **Qué decisiones de diseño** tomar: qué modelo, cuánto contexto, cuándo usar RAG o herramientas.

No vas a entrenar modelos, pero sí vas a explicar en entrevistas qué es un token, qué hace la temperatura o por qué un modelo alucina, y
vas a tomar decisiones de costo con números. Este capítulo te da todo eso, con las matemáticas justas explicadas paso a paso, y termina
con cómo llamar a un modelo desde Python.

---

## 1. La idea central: predecir el siguiente fragmento de texto

Un **LLM** (*Large Language Model*, modelo de lenguaje grande) es, en esencia, una función que recibe un texto y devuelve **cuál es el
fragmento siguiente más probable**. Para generar una respuesta completa repite ese paso una y otra vez:

```
Entrada:  "La capital de Francia es"
Paso 1:   predice " París"           → "La capital de Francia es París"
Paso 2:   predice "."                → "La capital de Francia es París."
Paso 3:   predice <fin>              → termina
```

Todo lo que parece "razonamiento", "conocimiento" o "creatividad" sale de este mecanismo aplicado a una escala enorme: modelos con
cientos de miles de millones de parámetros, entrenados con billones de palabras. Esa escala hace que, para predecir bien el siguiente
fragmento, el modelo haya tenido que aprender gramática, hechos del mundo, estilos de escritura y patrones de razonamiento.

Tenlo presente durante todo el capítulo: **el modelo genera texto plausible**. A menudo plausible y verdadero coinciden; cuando no,
aparecen las alucinaciones.

---

## 2. Tokens: la unidad de todo

Un LLM no ve letras ni palabras completas: ve **tokens**, fragmentos de texto que pueden ser una palabra corta, parte de una palabra, un
signo de puntuación o un espacio con una palabra.

```
"Aprendiendo Python rápidamente"
→ ["Ap", "rend", "iendo", " Python", " rápid", "amente"]     (división ilustrativa)
```

Cada modelo tiene su propio **tokenizador** (su forma de cortar el texto). Reglas aproximadas:

- En inglés, un token equivale de media a unos **4 caracteres** (unas tres cuartas partes de una palabra).
- En **español** y otros idiomas, una misma frase suele necesitar **más tokens** que en inglés, porque los tokenizadores se construyeron
  con mucho texto en inglés.
- El código, los números y los textos con muchos símbolos también consumen más tokens.

Para saber el número exacto no se adivina: los proveedores ofrecen funciones para **contar tokens** (en la API de Claude,
`client.messages.count_tokens(...)`).

### Por qué importan los tokens

**1. El precio.** Las APIs cobran por **tokens de entrada** (todo lo que envías: instrucciones, documentos, historial) y **tokens de
salida** (lo que genera el modelo). Los de salida cuestan varias veces más. Los precios se expresan normalmente **en dólares por millón de
tokens**.

**2. La ventana de contexto.** Es el número máximo de tokens que el modelo puede "ver" a la vez en una llamada: instrucciones +
documentos + conversación + respuesta. Los modelos actuales tienen ventanas muy grandes (cientos de miles o un millón de tokens), pero no
infinitas, y llenarlas tiene un costo.

**3. La latencia.** El modelo genera la respuesta **token a token**: una respuesta de 1 000 tokens tarda más que una de 100. Por eso las
respuestas largas se muestran con *streaming* (lo verás en la sección 9).

### Calcular el costo de una llamada

La fórmula es:

```
costo = tokens_entrada × precio_entrada / 1 000 000  +  tokens_salida × precio_salida / 1 000 000
```

Ejemplo con precios **de ejemplo** de 3 USD por millón de tokens de entrada y 15 USD por millón de salida: una llamada con 2 000 tokens de
entrada y 500 de salida cuesta:

```
2 000 × 3 / 1 000 000  = 0,006 USD
  500 × 15 / 1 000 000 = 0,0075 USD
total                  = 0,0135 USD
```

Parece poco, pero un chatbot con 1 000 conversaciones diarias de 10 mensajes son 10 000 llamadas: unos 135 USD al día. Hacer esta cuenta
**antes** de construir es parte del trabajo (y de lo que le presupuestas a un cliente).

### ¿Cabe en el contexto?

Antes de enviar una petición grande hay que comprobar que **la entrada más la salida máxima permitida** caben en la ventana:

```
tokens_entrada + max_tokens_salida  ≤  ventana_de_contexto
```

Si reservas 4 000 tokens para la respuesta y la ventana es de 200 000, la entrada puede ocupar como mucho 196 000.

### Comprueba que entendiste

**Pregunta:** con precios de 1 USD (entrada) y 5 USD (salida) por millón, ¿cuánto cuestan 10 000 tokens de entrada y 1 000 de salida?

**Respuesta:** 10 000 × 1 / 1 000 000 = 0,01 USD, más 1 000 × 5 / 1 000 000 = 0,005 USD. Total: 0,015 USD.

---

## 3. Embeddings: el significado como números

Una red neuronal solo trabaja con números. El primer paso de un LLM es convertir cada token en un **vector**: una lista de cientos o miles
de números. A ese vector se le llama **embedding**.

Lo interesante es que, durante el entrenamiento, el modelo aprende vectores donde **los significados parecidos quedan cerca**. En un
espacio así, "perro" queda cerca de "gato", "rey" cerca de "reina", y "factura" cerca de "recibo".

```
"perro"    → [0.21, -0.43, 0.88, ...]
"gato"     → [0.19, -0.40, 0.85, ...]      ← muy parecido a "perro"
"factura"  → [-0.65, 0.12, -0.07, ...]     ← muy distinto
```

Existen además modelos específicos que producen **un embedding para una frase o un documento completo**. Esos son la base de la búsqueda
semántica y del RAG (el siguiente tema): para encontrar los documentos que responden a una pregunta, se buscan los vectores más cercanos
al vector de la pregunta.

---

## 4. De puntuaciones a probabilidades: softmax y temperatura

En cada paso, el modelo produce una **puntuación** para cada token posible de su vocabulario (decenas de miles). Esas puntuaciones se
llaman **logits** y pueden ser cualquier número: positivo, negativo, grande o pequeño. Para elegir el siguiente token hay que convertirlas
en **probabilidades** (números entre 0 y 1 que suman 1). Eso lo hace la función **softmax**.

### Softmax paso a paso

Para cada logit `z`, softmax calcula `e^z` (la función exponencial) y divide entre la suma de todos:

```
p_i = e^(z_i) / (e^(z_1) + e^(z_2) + ... + e^(z_n))
```

Ejemplo con tres tokens candidatos y logits `[3.0, 1.0, 0.0]`:

| Token | logit `z` | `e^z` | probabilidad |
|---|---|---|---|
| A | 3.0 | 20.09 | 20.09 / 23.81 = **0.844** |
| B | 1.0 | 2.72 | 2.72 / 23.81 = **0.114** |
| C | 0.0 | 1.00 | 1.00 / 23.81 = **0.042** |
| | | suma = 23.81 | suma = 1.000 |

Por qué la exponencial: siempre da números positivos (las probabilidades no pueden ser negativas) y **exagera las diferencias**: un logit
solo dos puntos mayor se convierte en una probabilidad unas siete veces mayor (`e^2 ≈ 7.4`).

En Python, `e^z` es `math.exp(z)`.

### La temperatura

La **temperatura** `T` divide los logits **antes** del softmax:

```
p_i = e^(z_i / T) / Σ e^(z_j / T)
```

Con los mismos logits `[3.0, 1.0, 0.0]`:

| Temperatura | logits divididos | probabilidades (A, B, C) | Efecto |
|---|---|---|---|
| `T = 0.5` | `[6.0, 2.0, 0.0]` | 0.98, 0.02, 0.00 | Casi siempre elige A |
| `T = 1.0` | `[3.0, 1.0, 0.0]` | 0.84, 0.11, 0.04 | La distribución "natural" |
| `T = 2.0` | `[1.5, 0.5, 0.0]` | 0.63, 0.23, 0.14 | Más variedad |

- **Temperatura baja** (cerca de 0): las diferencias se agrandan y el modelo elige casi siempre lo más probable. Respuestas estables y
  repetibles: lo adecuado para **extraer datos, clasificar o generar JSON**.
- **Temperatura alta**: las diferencias se reducen y aparecen opciones menos probables. Más variedad y "creatividad", pero también más
  riesgo de errores.
- La temperatura debe ser **positiva**: dividir entre 0 no está definido (y una temperatura negativa invertiría las preferencias).

Junto a la temperatura existen **top-k** (elegir solo entre los k tokens más probables) y **top-p** (elegir entre los tokens más probables
cuya probabilidad acumulada llega a p).

**Importante para tu código:** en los modelos más recientes de Claude, la API **ya no acepta** `temperature`, `top_p` ni `top_k` (enviarlos
da un error). El muestreo lo gestiona el proveedor y tú controlas el comportamiento con las instrucciones, con **salidas estructuradas**
(cuando necesitas JSON fiable) y con el parámetro **`effort`**, que regula cuánto "piensa" el modelo. El concepto de temperatura sigue
siendo esencial para entender cómo generan texto los LLM, aparece en entrevistas y en otras APIs y modelos abiertos, pero no lo pongas en
una llamada a un modelo actual de Claude.

### El truco de estabilidad numérica

`e^z` crece muy rápido: `e^1000` es un número tan grande que el ordenador no puede representarlo (desbordamiento, *overflow*). La solución
estándar es **restar el valor máximo** a todos los logits antes de aplicar la exponencial:

```
logits:          [1000, 999, 998]
menos el máximo: [0, -1, -2]          → e^0 = 1, e^-1 = 0.37, e^-2 = 0.14   (números manejables)
```

¿Por qué no cambia el resultado? Porque restar la misma constante `c` a todos multiplica numerador y denominador por el mismo factor
`e^(-c)`, que se cancela:

```
e^(z_i - c) / Σ e^(z_j - c)  =  (e^(z_i) · e^(-c)) / (Σ e^(z_j) · e^(-c))  =  e^(z_i) / Σ e^(z_j)
```

Todas las implementaciones reales de softmax hacen este paso. Si aplicas temperatura, réstalo después de dividir entre `T`.

### Comprueba que entendiste

**Pregunta:** con logits `[2.0, 2.0]`, ¿qué probabilidades da softmax? ¿Cambian con la temperatura?

**Respuesta:** `[0.5, 0.5]`: los dos son iguales. La temperatura no lo cambia, porque dividir dos números iguales entre `T` los deja
iguales.

---

## 5. Atención: cómo el modelo relaciona las palabras

El significado de una palabra depende de las demás. En *"el banco donde me senté estaba frío"*, "banco" es un asiento; en *"el banco me
cobró una comisión"*, es una entidad financiera. Un buen modelo necesita que cada token **"mire" a los demás** para ajustar su
significado. Ese mecanismo se llama **atención**, y es el corazón de la arquitectura **transformer** (publicada en 2017), sobre la que se
construyen todos los LLM actuales.

### Las tres piezas: consulta, clave y valor

Para cada token, el modelo calcula tres vectores:

- **Consulta (Q, *query*)**: "¿qué estoy buscando?".
- **Clave (K, *key*)**: "¿qué ofrezco yo?".
- **Valor (V, *value*)**: "¿qué información aporto si me eligen?".

Una analogía: en una biblioteca, la consulta es lo que buscas, la clave es la etiqueta de cada libro y el valor es su contenido. Comparas
tu búsqueda con todas las etiquetas y te llevas un poco del contenido de cada libro, más de los que mejor encajan.

### El cálculo, paso a paso

Para un token (su consulta) frente a todos los tokens (sus claves y valores):

1. **Puntuación** de cada clave: el **producto escalar** de la consulta con la clave, dividido entre la raíz cuadrada de la dimensión `d`
   (la longitud de los vectores):

   ```
   puntuación_i = (Q · K_i) / √d
   ```

   El **producto escalar** de dos vectores multiplica sus elementos uno a uno y suma: `[1, 2] · [3, 4] = 1×3 + 2×4 = 11`. Es grande
   cuando los vectores "apuntan en la misma dirección" (se parecen). Dividir entre `√d` evita que las puntuaciones crezcan demasiado con
   vectores largos, lo que haría al softmax demasiado extremo.

2. **Pesos**: se aplica softmax a las puntuaciones, para que sean positivas y sumen 1.

3. **Salida**: la **suma ponderada de los valores**: cada valor multiplicado por su peso, y todo sumado (elemento a elemento).

### Un ejemplo con números

Dimensión `d = 2`, así que `√d ≈ 1.414`.

```
Consulta:  Q  = [1, 0]
Claves:    K1 = [1, 0]     K2 = [0, 1]
Valores:   V1 = [10, 0]    V2 = [0, 10]
```

1. Puntuaciones:
   - `Q · K1 = 1×1 + 0×0 = 1` → `1 / 1.414 = 0.707`
   - `Q · K2 = 1×0 + 0×1 = 0` → `0 / 1.414 = 0`
2. Softmax de `[0.707, 0]`: `e^0.707 = 2.03`, `e^0 = 1`, suma 3.03 → pesos **`[0.67, 0.33]`**.
3. Salida: `0.67 × [10, 0] + 0.33 × [0, 10]` = `[6.7, 0] + [0, 3.3]` = **`[6.7, 3.3]`**.

La consulta se parecía más a la primera clave, así que la salida toma más información del primer valor. Eso es todo: **atención es una
media ponderada, donde los pesos dicen cuánto se parece lo que busco a lo que ofrece cada uno**.

### A escala

Un modelo real hace esto con vectores de miles de dimensiones, para cada token frente a todos los demás, con muchas "cabezas" de atención
en paralelo (cada una aprende a fijarse en relaciones distintas: gramática, referencias, temas) y apilando decenas de capas. Los vectores
Q, K y V no se diseñan a mano: se calculan con matrices de números que el modelo **aprende** durante el entrenamiento.

Una consecuencia práctica: como cada token se compara con todos los demás, el costo de la atención crece mucho con la longitud del texto.
Y aunque los modelos actuales manejan contextos enormes, la información importante se aprovecha mejor si es **relevante y está bien
organizada** que si está enterrada entre mucho texto irrelevante.

---

## 6. Cómo se entrena un LLM

1. **Preentrenamiento.** El modelo aprende a predecir el siguiente token sobre una cantidad enorme de texto y código. Así adquiere el
   idioma, conocimiento del mundo y patrones de razonamiento. Es carísimo (meses de cómputo en miles de procesadores especializados) y
   solo lo hacen unas pocas empresas.
2. **Ajuste por instrucciones** (*SFT, supervised fine-tuning*). Con ejemplos de pregunta y respuesta de buena calidad, aprende a **seguir
   instrucciones** y a responder como un asistente, en lugar de simplemente continuar el texto.
3. **Ajuste por preferencias** (*RLHF* y variantes). Personas (o modelos) comparan respuestas y el modelo aprende a preferir las más
   **útiles, honestas y seguras**.

Lo que tú harás casi siempre es **elegir un modelo ya entrenado y adaptarlo** a tu problema con:

- **Instrucciones** (el *system prompt*): el rol, las reglas, el formato.
- **Contexto** (RAG): los documentos que necesita para responder.
- **Herramientas**: funciones que puede llamar para consultar datos o actuar.
- A veces, **ajuste fino** (*fine-tuning*) para un estilo o un formato muy concreto.

---

## 7. Por qué alucinan

Una **alucinación** es una respuesta falsa dicha con total seguridad: una cita bibliográfica que no existe, una función de una librería
inventada, una política de la empresa que nadie escribió.

Las causas se deducen de todo lo anterior:

1. **El modelo genera lo plausible, no lo verdadero.** No consulta una base de datos de hechos: produce el texto que mejor encaja con los
   patrones que aprendió. Una cita inventada "suena" exactamente igual que una real.
2. **No tenía la información.** Tus documentos internos, los datos de tu cliente o los hechos posteriores a su entrenamiento no están en el
   modelo.
3. **Fecha de corte.** El conocimiento del modelo se congela en la fecha en que terminó su entrenamiento.
4. **No tiene una señal interna fiable de "no sé"**, salvo que se le enseñe y se le pida explícitamente.

Las alucinaciones **no se eliminan del todo; se reducen**:

- **Dale el contexto** que necesita (RAG, herramientas) en lugar de confiar en su memoria.
- **Pídele que responda solo con ese contexto**, que **cite** de dónde saca cada afirmación y que diga **"no lo sé"** si la información no
  está.
- **Valida** la salida con código cuando sea posible (que el JSON cumpla un esquema, que el total cuadre con la suma).
- **Mide** con un conjunto de evaluación (lo verás en *Evaluación y seguridad*): sin medir, no sabes si tus cambios ayudaron.

---

## 8. Elegir modelo

Los proveedores ofrecen familias de modelos de distintos tamaños. Por ejemplo, Anthropic tiene tres líneas de Claude:

| Línea | Para qué |
|---|---|
| **Opus** | El más capaz de uso general: tareas complejas, agentes, programación difícil |
| **Sonnet** | Equilibrio entre capacidad, velocidad y costo: mucho volumen con buena calidad |
| **Haiku** | El más rápido y barato: tareas simples y de gran volumen (clasificar, extraer, resumir) |

Además existen **modelos de pesos abiertos** (que puedes ejecutar en tu propia infraestructura): útiles cuando los datos no pueden salir de
la empresa o cuando el volumen es enorme.

Criterios para decidir:

- **Calidad necesaria**: ¿es una tarea simple (clasificar un mensaje) o compleja (razonar sobre un contrato)?
- **Volumen y presupuesto**: multiplica el costo por llamada por las llamadas diarias.
- **Latencia**: ¿el usuario espera mirando la pantalla?
- **Privacidad**: ¿qué datos envías y a quién?

Y lo más importante: **decide con pruebas sobre tus propios casos**, no por los rankings genéricos de internet. Prepara 20-50 ejemplos
reales de tu tarea, ejecútalos con dos o tres modelos y compara calidad, latencia y costo. Muchas veces un modelo pequeño basta para la
tarea; otras, el grande se paga solo porque comete menos errores.

---

## 9. Llamar a un LLM desde Python

Con la teoría clara, veamos cómo se usa en la práctica con el SDK oficial de Anthropic. Instalación: `pip install anthropic`. La clave de la
API se lee de la variable de entorno `ANTHROPIC_API_KEY`: **nunca la escribas en el código**.

### Una llamada básica

```python
import anthropic

client = anthropic.Anthropic()        # lee ANTHROPIC_API_KEY del entorno

respuesta = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    system="Eres un asistente de soporte de una tienda en línea. Responde en español, en menos de 80 palabras.",
    messages=[
        {"role": "user", "content": "¿Cuánto tarda un envío a Valencia?"},
    ],
)

for bloque in respuesta.content:
    if bloque.type == "text":
        print(bloque.text)

print(respuesta.usage.input_tokens, respuesta.usage.output_tokens)   # tokens consumidos
print(respuesta.stop_reason)                                          # por qué terminó
```

Las piezas:

- **`model`**: el identificador exacto del modelo.
- **`max_tokens`**: el máximo de tokens que puede generar. Si se alcanza, la respuesta queda **cortada** y `stop_reason` vale
  `"max_tokens"`. No lo pongas demasiado bajo.
- **`system`**: las instrucciones generales: el rol, las reglas, el tono, el formato. Es el lugar de la "personalidad" de tu chatbot.
- **`messages`**: la conversación, como una lista de mensajes con `role` (`"user"` o `"assistant"`) y `content`.
- La respuesta trae una lista de **bloques** en `content` (de texto, de herramientas, de razonamiento...): por eso se recorre y se
  comprueba el tipo.
- **`usage`** dice cuántos tokens de entrada y salida consumió la llamada: guárdalo para controlar costos.

### La API no tiene memoria

Cada llamada es **independiente**: el modelo no recuerda la anterior. Para mantener una conversación, **tú** guardas el historial y lo
envías completo cada vez:

```python
historial = [
    {"role": "user", "content": "Me llamo Ana."},
    {"role": "assistant", "content": "¡Hola, Ana! ¿En qué te ayudo?"},
    {"role": "user", "content": "¿Cómo me llamo?"},
]
respuesta = client.messages.create(model="claude-opus-5-5", max_tokens=1024, messages=historial)
```

Consecuencia: cada mensaje nuevo cuesta más que el anterior, porque reenvías todo el historial como tokens de entrada. En conversaciones
largas hay que gestionarlo (resumir, recortar o usar técnicas como el *prompt caching*, que abarata la parte repetida).

### Streaming: mostrar la respuesta mientras se genera

```python
with client.messages.stream(
    model="claude-opus-5-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Explica qué es un embedding en tres frases."}],
) as stream:
    for texto in stream.text_stream:
        print(texto, end="", flush=True)     # cada fragmento en cuanto llega
```

Con streaming, el usuario ve las primeras palabras en uno o dos segundos en lugar de esperar la respuesta completa. Es lo que reenviará tu
backend al frontend con SSE (tema *Diseño de APIs*).

### Errores que hay que manejar

```python
try:
    respuesta = client.messages.create(...)
except anthropic.RateLimitError:
    ...   # demasiadas peticiones: esperar y reintentar
except anthropic.APIStatusError as error:
    ...   # otro error de la API (error.status_code)
except anthropic.APIConnectionError:
    ...   # problema de red
```

El SDK ya **reintenta automáticamente** algunos errores temporales (límites de uso, errores del servidor). Tú decides qué mostrar al
usuario si, aun así, falla.

---

## 10. Errores típicos

| Síntoma | Causa | Solución |
|---|---|---|
| La respuesta se corta a mitad de frase | `max_tokens` demasiado bajo | Súbelo; revisa `stop_reason == "max_tokens"` |
| El bot "olvida" lo que se dijo | No reenvías el historial | Guarda y envía la conversación completa |
| La factura crece sin control | Historiales largos, documentos enteros en cada llamada | Mide `usage`, recorta contexto, usa caché |
| Datos inventados con seguridad | Falta de contexto o pregunta ambigua | RAG, citas, "no lo sé", validación |
| Error al enviar `temperature` | Los modelos actuales no lo aceptan | Quítalo; controla con instrucciones, `effort` o salidas estructuradas |
| `AuthenticationError` | Falta la clave o es inválida | Variable de entorno `ANTHROPIC_API_KEY` |
| Una clave de API en GitHub | Clave escrita en el código | Revócala y usa variables de entorno |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| LLM | Predice el siguiente token; genera lo plausible, no necesariamente lo verdadero |
| Token | Fragmento de texto; mide precio, contexto y latencia; el español usa más tokens que el inglés |
| Costo | `tokens × precio / 1 000 000`, entrada y salida por separado (la salida es más cara) |
| Contexto | Entrada + salida máxima deben caber en la ventana |
| Embedding | Vector donde significados parecidos quedan cerca |
| Softmax | `e^z / Σ e^z`: puntuaciones → probabilidades; restar el máximo evita desbordes |
| Temperatura | Divide los logits: baja = estable, alta = variada; los Claude actuales no la aceptan |
| Atención | `softmax(Q·K / √d)` como pesos de una media ponderada de los valores |
| Entrenamiento | Preentrenamiento, instrucciones, preferencias; tú adaptas con instrucciones, contexto y herramientas |
| Alucinaciones | Se reducen con contexto, citas, "no lo sé", validación y evaluación |
| API | `system`, `messages`, `max_tokens`; sin memoria; `usage`; streaming |

## Autoevaluación final

1. ¿Por qué una misma frase cuesta más tokens en español que en inglés?
2. Calcula el costo de 50 000 tokens de entrada y 2 000 de salida con precios de 2 y 10 USD por millón.
3. ¿Qué hace softmax y por qué usa la exponencial?
4. ¿Qué efecto tiene una temperatura baja sobre las probabilidades?
5. ¿Por qué se resta el máximo antes de aplicar la exponencial, y por qué no cambia el resultado?
6. En la atención, ¿qué representan los pesos y qué es la salida?
7. ¿Por qué un LLM puede inventar una cita bibliográfica?
8. Tu chatbot no recuerda el nombre que el usuario dijo antes. ¿Qué falta?

**Respuestas:** 1) Porque los tokenizadores se construyeron con mucho texto en inglés y cortan el español en más fragmentos. 2) 50 000 × 2
/ 1 000 000 = 0,10 USD más 2 000 × 10 / 1 000 000 = 0,02 USD: 0,12 USD. 3) Convierte puntuaciones en probabilidades positivas que suman 1;
la exponencial garantiza valores positivos y exagera las diferencias. 4) Agranda las diferencias: el token más probable se lleva casi toda
la probabilidad. 5) Para evitar desbordes con números enormes; no cambia porque el factor `e^(-c)` aparece arriba y abajo y se cancela.
6) Los pesos dicen cuánto se parece la consulta a cada clave (tras softmax, suman 1); la salida es la suma de los valores multiplicados por
sus pesos. 7) Porque genera el texto más plausible y no comprueba si es verdad; si no tenía la información, inventa algo que encaje.
8) Enviar el historial completo de la conversación en cada llamada: la API no tiene memoria.

En la práctica vas a implementar softmax con temperatura (con el truco de estabilidad), el mecanismo de atención desde cero y las
funciones de costo y contexto. Usa los ejemplos numéricos de este capítulo para comprobar tus funciones antes de pulsar **Comprobar**.
