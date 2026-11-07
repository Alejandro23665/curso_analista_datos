"""Área de interés: Machine learning moderno.

Bloque A (fundamentos para entender la IA) completo. El bloque B (ML moderno en la práctica: Ollama, cuantización,
Hugging Face, RAG local, fine-tuning...) está pendiente y se añadirá como un segundo bloque de esta misma área.
"""
from ..._helpers import checklist, predict, py, quiz

SK_MATE = "ML: matemáticas"
SK_CLASICO = "ML: aprendizaje clásico"
SK_REDES = "ML: redes neuronales"
SK_PYTORCH = "ML: PyTorch"
SK_GPT = "ML: transformers"

_PENDIENTE = "Capítulo en preparación. " * 40

AREA = {
    "slug": "machine-learning",
    "title": "Machine learning moderno",
    "order": 1,
    "description": "Entender cómo funcionan por dentro los modelos que usas, y después sacarles partido: de las matemáticas justas y "
                   "las redes neuronales a construir un GPT pequeño. Más adelante: Ollama, Hugging Face, RAG local y fine-tuning.",
    "notice": "**Tu equipo:** 12 GB de RAM y gráfica Radeon integrada. Los ejemplos de este bloque funcionan en el procesador (CPU); "
              "los entrenamientos más pesados se hacen gratis en **Google Colab**, que da una GPU. Los ejercicios de la plataforma "
              "se corrigen en el navegador con Python puro y NumPy; los laboratorios los haces en tu ordenador o en Colab.",
    "blocks": [
        {
            "label": "A",
            "title": "Fundamentos para entender la IA",
            "description": "Lo que pasa dentro de un modelo: vectores, probabilidad, gradientes, aprendizaje clásico, redes neuronales, "
                           "PyTorch y un GPT construido desde cero.",
            "topics": ["ml-matematicas", "ml-clasico", "ml-redes", "ml-pytorch", "ml-mini-gpt"],
        },
    ],
}

TOPICS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "ml-matematicas",
        "title": "Matemáticas para IA, con intuición",
        "summary": "Vectores, producto punto, matrices, probabilidad, entropía y gradiente: solo lo necesario, explicado con ejemplos y NumPy.",
        "hours": 6,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mlm-matvec", "Matriz por vector", SK_MATE,
                "Escribe `matriz_por_vector(M, v)` que multiplique una matriz (lista de filas) por un vector, **sin NumPy**. Cada elemento "
                "del resultado es el producto punto de una fila por el vector. Si el número de columnas de `M` no coincide con la longitud "
                "de `v`, lanza `ValueError`.",
                """
def matriz_por_vector(M, v):
    pass
""",
                """
def matriz_por_vector(M, v):
    resultado = []
    for fila in M:
        if len(fila) != len(v):
            raise ValueError("dimensiones incompatibles")
        resultado.append(sum(a * b for a, b in zip(fila, v)))
    return resultado
""",
                """
assert matriz_por_vector([[1, 2], [3, 4]], [5, 6]) == [17, 39], "fila 1: 1*5 + 2*6 = 17; fila 2: 3*5 + 4*6 = 39"
assert matriz_por_vector([[2, 0, 1]], [1, 1, 1]) == [3]
assert matriz_por_vector([], [1, 2]) == []
try:
    matriz_por_vector([[1, 2, 3]], [1, 2])
    raise AssertionError("debía lanzar ValueError: 3 columnas y un vector de 2")
except ValueError:
    pass
""",
                hint="Para cada fila: suma de fila[i] * v[i]. zip(fila, v) recorre las dos a la vez.",
            ),
            py(
                "mlm-entropia", "Entropía: ¿cuánta incertidumbre hay?", SK_MATE,
                "Escribe `entropia(probs)` que devuelva la entropía en bits de una distribución: `-Σ p · log2(p)`, **ignorando los p = 0**. "
                "Redondea a 3 decimales. Si las probabilidades no suman 1 (con tolerancia de 1e-6), lanza `ValueError`.",
                """
import math

def entropia(probs):
    pass
""",
                """
import math

def entropia(probs):
    if abs(sum(probs) - 1) > 1e-6:
        raise ValueError("las probabilidades deben sumar 1")
    return round(-sum(p * math.log2(p) for p in probs if p > 0), 3)
""",
                """
assert entropia([0.5, 0.5]) == 1.0, "una moneda justa: 1 bit"
assert entropia([1.0, 0.0]) == 0.0, "sin incertidumbre: 0 (y log2(0) no se calcula)"
assert entropia([0.25] * 4) == 2.0
assert entropia([0.9, 0.1]) == 0.469
try:
    entropia([0.5, 0.2])
    raise AssertionError("debía lanzar ValueError: no suman 1")
except ValueError:
    pass
""",
                hint="Filtra los p > 0 antes de calcular log2: el logaritmo de 0 no existe.",
            ),
            py(
                "mlm-descenso", "Descenso de gradiente en una dimensión", SK_MATE,
                "Escribe `descenso(derivada, x0, tasa, pasos)` que aplique descenso de gradiente: en cada paso, `x = x - tasa * derivada(x)`. "
                "Devuelve el `x` final redondeado a 4 decimales. `derivada` es una función.",
                """
def descenso(derivada, x0, tasa, pasos):
    pass
""",
                """
def descenso(derivada, x0, tasa, pasos):
    x = x0
    for _ in range(pasos):
        x = x - tasa * derivada(x)
    return round(x, 4)
""",
                """
# f(x) = (x - 3)^2 tiene su mínimo en x = 3; su derivada es 2(x - 3)
d = lambda x: 2 * (x - 3)
assert descenso(d, 0, 0.1, 1) == 0.6, "un paso: 0 - 0.1 * (-6) = 0.6"
assert abs(descenso(d, 0, 0.1, 100) - 3) < 1e-3, "con muchos pasos se acerca a 3"
assert descenso(d, 5, 0.1, 0) == 5, "con 0 pasos no se mueve"
assert abs(descenso(d, 10, 1.1, 20)) > 100, "con una tasa demasiado grande diverge"
""",
            ),
            predict(
                "mlm-pred-numpy", "¿Qué imprime? Operaciones con NumPy", SK_MATE,
                "NumPy opera con vectores enteros a la vez. Sigue el código y escribe lo que imprime.",
                """
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a * b)
print(a @ b)
print(a + 10)
""",
                "[ 4 10 18]\n32\n[11 12 13]",
                "`*` multiplica elemento a elemento: [1·4, 2·5, 3·6]. `@` es el producto punto (o matricial): 4 + 10 + 18 = 32. `a + 10` "
                "suma 10 a cada elemento (broadcasting). NumPy imprime los números alineados, por eso hay un espacio antes del 4.",
                hint="* y @ no son lo mismo: uno da un vector, el otro un solo número.",
            ),
            quiz(
                "mlm-quiz-coseno", "Qué mide el producto punto", SK_MATE,
                "Dos embeddings normalizados (longitud 1) tienen producto punto 0.95; otros dos, -0.1. ¿Qué significa?",
                [
                    "Los primeros son casi perpendiculares y los segundos, casi iguales",
                    "Los primeros apuntan casi en la misma dirección (significado parecido); los segundos no tienen relación (casi perpendiculares)",
                    "El producto punto mide la longitud de los vectores",
                    "No se puede interpretar sin conocer la dimensión",
                ],
                1,
                "Con vectores de longitud 1, el producto punto es el coseno del ángulo: cerca de 1, misma dirección; cerca de 0, perpendiculares; "
                "cerca de -1, opuestos.",
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "ml-clasico",
        "title": "Machine learning clásico",
        "summary": "Aprendizaje supervisado, entrenamiento y prueba, sobreajuste, métricas y dos modelos implementados a mano: k vecinos y regresión.",
        "hours": 6,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mlc-confusion", "Matriz de confusión y métricas", SK_CLASICO,
                "Escribe `metricas(reales, predichos)` para un clasificador binario (etiquetas 0 y 1). Devuelve un diccionario con "
                "`tp`, `fp`, `fn`, `tn` (verdaderos/falsos positivos y negativos) y `precision`, `recall` y `f1` redondeados a 3 decimales. "
                "Si un denominador es 0, esa métrica vale `0.0`.",
                """
def metricas(reales, predichos):
    pass
""",
                """
def metricas(reales, predichos):
    tp = sum(1 for r, p in zip(reales, predichos) if r == 1 and p == 1)
    fp = sum(1 for r, p in zip(reales, predichos) if r == 0 and p == 1)
    fn = sum(1 for r, p in zip(reales, predichos) if r == 1 and p == 0)
    tn = sum(1 for r, p in zip(reales, predichos) if r == 0 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": round(precision, 3), "recall": round(recall, 3), "f1": round(f1, 3)}
""",
                """
m = metricas([1, 1, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0])
assert (m["tp"], m["fp"], m["fn"], m["tn"]) == (2, 1, 1, 2)
assert m["precision"] == 0.667, "de 3 predichos como 1, acertó 2"
assert m["recall"] == 0.667, "de 3 que eran 1, encontró 2"
assert m["f1"] == 0.667
m = metricas([0, 0], [0, 0])
assert (m["precision"], m["recall"], m["f1"]) == (0.0, 0.0, 0.0), "sin positivos: los denominadores son 0"
""",
                hint="Primero los cuatro contadores; después las fórmulas, comprobando cada denominador.",
            ),
            py(
                "mlc-knn", "k vecinos más cercanos", SK_CLASICO,
                "Escribe `knn(entrenamiento, punto, k)`. `entrenamiento` es una lista de `((x, y), etiqueta)`. Calcula la distancia euclídea "
                "de `punto` a cada ejemplo, toma los `k` más cercanos y devuelve la etiqueta **más frecuente** entre ellos. Si hay empate de "
                "votos, gana la etiqueta del vecino **más cercano** entre las empatadas.",
                """
import math

def knn(entrenamiento, punto, k):
    pass
""",
                """
import math

def knn(entrenamiento, punto, k):
    ordenados = sorted(entrenamiento, key=lambda e: math.dist(e[0], punto))
    vecinos = ordenados[:k]
    votos = {}
    for _, etiqueta in vecinos:
        votos[etiqueta] = votos.get(etiqueta, 0) + 1
    maximo = max(votos.values())
    for _, etiqueta in vecinos:          # el primero de la lista ordenada es el más cercano
        if votos[etiqueta] == maximo:
            return etiqueta
""",
                """
datos = [((1, 1), "A"), ((1, 2), "A"), ((5, 5), "B"), ((6, 5), "B"), ((5, 6), "B")]
assert knn(datos, (1.5, 1.5), 3) == "A", "los 3 más cercanos: A, A, B"
assert knn(datos, (5, 5.5), 3) == "B"
assert knn(datos, (2, 2), 1) == "A"
# empate 1 a 1 con k = 2: gana el más cercano
assert knn([((0, 0), "X"), ((3, 0), "Y")], (1, 0), 2) == "X"
""",
                hint="math.dist(p, q) calcula la distancia euclídea. Ordena por distancia y recorre los k primeros.",
            ),
            py(
                "mlc-split", "Separar entrenamiento y prueba sin trampas", SK_CLASICO,
                "Escribe `separar(datos, proporcion_prueba, semilla)` que **baraje una copia** de los datos con `random.Random(semilla)` "
                "y devuelva `(entrenamiento, prueba)`, donde la prueba son los **últimos** `round(len(datos) * proporcion_prueba)` "
                "elementos de la copia barajada. No modifiques la lista original.",
                """
import random

def separar(datos, proporcion_prueba, semilla):
    pass
""",
                """
import random

def separar(datos, proporcion_prueba, semilla):
    copia = list(datos)
    random.Random(semilla).shuffle(copia)
    n_prueba = round(len(copia) * proporcion_prueba)
    corte = len(copia) - n_prueba
    return copia[:corte], copia[corte:]
""",
                """
datos = list(range(10))
ent, pru = separar(datos, 0.2, 42)
assert len(ent) == 8 and len(pru) == 2
assert sorted(ent + pru) == datos, "no se pierde ni se repite ningún dato"
assert datos == list(range(10)), "la lista original no debe cambiar"
assert separar(datos, 0.2, 42) == (ent, pru), "con la misma semilla, el mismo resultado"
assert ent + pru != datos, "hay que barajar antes de separar"
assert separar([], 0.3, 1) == ([], [])
""",
                hint="list(datos) crea una copia. random.Random(semilla).shuffle(copia) baraja de forma reproducible.",
            ),
            quiz(
                "mlc-quiz-overfitting", "Diagnóstico: entrenamiento frente a prueba", SK_CLASICO,
                "Tu modelo acierta el 99 % en los datos de entrenamiento y el 61 % en los de prueba. ¿Qué pasa?",
                [
                    "Subajuste: el modelo es demasiado simple",
                    "Sobreajuste: memorizó los datos de entrenamiento y no generaliza; hay que simplificarlo, regularizar o conseguir más datos",
                    "Todo va bien: el 99 % es excelente",
                    "Los datos de prueba están mal etiquetados seguro",
                ],
                1,
                "Una gran diferencia entre entrenamiento y prueba es la señal clásica del sobreajuste. Lo que importa es el resultado en datos que "
                "el modelo no ha visto.",
            ),
            quiz(
                "mlc-quiz-metrica", "Elegir la métrica", SK_CLASICO,
                "Un modelo detecta transacciones fraudulentas, que son el 1 % del total. Un modelo que dice siempre «no es fraude» acierta el "
                "99 %. ¿Qué métrica te dice que es inútil?",
                ["La exactitud (accuracy)", "El recall de la clase fraude, que es 0 %", "El número de filas", "La velocidad del modelo"],
                1,
                "Con clases desbalanceadas la exactitud engaña. El recall de la clase importante mide cuántos fraudes encuentra de verdad: ninguno.",
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "ml-redes",
        "title": "Redes neuronales desde cero",
        "summary": "Una neurona, las funciones de activación, la pérdida, el descenso de gradiente y la retropropagación, programados a mano.",
        "hours": 7,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mlr-neurona", "Una neurona", SK_REDES,
                "Escribe `neurona(entradas, pesos, sesgo)` que devuelva `sigmoide(Σ entrada·peso + sesgo)`, redondeado a 4 decimales, con "
                "`sigmoide(z) = 1 / (1 + e^-z)`. Si `entradas` y `pesos` tienen distinta longitud, lanza `ValueError`.",
                """
import math

def neurona(entradas, pesos, sesgo):
    pass
""",
                """
import math

def neurona(entradas, pesos, sesgo):
    if len(entradas) != len(pesos):
        raise ValueError("cada entrada necesita su peso")
    z = sum(x * w for x, w in zip(entradas, pesos)) + sesgo
    return round(1 / (1 + math.exp(-z)), 4)
""",
                """
assert neurona([0, 0], [1, 1], 0) == 0.5, "z = 0 -> sigmoide(0) = 0.5"
assert neurona([1, 2], [0.5, -0.25], 1) == 0.7311, "z = 0.5 - 0.5 + 1 = 1"
assert neurona([3], [2], -10) == 0.018, "z = 6 - 10 = -4"
try:
    neurona([1, 2], [1], 0)
    raise AssertionError("debía lanzar ValueError")
except ValueError:
    pass
""",
            ),
            py(
                "mlr-capa", "Una capa densa con ReLU", SK_REDES,
                "Escribe `capa(entradas, pesos, sesgos)`. `pesos` es una lista con una fila de pesos **por neurona**; `sesgos`, un sesgo por "
                "neurona. Cada neurona calcula `Σ entrada·peso + sesgo` y aplica **ReLU** (`max(0, z)`). Devuelve la lista de salidas.",
                """
def capa(entradas, pesos, sesgos):
    pass
""",
                """
def capa(entradas, pesos, sesgos):
    salidas = []
    for fila, sesgo in zip(pesos, sesgos):
        z = sum(x * w for x, w in zip(entradas, fila)) + sesgo
        salidas.append(max(0, z))
    return salidas
""",
                """
assert capa([1, 2], [[1, 1], [-1, 0], [0.5, 0.5]], [0, 0, 1]) == [3, 0, 2.5], "la segunda neurona da -1 y ReLU la deja en 0"
assert capa([0, 0], [[1, 1]], [-2]) == [0]
assert capa([2], [[3], [-3]], [1, 1]) == [7, 0]
""",
            ),
            py(
                "mlr-entrenar", "Entrena una regresión con descenso de gradiente", SK_REDES,
                "Escribe `entrenar(xs, ys, tasa, epocas)` que ajuste `y ≈ w·x + b` empezando en `w = 0`, `b = 0`. En cada época calcula, "
                "con **todos** los datos, los gradientes del error cuadrático medio:\n\n"
                "`dw = (2/n) · Σ (pred - y) · x` y `db = (2/n) · Σ (pred - y)`\n\n"
                "y actualiza `w -= tasa·dw`, `b -= tasa·db`. Devuelve `(w, b)` redondeados a 3 decimales.",
                """
def entrenar(xs, ys, tasa, epocas):
    w, b = 0.0, 0.0
    return round(w, 3), round(b, 3)
""",
                """
def entrenar(xs, ys, tasa, epocas):
    w, b = 0.0, 0.0
    n = len(xs)
    for _ in range(epocas):
        preds = [w * x + b for x in xs]
        dw = 2 / n * sum((p - y) * x for p, y, x in zip(preds, ys, xs))
        db = 2 / n * sum(p - y for p, y in zip(preds, ys))
        w -= tasa * dw
        b -= tasa * db
    return round(w, 3), round(b, 3)
""",
                """
xs, ys = [0, 1, 2, 3], [1, 3, 5, 7]          # y = 2x + 1
w, b = entrenar(xs, ys, 0.05, 2000)
assert (w, b) == (2.0, 1.0), "debería aprender w = 2 y b = 1"
assert entrenar(xs, ys, 0.05, 1) == (0.85, 0.4), "primera época: dw = -17, db = -8"
assert entrenar(xs, ys, 0.05, 0) == (0.0, 0.0)
""",
                hint="Calcula todas las predicciones con los w y b actuales ANTES de actualizarlos.",
            ),
            py(
                "mlr-perdida", "Entropía cruzada", SK_REDES,
                "Escribe `entropia_cruzada(probs, correcta)` que devuelva `-ln(probs[correcta])` redondeado a 4 decimales: la pérdida que "
                "usan los clasificadores (y los LLM al predecir el siguiente token). Para evitar `ln(0)`, usa `max(p, 1e-12)`.",
                """
import math

def entropia_cruzada(probs, correcta):
    pass
""",
                """
import math

def entropia_cruzada(probs, correcta):
    return round(-math.log(max(probs[correcta], 1e-12)), 4)
""",
                """
assert entropia_cruzada([0.7, 0.2, 0.1], 0) == 0.3567, "acertar con bastante confianza: pérdida baja"
assert entropia_cruzada([0.7, 0.2, 0.1], 2) == 2.3026, "la clase correcta tenía 0.1: pérdida alta"
assert entropia_cruzada([1.0, 0.0], 0) == 0.0
assert entropia_cruzada([1.0, 0.0], 1) == 27.631, "p = 0 no debe romper el cálculo"
""",
            ),
            quiz(
                "mlr-quiz-tasa", "La tasa de aprendizaje", SK_REDES,
                "Entrenas una red y la pérdida, en vez de bajar, crece y termina en `nan`. ¿Qué es lo primero que pruebas?",
                [
                    "Aumentar la tasa de aprendizaje",
                    "Reducir la tasa de aprendizaje (por ejemplo, dividirla entre 10)",
                    "Añadir más capas",
                    "Entrenar más épocas",
                ],
                1,
                "Con una tasa demasiado grande cada paso se pasa del mínimo y los valores explotan. Reducirla es la primera prueba.",
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "ml-pytorch",
        "title": "PyTorch esencial",
        "summary": "Tensores, formas, gradientes automáticos, nn.Module y el bucle de entrenamiento: la base de Hugging Face y de casi todo el deep learning.",
        "hours": 5,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mlp-formas", "Formas de un producto de matrices", SK_PYTORCH,
                "La mitad de los errores en PyTorch son de formas (*shapes*). Escribe `forma_matmul(a, b)` que reciba dos formas como tuplas "
                "(2D, o 3D con el lote primero) y devuelva la forma del resultado de `a @ b`, o lance `ValueError` si no son compatibles. "
                "Reglas: `(n, k) @ (k, m) -> (n, m)`; `(lote, n, k) @ (k, m) -> (lote, n, m)`; `(lote, n, k) @ (lote, k, m) -> (lote, n, m)`.",
                """
def forma_matmul(a, b):
    pass
""",
                """
def forma_matmul(a, b):
    if a[-1] != b[-2]:
        raise ValueError("la última dimensión de a debe coincidir con la penúltima de b")
    if len(b) == 3 and len(a) == 3 and a[0] != b[0]:
        raise ValueError("los lotes no coinciden")
    if len(b) == 3 and len(a) == 2:
        raise ValueError("forma no soportada")
    return tuple(a[:-1]) + (b[-1],)
""",
                """
assert forma_matmul((2, 3), (3, 4)) == (2, 4)
assert forma_matmul((32, 10, 64), (64, 16)) == (32, 10, 16), "un lote de 32 secuencias de 10 vectores de 64"
assert forma_matmul((8, 5, 4), (8, 4, 2)) == (8, 5, 2)
for malo in [((2, 3), (4, 5)), ((8, 5, 4), (7, 4, 2))]:
    try:
        forma_matmul(*malo)
        raise AssertionError("debía lanzar ValueError con %s" % (malo,))
    except ValueError:
        pass
""",
                hint="Compara a[-1] con b[-2]. El resultado conserva todas las dimensiones de a menos la última, y añade la última de b.",
            ),
            py(
                "mlp-lotes", "Mini-lotes (batches)", SK_PYTORCH,
                "El entrenamiento no usa todos los datos a la vez sino **mini-lotes**. Escribe `lotes(datos, tamano)` que devuelva una lista "
                "de listas con `tamano` elementos cada una; la última puede ser más corta. Si `tamano < 1`, lanza `ValueError`.",
                """
def lotes(datos, tamano):
    pass
""",
                """
def lotes(datos, tamano):
    if tamano < 1:
        raise ValueError("el tamaño de lote debe ser al menos 1")
    return [datos[i:i + tamano] for i in range(0, len(datos), tamano)]
""",
                """
assert lotes([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
assert lotes([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
assert lotes([], 3) == []
try:
    lotes([1], 0)
    raise AssertionError("debía lanzar ValueError")
except ValueError:
    pass
""",
            ),
            quiz(
                "mlp-quiz-zero-grad", "¿Por qué optimizer.zero_grad()?", SK_PYTORCH,
                "En el bucle de entrenamiento de PyTorch se llama a `optimizer.zero_grad()` antes de `loss.backward()`. ¿Por qué?",
                [
                    "Para poner los pesos a cero",
                    "Porque PyTorch acumula (suma) los gradientes en cada backward; sin reiniciarlos, se mezclarían con los del lote anterior",
                    "Para liberar la memoria de la GPU",
                    "Es opcional y solo mejora la velocidad",
                ],
                1,
                "`backward()` suma los gradientes nuevos a los que ya había en `.grad`. Por eso se ponen a cero en cada iteración.",
            ),
            quiz(
                "mlp-quiz-eval", "Entrenar frente a evaluar", SK_PYTORCH,
                "Vas a medir tu modelo con los datos de prueba. ¿Qué haces en PyTorch?",
                [
                    "Nada especial",
                    "model.eval() y envolver el cálculo en torch.no_grad(): sin dropout y sin guardar gradientes (más rápido y con menos memoria)",
                    "Llamar a optimizer.step() para que aprenda de la prueba",
                    "Pasar el modelo a la GPU",
                ],
                1,
                "eval() cambia el comportamiento de capas como Dropout; no_grad() evita guardar el grafo de gradientes. Y nunca se entrena con "
                "los datos de prueba.",
            ),
            checklist(
                "mlp-lab", "Laboratorio: tu primer entrenamiento en PyTorch", SK_PYTORCH,
                "Hazlo en tu ordenador (CPU) o en Google Colab siguiendo el capítulo.",
                [
                    "Instalé PyTorch para CPU (o abrí un cuaderno de Colab) y comprobé torch.__version__",
                    "Creé tensores, revisé su .shape y multipliqué matrices con @",
                    "Calculé un gradiente con requires_grad=True y .backward()",
                    "Definí un modelo con nn.Module y lo entrené con el bucle completo (zero_grad, forward, loss, backward, step)",
                    "Vi bajar la pérdida época a época y evalué con model.eval() y torch.no_grad()",
                ],
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "ml-mini-gpt",
        "title": "Construye un GPT pequeño",
        "summary": "Tokenizar, preparar los datos, la atención causal y el muestreo: entiende un transformer construyendo uno que escribe texto.",
        "hours": 8,
        "theory": _PENDIENTE,
        "exercises": [
            py(
                "mlg-vocab", "Tokenizador de caracteres", SK_GPT,
                "Escribe `vocabulario(texto)` que devuelva `(stoi, itos)`: `stoi` asigna a cada carácter distinto un número, en **orden "
                "alfabético** (según `sorted`), empezando en 0; `itos` es el diccionario inverso. Escribe también `codificar(texto, stoi)` "
                "(texto → lista de números) y `decodificar(ids, itos)` (lista de números → texto).",
                """
def vocabulario(texto):
    pass

def codificar(texto, stoi):
    pass

def decodificar(ids, itos):
    pass
""",
                """
def vocabulario(texto):
    chars = sorted(set(texto))
    stoi = {c: i for i, c in enumerate(chars)}
    itos = {i: c for c, i in stoi.items()}
    return stoi, itos

def codificar(texto, stoi):
    return [stoi[c] for c in texto]

def decodificar(ids, itos):
    return "".join(itos[i] for i in ids)
""",
                """
stoi, itos = vocabulario("hola mundo")
assert stoi == {" ": 0, "a": 1, "d": 2, "h": 3, "l": 4, "m": 5, "n": 6, "o": 7, "u": 8}
assert itos[3] == "h"
assert codificar("hola", stoi) == [3, 7, 4, 1]
assert decodificar([5, 8, 6, 2, 7], itos) == "mundo"
assert decodificar(codificar("la luna", vocabulario("la luna")[0]), vocabulario("la luna")[1]) == "la luna", "ida y vuelta sin pérdidas"
""",
            ),
            py(
                "mlg-pares", "Pares de entrenamiento", SK_GPT,
                "Un modelo de lenguaje aprende a predecir el siguiente token. Escribe `pares(ids, contexto)` que devuelva una lista de tuplas "
                "`(x, y)`: `x` son `contexto` tokens seguidos y `y`, los mismos **desplazados una posición** (el siguiente de cada uno). "
                "Recorre todas las posiciones iniciales posibles.",
                """
def pares(ids, contexto):
    pass
""",
                """
def pares(ids, contexto):
    return [(ids[i:i + contexto], ids[i + 1:i + contexto + 1]) for i in range(len(ids) - contexto)]
""",
                """
assert pares([10, 11, 12, 13], 2) == [([10, 11], [11, 12]), ([11, 12], [12, 13])]
assert pares([1, 2, 3], 2) == [([1, 2], [2, 3])]
assert pares([1, 2], 2) == [], "no hay siguiente token para el último"
assert len(pares(list(range(100)), 8)) == 92
""",
                hint="Para cada i: x = ids[i : i + contexto] y y = ids[i + 1 : i + contexto + 1]. ¿Hasta qué i llega?",
            ),
            py(
                "mlg-atencion", "Pesos de atención", SK_GPT,
                "Escribe `pesos_atencion(q, ks)` que calcule cuánto atiende una consulta `q` a cada clave de `ks`: el producto punto de `q` "
                "con cada clave, **dividido entre √d** (d = longitud de `q`), y después softmax. Devuelve la lista de pesos redondeados "
                "a 3 decimales. Usa el truco de restar el máximo antes de `exp`.",
                """
import math

def pesos_atencion(q, ks):
    pass
""",
                """
import math

def pesos_atencion(q, ks):
    d = len(q)
    puntuaciones = [sum(a * b for a, b in zip(q, k)) / math.sqrt(d) for k in ks]
    m = max(puntuaciones)
    exps = [math.exp(s - m) for s in puntuaciones]
    total = sum(exps)
    return [round(e / total, 3) for e in exps]
""",
                """
assert pesos_atencion([1, 0], [[1, 0], [0, 1]]) == [0.67, 0.33], "puntuaciones 1/√2 y 0"
assert pesos_atencion([0, 0], [[5, 5], [1, 1]]) == [0.5, 0.5], "una consulta nula atiende a todo por igual"
assert pesos_atencion([2, 2, 2, 2], [[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0]]) == [0.495, 0.495, 0.009], "puntuaciones 4, 4 y 0 (8 / √4 = 4)"
assert abs(sum(pesos_atencion([1, 2], [[3, 1], [0, 2], [1, 1]])) - 1) < 0.01
""",
            ),
            py(
                "mlg-muestreo", "Muestrear el siguiente token", SK_GPT,
                "Para generar texto se **muestrea** un token según sus probabilidades. Escribe `muestrear(probs, r)` que, dado un número `r` "
                "entre 0 y 1 (en la práctica, aleatorio), devuelva el índice `i` tal que la suma acumulada de `probs` hasta `i` incluido es la "
                "primera que **supera** `r`.",
                """
def muestrear(probs, r):
    pass
""",
                """
def muestrear(probs, r):
    acumulado = 0.0
    for i, p in enumerate(probs):
        acumulado += p
        if r < acumulado:
            return i
    return len(probs) - 1
""",
                """
probs = [0.5, 0.3, 0.2]
assert muestrear(probs, 0.1) == 0
assert muestrear(probs, 0.5) == 1, "0.5 no supera 0.5: pasa al siguiente (acumulado 0.8)"
assert muestrear(probs, 0.79) == 1
assert muestrear(probs, 0.95) == 2
assert muestrear([1.0], 0.99) == 0
""",
                hint="Ve sumando las probabilidades; en cuanto la suma supere r, ese es el índice.",
            ),
            quiz(
                "mlg-quiz-mascara", "La máscara causal", SK_GPT,
                "Al entrenar un GPT, cada posición solo puede atender a las posiciones anteriores (máscara causal). ¿Por qué?",
                [
                    "Para que el entrenamiento sea más rápido",
                    "Porque al generar texto el modelo no conoce el futuro: si durante el entrenamiento pudiera ver el siguiente token, "
                    "aprendería a copiarlo en lugar de predecirlo",
                    "Para ahorrar memoria",
                    "Porque los transformers no pueden mirar hacia atrás",
                ],
                1,
                "La tarea es predecir el siguiente token a partir de los anteriores. La máscara impide hacer trampa mirando la respuesta.",
            ),
            checklist(
                "mlg-lab", "Laboratorio: entrena tu GPT pequeño", SK_GPT,
                "Sigue el capítulo en tu ordenador (CPU) o en Google Colab.",
                [
                    "Preparé un texto de entrenamiento (por ejemplo, unas decenas de miles de caracteres de un libro de dominio público)",
                    "Construí el vocabulario de caracteres y separé entrenamiento y validación",
                    "Entrené el modelo bigrama y después el transformer pequeño, y vi bajar la pérdida de validación",
                    "Generé texto antes y después de entrenar y comparé",
                    "Probé distintas temperaturas al generar y anoté qué cambia",
                ],
            ),
        ],
    },
]
