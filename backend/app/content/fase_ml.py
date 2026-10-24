from ._helpers import py, quiz

TOPICS = [
    {
        "slug": "ml-sklearn",
        "phase": "ml",
        "title": "Machine learning: fundamentos con scikit-learn",
        "summary": "Aprendizaje supervisado, división train/test, métricas, sobreajuste y fuga de datos.",
        "hours": 14,
        "theory": r"""
# Machine learning: fundamentos con scikit-learn

Como analista/ingeniero de datos no necesitas ser investigador de ML, pero sí **entender qué es un modelo, cómo se evalúa y cuándo no
fiarte de él**. Eso ya te pone por delante de mucha gente.

## 1. Tipos de problemas

- **Supervisado:** tienes ejemplos con la respuesta correcta (etiqueta).
  - *Clasificación:* predecir una categoría (¿cancelará el cliente? sí/no).
  - *Regresión:* predecir un número (¿cuánto venderemos?).
- **No supervisado:** no hay etiqueta; buscas estructura (clustering de clientes, detección de anomalías).

## 2. El flujo básico

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

X = df[["edad", "compras_ult_90d", "dias_desde_ultima_compra"]]   # características (features)
y = df["cancelo"]                                                   # objetivo (target)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
modelo = RandomForestClassifier(random_state=42).fit(X_train, y_train)
print(classification_report(y_test, modelo.predict(X_test)))
```

**Nunca evalúes con los mismos datos con los que entrenaste:** un modelo que memoriza saca nota perfecta y falla en producción.

## 3. Sobreajuste (overfitting)

Si el rendimiento en entrenamiento es excelente y en prueba es malo, el modelo **memorizó el ruido**. Remedios: más datos, modelos más simples,
regularización, validación cruzada (`cross_val_score`).

## 4. Métricas de clasificación

Con `TP`, `FP`, `FN`, `TN` (verdaderos/falsos positivos y negativos):

- **Accuracy** = aciertos / total. **Engaña** con clases desbalanceadas: si el 95 % de clientes no cancela, un modelo que siempre dice "no cancela" tiene 95 % de accuracy y es inútil.
- **Precisión** = TP / (TP + FP): de los que marqué como positivos, ¿cuántos lo eran?
- **Recall (sensibilidad)** = TP / (TP + FN): de los positivos reales, ¿cuántos detecté?
- **F1** = media armónica de precisión y recall.

¿Qué priorizar? Depende del negocio: en detección de fraude interesa un recall alto; en campañas costosas, una precisión alta.

Regresión: **MAE** (error absoluto medio, fácil de explicar), **RMSE** (penaliza más los errores grandes), **R²**.

## 5. Fuga de datos (data leakage): el error más caro

Ocurre cuando el modelo usa información que **no tendrá al predecir** en la vida real (por ejemplo, la columna `fecha_cancelacion` para predecir cancelación) o cuando preprocesas (escalas, imputas) **antes** de dividir train/test.
Los resultados parecen espectaculares y luego fallan. Usa `Pipeline` para que el preprocesamiento se ajuste solo con los datos de entrenamiento.

## 6. Siempre empieza con una línea base

Antes de un modelo complejo prueba algo trivial (predecir siempre la clase mayoritaria o el promedio) y una regresión logística/lineal.
Si el modelo complejo no supera claramente la línea base, no justifica su costo.

## Cómo sabes que dominas este tema

- Explicas la diferencia entre accuracy, precisión y recall con un ejemplo de negocio.
- Detectas fugas de datos en un enunciado.
- Entrenas, evalúas y comparas contra una línea base sin ayuda.
""",
        "exercises": [
            py("ml-precision", "Precisión y recall", "ML: métricas y evaluación",
               "Escribe `precision_recall(y_real, y_pred)` para etiquetas binarias (0/1). Devuelve `(precision, recall)`. "
               "Si el denominador de alguna métrica es 0, esa métrica vale `0.0`.",
               starter="""
def precision_recall(y_real, y_pred):
    # tu código aquí
    pass
""",
               solution="""
def precision_recall(y_real, y_pred):
    pares = list(zip(y_real, y_pred))
    tp = sum(1 for r, p in pares if r == 1 and p == 1)
    fp = sum(1 for r, p in pares if r == 0 and p == 1)
    fn = sum(1 for r, p in pares if r == 1 and p == 0)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return precision, recall
""",
               tests="""
p, r = precision_recall([1, 1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0, 0])
assert abs(p - 2 / 3) < 1e-9 and abs(r - 2 / 3) < 1e-9, "TP=2, FP=1, FN=1 -> precision y recall = 2/3"
assert precision_recall([1, 0, 1], [0, 0, 0]) == (0.0, 0.0), "Si nunca predice positivo, ambas valen 0.0"
assert precision_recall([0, 0], [0, 0]) == (0.0, 0.0)
"""),
            py("ml-split", "Dividir en train y test", "ML: métricas y evaluación",
               "Escribe `dividir_train_test(datos, proporcion_test=0.2, semilla=42)` que mezcle una **copia** de la lista con `random.Random(semilla)` "
               "y devuelva `(train, test)`, donde `test` tiene `round(len(datos) * proporcion_test)` elementos. No debe modificar la lista original "
               "y con la misma semilla debe dar siempre el mismo resultado.",
               starter="""
import random

def dividir_train_test(datos, proporcion_test=0.2, semilla=42):
    # tu código aquí
    pass
""",
               solution="""
import random

def dividir_train_test(datos, proporcion_test=0.2, semilla=42):
    copia = list(datos)
    random.Random(semilla).shuffle(copia)
    n_test = round(len(copia) * proporcion_test)
    return copia[n_test:], copia[:n_test]
""",
               tests="""
datos = list(range(100))
train, test = dividir_train_test(datos)
assert len(train) == 80 and len(test) == 20, "Con 100 datos y 0.2: 80 train y 20 test"
assert set(train).isdisjoint(test) and sorted(train + test) == datos, "No debe haber solapamiento ni perder datos"
assert datos == list(range(100)), "No modifiques la lista original"
assert dividir_train_test(datos) == (train, test), "Con la misma semilla el resultado debe ser reproducible"
"""),
            py("ml-mae", "Error absoluto medio", "ML: métricas y evaluación",
               "Escribe `mae(y_real, y_pred)` que calcule el error absoluto medio entre dos listas de números.",
               starter="""
def mae(y_real, y_pred):
    # tu código aquí
    pass
""",
               solution="""
def mae(y_real, y_pred):
    return sum(abs(r - p) for r, p in zip(y_real, y_pred)) / len(y_real)
""",
               tests="""
assert mae([10, 20, 30], [12, 18, 33]) == (2 + 2 + 3) / 3
assert mae([5, 5], [5, 5]) == 0
"""),
            quiz("ml-quiz-acc", "Accuracy engañosa", "ML: métricas y evaluación",
                 "El 98 % de las transacciones son legítimas y 2 % fraudulentas. Un modelo que siempre responde 'legítima' tiene 98 % de accuracy. ¿Qué es lo correcto?",
                 ["Es un excelente modelo", "Es inútil para detectar fraude; hay que mirar recall y precisión de la clase fraude",
                  "Hay que subir el accuracy a 100 %", "Hay que eliminar las transacciones legítimas"], 1,
                 "Con clases desbalanceadas la accuracy engaña. Importa cuántos fraudes detecta (recall) y cuántas alertas son reales (precisión)."),
            quiz("ml-quiz-leak", "Detectar fuga de datos", "ML: métricas y evaluación",
                 "Entrenas un modelo para predecir si un cliente cancelará y una de las variables es 'motivo_de_cancelacion'. Obtienes 99 % de accuracy. ¿Qué pasa?",
                 ["El modelo es genial", "Hay fuga de datos: esa variable solo existe después de cancelar", "Falta más entrenamiento", "Hay que usar otra métrica"], 1,
                 "El motivo de cancelación solo se conoce una vez que el cliente ya canceló. El modelo 'hace trampa' y fallará en producción."),
            quiz("ml-quiz-over", "Sobreajuste", "ML: métricas y evaluación",
                 "Tu modelo tiene 100 % de acierto en entrenamiento y 62 % en prueba. ¿Cuál es el diagnóstico más probable?",
                 ["Subajuste", "Sobreajuste", "Los datos de prueba son mejores", "Todo va bien"], 1,
                 "Una gran brecha entre entrenamiento y prueba indica que el modelo memorizó el ruido en lugar de aprender patrones generales."),
        ],
    },
    {
        "slug": "ia-llm-rag",
        "phase": "ml",
        "title": "IA generativa aplicada: LLMs, embeddings y RAG",
        "summary": "Qué son los LLMs, cómo funcionan los embeddings y cómo construir un asistente que responda sobre tus documentos (RAG).",
        "hours": 12,
        "theory": r"""
# IA generativa aplicada: LLMs, embeddings y RAG

Si te atrae la IA, este es el terreno donde un perfil de datos + backend tiene **más oportunidades**: no hace falta entrenar modelos,
hay que **integrarlos bien en productos reales** con datos propios.

## 1. LLMs en una página

- Un **LLM** (modelo de lenguaje grande) predice el siguiente *token* (trozo de texto) dado el texto anterior.
- **Ventana de contexto:** cuánto texto cabe en una consulta (instrucciones + documentos + conversación).
- **Temperatura:** controla la aleatoriedad (baja = más predecible; alta = más creativa).
- **Alucinaciones:** pueden afirmar cosas falsas con total seguridad. Se **mitigan**, no se eliminan.
- Se usan por **API** de un proveedor (o modelos abiertos en tu infraestructura). Se paga por tokens: controla costos y latencia.

## 2. Embeddings: significado como números

Un **embedding** convierte un texto en un vector de cientos de números tal que **textos con significado parecido quedan cerca**.
La cercanía se mide con la **similitud coseno**:

```
coseno(a, b) = (a · b) / (|a| · |b|)      # 1 = misma dirección, 0 = sin relación
```

## 3. RAG: Retrieval-Augmented Generation

El modelo no conoce tus documentos privados. RAG le **entrega** los fragmentos relevantes junto con la pregunta:

1. **Preparar:** dividir los documentos en *chunks* (con algo de solapamiento) → calcular su embedding → guardarlos en una **base vectorial** (pgvector en PostgreSQL, Qdrant, Chroma...).
2. **Consultar:** convertir la pregunta en embedding → recuperar los *k* chunks más similares.
3. **Generar:** construir un prompt con esos chunks y pedir al LLM que responda **solo con esa información** y cite la fuente.

```python
contexto = "\n\n".join(chunk.texto for chunk in recuperados)
prompt = f"Responde solo con el contexto. Si no está, di que no lo sabes.\n\nContexto:\n{contexto}\n\nPregunta: {pregunta}"
```

## 4. Lo que marca la diferencia en la práctica

- **Calidad del chunking** (tamaño, solapamiento, respetar títulos y párrafos).
- **Evaluación:** crea un conjunto de preguntas con respuestas esperadas y mide si el sistema recupera el fragmento correcto y responde bien. Sin evaluación, "parece que funciona".
- **Citas y trazabilidad:** muestra de qué documento salió cada afirmación.
- **Seguridad:** el contenido recuperado puede incluir instrucciones maliciosas (*prompt injection*). Trata los documentos como **datos**, no como órdenes, y limita lo que el modelo puede hacer.
- **Privacidad:** no envíes datos sensibles a terceros sin revisar el contrato y la normativa.
- **Cuándo NO usar un LLM:** si una consulta SQL, una regla o un modelo clásico resuelve el problema, es más barato, rápido y fiable.

## 5. RAG vs fine-tuning

- **RAG:** añade **conocimiento** actualizable (documentos que cambian). Es lo primero que se prueba.
- **Fine-tuning:** ajusta el **estilo/comportamiento** del modelo; no es buena forma de "enseñarle datos" que cambian.

## 6. Proyecto sugerido para tu portafolio

Un asistente que responda preguntas sobre documentos (por ejemplo, tus apuntes de esta plataforma o un manual público): FastAPI + PostgreSQL con
pgvector + una interfaz mínima en React, con citas y un conjunto de preguntas de evaluación. Combina todo lo que ya sabes.

## Cómo sabes que dominas este tema

- Dibujas la arquitectura de un RAG de memoria.
- Explicas por qué un RAG puede fallar y cómo lo medirías.
- Sabes cuándo un LLM no es la herramienta adecuada.
""",
        "exercises": [
            py("rag-coseno", "Similitud coseno", "IA aplicada: embeddings y RAG",
               "Escribe `similitud_coseno(a, b)` para dos vectores (listas de números del mismo tamaño). Devuelve `0.0` si alguno de los dos tiene norma cero.",
               starter="""
def similitud_coseno(a, b):
    # tu código aquí
    pass
""",
               solution="""
def similitud_coseno(a, b):
    producto = sum(x * y for x, y in zip(a, b))
    norma_a = sum(x * x for x in a) ** 0.5
    norma_b = sum(y * y for y in b) ** 0.5
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return producto / (norma_a * norma_b)
""",
               tests="""
assert similitud_coseno([1, 0], [0, 1]) == 0.0, "Vectores perpendiculares -> 0"
assert abs(similitud_coseno([1, 2], [2, 4]) - 1.0) < 1e-9, "Misma direccion -> 1"
assert abs(similitud_coseno([1, 0], [-1, 0]) + 1.0) < 1e-9, "Direcciones opuestas -> -1"
assert similitud_coseno([0, 0], [1, 2]) == 0.0, "Norma cero -> 0.0"
"""),
            py("rag-chunks", "Dividir un texto en chunks", "IA aplicada: embeddings y RAG",
               "Escribe `dividir_en_chunks(texto, tamano, solape)` que devuelva una lista de trozos de `tamano` caracteres donde cada trozo comparte `solape` "
               "caracteres con el anterior (el paso es `tamano - solape`). Un texto vacío devuelve `[]`. "
               "Ejemplo: `dividir_en_chunks('abcdefghij', 4, 1)` → `['abcd', 'defg', 'ghij']`.",
               starter="""
def dividir_en_chunks(texto, tamano, solape):
    # tu código aquí
    pass
""",
               solution="""
def dividir_en_chunks(texto, tamano, solape):
    if not texto:
        return []
    paso = tamano - solape
    return [texto[i:i + tamano] for i in range(0, max(len(texto) - solape, 1), paso)]
""",
               tests="""
assert dividir_en_chunks("abcdefghij", 4, 1) == ["abcd", "defg", "ghij"], "Con tamano=4 y solape=1 esperaba ['abcd', 'defg', 'ghij']"
assert dividir_en_chunks("abcdefghij", 4, 0) == ["abcd", "efgh", "ij"]
assert dividir_en_chunks("", 4, 1) == []
"""),
            py("rag-topk", "Recuperar los k más parecidos", "IA aplicada: embeddings y RAG",
               "Escribe `top_k(consulta, documentos, k)`. `documentos` es un diccionario `{nombre: vector}`. Devuelve la lista con los nombres de los `k` documentos "
               "con mayor similitud coseno con `consulta`, del más al menos parecido. (La función `similitud_coseno` ya está escrita.)",
               starter="""
def similitud_coseno(a, b):
    producto = sum(x * y for x, y in zip(a, b))
    norma_a = sum(x * x for x in a) ** 0.5
    norma_b = sum(y * y for y in b) ** 0.5
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return producto / (norma_a * norma_b)

def top_k(consulta, documentos, k):
    # tu código aquí
    pass
""",
               solution="""
def similitud_coseno(a, b):
    producto = sum(x * y for x, y in zip(a, b))
    norma_a = sum(x * x for x in a) ** 0.5
    norma_b = sum(y * y for y in b) ** 0.5
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return producto / (norma_a * norma_b)

def top_k(consulta, documentos, k):
    ranking = sorted(documentos, key=lambda nombre: similitud_coseno(consulta, documentos[nombre]), reverse=True)
    return ranking[:k]
""",
               tests="""
docs = {"gatos": [0.9, 0.1, 0.0], "perros": [0.8, 0.3, 0.1], "finanzas": [0.0, 0.1, 0.95]}
assert top_k([1.0, 0.2, 0.0], docs, 2) == ["gatos", "perros"], "Los dos mas parecidos deben ser gatos y perros"
assert top_k([0.0, 0.0, 1.0], docs, 1) == ["finanzas"]
"""),
            quiz("rag-quiz-1", "RAG o fine-tuning", "IA aplicada: embeddings y RAG",
                 "Quieres que un asistente responda con las políticas internas de la empresa, que cambian cada mes. ¿Qué enfoque priorizarías?",
                 ["Fine-tuning cada mes", "RAG con los documentos actualizados", "Escribir las respuestas a mano en el código", "Entrenar un modelo desde cero"], 1,
                 "RAG permite actualizar el conocimiento cambiando los documentos indexados, sin reentrenar nada, y además permite citar fuentes."),
            quiz("rag-quiz-2", "Reducir alucinaciones", "IA aplicada: embeddings y RAG",
                 "¿Cuál de estas medidas ayuda **más** a reducir alucinaciones en un asistente RAG?",
                 ["Subir la temperatura", "Instruir al modelo a responder solo con el contexto recuperado, citar fuentes y decir 'no lo sé' si falta información",
                  "Usar prompts más largos sin contenido", "Quitar la base vectorial"], 1,
                 "Anclar la respuesta al contexto recuperado, exigir citas y permitir 'no lo sé' reduce las afirmaciones inventadas."),
            quiz("rag-quiz-3", "Evaluar un RAG", "IA aplicada: embeddings y RAG",
                 "Tu RAG 'parece funcionar' en tres pruebas manuales. ¿Qué haces antes de confiar en él?",
                 ["Nada, ya funciona", "Crear un conjunto de preguntas con respuestas esperadas y medir recuperación y calidad de respuesta", "Cambiar el modelo por uno más grande", "Aumentar la ventana de contexto"], 1,
                 "Sin un conjunto de evaluación repetible no puedes saber si un cambio mejora o empeora el sistema."),
        ],
    },
]
