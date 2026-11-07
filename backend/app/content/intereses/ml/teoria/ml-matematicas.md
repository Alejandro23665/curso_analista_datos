# Matemáticas para IA, con intuición

Para usar un modelo no hace falta saber matemáticas. Para **entender** qué hace, por qué falla y cómo mejorarlo, sí hace falta un poco:
el suficiente para que palabras como *embedding*, *softmax*, *pérdida* o *gradiente* dejen de ser magia. La buena noticia es que es una
porción pequeña de las matemáticas, y se entiende mejor con ejemplos y código que con fórmulas.

Este capítulo cubre exactamente lo que vas a necesitar en el resto del bloque: **vectores** (cómo representa un modelo el significado),
**matrices** (cómo transforma esa información una red), **probabilidad** (cómo elige un modelo la siguiente palabra) y **derivadas y
gradiente** (cómo aprende). Sin demostraciones: intuición, ejemplos a mano y NumPy.

---

## 1. Vectores: listas de números con significado

Un **vector** es una lista ordenada de números. En IA casi todo se convierte en vectores:

- Una casa: `[metros, habitaciones, antigüedad]` → `[85, 3, 12]`.
- Una imagen pequeña en blanco y negro: un vector con el brillo de cada píxel.
- Una palabra o una frase: un **embedding**, un vector de cientos o miles de números que representa su significado.

Lo importante: **la posición importa**. `[85, 3, 12]` y `[3, 85, 12]` son casas muy distintas. Cada posición es una **dimensión** o
característica.

Se puede pensar en un vector de 2 números como una flecha en un plano: `[3, 4]` va 3 a la derecha y 4 hacia arriba. Con 768 números no se
puede dibujar, pero las mismas ideas (longitud, dirección, ángulo) siguen funcionando.

### Operaciones básicas

| Operación | Ejemplo | Resultado |
|---|---|---|
| Suma (elemento a elemento) | `[1, 2] + [3, 5]` | `[4, 7]` |
| Multiplicar por un número | `3 · [1, 2]` | `[3, 6]` |
| Longitud (norma) | `‖[3, 4]‖ = √(3² + 4²)` | `5` |

### NumPy: vectores de verdad en Python

Con listas de Python, `[1, 2] + [3, 5]` **concatena** (`[1, 2, 3, 5]`). Para operar como vectores se usa **NumPy**:

```python
import numpy as np

a = np.array([1, 2])
b = np.array([3, 5])
print(a + b)              # [4 7]
print(3 * a)              # [3 6]
print(np.linalg.norm(np.array([3, 4])))   # 5.0
```

NumPy opera con todos los elementos a la vez (**vectorización**), escrito en C y muchísimo más rápido que un bucle de Python. Es la base de
PyTorch, de scikit-learn y de casi todo el ML en Python.

---

## 2. El producto punto: la operación más importante de la IA

El **producto punto** de dos vectores multiplica elemento a elemento y suma:

```
[2, 1, 3] · [4, 0, 1] = 2·4 + 1·0 + 3·1 = 11
```

```python
np.dot([2, 1, 3], [4, 0, 1])    # 11
np.array([2, 1, 3]) @ np.array([4, 0, 1])   # 11 (el operador @)
```

¿Por qué es tan importante? Porque mide **cuánto se parecen dos vectores en dirección**:

- Si apuntan en la misma dirección, el producto es grande y positivo.
- Si son perpendiculares (sin relación), es 0.
- Si apuntan en direcciones opuestas, es negativo.

Cuando los vectores tienen longitud 1 (están **normalizados**), el producto punto es exactamente la **similitud coseno**: un número entre −1
y 1. Así se comparan embeddings en un RAG: los fragmentos cuyo embedding tiene mayor producto punto con el de la pregunta son los más
relevantes.

Y es el corazón de dos piezas que verás en este bloque:

- **Una neurona** calcula un producto punto entre sus entradas y sus pesos.
- **La atención** de un transformer calcula productos punto entre una "consulta" y unas "claves" para decidir a qué palabras prestar
  atención.

### Comprueba que entendiste

**Pregunta:** ¿cuál es el producto punto de `[1, -1]` y `[1, 1]`? ¿Qué dice de los dos vectores?

**Respuesta:** 1·1 + (−1)·1 = 0: son perpendiculares (no se parecen en dirección).

---

## 3. Matrices: tablas que transforman vectores

Una **matriz** es una tabla de números con filas y columnas. Su **forma** (*shape*) se escribe `(filas, columnas)`.

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])
M.shape          # (2, 3): 2 filas, 3 columnas
```

En ML, una matriz suele ser:

- **Un conjunto de datos**: una fila por ejemplo, una columna por característica (100 casas × 3 características = forma `(100, 3)`).
- **Los pesos de una capa** de una red neuronal.

### Matriz por vector

Multiplicar una matriz por un vector da **otro vector**: cada elemento del resultado es el **producto punto de una fila** de la matriz con
el vector.

```
| 2  0 |   | 3 |   | 2·3 + 0·1 |   | 6 |
| 1  4 | · | 1 | = | 1·3 + 4·1 | = | 7 |
| 0  1 |           | 0·3 + 1·1 |   | 1 |
```

Una matriz de forma `(3, 2)` por un vector de 2 elementos da un vector de 3: **transforma** un vector de 2 dimensiones en uno de 3. Eso es,
exactamente, lo que hace una **capa** de una red neuronal: recibe un vector y produce otro, con tantos elementos como neuronas tiene.

La condición: **el número de columnas de la matriz debe coincidir con la longitud del vector**. Si no, la operación no está definida (y en
NumPy o PyTorch obtienes un error de formas, el error más frecuente del deep learning).

### Matriz por matriz

Multiplicar dos matrices es hacer muchos "matriz por vector" a la vez. La regla de formas:

```
(n, k) @ (k, m) → (n, m)
```

Las dimensiones "de dentro" (`k`) deben coincidir y desaparecen; las de fuera dan la forma del resultado. Por ejemplo, 100 casas con 3
características `(100, 3)` multiplicadas por los pesos de una capa de 16 neuronas `(3, 16)` dan `(100, 16)`: 16 valores nuevos para cada
una de las 100 casas, todo en una sola operación. Por eso las GPU, que hacen multiplicaciones de matrices enormes en paralelo, aceleran
tanto el ML.

```python
X = np.random.rand(100, 3)
W = np.random.rand(3, 16)
(X @ W).shape        # (100, 16)
```

### La transpuesta

La **transpuesta** `M.T` intercambia filas y columnas: una matriz `(2, 3)` pasa a `(3, 2)`. La verás constantemente para hacer encajar las
formas de un producto.

---

## 4. Probabilidad: cómo "elige" un modelo

Un modelo de lenguaje no "sabe" la siguiente palabra: calcula una **distribución de probabilidad** sobre todas las posibles.

```
"El gato está en el ___"
  tejado: 0.42   sofá: 0.31   jardín: 0.18   coche: 0.09
```

Una distribución de probabilidad cumple dos reglas: **cada probabilidad está entre 0 y 1** y **todas suman 1**.

### Estadística mínima: centro, dispersión y la distribución normal

Tres medidas que aparecen en todo el ML (al preparar los datos y al crear los pesos iniciales de una red):

- **Media**: la suma dividida entre la cantidad. El "centro" de los datos.
- **Varianza**: el promedio de las distancias **al cuadrado** a la media. Mide cuánto se dispersan los datos.
- **Desviación típica** (*standard deviation*): la raíz cuadrada de la varianza. Está en las mismas unidades que los datos: "la mayoría de
  los valores están a unas 2 unidades de la media".

Ejemplo con `[2, 4, 4, 4, 5, 5, 7, 9]`: media **5**; distancias a la media al cuadrado `9, 1, 1, 1, 0, 0, 4, 16`, cuyo promedio es la
varianza, **4**; desviación típica **√4 = 2**.

```python
d = np.array([2, 4, 4, 4, 5, 5, 7, 9])
d.mean(), d.var(), d.std()      # (5.0, 4.0, 2.0)
```

**Estandarizar** un valor es expresarlo en "desviaciones típicas respecto a la media": `z = (x − media) / desviación`. El 9 del ejemplo
tiene `z = (9 − 5) / 2 = 2`: está dos desviaciones por encima de la media. Estandarizar todas las columnas de un conjunto de datos las pone
en la misma escala (media 0, desviación 1), y eso es lo que necesitan algoritmos como k vecinos o las redes neuronales para que una
característica con números grandes (metros: 60-120) no domine a otra con números pequeños (habitaciones: 1-3). Lo verás en *Machine
learning clásico*.

La **distribución normal** (la "campana de Gauss") describe muchísimos fenómenos: la mayoría de los valores cerca de la media y cada vez
menos hacia los extremos. Una regla útil: aproximadamente el **68 %** de los valores cae a menos de 1 desviación típica de la media, el
**95 %** a menos de 2 y el **99.7 %** a menos de 3. Cuando en PyTorch creas pesos con `torch.randn`, los estás sacando de una normal de
media 0 y desviación 1.

### De puntuaciones a probabilidades: softmax

La red produce primero **puntuaciones** cualesquiera (*logits*), que pueden ser negativas o mayores que 1. La función **softmax** las
convierte en probabilidades: aplica la exponencial (que hace todo positivo y exagera las diferencias) y divide entre la suma.

```python
def softmax(z):
    e = np.exp(z - np.max(z))     # restar el máximo evita desbordamientos
    return e / e.sum()

softmax(np.array([2.0, 1.0, 0.1]))   # [0.659, 0.242, 0.099]
```

Ya viste en la ruta (*Cómo funcionan los LLMs por dentro*) cómo la **temperatura** divide los logits antes del softmax para hacer la
distribución más "afilada" o más "plana".

### Entropía: cuánta incertidumbre hay

La **entropía** mide cuánta incertidumbre tiene una distribución. Su fórmula (en bits):

```
H = − Σ p · log₂(p)
```

(los términos con p = 0 no cuentan: se toma 0 · log 0 = 0).

| Distribución | Entropía | Interpretación |
|---|---|---|
| `[1.0, 0, 0, 0]` | 0 bits | Certeza total |
| `[0.5, 0.5]` | 1 bit | Una moneda justa |
| `[0.25, 0.25, 0.25, 0.25]` | 2 bits | Máxima incertidumbre con 4 opciones |
| `[0.7, 0.1, 0.1, 0.1]` | 1.357 bits | Bastante seguro, pero no del todo |

Calculemos la última a mano: `0.7·log₂(0.7) ≈ −0.360`, y `0.1·log₂(0.1) ≈ −0.332` tres veces (−0.997). Suma: −1.357, con el signo cambiado,
**1.357 bits**.

¿Para qué sirve? La **entropía cruzada**, una pariente cercana, es la **función de pérdida** con la que se entrenan los clasificadores y
los LLM: mide lo "sorprendido" que está el modelo al ver la respuesta correcta. La verás en *Redes neuronales desde cero*.

### Logaritmos en dos líneas

- `log₂(8) = 3` porque 2³ = 8. El logaritmo pregunta "¿a qué número elevo la base para obtener esto?".
- `log(1) = 0` en cualquier base, y el logaritmo de un número entre 0 y 1 es **negativo**. Por eso la entropía lleva un signo menos: para
  que el resultado sea positivo.
- En Python: `math.log2(x)`, `math.log(x)` (logaritmo natural, base e) y `np.log(x)` para vectores. El logaritmo de 0 **no existe**: hay que
  evitar calcularlo.

### Comprueba que entendiste

**Pregunta:** ¿qué distribución tiene más entropía, `[0.9, 0.1]` o `[0.6, 0.4]`?

**Respuesta:** `[0.6, 0.4]`: está más cerca de la incertidumbre total (0.5, 0.5).

---

## 5. Derivadas: hacia dónde ir para mejorar

Entrenar un modelo significa **ajustar sus números (pesos) para que se equivoque menos**. Para eso se mide el error con una **función de
pérdida** y se busca cómo cambiar cada peso para que la pérdida baje. La herramienta para eso es la **derivada**.

La derivada de una función en un punto dice **cuánto cambia la salida si mueves un poco la entrada**, y en qué sentido:

- Derivada **positiva**: si aumentas la entrada, la salida sube.
- Derivada **negativa**: si aumentas la entrada, la salida baja.
- Derivada **cero**: estás en un punto plano (a menudo, un mínimo o un máximo).

Ejemplo: `f(x) = x²`. Su derivada es `f'(x) = 2x`.

- En `x = 3`: derivada 6, positiva. Si aumentas x, f sube. **Para bajar, mueve x hacia la izquierda.**
- En `x = −2`: derivada −4, negativa. **Para bajar, mueve x hacia la derecha.**
- En `x = 0`: derivada 0. Es el mínimo.

Fíjate en la regla: **para bajar, muévete en sentido contrario a la derivada**. Esa es toda la idea del entrenamiento.

No necesitas calcular derivadas a mano (PyTorch lo hace solo, como verás). Algunas útiles para entender los ejemplos:

| Función | Derivada |
|---|---|
| `c` (constante) | 0 |
| `a·x` | `a` |
| `x²` | `2x` |
| `(x − c)²` | `2(x − c)` |
| `eˣ` | `eˣ` |

### Derivada numérica

Si no conoces la fórmula, puedes aproximar la derivada calculando la función en dos puntos muy cercanos:

```python
def derivada_numerica(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

derivada_numerica(lambda x: x ** 2, 3)    # ≈ 6.0
```

Es útil para **comprobar** que una derivada calculada a mano (o por tu código) es correcta.

---

## 6. El gradiente y el descenso de gradiente

Un modelo real no tiene un número que ajustar, sino millones. El **gradiente** es el vector con la derivada de la pérdida respecto a
**cada** peso: dice, para cada peso, en qué sentido y con qué fuerza afecta a la pérdida.

El **descenso de gradiente** repite un paso muy simple:

```
peso_nuevo = peso − tasa_de_aprendizaje × derivada
```

- Se resta porque queremos ir **en contra** de la derivada (hacia abajo).
- La **tasa de aprendizaje** (*learning rate*) decide el tamaño del paso.

Imagina que bajas una montaña con niebla: no ves el valle, pero sientes la pendiente bajo los pies y das un paso cuesta abajo. Repites.

### Un ejemplo a mano

Minimicemos `f(x) = (x − 5)²`, cuyo mínimo está en `x = 5`. Su derivada es `2(x − 5)`. Empezamos en `x = 1` con tasa 0.25:

| Paso | x | derivada 2(x − 5) | x nuevo = x − 0.25 · derivada |
|---|---|---|---|
| 1 | 1 | −8 | 1 + 2 = 3 |
| 2 | 3 | −4 | 3 + 1 = 4 |
| 3 | 4 | −2 | 4 + 0.5 = 4.5 |
| 4 | 4.5 | −1 | 4.75 |

Cada paso se acerca al 5, y los pasos se hacen más pequeños porque la pendiente es más suave cerca del mínimo.

### La tasa de aprendizaje importa muchísimo

- **Demasiado pequeña**: llegas, pero tardas muchísimos pasos.
- **Adecuada**: llegas en pocos pasos.
- **Demasiado grande**: cada paso se pasa del mínimo hacia el otro lado, cada vez más lejos, y los valores **explotan** (en la práctica,
  ves la pérdida crecer hasta `inf` o `nan`).

Con `f(x) = (x − 5)²` y una tasa de 1.2, desde x = 1: la derivada es −8, x pasa a 1 + 9.6 = 10.6; la derivada ahora es 11.2, x pasa a
10.6 − 13.44 = −2.84... cada vez más lejos. Es el primer sospechoso cuando un entrenamiento "explota".

### Comprueba que entendiste

**Pregunta:** en `f(x) = x²`, estás en `x = −4` con tasa 0.1. ¿Cuál es el siguiente x?

**Respuesta:** la derivada es 2·(−4) = −8; x nuevo = −4 − 0.1·(−8) = −3.2. Se acerca al mínimo (0).

---

## 7. Cómo encaja todo

Este es el mapa del resto del bloque, con las piezas de este capítulo:

```
datos ──► vectores (características o embeddings)
           │
           ▼
capa: matriz de pesos @ vector + sesgo ──► activación ──► ... más capas ...
           │
           ▼
puntuaciones (logits) ──► softmax ──► probabilidades
           │
           ▼
pérdida (entropía cruzada) frente a la respuesta correcta
           │
           ▼
gradiente de la pérdida respecto a cada peso ──► descenso de gradiente ──► pesos un poco mejores
           │
           └── se repite miles de veces = entrenar
```

Cada flecha usa algo de este capítulo: vectores, productos de matrices, probabilidades, logaritmos y derivadas.

---

## 8. Errores frecuentes

| Error | Qué pasa | Solución |
|---|---|---|
| Sumar listas de Python esperando sumar vectores | Se concatenan | Usar arrays de NumPy |
| Confundir `*` y `@` en NumPy | `*` multiplica elemento a elemento; `@` hace producto punto o matricial | Pensar qué forma esperas |
| Formas incompatibles en un producto | Error de *shape* | Comprobar que coincidan las dimensiones de dentro |
| Calcular `log(0)` | `-inf` o error | Filtrar los ceros o usar un mínimo pequeño |
| `exp` de números grandes | Desbordamiento (`inf`) | Restar el máximo antes del softmax |
| Tasa de aprendizaje demasiado grande | La pérdida explota | Reducirla (por ejemplo, dividir entre 10) |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Vector | Lista ordenada de números; cada posición, una característica |
| NumPy | Operaciones con vectores y matrices enteros, rápidas |
| Producto punto | Multiplicar y sumar; mide similitud de dirección; base de neuronas y atención |
| Matriz | Tabla `(filas, columnas)`; matriz por vector = una capa |
| Regla de formas | `(n, k) @ (k, m) → (n, m)` |
| Media y desviación típica | Centro y dispersión; estandarizar = `(x − media) / desviación` |
| Softmax | Puntuaciones → probabilidades que suman 1 |
| Entropía | `−Σ p·log₂ p`; 0 = certeza; más alta = más incertidumbre |
| Derivada | Cuánto y en qué sentido cambia la salida |
| Descenso de gradiente | `peso − tasa × derivada`, repetido; la tasa decide si converge o explota |

## Autoevaluación final

1. ¿Qué devuelve `[1, 2] + [3, 4]` con listas de Python y con arrays de NumPy?
2. Calcula el producto punto de `[1, 2, 3]` y `[4, 5, 6]`.
3. Una matriz de forma `(5, 3)` multiplica a un vector de 3 elementos. ¿Qué forma tiene el resultado?
4. ¿Se puede calcular `(4, 2) @ (3, 5)`? ¿Por qué?
5. ¿Cuál es la entropía de `[0.25, 0.25, 0.25, 0.25]`?
6. En el descenso de gradiente, ¿por qué se **resta** la derivada?
7. La pérdida de tu entrenamiento crece en cada paso hasta `nan`. ¿Qué sospechas?

**Respuestas:** 1) Listas: `[1, 2, 3, 4]` (se concatenan); NumPy: `[4, 6]`. 2) 4 + 10 + 18 = 32. 3) Un vector de 5 elementos. 4) No: las
dimensiones de dentro (2 y 3) no coinciden. 5) 2 bits. 6) Porque la derivada apunta hacia donde la pérdida sube; restarla mueve el peso
hacia donde baja. 7) Una tasa de aprendizaje demasiado grande.
