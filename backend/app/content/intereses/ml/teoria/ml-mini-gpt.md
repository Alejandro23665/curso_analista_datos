# Construye un GPT pequeño

La mejor forma de entender cómo funciona un modelo como los que ejecutas con Ollama es **construir uno**. No uno de miles de millones de
parámetros, sino uno diminuto, de cientos de miles, que puedas entrenar en tu portátil en unos minutos y que aprenda a escribir texto
"al estilo" de lo que le des. La arquitectura es la misma que la de los grandes: tokens, embeddings, atención, bloques transformer y una
capa final que predice el siguiente token. Lo que cambia es la escala.

Este capítulo sigue el camino que popularizó Andrej Karpathy en su vídeo *Let's build GPT: from scratch, in code, spelled out* (muy
recomendable como complemento, en inglés y con subtítulos): primero un modelo trivial, después la atención, después el transformer
completo. Necesitas los capítulos anteriores, sobre todo *PyTorch esencial*.

---

## 1. La tarea: predecir el siguiente token

Un modelo de lenguaje hace una sola cosa: dado un texto, **dar la probabilidad de cada posible token siguiente**. Para generar, se elige
un token según esas probabilidades, se añade al texto y se repite.

```
"hola mund" → modelo → { "o": 0.92, "a": 0.03, ... } → se elige "o" → "hola mundo"
```

Todo lo demás (responder preguntas, programar, traducir) emerge de hacer esto muy bien con cantidades enormes de texto.

---

## 2. Tokenizar: de texto a números

La red solo trabaja con números. El **tokenizador** convierte texto en una lista de enteros (**ids**) y al revés.

Los LLM reales usan tokens de subpalabras (con algoritmos como BPE: "programación" puede ser `["program", "ación"]`). Para nuestro modelo
usaremos el tokenizador más simple: **un token por carácter**.

- El **vocabulario** es la lista de caracteres distintos del texto, ordenada.
- `stoi` (*string to integer*) asigna a cada carácter su posición en esa lista; `itos` es el diccionario inverso.
- **Codificar** es convertir cada carácter en su id; **decodificar**, convertir cada id en su carácter y unirlos.

Por ejemplo, con el texto `"la sal"` los caracteres distintos ordenados son `[" ", "a", "l", "s"]`, así que el espacio es el 0, la "a" el 1,
la "l" el 2 y la "s" el 3. `"sala"` se codifica como `[3, 1, 2, 1]`.

Estas tres funciones son las que escribiste en el ejercicio **Tokenizador de caracteres**: el laboratorio las reutiliza. Una propiedad que
siempre debe cumplirse: `decodificar(codificar(texto)) == texto`.

Un vocabulario de caracteres es pequeño (un texto en español tiene unos 60-90 caracteres distintos), pero hace las secuencias largas. Los
tokenizadores de los LLM usan vocabularios de 30 000 a 200 000 tokens: secuencias más cortas a cambio de una tabla de embeddings mayor.

---

## 3. Preparar los datos de entrenamiento

Se codifica todo el texto en un solo tensor de ids y se separa en **entrenamiento** (90 %) y **validación** (10 %), sin barajar: el texto es
una secuencia y queremos medir si el modelo generaliza a un trozo que no vio.

### Contexto y desplazamiento

El modelo no lee el texto entero de una vez: trabaja con trozos de longitud fija, el **contexto** (`block_size`). De cada trozo se obtienen
a la vez muchos ejemplos de entrenamiento, porque la etiqueta de cada posición es, simplemente, **el carácter siguiente**:

```
ids:     [18, 47, 56, 57, 58,  1, 15]
x:       [18, 47, 56, 57]          ← contexto de 4
y:       [47, 56, 57, 58]          ← los mismos, desplazados una posición

ejemplos dentro de este trozo:
  con [18]             → el siguiente es 47
  con [18, 47]         → el siguiente es 56
  con [18, 47, 56]     → el siguiente es 57
  con [18, 47, 56, 57] → el siguiente es 58
```

Esa es la idea del ejercicio **Pares de entrenamiento**. Al entrenar, en cada paso se toman trozos de posiciones **aleatorias** del texto y
se apilan en un **lote**:

```python
def lote(datos, block_size, batch_size):
    ix = torch.randint(len(datos) - block_size, (batch_size,))         # posiciones de inicio al azar
    x = torch.stack([datos[i:i + block_size] for i in ix])
    y = torch.stack([datos[i + 1:i + block_size + 1] for i in ix])
    return x, y      # formas: (batch_size, block_size)
```

### Comprueba que entendiste

**Pregunta:** con `block_size = 8` y `batch_size = 4`, ¿cuántos ejemplos de "contexto → siguiente token" contiene un lote?

**Respuesta:** 32: cada una de las 4 secuencias aporta 8 ejemplos (con 1, 2, ... y 8 tokens de contexto).

---

## 4. El modelo más simple: bigrama

Antes del transformer, un modelo que predice el siguiente carácter **mirando solo el actual**. Es una tabla: para cada carácter, las
puntuaciones (logits) del siguiente. En PyTorch, esa tabla es un `nn.Embedding(vocab, vocab)`:

```python
class Bigrama(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.tabla = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, objetivos=None):
        logits = self.tabla(idx)                         # (B, T, vocab)
        if objetivos is None:
            return logits, None
        B, T, C = logits.shape
        perdida = F.cross_entropy(logits.view(B * T, C), objetivos.view(B * T))
        return logits, perdida
```

Fíjate en el `view`: `cross_entropy` espera los logits como `(N, clases)` y los objetivos como `(N,)`, así que se "aplanan" el lote y las
posiciones en una sola dimensión.

### La pérdida de referencia

Antes de entrenar, con pesos aleatorios, el modelo da probabilidades casi iguales a todos los caracteres. Con un vocabulario de 65, la
pérdida esperada es `−ln(1/65) ≈ 4.17`. En la práctica sale algo más alta (en una prueba real, 4.53), porque los pesos aleatorios no dan
probabilidades exactamente iguales. **Si tu pérdida inicial está muy lejos de ese valor (por ejemplo, 0.5 o 20), algo está mal**: es una
comprobación que usan los profesionales. Tras entrenar, un bigrama baja a una pérdida de unos 2.5 en texto inglés: ha aprendido qué letras suelen seguir a cuáles,
pero genera palabras sin sentido, porque no tiene memoria más allá de un carácter.

---

## 5. Generar texto: muestrear

Para generar, se repite: calcular los logits de la **última posición**, convertirlos en probabilidades con softmax, **muestrear** un token y
añadirlo.

```python
@torch.no_grad()
def generar(modelo, idx, nuevos, temperatura=1.0):
    for _ in range(nuevos):
        idx_cond = idx[:, -block_size:]                 # no superar el contexto máximo
        logits, _ = modelo(idx_cond)
        logits = logits[:, -1, :] / temperatura         # solo la última posición
        probs = F.softmax(logits, dim=-1)
        siguiente = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, siguiente], dim=1)
    return idx
```

### Cómo funciona el muestreo

`torch.multinomial` elige un índice con probabilidad proporcional a `probs`. Por dentro equivale a: tomar un número aleatorio `r` entre 0 y
1 y recorrer las probabilidades **sumándolas** hasta que la suma supere `r`. Con probabilidades `[0.6, 0.3, 0.1]`, un `r` entre 0 y 0.6 da el
token 0; entre 0.6 y 0.9, el 1; por encima, el 2. Es lo que implementas en el ejercicio **Muestrear el siguiente token**.

### La temperatura

Dividir los logits entre la temperatura antes del softmax cambia cuánto se arriesga el modelo (lo viste en la ruta):

| Temperatura | Efecto |
|---|---|
| Baja (0.5) | Casi siempre el token más probable: texto repetitivo y "seguro" |
| 1.0 | Las probabilidades que aprendió el modelo |
| Alta (1.5) | Más variedad, más errores y texto más raro |

---

## 6. La atención: que cada token mire a los anteriores

El problema del bigrama es que cada posición ignora todo lo anterior. Queremos que la predicción en la posición *t* use la información de
las posiciones 0 a *t*... **y nunca de las siguientes**, porque al generar el futuro no existe.

### La versión más simple: promediar el pasado

Una primera idea: que cada posición reciba el **promedio** de los vectores de todas las anteriores (incluida ella). Hay un truco con
matrices para hacerlo de una vez: una matriz triangular inferior normalizada.

```python
T = 4
pesos = torch.tril(torch.ones(T, T))            # 1 en el triángulo inferior, 0 arriba
pesos = pesos / pesos.sum(dim=1, keepdim=True)  # cada fila suma 1
# fila 0: [1,   0,   0,   0  ]   ← la posición 0 solo se ve a sí misma
# fila 1: [0.5, 0.5, 0,   0  ]
# fila 2: [1/3, 1/3, 1/3, 0  ]
# fila 3: [1/4, 1/4, 1/4, 1/4]
# salida = pesos @ x    → cada posición, el promedio de su pasado
```

### Atención de verdad: pesos que dependen del contenido

Un promedio trata igual todo el pasado. La **autoatención** (*self-attention*) deja que cada posición **decida a qué atender** según el
contenido. Cada token produce tres vectores, con tres capas lineales:

- **Consulta** (*query*, q): "¿qué estoy buscando?"
- **Clave** (*key*, k): "¿qué contengo?"
- **Valor** (*value*, v): "¿qué información aporto si me eligen?"

La afinidad entre una posición y otra es el **producto punto** de la consulta de la primera con la clave de la segunda: si se parecen, la
afinidad es alta. Después:

1. Se **escalan** las afinidades dividiendo entre `√d` (d = tamaño de los vectores). Sin esto, con vectores grandes los productos punto
   crecen mucho, el softmax se vuelve casi "todo o nada" y el entrenamiento se complica.
2. Se aplica la **máscara causal**: las afinidades con posiciones **futuras** se ponen a `−∞`, para que el softmax les dé peso 0.
3. **Softmax** por filas: los pesos de atención, que suman 1.
4. La salida de cada posición es la **suma de los valores** ponderada por esos pesos.

Un ejemplo con una sola consulta: `q = [1, 0]` y dos claves `[1, 0]` y `[0, 1]`. Afinidades: 1 y 0; escaladas por √2: 0.707 y 0; softmax:
**[0.67, 0.33]**. La consulta atiende el doble a la primera clave, que "se le parece". Es el cálculo del ejercicio **Pesos de atención**.

```python
class Cabeza(nn.Module):
    """Una cabeza de autoatención causal."""
    def __init__(self, n_embd, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer("tril", torch.tril(torch.ones(block_size, block_size)))
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)                                               # (B, T, hs)
        q = self.query(x)                                             # (B, T, hs)
        afinidad = q @ k.transpose(-2, -1) * k.shape[-1] ** -0.5      # (B, T, T), escalada
        afinidad = afinidad.masked_fill(self.tril[:T, :T] == 0, float("-inf"))   # máscara causal
        pesos = F.softmax(afinidad, dim=-1)
        pesos = self.dropout(pesos)
        v = self.value(x)                                             # (B, T, hs)
        return pesos @ v                                              # (B, T, hs)
```

Lee las formas con calma: `q @ k.transpose(-2, -1)` es `(B, T, hs) @ (B, hs, T)` = `(B, T, T)`: una matriz de afinidades de cada posición
con cada posición, para cada secuencia del lote.

### Varias cabezas

Una sola cabeza aprende un tipo de relación. La **atención multicabeza** ejecuta varias en paralelo (una puede fijarse en la letra
anterior, otra en el inicio de la palabra...) y concatena sus resultados:

```python
class MultiCabeza(nn.Module):
    def __init__(self, n_embd, n_head):
        super().__init__()
        head_size = n_embd // n_head
        self.cabezas = nn.ModuleList([Cabeza(n_embd, head_size) for _ in range(n_head)])
        self.proj = nn.Linear(n_embd, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.cabezas], dim=-1)
        return self.dropout(self.proj(out))
```

### Comprueba que entendiste

**Pregunta:** en una secuencia de 5 tokens, ¿a cuántas posiciones puede atender el token de la posición 2 (contando desde 0)? Con `n_embd =
128` y 4 cabezas, ¿qué tamaño tiene cada cabeza?

**Respuesta:** a 3 posiciones (la 0, la 1 y ella misma); la máscara bloquea la 3 y la 4. Cada cabeza tiene 128 / 4 = 32 dimensiones, y al
concatenar las 4 se vuelve a 128.

---

## 7. El bloque transformer

Un **bloque** combina la atención (comunicación entre posiciones) con una pequeña red densa aplicada a cada posición por separado
(computación), más dos ingredientes que hacen posible apilar muchos bloques:

- **Conexiones residuales**: `x = x + atencion(x)`. La salida suma lo nuevo a lo que ya había, y los gradientes fluyen directos hacia las
  primeras capas.
- **LayerNorm**: normaliza cada vector antes de cada subcapa, lo que estabiliza el entrenamiento.

```python
class FeedForward(nn.Module):
    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.GELU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)


class Bloque(nn.Module):
    def __init__(self, n_embd, n_head):
        super().__init__()
        self.atencion = MultiCabeza(n_embd, n_head)
        self.ffwd = FeedForward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.atencion(self.ln1(x))     # comunicación + residual
        x = x + self.ffwd(self.ln2(x))         # computación + residual
        return x
```

---

## 8. El modelo completo

Faltan dos piezas: los **embeddings** (una tabla que convierte cada id en un vector aprendido) y los **embeddings de posición** (otra tabla,
para que el modelo sepa en qué posición está cada token: la atención por sí sola no conoce el orden).

```python
class MiniGPT(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, n_embd)
        self.pos_emb = nn.Embedding(block_size, n_embd)
        self.bloques = nn.Sequential(*[Bloque(n_embd, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size)     # de vector a puntuación de cada token

    def forward(self, idx, objetivos=None):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T))     # (B, T, n_embd)
        x = self.bloques(x)
        logits = self.lm_head(self.ln_f(x))                       # (B, T, vocab)
        if objetivos is None:
            return logits, None
        perdida = F.cross_entropy(logits.view(B * T, -1), objetivos.view(B * T))
        return logits, perdida
```

Esta es, en esencia, la arquitectura de GPT-2. Los modelos actuales (Llama, Qwen, Mistral) cambian detalles (otra forma de codificar la
posición, otra activación, otra normalización, atención más eficiente), pero la estructura es la misma: embeddings → N bloques de atención
y red densa → capa final que predice el siguiente token.

### Hiperparámetros para tu portátil

```python
block_size = 64      # contexto: 64 caracteres
batch_size = 32
n_embd = 128         # tamaño de los vectores
n_head = 4
n_layer = 4
dropout = 0.1
learning_rate = 1e-3
max_iters = 3000
```

Esto da un modelo de unos 800 000 parámetros (algo más o menos según el tamaño del vocabulario). En la CPU de un Ryzen 7, 3 000 pasos
tardan unos 17 minutos (lo verás medido en la sección 10); en una GPU de Colab, bastante menos (no lo he medido allí). Si va lento, reduce `max_iters`,
`n_layer` o `n_embd`; si quieres más calidad (y tienes Colab), súbelos.

---

## 9. El bucle de entrenamiento

El mismo patrón del capítulo de PyTorch, con una evaluación periódica en el conjunto de validación:

```python
torch.manual_seed(1337)
modelo = MiniGPT(vocab_size)
optimizador = torch.optim.AdamW(modelo.parameters(), lr=learning_rate)

@torch.no_grad()
def estimar_perdida():
    modelo.eval()
    resultado = {}
    for nombre, datos in [("train", datos_train), ("val", datos_val)]:
        perdidas = [modelo(*lote(datos, block_size, batch_size))[1].item() for _ in range(50)]
        resultado[nombre] = sum(perdidas) / len(perdidas)
    modelo.train()
    return resultado

for paso in range(max_iters):
    if paso % 500 == 0:
        print(paso, estimar_perdida())
    xb, yb = lote(datos_train, block_size, batch_size)
    _, perdida = modelo(xb, yb)
    optimizador.zero_grad()
    perdida.backward()
    optimizador.step()

contexto = torch.zeros((1, 1), dtype=torch.long)     # empezar con el id 0
print(decodificar(generar(modelo, contexto, 500)[0].tolist(), itos))
```

Este fragmento muestra la idea; para ejecutarlo, usa el **programa completo de la sección 10**, que junta todas las piezas en el orden
correcto.

Qué esperar: la pérdida empieza cerca de `ln(vocab)` (≈ 4.4 con 80 caracteres) y baja. Vigila que la de **validación** baje junto con la de
entrenamiento; si la de entrenamiento sigue bajando y la de validación sube, el modelo está memorizando (sobreajuste): con textos pequeños
pasa pronto, y el remedio es más texto, más dropout o un modelo más pequeño.

El texto generado no tendrá sentido, pero tendrá **la forma** del texto de entrenamiento: palabras que parecen del idioma, puntuación,
saltos de línea, nombres de personajes si entrenas con una obra de teatro. Esa mejora visible, del ruido aleatorio a "algo que parece
español", es lo que hace que este ejercicio cambie tu forma de entender los LLM.

---

## 10. El programa completo, listo para ejecutar

Las secciones anteriores explican el modelo por partes. Este es el programa entero, en orden, en un solo archivo. Está probado en un
portátil con PyTorch 2.x para CPU.

### Preparación

1. Instala PyTorch para CPU (ver *PyTorch esencial*).
2. Consigue un texto **largo** en un archivo `texto.txt` (UTF-8), en la misma carpeta que el programa. Cuanto más texto, mejor: al menos
   unos cientos de miles de caracteres. Buenas opciones:
   - Un libro en español de dominio público de **gutenberg.org** (por ejemplo, *Don Quijote*), descargado en formato *Plain Text UTF-8*.
   - Tus propios textos: tus apuntes, artículos que hayas escrito, letras de canciones que te gusten (solo para tu uso personal).
3. Guarda el programa como `mini_gpt.py` y ejecútalo con `python mini_gpt.py`.

### El programa

```python
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

# ---------------------------------------------------------------- ajustes
block_size = 64        # contexto: cuántos caracteres mira el modelo
batch_size = 32        # secuencias por lote
n_embd = 128           # tamaño de los vectores
n_head = 4             # cabezas de atención
n_layer = 4            # bloques transformer
dropout = 0.1
learning_rate = 1e-3
max_iters = 3000
eval_interval = 500
eval_iters = 50
torch.manual_seed(1337)

# ---------------------------------------------------------------- datos
with open("texto.txt", encoding="utf-8") as f:
    texto = f.read()

chars = sorted(set(texto))
vocab_size = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}


def codificar(s):
    return [stoi[c] for c in s]


def decodificar(ids):
    return "".join(itos[i] for i in ids)


datos = torch.tensor(codificar(texto), dtype=torch.long)
n = int(0.9 * len(datos))
datos_train, datos_val = datos[:n], datos[n:]
print(f"{len(texto):,} caracteres, vocabulario de {vocab_size}")


def lote(split):
    d = datos_train if split == "train" else datos_val
    ix = torch.randint(len(d) - block_size, (batch_size,))
    x = torch.stack([d[i:i + block_size] for i in ix])
    y = torch.stack([d[i + 1:i + block_size + 1] for i in ix])
    return x, y


# ---------------------------------------------------------------- modelo
class Cabeza(nn.Module):
    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer("tril", torch.tril(torch.ones(block_size, block_size)))
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)
        q = self.query(x)
        afinidad = q @ k.transpose(-2, -1) * k.shape[-1] ** -0.5
        afinidad = afinidad.masked_fill(self.tril[:T, :T] == 0, float("-inf"))
        pesos = self.dropout(F.softmax(afinidad, dim=-1))
        return pesos @ self.value(x)


class MultiCabeza(nn.Module):
    def __init__(self):
        super().__init__()
        self.cabezas = nn.ModuleList([Cabeza(n_embd // n_head) for _ in range(n_head)])
        self.proj = nn.Linear(n_embd, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.cabezas], dim=-1)
        return self.dropout(self.proj(out))


class FeedForward(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd), nn.GELU(), nn.Linear(4 * n_embd, n_embd), nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)


class Bloque(nn.Module):
    def __init__(self):
        super().__init__()
        self.atencion = MultiCabeza()
        self.ffwd = FeedForward()
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.atencion(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x


class MiniGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, n_embd)
        self.pos_emb = nn.Embedding(block_size, n_embd)
        self.bloques = nn.Sequential(*[Bloque() for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, objetivos=None):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T))
        x = self.bloques(x)
        logits = self.lm_head(self.ln_f(x))
        if objetivos is None:
            return logits, None
        perdida = F.cross_entropy(logits.view(B * T, -1), objetivos.view(B * T))
        return logits, perdida

    @torch.no_grad()
    def generar(self, idx, nuevos, temperatura=1.0):
        for _ in range(nuevos):
            logits, _ = self(idx[:, -block_size:])
            probs = F.softmax(logits[:, -1, :] / temperatura, dim=-1)
            idx = torch.cat([idx, torch.multinomial(probs, num_samples=1)], dim=1)
        return idx


@torch.no_grad()
def estimar_perdida(modelo):
    modelo.eval()
    resultado = {}
    for split in ("train", "val"):
        perdidas = [modelo(*lote(split))[1].item() for _ in range(eval_iters)]
        resultado[split] = round(sum(perdidas) / len(perdidas), 3)
    modelo.train()
    return resultado


# ---------------------------------------------------------------- entrenamiento
modelo = MiniGPT()
print(f"{sum(p.numel() for p in modelo.parameters()):,} parámetros")
optimizador = torch.optim.AdamW(modelo.parameters(), lr=learning_rate)

inicio = time.time()
for paso in range(max_iters):
    if paso % eval_interval == 0:
        print(paso, estimar_perdida(modelo), f"{time.time() - inicio:.0f} s")
    xb, yb = lote("train")
    _, perdida = modelo(xb, yb)
    optimizador.zero_grad()
    perdida.backward()
    optimizador.step()
print(max_iters, estimar_perdida(modelo), f"{time.time() - inicio:.0f} s")

# ---------------------------------------------------------------- generar
modelo.eval()
contexto = torch.zeros((1, 1), dtype=torch.long)
print(decodificar(modelo.generar(contexto, 400)[0].tolist()))
torch.save(modelo.state_dict(), "mini_gpt.pt")
```

(En este programa, `codificar` y `decodificar` usan los diccionarios del propio texto, igual que en tu ejercicio del tokenizador.)

### Qué esperar

Así fue una ejecución real en un portátil con un Ryzen 7 (solo CPU), entrenando con unos 680 000 caracteres de apuntes técnicos en español
(vocabulario de 156 caracteres, porque incluía símbolos de código y tablas):

```
682,976 caracteres, vocabulario de 156
840,092 parámetros
0 {'train': 5.221, 'val': 5.23} 6 s
500 {'train': 2.075, 'val': 2.162} 177 s
1000 {'train': 1.71, 'val': 1.86} 354 s
1500 {'train': 1.541, 'val': 1.733} 522 s
2000 {'train': 1.445, 'val': 1.648} 694 s
2500 {'train': 1.385, 'val': 1.604} 860 s
3000 {'train': 1.34, 'val': 1.583} 1028 s
```

Cómo leerlo:

- **Al inicio**, la pérdida (5.22) es cercana a `ln(156) ≈ 5.05`: el modelo no sabe nada. La comprobación de la sección 4 se cumple.
- **Baja rápido al principio** y después cada vez más despacio: lo normal.
- **La de validación va por encima de la de entrenamiento** y la distancia crece poco a poco (1.34 frente a 1.58 al final): empieza un
  ligero sobreajuste. Con más pasos, la de validación dejaría de bajar; ese sería el momento de parar.
- **El tiempo**: unos 17 minutos para 3 000 pasos en CPU. Si quieres probar rápido, empieza con `max_iters = 500` (unos 3 minutos); en una
  GPU de Colab tarda bastante menos (no lo he medido allí).

Y un fragmento del texto que generó tras entrenar:

```
2. **Documentos como entradas** explice, ni claves de por por copia azar un costo, el pedido de `undevuelve`.

---

## 3. Cada
```

No tiene sentido, pero fíjate en lo que **sí** aprendió en 17 minutos y sin saber nada de español: palabras reales ("documentos", "claves",
"costo", "pedido"), la puntuación, el formato Markdown de los apuntes (listas numeradas, negritas, separadores `---`, títulos `##`) e incluso
el estilo de las comillas de código. Con un texto narrativo (una novela) verás diálogos, nombres y frases con mucha más forma de español.

## 11. De tu mini-GPT a un LLM real

| | Tu mini-GPT | Un modelo de 8B (por ejemplo, Llama 3.1 8B) |
|---|---|---|
| Parámetros | ~0.8 millones | ~8 000 millones |
| Tokenizador | Caracteres (~80) | Subpalabras (~128 000) |
| Contexto | 64 tokens | 128 000 tokens |
| Capas | 4 | 32 |
| Datos de entrenamiento | Un libro | Billones de tokens |
| Hardware | Tu CPU, minutos | Miles de GPU, semanas |
| Después del preentrenamiento | Nada | Ajuste con instrucciones y con preferencias humanas |

Ese último punto es clave: tu mini-GPT (y cualquier modelo **base**) solo **continúa texto**. Los modelos que usas con Ollama en modo chat
(*instruct*) pasaron además por un **ajuste con instrucciones** (*SFT*: miles de ejemplos de pregunta y respuesta) y por un ajuste con
preferencias humanas (RLHF o DPO). El fine-tuning del bloque B es una versión pequeña de ese segundo paso.

---

## 12. Errores frecuentes

| Problema | Causa | Solución |
|---|---|---|
| La pérdida inicial no se parece a `ln(vocab)` | Error en los datos o en la pérdida | Revisar formas y que `y` esté desplazado una posición |
| Error de índice en `pos_emb` al generar | El contexto superó `block_size` | Recortar con `idx[:, -block_size:]` |
| El modelo genera texto perfecto del libro | Sobreajuste o fuga: memoriza | Más datos, más dropout, validar con otro trozo |
| La pérdida de validación sube | Sobreajuste | Parar antes o regularizar |
| Muy lento en CPU | Modelo o contexto demasiado grandes | Reducir `n_layer`, `n_embd` o `block_size`; o usar Colab |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Tarea | Predecir el siguiente token; generar = repetir muestreando |
| Tokenizador | Texto ↔ ids; aquí, un token por carácter |
| Pares | `y` es `x` desplazado una posición; muchos ejemplos por trozo |
| Bigrama | Una tabla; pérdida inicial ≈ `ln(vocab)` |
| Muestreo | Probabilidades acumuladas; temperatura antes del softmax |
| Atención | q·k / √d, máscara causal, softmax, suma ponderada de v |
| Multicabeza | Varias atenciones en paralelo, concatenadas |
| Bloque | Atención + red densa, con residuales y LayerNorm |
| Modelo | Embeddings de token y posición → bloques → capa final |
| Base frente a instruct | Un modelo base continúa texto; el chat requiere ajuste adicional |

## Autoevaluación final

1. Con un vocabulario de 50 caracteres, ¿qué pérdida esperas antes de entrenar?
2. Con los ids `[5, 9, 2, 7, 1]` y contexto 3, escribe el primer par `(x, y)`.
3. ¿Para qué sirve la máscara causal?
4. ¿Por qué se divide la afinidad entre `√d`?
5. ¿Qué aportan los embeddings de posición?
6. Generas con temperatura 0.3 y el texto se repite. ¿Por qué?
7. ¿Qué le falta a tu mini-GPT para comportarse como un asistente de chat?

**Respuestas:** 1) `ln(50) ≈ 3.91`. 2) `x = [5, 9, 2]`, `y = [9, 2, 7]`. 3) Para que cada posición solo atienda a las anteriores, como ocurre
al generar, y no "copie" el token que tiene que predecir. 4) Para que los productos punto no crezcan con la dimensión y el softmax no se
vuelva casi todo o nada. 5) La información del orden: la atención por sí sola no sabe en qué posición está cada token. 6) Una temperatura
baja concentra la probabilidad en los tokens más probables, así que elige casi siempre lo mismo. 7) Un ajuste con instrucciones (ejemplos de
pregunta y respuesta) y, después, con preferencias humanas; además de mucha más escala.
