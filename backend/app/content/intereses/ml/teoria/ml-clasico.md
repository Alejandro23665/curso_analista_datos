# Machine learning clásico

Antes de los LLM y las redes neuronales gigantes, el machine learning ya resolvía problemas enormes: detectar fraude, recomendar
productos, predecir precios, filtrar spam. Y lo sigue haciendo: en muchas empresas, un modelo clásico bien hecho es más barato, más rápido
y más fácil de explicar que un modelo de lenguaje.

Pero la razón principal para estudiarlo aquí es otra: **todas las ideas importantes del ML moderno nacen aquí**. Separar entrenamiento y
prueba, el sobreajuste, las métricas, la fuga de datos, la línea base... Cuando más adelante afines un modelo de lenguaje o evalúes un RAG,
usarás exactamente estos conceptos.

---

## 1. Qué es "aprender" para una máquina

En la programación tradicional escribes las **reglas**: "si el correo contiene *premio gratis*, es spam". En el machine learning das
**ejemplos** con su respuesta, y el algoritmo **encuentra las reglas** por sí mismo.

```
Programación tradicional:   datos + reglas    →  respuestas
Machine learning:           datos + respuestas →  reglas (el modelo)
```

Un **modelo** es, en el fondo, una función con parámetros ajustables. **Entrenar** es ajustar esos parámetros para que la función acierte
en los ejemplos. **Predecir** (o hacer **inferencia**) es usar la función ya ajustada con datos nuevos.

### Vocabulario básico

| Término | Significado | Ejemplo (precio de casas) |
|---|---|---|
| **Característica** (*feature*) | Una variable de entrada | metros, habitaciones, barrio |
| **Etiqueta** (*label*, *target*) | Lo que quieres predecir | el precio |
| **Ejemplo** (*sample*) | Una fila de datos | una casa concreta |
| **Conjunto de datos** (*dataset*) | Todos los ejemplos | 5 000 casas vendidas |

Por convención, las características se llaman **X** (una matriz: una fila por ejemplo, una columna por característica) y las etiquetas,
**y** (un vector).

---

## 2. Tipos de aprendizaje

| Tipo | Datos | Pregunta | Ejemplos |
|---|---|---|---|
| **Supervisado: clasificación** | Con etiqueta (una categoría) | ¿A qué clase pertenece? | Spam o no spam, fraude, sentimiento de una reseña |
| **Supervisado: regresión** | Con etiqueta (un número) | ¿Cuánto vale? | Precio, demanda de mañana, tiempo de entrega |
| **No supervisado** | Sin etiqueta | ¿Qué estructura hay? | Agrupar clientes parecidos (*clustering*), detectar anomalías |
| **Por refuerzo** | Recompensas por acciones | ¿Qué acción conviene? | Juegos, robótica; también parte del entrenamiento de los LLM (RLHF) |

Y un dato curioso que conecta con lo moderno: un LLM se preentrena de forma **autosupervisada**: la etiqueta de cada posición es,
simplemente, la siguiente palabra del texto. No hace falta que nadie etiquete nada.

---

## 3. Entrenamiento, validación y prueba

La regla más importante de todo el machine learning:

> **Un modelo se evalúa con datos que no ha visto durante el entrenamiento.**

Si mides con los mismos datos con los que aprendió, mides su memoria, no su capacidad de generalizar. Es como evaluar a un estudiante con
las mismas preguntas exactas que practicó: puede sacar un 10 sin entender nada.

Por eso los datos se dividen:

| Conjunto | Proporción típica | Para qué |
|---|---|---|
| **Entrenamiento** | 60-80 % | Ajustar los parámetros del modelo |
| **Validación** | 10-20 % | Elegir entre modelos y ajustar la configuración (*hiperparámetros*) |
| **Prueba** | 10-20 % | Medir el resultado final, **una sola vez**, al terminar |

### Cómo separar bien

- **Baraja antes de separar.** Si los datos vienen ordenados (por fecha, por clase), cortar sin barajar deja en la prueba solo un tipo de
  ejemplos. Por ejemplo, si están ordenados por precio, la prueba tendría solo las casas más caras.
- **Usa una semilla** para que la mezcla sea **reproducible**: con la misma semilla, la misma división. Así puedes comparar experimentos.
- **No modifiques los datos originales** al barajar: trabaja sobre una copia.
- **Excepción, los datos temporales**: si predices el futuro (ventas de la semana que viene), no barajes; entrena con el pasado y prueba con
  lo más reciente, que es lo que ocurrirá en la realidad.

```python
import random

datos = list(range(20))
copia = list(datos)                    # no tocar el original
random.Random(7).shuffle(copia)        # misma semilla, misma mezcla
```

### Validación cruzada

Con pocos datos, una sola división puede salir "con suerte". La **validación cruzada** (*k-fold*) divide los datos en k partes (por
ejemplo, 5), entrena 5 veces dejando cada vez una parte distinta para validar, y promedia los resultados. Es más fiable, a cambio de
entrenar varias veces.

---

## 4. Sobreajuste y subajuste

| | Entrenamiento | Prueba | Diagnóstico |
|---|---|---|---|
| **Subajuste** (*underfitting*) | Mal | Mal | El modelo es demasiado simple para el problema |
| **Buen ajuste** | Bien | Bien (algo peor) | Generaliza |
| **Sobreajuste** (*overfitting*) | Muy bien | Mal | Memorizó los ejemplos, incluido su ruido |

Ejemplo: un modelo acierta el 99 % en entrenamiento y el 61 % en prueba. La gran diferencia es la firma del **sobreajuste**: aprendió
detalles irrelevantes de los ejemplos concretos.

Remedios contra el sobreajuste:

- **Más datos** (la solución más eficaz, cuando es posible).
- **Un modelo más simple** (menos parámetros, un árbol menos profundo).
- **Regularización**: penalizar los modelos demasiado complejos.
- **Parar antes** (*early stopping*): dejar de entrenar cuando la pérdida de validación deja de bajar, aunque la de entrenamiento siga
  bajando.

Esto mismo pasa al afinar un LLM con pocos ejemplos: si entrenas demasiadas épocas, repite frases de tus datos al pie de la letra.

### Comprueba que entendiste

**Pregunta:** un modelo acierta el 62 % en entrenamiento y el 60 % en prueba, en un problema donde un humano acierta el 95 %. ¿Sobreajuste o
subajuste? ¿Qué probarías?

**Respuesta:** subajuste: va mal en los dos conjuntos. Probaría un modelo más complejo o mejores características, no más regularización.

---

## 5. Métricas de clasificación

### Exactitud y su trampa

La **exactitud** (*accuracy*) es el porcentaje de aciertos. Parece suficiente, pero engaña cuando las clases están **desbalanceadas**: si
el 99 % de las transacciones son legítimas, un modelo que dice siempre "legítima" tiene un 99 % de exactitud... y no detecta ni un fraude.

### La matriz de confusión

Para una clasificación binaria (positivo = la clase que te interesa detectar, por ejemplo "fraude"), cada predicción cae en una de cuatro
casillas:

| | Predijo positivo | Predijo negativo |
|---|---|---|
| **Era positivo** | Verdadero positivo (TP) | Falso negativo (FN): se te escapó |
| **Era negativo** | Falso positivo (FP): falsa alarma | Verdadero negativo (TN) |

### Precisión, recall y F1

| Métrica | Fórmula | Pregunta que responde |
|---|---|---|
| **Precisión** | TP / (TP + FP) | De los que marqué como positivos, ¿cuántos lo eran? |
| **Recall** (sensibilidad) | TP / (TP + FN) | De los positivos reales, ¿cuántos encontré? |
| **F1** | 2 · P · R / (P + R) | Equilibrio entre las dos (media armónica) |

Ejemplo con un detector de correos importantes sobre 10 correos:

```
reales:    [1, 0, 1, 1, 0, 0, 1, 0, 0, 0]
predichos: [1, 1, 1, 0, 0, 0, 1, 0, 0, 0]
```

- TP = 3 (posiciones 0, 2 y 6), FP = 1 (posición 1), FN = 1 (posición 3), TN = 5.
- Precisión = 3 / 4 = **0.75**: de cada 4 que marcó como importantes, 3 lo eran.
- Recall = 3 / 4 = **0.75**: encontró 3 de los 4 importantes.
- F1 = 2 · 0.75 · 0.75 / 1.5 = **0.75**.

Fíjate en un caso límite: si el modelo **no predice ningún positivo**, TP + FP = 0 y la precisión dividiría entre cero. Por convención se
toma 0. Lo mismo con el recall si no hay positivos reales.

### ¿Cuál importa más?

Depende del **coste de cada error**:

- **Detectar cáncer o fraude**: un falso negativo (no detectarlo) es muy caro → prioriza el **recall**.
- **Filtro de spam**: un falso positivo (mandar un correo importante a spam) es muy molesto → prioriza la **precisión**.

Muchos modelos dan una **probabilidad** y tú eliges el **umbral** (por ejemplo, "es fraude si p > 0.3"). Bajar el umbral sube el recall y
baja la precisión; subirlo hace lo contrario.

### Comprueba que entendiste

**Pregunta:** un detector marca 20 transacciones como fraude; 5 lo eran. En total había 10 fraudes. ¿Precisión y recall?

**Respuesta:** precisión 5/20 = 0.25 (muchas falsas alarmas); recall 5/10 = 0.5 (encontró la mitad de los fraudes).

### Métricas de regresión

| Métrica | Qué mide |
|---|---|
| **MAE** (error absoluto medio) | El error típico, en las unidades del problema ("me equivoco en 12 000 $ de media") |
| **RMSE** (raíz del error cuadrático medio) | Como el MAE, pero castiga más los errores grandes |
| **R²** | Qué fracción de la variación explica el modelo (1 = perfecto; 0 = como predecir siempre la media) |

---

## 6. La línea base: ¿tu modelo sirve de algo?

Antes de celebrar un resultado, compáralo con una **línea base** (*baseline*) trivial:

- Clasificación: predecir siempre la clase más frecuente.
- Regresión: predecir siempre la media.

Si tu modelo sofisticado apenas mejora la línea base, no aporta. Esta pregunta también sirve para los LLM: ¿mi asistente con RAG responde
mejor que una búsqueda por palabras clave?

---

## 7. Dos modelos para entender cómo funcionan

### k vecinos más cercanos (k-NN)

La idea más intuitiva del ML: **para clasificar algo nuevo, mira los k ejemplos más parecidos y haz una votación**.

```
Ejemplos de entrenamiento (frutas por [peso en g, rugosidad 0-10]):
  [150, 2] manzana   [160, 3] manzana   [120, 8] naranja   [130, 9] naranja   [140, 7] naranja

Nueva fruta: [145, 4]
Distancias: a [150,2] ≈ 5.4   a [160,3] ≈ 15.0   a [140,7] ≈ 5.8   a [130,9] ≈ 15.8   a [120,8] ≈ 25.3
Con k = 3, los más cercanos: manzana (5.4), naranja (5.8), manzana (15.0) → 2 votos a 1: manzana
```

Los pasos del algoritmo: calcular la **distancia** a cada ejemplo (la euclídea, `math.dist(p, q)` en Python, es la longitud del segmento
entre dos puntos), **ordenar** por distancia, quedarte con los **k primeros** y **contar votos**. Detalles de diseño que hay que decidir:
qué hacer si hay **empate de votos** (una regla habitual: gana la etiqueta del vecino más cercano) y elegir **k** (impar con dos clases
evita empates).

Una advertencia práctica: si una característica tiene números mucho más grandes que otra (el peso en gramos frente a una rugosidad de 0 a
10), **domina la distancia**. En el ejemplo, el peso pesa mucho más que la rugosidad. Por eso se suelen **escalar** las características
(por ejemplo, restar la media y dividir entre la desviación típica) antes de usar k-NN.

k-NN no "entrena" nada: memoriza los ejemplos y hace todo el trabajo al predecir. Es exactamente la idea de la **búsqueda semántica** de un
RAG: encontrar los vectores más cercanos.

### Regresión lineal

Para predecir un número, la idea más simple es una **recta**: `precio = w · metros + b`. Entrenar es encontrar el `w` (pendiente) y el `b`
(intercepto) que mejor se ajustan a los ejemplos, normalmente minimizando el **error cuadrático medio**.

Con varias características: `precio = w₁·metros + w₂·habitaciones + w₃·antigüedad + b`. Cada peso dice cuánto aporta su característica, lo
que hace a la regresión lineal muy **interpretable**: "cada metro cuadrado suma unos 900 $".

En *Redes neuronales desde cero* entrenarás una regresión lineal con descenso de gradiente: es, literalmente, una neurona sin activación.

### Otros modelos que conviene conocer por su nombre

| Modelo | Idea | Cuándo |
|---|---|---|
| Regresión logística | Como la lineal, pero con una sigmoide para dar una probabilidad | Clasificación simple e interpretable |
| Árbol de decisión | Una serie de preguntas sí/no ("¿metros > 90?") | Interpretable; tiende a sobreajustar |
| Random forest | Muchos árboles distintos que votan | Muy buen resultado sin mucho ajuste |
| Gradient boosting (XGBoost, LightGBM) | Árboles que corrigen los errores de los anteriores | El rey de los datos tabulares en la industria |
| K-means | Agrupa en k grupos por cercanía | Segmentar clientes |

Para **datos en tablas** (filas y columnas, como los de una base de datos), los árboles con *gradient boosting* siguen ganando a menudo a
las redes neuronales. Las redes dominan en texto, imágenes y audio.

---

## 8. scikit-learn: el flujo estándar

La librería de ML clásico de Python es **scikit-learn**. Todos sus modelos siguen la misma interfaz, así que cambiar de modelo es cambiar
una línea:

```python
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = KNeighborsClassifier(n_neighbors=5)
modelo.fit(X_train, y_train)               # entrenar
predicciones = modelo.predict(X_test)      # predecir

print(classification_report(y_test, predicciones))   # precisión, recall y F1 por clase
```

Los tres verbos que verás siempre: **`fit`** (entrenar), **`predict`** (predecir) y, para las transformaciones de datos, **`transform`**.

Para instalarla en tu ordenador: `pip install scikit-learn`. Funciona perfectamente en el procesador; los modelos clásicos no necesitan
GPU.

### Preparar los datos

Los modelos solo entienden **tablas de números sin huecos**. Los datos reales casi nunca vienen así, y prepararlos suele llevar más tiempo
que entrenar. Los tres problemas que encontrarás siempre:

**1. Valores que faltan.** Una casa sin dato de antigüedad, un cliente sin edad. Opciones:

- **Eliminar** las filas incompletas, si son pocas y no siguen ningún patrón.
- **Rellenar** (*imputar*) con un valor razonable: la **mediana** o la media de la columna para números, la categoría más frecuente para
  textos. Ese valor se calcula **solo con los datos de entrenamiento** y se aplica igual a la prueba.
- A veces, el propio hecho de que falte es información: se puede añadir una columna "faltaba la antigüedad" (sí/no).

**2. Categorías de texto.** El barrio "Centro", "Norte" o "Sur" no se puede multiplicar por un peso. Tampoco sirve numerarlas (Centro = 1,
Norte = 2, Sur = 3): el modelo creería que Sur es "el triple" de Centro. La solución estándar es el **one-hot**: una columna por categoría,
con 1 en la que corresponde y 0 en las demás.

| barrio | → | barrio_Centro | barrio_Norte | barrio_Sur |
|---|---|---|---|---|
| Norte | | 0 | 1 | 0 |
| Centro | | 1 | 0 | 0 |

**3. Escalas distintas.** Con `metros = [80, 120, 60]` y `habitaciones = [2, 3, 1]`, una diferencia de 40 metros pesa veinte veces más que
una de 2 habitaciones en una distancia. Se **estandariza** cada columna con su media y su desviación típica (del entrenamiento): metros
pasa a `[−0.27, 1.34, −1.07]` y habitaciones a `[0, 1.22, −1.22]`. Ahora las dos columnas pesan parecido. Los árboles de decisión no lo
necesitan (comparan cada columna por separado); k vecinos, la regresión con regularización y las redes neuronales, sí.

En scikit-learn, cada paso es un transformador (`SimpleImputer`, `OneHotEncoder`, `StandardScaler`) y `ColumnTransformer` aplica a cada
columna el suyo:

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

preparar = ColumnTransformer([
    ("numeros", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), ["metros", "habitaciones"]),
    ("categorias", OneHotEncoder(handle_unknown="ignore"), ["barrio"]),
])
```

Lo importante de verdad no es la sintaxis, sino la regla: **todo lo que se "aprende" de los datos (medianas, medias, desviaciones,
categorías existentes) se aprende del entrenamiento**. Por eso se mete en un pipeline.

### Pipelines: preparar los datos sin hacer trampa

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

modelo = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
modelo.fit(X_train, y_train)
```

El **pipeline** aprende el escalado (la media y la desviación) **solo con los datos de entrenamiento** y lo aplica igual a la prueba. Eso
evita el error de la sección siguiente.

---

## 9. La fuga de datos (*data leakage*)

Es el error más traicionero del ML: **información de la prueba (o del futuro) se cuela en el entrenamiento**, y el modelo parece mucho
mejor de lo que es. Funciona de maravilla en tus pruebas y falla en la realidad.

Ejemplos:

- Escalar o normalizar **todos** los datos antes de separar: la media incluye la prueba.
- Una característica que **contiene la respuesta**: para predecir si un cliente abandonará, usar "fecha de baja" (que solo existe si ya se
  fue).
- **Duplicados** entre entrenamiento y prueba: el modelo "acierta" porque ya vio ese mismo ejemplo.
- En datos temporales, **barajar** y entrenar con datos posteriores a los de la prueba.

Si un resultado parece demasiado bueno para ser verdad, busca una fuga.

---

## 10. Errores frecuentes

| Error | Consecuencia | Solución |
|---|---|---|
| Evaluar con los datos de entrenamiento | Resultado inflado | Separar entrenamiento y prueba |
| No barajar datos ordenados | Prueba sesgada | Barajar con semilla (salvo datos temporales) |
| Usar solo la exactitud con clases desbalanceadas | Un modelo inútil parece bueno | Precisión, recall, F1 y matriz de confusión |
| Ajustar el modelo mirando la prueba muchas veces | La prueba deja de ser "no vista" | Ajustar con validación; prueba una vez |
| No comparar con una línea base | No sabes si el modelo aporta | Clase más frecuente o media |
| Escalar antes de separar | Fuga de datos | Pipeline |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Aprender | Encontrar reglas a partir de ejemplos con respuesta |
| Supervisado | Clasificación (categorías) y regresión (números) |
| Entrenamiento / validación / prueba | Evaluar siempre con datos no vistos; barajar con semilla |
| Sobreajuste | Muy bien en entrenamiento, mal en prueba: memorizó |
| Matriz de confusión | TP, FP, FN, TN |
| Precisión / recall / F1 | ¿Cuántos de los marcados acerté? / ¿Cuántos de los reales encontré? / equilibrio |
| Línea base | Comparar con la clase más frecuente o la media |
| k-NN | Votación de los k ejemplos más cercanos; escalar las características |
| Regresión lineal | `w·x + b`; interpretable |
| Preparar los datos | Rellenar los huecos, one-hot para categorías, estandarizar; todo aprendido del entrenamiento |
| scikit-learn | `fit`, `predict`, pipelines |
| Fuga de datos | Información de la prueba en el entrenamiento: resultados falsamente buenos |

## Autoevaluación final

1. ¿Qué diferencia hay entre clasificación y regresión? Da un ejemplo de cada una.
2. ¿Por qué hay que barajar antes de separar, y cuándo **no** hay que hacerlo?
3. Un modelo: 97 % en entrenamiento, 95 % en prueba. Otro: 99 % y 70 %. ¿Cuál prefieres?
4. Con TP = 8, FP = 2, FN = 8, calcula la precisión y el recall.
5. Para detectar tumores, ¿priorizas la precisión o el recall?
6. En k-NN con k = 2, un vecino dice "A" y otro "B". ¿Cómo desempatas?
7. ¿Por qué escalar todos los datos antes de separar es una fuga de datos?

**Respuestas:** 1) Clasificación predice una categoría (spam o no); regresión, un número (el precio). 2) Para que entrenamiento y prueba
tengan ejemplos parecidos; no se baraja con datos temporales, donde se entrena con el pasado y se prueba con lo más reciente. 3) El
primero: generaliza; el segundo sobreajusta. 4) Precisión = 8/10 = 0.8; recall = 8/16 = 0.5. 5) El recall: no detectar un tumor (falso
negativo) es lo más grave. 6) Con una regla fija, por ejemplo, la etiqueta del vecino más cercano (o usando un k impar). 7) Porque la media
y la desviación usadas incluyen los datos de prueba, que el modelo no debería conocer.
