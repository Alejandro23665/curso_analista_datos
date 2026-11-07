# Redes neuronales desde cero

Detrás de ChatGPT, Claude, los modelos que descargas con Ollama, el reconocimiento de voz y la generación de imágenes hay una misma idea,
repetida a escala gigantesca: **la red neuronal**. Y la red neuronal, a su vez, está hecha de una pieza muy simple: **la neurona
artificial**, que no es más que un producto punto, una suma y una función.

En este capítulo construyes esa pieza, la combinas en capas, defines cómo se mide el error y ves cómo la red **aprende** ajustando sus
pesos con el descenso de gradiente y la retropropagación. Al final entrenarás una red pequeña escrita entera con NumPy. Cuando más adelante
uses PyTorch, sabrás qué hace por dentro cada línea.

Necesitas el capítulo *Matemáticas para IA* (producto punto, matrices, softmax y descenso de gradiente).

---

## 1. La neurona artificial

Una neurona recibe varias **entradas** (números), multiplica cada una por un **peso**, suma todo, añade un **sesgo** (*bias*) y pasa el
resultado por una **función de activación**:

```
entradas:  x₁   x₂   x₃
pesos:     w₁   w₂   w₃

z = x₁·w₁ + x₂·w₂ + x₃·w₃ + b        ← producto punto + sesgo
salida = activación(z)
```

- Los **pesos** dicen cuánto importa cada entrada (y en qué sentido: un peso negativo resta).
- El **sesgo** desplaza el resultado, como el término independiente de una recta.
- Pesos y sesgo son los **parámetros**: lo que se ajusta al entrenar. Un modelo "de 3B" tiene unos 3 000 millones de estos números.

### Un ejemplo a mano

Entradas `[2, 1]`, pesos `[0.4, −0.5]`, sesgo `0.1`, activación sigmoide:

```
z = 2·0.4 + 1·(−0.5) + 0.1 = 0.8 − 0.5 + 0.1 = 0.4
sigmoide(0.4) = 1 / (1 + e^(−0.4)) ≈ 0.599
```

La neurona responde 0.599, que se puede leer como "un 60 % de probabilidad de que sí".

Una cosa importante: la cantidad de entradas y de pesos **tiene que coincidir**. Cada entrada necesita su peso; si no, el producto punto no
está definido.

---

## 2. Funciones de activación

Sin una función de activación, una neurona solo calcula una línea recta (o un plano). Y por muchas neuronas lineales que apiles, el
resultado sigue siendo lineal: una red así no podría aprender nada que no aprenda una regresión lineal. La activación añade la **no
linealidad** que permite aprender relaciones complejas.

| Activación | Fórmula | Rango | Uso típico |
|---|---|---|---|
| **Sigmoide** | `1 / (1 + e⁻ᶻ)` | 0 a 1 | Salida de una clasificación binaria (una probabilidad) |
| **Tanh** | `(eᶻ − e⁻ᶻ) / (eᶻ + e⁻ᶻ)` | −1 a 1 | Capas ocultas en redes pequeñas |
| **ReLU** | `max(0, z)` | 0 a ∞ | Capas ocultas: la más usada (simple y rápida) |
| **GELU** | Una ReLU "suavizada" | ≈ −0.17 a ∞ | Capas ocultas de los transformers (GPT, BERT) |
| **Softmax** | `eᶻⁱ / Σ eᶻʲ` | 0 a 1, suman 1 | Salida de una clasificación con varias clases (o el siguiente token) |

```python
import math

relu = lambda z: max(0, z)
sigmoide = lambda z: 1 / (1 + math.exp(-z))

relu(-3), relu(2.5)        # (0, 2.5)
sigmoide(0)                # 0.5
```

ReLU es sorprendentemente eficaz: deja pasar los valores positivos tal cual y convierte los negativos en 0. Con esa "esquina" se pueden
construir funciones tan complejas como haga falta combinando muchas neuronas.

### Comprueba que entendiste

**Pregunta:** una neurona con ReLU recibe `[1, 1]`, con pesos `[−2, 1]` y sesgo `0.5`. ¿Qué devuelve? ¿Y si la activación fuera sigmoide?

**Respuesta:** z = −2 + 1 + 0.5 = −0.5. Con ReLU, 0; con sigmoide, 1 / (1 + e^0.5) ≈ 0.378.

---

## 3. Capas y redes

Una **capa densa** (o *totalmente conectada*) es un grupo de neuronas que reciben **las mismas entradas**, cada una con sus propios
pesos y su sesgo. Si una capa tiene 3 neuronas y recibe 2 entradas, sus pesos forman una matriz de 3 × 2 (una fila de pesos por neurona) y
produce 3 salidas.

```
entradas [x₁, x₂] ──► neurona 1: w₁₁·x₁ + w₁₂·x₂ + b₁ → ReLU → s₁
                  ──► neurona 2: w₂₁·x₁ + w₂₂·x₂ + b₂ → ReLU → s₂
                  ──► neurona 3: w₃₁·x₁ + w₃₂·x₂ + b₃ → ReLU → s₃
```

Ejemplo numérico de una capa de 2 neuronas con ReLU, entradas `[3, −1]`:

```
neurona 1: pesos [1, 2],  sesgo 0  → 3·1 + (−1)·2 + 0 = 1   → ReLU → 1
neurona 2: pesos [−1, 1], sesgo 1  → 3·(−1) + (−1)·1 + 1 = −3 → ReLU → 0
salida de la capa: [1, 0]
```

Con NumPy, toda la capa es **una multiplicación de matriz por vector** más el sesgo: `np.maximum(0, W @ x + b)`. (Como viste en el
capítulo de matemáticas, cada fila de la matriz es una neurona.)

Una **red** apila capas: la salida de una es la entrada de la siguiente.

```
entrada (2) → capa oculta (16, ReLU) → capa oculta (16, ReLU) → salida (1, sigmoide)
```

Las capas del medio se llaman **ocultas**. Una red con varias capas ocultas es **profunda**: de ahí *deep learning*. Este recorrido de la
entrada a la salida se llama **paso hacia delante** (*forward pass*).

### Cuántos parámetros tiene una red

Cada capa densa tiene `entradas × neuronas` pesos más `neuronas` sesgos. La red de arriba: (2·16 + 16) + (16·16 + 16) + (16·1 + 1) = 48 +
272 + 17 = **337 parámetros**. Un LLM pequeño tiene miles de millones: misma idea, otra escala.

---

## 4. Medir el error: la función de pérdida

Para aprender, la red necesita un número que diga **cuánto se equivoca**. Esa es la **pérdida** (*loss*): cuanto más baja, mejor.

### Error cuadrático medio (para regresión)

```
MSE = promedio de (predicción − real)²
```

Elevar al cuadrado hace positivo cada error y castiga mucho los errores grandes. Predicciones `[2.5, 4]` frente a reales `[3, 3]`: errores
−0.5 y 1, cuadrados 0.25 y 1, media **0.625**.

### Entropía cruzada (para clasificación)

Cuando la red da **probabilidades**, la pérdida es menos el logaritmo de la probabilidad que asignó a la **respuesta correcta**:

```
pérdida = −ln(p_correcta)
```

| Probabilidad dada a la respuesta correcta | Pérdida |
|---|---|
| 0.9 | 0.105 (bien) |
| 0.5 | 0.693 |
| 0.1 | 2.303 (mal) |
| 0.001 | 6.908 (muy mal) |

Castiga mucho estar **seguro y equivocado**. Esta es exactamente la pérdida con la que se entrenan los LLM: en cada posición del texto, el
modelo da una distribución sobre el vocabulario, y la pérdida es −ln de la probabilidad que dio al token que de verdad venía. Si `p` llega
a ser 0, el logaritmo es −∞; en la práctica se usa un mínimo muy pequeño para no romper el cálculo.

---

## 5. Aprender: el descenso de gradiente aplicado a un modelo

Empecemos por el modelo más simple: **una neurona sin activación**, que es una regresión lineal: `pred = w·x + b`. Queremos aprender `w` y
`b` a partir de ejemplos, minimizando el MSE.

Las derivadas del MSE respecto a cada parámetro (con n ejemplos) son:

```
∂L/∂w = (2/n) · Σ (pred − y) · x
∂L/∂b = (2/n) · Σ (pred − y)
```

Intuición: si la predicción es demasiado alta (`pred − y` positivo) en ejemplos con `x` grande, conviene **bajar** `w`; el gradiente es
positivo y el descenso lo resta.

### Una época a mano

Datos que siguen `y = 2x + 1`: `xs = [1, 2, 3]`, `ys = [3, 5, 7]`. Empezamos en `w = 0`, `b = 0`, tasa 0.1:

| x | y | pred = 0·x + 0 | pred − y | (pred − y)·x |
|---|---|---|---|---|
| 1 | 3 | 0 | −3 | −3 |
| 2 | 5 | 0 | −5 | −10 |
| 3 | 7 | 0 | −7 | −21 |
| **suma** | | | **−15** | **−34** |

- `∂L/∂w = (2/3)·(−34) ≈ −22.67` y `∂L/∂b = (2/3)·(−15) = −10`.
- `w = 0 − 0.1·(−22.67) ≈ 2.27` y `b = 0 − 0.1·(−10) = 1.0`.

Tras una sola época, `w` ya está cerca de 2. Repitiendo cientos de épocas, converge a `w = 2`, `b = 1`.

Un detalle de implementación que causa muchos errores: **calcula todas las predicciones con los `w` y `b` actuales antes de
actualizarlos**. Si actualizas `w` a mitad del recorrido, el resto de los ejemplos usa un `w` distinto y los gradientes ya no son los del
mismo punto.

### Vocabulario del entrenamiento

| Término | Significado |
|---|---|
| **Época** | Una pasada completa por todos los datos de entrenamiento |
| **Lote** (*batch*) | Un grupo de ejemplos con el que se calcula un paso; con millones de datos no se usan todos a la vez |
| **Iteración** | Un paso de actualización (un lote) |
| **Tasa de aprendizaje** | El tamaño del paso; el hiperparámetro más importante |
| **Hiperparámetro** | Algo que eliges tú, no la red: tasa, épocas, tamaño de lote, número de capas |

### Optimizadores: mejoras al descenso de gradiente

El descenso de gradiente básico usa **el mismo tamaño de paso para todos los pesos** y solo mira el gradiente **del paso actual**. Funciona,
pero es lento en terrenos irregulares. Los optimizadores modernos añaden dos ideas:

- **Momento** (*momentum*): en lugar de moverse solo según el gradiente actual, se mueve según un **promedio de los gradientes recientes**,
  como una bola que rueda y gana inercia. Atraviesa zonas planas más rápido y oscila menos cuando la pendiente cambia de dirección.
- **Paso adaptativo por peso**: cada peso lleva la cuenta de cuánto han variado sus gradientes. Los pesos con gradientes grandes y
  ruidosos dan pasos más cortos; los que reciben gradientes pequeños, pasos más largos.

**Adam** combina las dos ideas, y **AdamW** es la variante que aplica correctamente la regularización (*weight decay*). Es el optimizador
por defecto para entrenar y afinar redes, incluidos los LLM: converge rápido y es poco sensible a la tasa de aprendizaje elegida (valores
típicos: `1e-3` para entrenar redes pequeñas, entre `1e-5` y `2e-4` para afinar modelos de lenguaje). A cambio, guarda **dos números
extra por cada peso** (el promedio de los gradientes y el de sus cuadrados), lo que triplica la memoria de los parámetros durante el
entrenamiento: una de las razones por las que entrenar gasta mucha más memoria que usar el modelo.

### Comprueba que entendiste

**Pregunta:** con datos `xs = [1, 2]`, `ys = [2, 4]`, `w = 0`, `b = 0` y tasa 0.1, ¿cuánto vale `w` tras una época?

**Respuesta:** las predicciones son 0, así que `pred − y` vale −2 y −4; `∂L/∂w = (2/2)·(−2·1 − 4·2) = −10` y `w = 0 − 0.1·(−10) = 1`.

---

## 6. Retropropagación: el gradiente de una red entera

Con una neurona, las derivadas se escriben a mano. Con una red de varias capas, cada peso influye en la pérdida **a través de las capas
siguientes**. La **retropropagación** (*backpropagation*) calcula todos esos gradientes de forma eficiente usando la **regla de la
cadena**: si `a` afecta a `b` y `b` afecta a la pérdida, entonces

```
∂pérdida/∂a = ∂pérdida/∂b · ∂b/∂a
```

Es decir, el efecto de `a` sobre la pérdida es el efecto de `b` sobre la pérdida **multiplicado** por cuánto cambia `b` cuando cambia `a`.

La retropropagación aplica esta regla **desde la salida hacia atrás**, capa a capa:

1. **Paso hacia delante**: calcula y guarda la salida de cada capa.
2. Calcula la pérdida.
3. **Paso hacia atrás**: empezando por la salida, calcula el gradiente de la pérdida respecto a la salida de cada capa, y de ahí respecto a
   sus pesos, reutilizando lo calculado en la capa de después.
4. **Actualiza** todos los pesos con el descenso de gradiente.

### Un ejemplo mínimo con números

Una cadena de dos operaciones: `h = 3·w` y `L = (h − 12)²`, con `w = 2`.

- Hacia delante: `h = 6`, `L = (6 − 12)² = 36`.
- Hacia atrás: `∂L/∂h = 2·(h − 12) = −12`; `∂h/∂w = 3`.
- Regla de la cadena: `∂L/∂w = −12 · 3 = −36`. Negativo: aumentar `w` reduce la pérdida (y efectivamente, con `w = 4`, `h = 12` y la
  pérdida sería 0).

No vas a escribir retropropagaciones a mano en tu trabajo: **PyTorch lo hace automáticamente** (lo verás en el siguiente tema). Pero saber
que es "la regla de la cadena aplicada hacia atrás" explica muchos fenómenos: por qué los gradientes pueden hacerse diminutos o enormes en
redes muy profundas, o por qué hay que guardar las activaciones del paso hacia delante (y por eso entrenar gasta mucha más memoria que
usar el modelo).

---

## 7. Una red completa en NumPy: aprender XOR

El problema **XOR** ("o exclusivo") es el ejemplo clásico de algo que **una sola neurona no puede aprender**, porque no se separa con una
línea recta: la salida es 1 cuando las dos entradas son distintas.

| x₁ | x₂ | XOR |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Con una capa oculta, sí. Esta es una red completa, con paso hacia delante, retropropagación y descenso de gradiente, en unas 20 líneas:

```python
import numpy as np

rng = np.random.default_rng(42)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)

W1 = rng.normal(0, 1, (2, 4)); b1 = np.zeros(4)     # capa oculta: 2 entradas → 4 neuronas
W2 = rng.normal(0, 1, (4, 1)); b2 = np.zeros(1)     # salida: 4 → 1
sigmoide = lambda z: 1 / (1 + np.exp(-z))
tasa = 0.5

for epoca in range(5001):
    # hacia delante
    h = np.tanh(X @ W1 + b1)
    p = sigmoide(h @ W2 + b2)
    perdida = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))

    # hacia atrás (regla de la cadena)
    dz2 = (p - y) / len(X)              # sigmoide + entropía cruzada: el gradiente queda así de simple
    dW2 = h.T @ dz2; db2 = dz2.sum(axis=0)
    dh = dz2 @ W2.T
    dz1 = dh * (1 - h ** 2)             # derivada de tanh
    dW1 = X.T @ dz1; db1 = dz1.sum(axis=0)

    # descenso de gradiente
    W1 -= tasa * dW1; b1 -= tasa * db1
    W2 -= tasa * dW2; b2 -= tasa * db2

    if epoca % 1000 == 0:
        print(epoca, round(perdida, 4))

print(np.round(p.ravel(), 2))
```

Salida:

```
0 0.8299
1000 0.0055
2000 0.0024
3000 0.0015
4000 0.0011
5000 0.0009
[0. 1. 1. 0.]
```

La pérdida baja de 0.83 a casi 0 y la red responde exactamente la tabla de XOR. Fíjate en que procesa **los 4 ejemplos a la vez** con
productos de matrices (`X @ W1`): así funciona el entrenamiento por lotes.

### Una lección inesperada: la inicialización importa

Con la semilla `default_rng(0)` en lugar de 42, esta misma red se queda atascada en una pérdida de 0.347 y responde `[0, 0.5, 1, 0.5]`:
cayó en un **mínimo local**, un valle que no es el más profundo. Los pesos iniciales aleatorios deciden por dónde empieza a bajar la
montaña. En redes grandes este problema se nota mucho menos (hay tantas dimensiones que casi siempre existe una dirección para seguir
bajando), y existen técnicas de inicialización pensadas para evitarlo. Pero es un buen recordatorio: **el entrenamiento no siempre sale
bien a la primera**, y repetir con otra semilla es una prueba legítima.

---

## 8. Problemas típicos al entrenar

| Síntoma | Causa probable | Qué probar |
|---|---|---|
| La pérdida crece o da `nan` | Tasa de aprendizaje demasiado grande | Dividirla entre 10 |
| La pérdida baja muy despacio | Tasa demasiado pequeña | Aumentarla |
| Pérdida de entrenamiento baja, validación sube | Sobreajuste | Más datos, parar antes, *dropout*, red más pequeña |
| La pérdida no baja nada desde el inicio | Error en el código, datos mal preparados, etiquetas desordenadas | Entrenar con 10 ejemplos: debería memorizarlos |
| Se estanca en un valor alto | Mínimo local, red demasiado pequeña | Otra semilla, más neuronas |

**El truco de los 10 ejemplos**: si tu red no consigue memorizar un conjunto diminuto, el problema no es la red, sino el código. Es la
primera prueba que hacen los profesionales.

### Dropout y otras regularizaciones

**Dropout** apaga al azar una parte de las neuronas en cada paso de entrenamiento (por ejemplo, el 10 %). La red no puede depender de
ninguna neurona concreta y generaliza mejor. Al **evaluar**, el dropout se desactiva: por eso en PyTorch hay que poner el modelo en modo
evaluación, como verás en el siguiente tema.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Neurona | Producto punto de entradas y pesos + sesgo, y una activación |
| Activación | Añade no linealidad; ReLU en capas ocultas, sigmoide o softmax en la salida |
| Capa densa | Varias neuronas con las mismas entradas: matriz por vector + sesgo |
| Red | Capas apiladas; paso hacia delante de la entrada a la salida |
| Pérdida | MSE para regresión; entropía cruzada (−ln p_correcta) para clasificación y LLM |
| Descenso de gradiente | Calcular todas las predicciones, luego los gradientes, luego actualizar |
| Retropropagación | Regla de la cadena desde la salida hacia atrás |
| Adam / AdamW | Momento + paso adaptativo por peso; el optimizador por defecto |
| Época, lote, tasa | Pasada completa, grupo de ejemplos, tamaño del paso |
| Problemas | Tasa grande → explota; sobreajuste → validación sube; no aprende → prueba con 10 ejemplos |

## Autoevaluación final

1. Calcula la salida de una neurona con entradas `[1, 3]`, pesos `[2, −1]`, sesgo `1` y activación ReLU.
2. ¿Por qué una red sin funciones de activación no es más potente que una regresión lineal?
3. Una capa densa recibe 10 entradas y tiene 5 neuronas. ¿Cuántos parámetros tiene?
4. Un modelo da probabilidad 0.25 a la respuesta correcta. ¿Cuál es su entropía cruzada?
5. Al entrenar `pred = w·x + b`, actualizas `w` en mitad del recorrido de los datos. ¿Qué problema hay?
6. Con `h = 2·w` y `L = h²`, ¿cuánto vale `∂L/∂w` cuando `w = 3`?
7. Tu pérdida no baja ni siquiera con 10 ejemplos. ¿Qué sospechas?

**Respuestas:** 1) z = 1·2 + 3·(−1) + 1 = 0 → ReLU(0) = 0. 2) Porque apilar operaciones lineales sigue dando una operación lineal; la
activación añade la no linealidad. 3) 10·5 pesos + 5 sesgos = 55. 4) −ln(0.25) ≈ 1.386. 5) Los ejemplos siguientes usan un `w` distinto:
el gradiente ya no corresponde a un único punto; hay que calcular todo antes de actualizar. 6) ∂L/∂h = 2h = 12 y ∂h/∂w = 2 → 24.
7) Un error en el código o en la preparación de los datos, no un problema de capacidad de la red.
