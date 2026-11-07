# PyTorch esencial

En el capítulo anterior escribiste a mano el paso hacia delante, la retropropagación y la actualización de los pesos. Funciona, pero con
una red de verdad sería imposible: millones de derivadas, capas de distintos tipos, GPU... **PyTorch** hace todo eso por ti. Es la
librería de deep learning más usada en investigación y en la industria, y sobre ella están construidos **Hugging Face Transformers**,
las librerías de fine-tuning (PEFT, TRL, Unsloth) y la mayoría de los modelos abiertos que descargas.

Este capítulo te enseña lo esencial: tensores, gradientes automáticos, cómo se define un modelo y el bucle de entrenamiento que verás,
con pocas variaciones, en cualquier proyecto de deep learning.

> Los ejercicios de la plataforma no pueden ejecutar PyTorch (corren en tu navegador). Los ejemplos de este capítulo son para tu
> ordenador o para Google Colab: el **laboratorio** del final te guía.

---

## 1. Instalación: CPU en tu portátil, GPU en Colab

Tu portátil tiene una gráfica **Radeon integrada**. PyTorch acelera con GPU sobre todo con tarjetas **NVIDIA** (CUDA); el soporte de AMD
(ROCm) es para algunas tarjetas dedicadas y principalmente en Linux. Para ti, la opción práctica es:

- **En tu ordenador: PyTorch para CPU.** Suficiente para aprender y para todos los ejemplos de este bloque.

  ```
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  ```

  (La instrucción exacta para tu sistema la da el selector de la web oficial, pytorch.org, en "Get Started".)

- **En Google Colab: GPU gratis.** Entra en colab.research.google.com, crea un cuaderno y elige *Entorno de ejecución → Cambiar tipo de
  entorno de ejecución → GPU (T4)*. PyTorch ya viene instalado. Es donde harás los entrenamientos pesados y, más adelante, el fine-tuning.

Comprueba la instalación:

```python
import torch
print(torch.__version__)
print(torch.cuda.is_available())   # False en tu portátil, True en Colab con GPU
```

---

## 2. Tensores: los arrays de PyTorch

Un **tensor** es como un array de NumPy (un vector, una matriz o algo con más dimensiones), con dos superpoderes: puede vivir en la **GPU**
y puede **calcular gradientes** automáticamente.

```python
import torch

a = torch.tensor([1.0, 2.0, 3.0])          # vector
M = torch.tensor([[1, 2], [3, 4]])         # matriz
ceros = torch.zeros(2, 3)                  # matriz de 2×3 llena de ceros
aleatorio = torch.randn(4, 5)              # números aleatorios (distribución normal)
rango = torch.arange(6)                    # tensor([0, 1, 2, 3, 4, 5])
```

### Forma y tipo

Las dos propiedades que más vas a mirar:

```python
x = torch.randn(32, 10, 64)
x.shape      # torch.Size([32, 10, 64])
x.dtype      # torch.float32
```

En deep learning las formas tienen un significado habitual. Por ejemplo, `(32, 10, 64)` en un modelo de lenguaje suele ser: un **lote** de
32 secuencias, de 10 tokens cada una, y cada token representado por un vector de 64 números. **El lote va casi siempre en la primera
dimensión.**

Los tipos más comunes: `float32` (el estándar para entrenar), `float16` y `bfloat16` (la mitad de memoria, muy usados en GPU) e `int64`
(índices, como los ids de los tokens).

### Operaciones

Funcionan como en NumPy:

```python
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])
a + b          # tensor([5., 7., 9.])
a * b          # elemento a elemento: tensor([ 4., 10., 18.])
a @ b          # producto punto: tensor(32.)
a.sum(), a.mean()
```

### Cambiar la forma

```python
x = torch.arange(12)          # forma (12,)
x.reshape(3, 4)               # forma (3, 4)
x.reshape(3, -1)              # -1: "calcúlalo tú" → (3, 4)
x.reshape(2, 2, 3)            # forma (2, 2, 3)
x.reshape(3, 4).T             # transpuesta: forma (4, 3)
x.unsqueeze(0)                # añade una dimensión: (1, 12)
```

### La regla de formas del producto de matrices

La misma del capítulo de matemáticas, ahora con lotes:

| Operación | Forma del resultado |
|---|---|
| `(n, k) @ (k, m)` | `(n, m)` |
| `(lote, n, k) @ (k, m)` | `(lote, n, m)`: la misma matriz se aplica a cada elemento del lote |
| `(lote, n, k) @ (lote, k, m)` | `(lote, n, m)`: un producto por cada elemento del lote |

Si las dimensiones de dentro no coinciden, obtendrás un error como `mm: mat1 and mat2 shapes cannot be multiplied (32x64 and 32x16)`. **Es
el error más frecuente en PyTorch**: cuando aparezca, imprime `.shape` de cada tensor y comprueba la regla.

### Comprueba que entendiste

**Pregunta:** tienes `x` de forma `(32, 128)` y quieres pasarlo por una capa que produzca 10 valores por ejemplo. ¿Qué forma debe tener la
matriz de pesos para hacer `x @ W`? ¿Y la salida?

**Respuesta:** `W` debe ser `(128, 10)` y la salida será `(32, 10)`: un vector de 10 valores para cada uno de los 32 ejemplos.

### NumPy y PyTorch

```python
import numpy as np
t = torch.from_numpy(np.array([1.0, 2.0]))     # de NumPy a PyTorch
arr = t.numpy()                                # de PyTorch a NumPy (si está en CPU)
```

---

## 3. Gradientes automáticos (autograd)

Esta es la pieza que hace innecesario escribir la retropropagación a mano. Si marcas un tensor con `requires_grad=True`, PyTorch **apunta
cada operación** que haces con él (construye un grafo) y, al llamar a `.backward()`, calcula las derivadas con la regla de la cadena.

Recupera el ejemplo del capítulo anterior: `h = 3·w`, `L = (h − 12)²`, con `w = 2`:

```python
w = torch.tensor(2.0, requires_grad=True)
h = 3 * w
L = (h - 12) ** 2
L.backward()           # retropropagación automática
print(w.grad)          # tensor(-36.)
```

Exactamente el −36 que calculaste a mano.

### Tres cosas que debes saber de autograd

1. **Los gradientes se acumulan.** Cada `.backward()` **suma** los gradientes nuevos a los que ya había en `.grad`. Por eso, en cada paso
   del entrenamiento, hay que ponerlos a cero antes de calcular los nuevos (lo hace `optimizer.zero_grad()`).
2. **Al evaluar no hacen falta gradientes.** Envolver el código en `with torch.no_grad():` evita guardar el grafo: es más rápido y gasta
   menos memoria.
3. **Las actualizaciones de los pesos no deben registrarse** en el grafo; el optimizador se encarga de hacerlas correctamente.

### Comprueba que entendiste

**Pregunta:** ejecutas dos veces seguidas `L = (3 * w - 12) ** 2; L.backward()` con `w = 2` sin poner el gradiente a cero. ¿Qué vale
`w.grad`?

**Respuesta:** −72: el segundo `backward()` suma otro −36 al que ya había. Por eso hay que reiniciar los gradientes en cada paso.

---

## 4. Definir un modelo con `nn.Module`

En PyTorch, un modelo es una clase que hereda de `nn.Module`: en `__init__` declaras las capas y en `forward` describes el paso hacia
delante.

```python
import torch
from torch import nn

class RedXOR(nn.Module):
    def __init__(self):
        super().__init__()
        self.oculta = nn.Linear(2, 4)      # capa densa: 2 entradas → 4 neuronas (pesos y sesgos incluidos)
        self.salida = nn.Linear(4, 1)

    def forward(self, x):
        h = torch.tanh(self.oculta(x))
        return self.salida(h)              # devuelve "logits" (sin sigmoide): ver la función de pérdida

modelo = RedXOR()
print(modelo)
print(sum(p.numel() for p in modelo.parameters()))    # 17 parámetros: (2·4 + 4) + (4·1 + 1)
```

`nn.Linear(entradas, salidas)` es exactamente la capa densa del capítulo anterior: guarda la matriz de pesos y el vector de sesgos, y los
registra como parámetros entrenables.

Para modelos que son una simple cadena de capas, existe un atajo:

```python
modelo = nn.Sequential(
    nn.Linear(2, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)
```

### Capas y piezas que verás a menudo

| Pieza | Para qué |
|---|---|
| `nn.Linear` | Capa densa |
| `nn.ReLU`, `nn.GELU`, `torch.tanh` | Activaciones |
| `nn.Embedding(vocabulario, dim)` | Convierte ids de tokens en vectores (una tabla de búsqueda entrenable) |
| `nn.LayerNorm` | Normaliza los valores de cada vector (estabiliza el entrenamiento de los transformers) |
| `nn.Dropout(p)` | Apaga neuronas al azar al entrenar |

---

## 5. Pérdida y optimizador

### Funciones de pérdida

| Pérdida | Para | Recibe |
|---|---|---|
| `nn.MSELoss()` | Regresión | Predicciones y valores reales |
| `nn.BCEWithLogitsLoss()` | Clasificación binaria | **Logits** (sin sigmoide) y etiquetas 0/1 en float |
| `nn.CrossEntropyLoss()` | Clasificación con varias clases (y LLM) | **Logits** (sin softmax) de forma `(N, clases)` y los **índices** de las clases correctas |

Fíjate en el detalle de los **logits**: estas pérdidas aplican internamente la sigmoide o el softmax, de forma numéricamente más estable.
Si aplicas tú el softmax antes de `CrossEntropyLoss`, lo estarías aplicando dos veces y el modelo aprendería peor. Es un error muy común.

### Optimizadores

El optimizador implementa la regla de actualización de los pesos:

```python
optimizador = torch.optim.SGD(modelo.parameters(), lr=0.1)      # descenso de gradiente clásico
optimizador = torch.optim.AdamW(modelo.parameters(), lr=1e-3)   # el más usado hoy
```

**Adam / AdamW** adapta automáticamente el tamaño del paso de cada parámetro y suele converger más rápido y con menos ajuste que el SGD
clásico. Es el que se usa para entrenar y afinar los LLM.

---

## 6. El bucle de entrenamiento

Este patrón de cinco pasos es el corazón de todo el deep learning. Apréndelo de memoria:

```python
import torch
from torch import nn

torch.manual_seed(0)
X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = torch.tensor([[0.], [1.], [1.], [0.]])

modelo = nn.Sequential(nn.Linear(2, 8), nn.Tanh(), nn.Linear(8, 1))
perdida_fn = nn.BCEWithLogitsLoss()
optimizador = torch.optim.AdamW(modelo.parameters(), lr=0.05)

for epoca in range(1000):
    optimizador.zero_grad()          # 1. borrar los gradientes del paso anterior
    logits = modelo(X)               # 2. paso hacia delante
    perdida = perdida_fn(logits, y)  # 3. calcular la pérdida
    perdida.backward()               # 4. retropropagación: calcular gradientes
    optimizador.step()               # 5. actualizar los pesos
    if epoca % 200 == 0:
        print(epoca, perdida.item())

with torch.no_grad():
    print(torch.sigmoid(modelo(X)).round())    # debería dar 0, 1, 1, 0
```

Al ejecutarlo en un portátil (PyTorch 2.x, CPU) se ve esto, en menos de un segundo:

```
0 0.7011651992797852
200 0.0014356622705236077
400 0.000635594769846648
600 0.0004301355220377445
800 0.0003381299029570073
tensor([[0.],
        [1.],
        [1.],
        [0.]])
```

(Con otra versión de PyTorch los decimales pueden variar ligeramente; lo importante es que la pérdida baje y el resultado final sea 0, 1, 1,
0.)

Compáralo con tu red XOR en NumPy: las mismas ideas, sin escribir una sola derivada. `.item()` convierte un tensor de un solo número en un
número de Python, para imprimirlo.

Si la pérdida no baja (puede pasar con alguna semilla, como viste en el capítulo anterior), prueba otra semilla o más neuronas.

---

## 7. Datos por lotes: `Dataset` y `DataLoader`

Con datos reales no se procesa todo de una vez: se usan **mini-lotes** (por ejemplo, de 32 o 64 ejemplos), que caben en memoria y dan
gradientes con algo de ruido que, curiosamente, ayuda a generalizar.

```python
from torch.utils.data import DataLoader, TensorDataset

datos = TensorDataset(X_entrenamiento, y_entrenamiento)
cargador = DataLoader(datos, batch_size=32, shuffle=True)    # baraja en cada época

for epoca in range(10):
    for xb, yb in cargador:                  # un mini-lote cada vez
        optimizador.zero_grad()
        perdida = perdida_fn(modelo(xb), yb)
        perdida.backward()
        optimizador.step()
```

Con 1 000 ejemplos y lotes de 32, cada época tiene 32 iteraciones (31 lotes completos y uno final de 8). El último lote suele ser más
pequeño, y no pasa nada.

---

## 8. Evaluar, guardar y cargar

### Modo evaluación

```python
modelo.eval()                 # desactiva el dropout y fija el comportamiento de algunas capas
with torch.no_grad():         # sin gradientes: más rápido y menos memoria
    predicciones = modelo(X_prueba)
modelo.train()                # vuelve al modo entrenamiento si vas a seguir entrenando
```

Olvidar `model.eval()` es un error clásico: con dropout activo, el modelo da resultados distintos cada vez y peores.

Y la regla del ML clásico sigue vigente: **nunca entrenes con los datos de prueba**. Ni siquiera un paso.

### Guardar y cargar

Lo habitual es guardar solo los **pesos** (el `state_dict`), no el objeto entero:

```python
torch.save(modelo.state_dict(), "modelo.pt")

nuevo = RedXOR()                                   # misma arquitectura
nuevo.load_state_dict(torch.load("modelo.pt"))
nuevo.eval()
```

Así es como se distribuyen los modelos abiertos: la arquitectura (código) por un lado y los pesos (un archivo grande) por otro. En Hugging
Face verás los pesos en formato `.safetensors`, un formato más seguro que no puede ejecutar código al cargarse.

---

## 9. CPU, GPU y memoria

Para usar la GPU, modelo y datos deben estar **en el mismo dispositivo**:

```python
dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
modelo = modelo.to(dispositivo)
xb, yb = xb.to(dispositivo), yb.to(dispositivo)
```

Si mezclas, PyTorch da un error del tipo *Expected all tensors to be on the same device*.

Cuánta memoria ocupa un modelo, en cifras redondas:

| Precisión | Bytes por parámetro | Modelo de 1 000 millones de parámetros |
|---|---|---|
| float32 | 4 | ~4 GB |
| float16 / bfloat16 | 2 | ~2 GB |
| 4 bits (cuantizado) | 0.5 | ~0.5 GB |

**Entrenar** gasta varias veces más que solo usar el modelo: hay que guardar los gradientes, el estado del optimizador (Adam guarda dos
números extra por parámetro) y las activaciones del paso hacia delante. Por eso, en tu portátil, entrenar desde cero solo es viable con
modelos pequeños (como el GPT del siguiente tema), y el fine-tuning de modelos de lenguaje se hace en Colab con técnicas como LoRA, que
solo entrenan una pequeña parte de los parámetros.

---

## 10. Errores frecuentes

| Error | Mensaje o síntoma | Solución |
|---|---|---|
| Formas incompatibles | `mat1 and mat2 shapes cannot be multiplied` | Imprimir `.shape` y revisar la regla de formas |
| Olvidar `zero_grad()` | La pérdida se comporta de forma errática | Llamarlo al principio de cada iteración |
| Aplicar softmax antes de `CrossEntropyLoss` | Aprende peor | Pasar los logits directamente |
| Etiquetas con el tipo equivocado | `expected scalar type Long` | `CrossEntropyLoss` quiere índices `int64`; `BCEWithLogitsLoss`, floats |
| Tensores en dispositivos distintos | `Expected all tensors to be on the same device` | `.to(dispositivo)` para modelo y datos |
| Evaluar sin `eval()` ni `no_grad()` | Resultados variables, memoria de más | Modo evaluación |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Instalación | CPU en tu portátil; GPU gratis en Colab |
| Tensor | Array con GPU y gradientes; mira siempre `.shape` y `.dtype` |
| Formas | El lote primero; `(n, k) @ (k, m) → (n, m)` |
| Autograd | `requires_grad=True`, `.backward()`, `.grad`; los gradientes se acumulan |
| `nn.Module` | Capas en `__init__`, paso hacia delante en `forward` |
| Pérdidas | Reciben logits; `CrossEntropyLoss` con índices de clase |
| Bucle | `zero_grad` → forward → pérdida → `backward` → `step` |
| `DataLoader` | Mini-lotes barajados |
| Evaluar | `model.eval()` + `torch.no_grad()` |
| Memoria | 4 bytes por parámetro en float32; entrenar gasta varias veces más |

## Autoevaluación final

1. ¿Qué forma tiene el resultado de `(16, 20, 32) @ (32, 8)`?
2. ¿Por qué hay que llamar a `optimizer.zero_grad()` en cada iteración?
3. Con `w = torch.tensor(1.0, requires_grad=True)` y `L = (4 * w) ** 2`, ¿qué vale `w.grad` tras `L.backward()`?
4. ¿Qué recibe `nn.CrossEntropyLoss`: probabilidades o logits?
5. Escribe los cinco pasos del bucle de entrenamiento en orden.
6. ¿Para qué sirven `model.eval()` y `torch.no_grad()`?
7. ¿Cuánta memoria ocupa, aproximadamente, un modelo de 3 000 millones de parámetros en float16?

**Respuestas:** 1) `(16, 20, 8)`. 2) Porque `backward()` suma los gradientes a los que ya había; sin borrarlos se mezclarían con los del
paso anterior. 3) L = 16w², dL/dw = 32w = 32. 4) Logits: aplica el softmax internamente. 5) `zero_grad`, paso hacia delante, calcular la
pérdida, `backward`, `step`. 6) `eval()` desactiva el dropout y fija el comportamiento de evaluación; `no_grad()` evita guardar gradientes
(más rápido y menos memoria). 7) Unos 6 GB (2 bytes por parámetro).
