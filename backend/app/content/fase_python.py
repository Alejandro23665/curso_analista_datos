from ._helpers import py, quiz

TOPICS = [
    {
        "slug": "python-datos",
        "phase": "python",
        "title": "Python esencial para trabajar con datos",
        "summary": "Comprensiones, diccionarios, funciones limpias, archivos CSV/JSON y manejo de errores.",
        "hours": 10,
        "theory": r"""
# Python esencial para trabajar con datos

Ya programas en Python, así que aquí **no** vamos a repasar la sintaxis desde cero. Vamos a reforzar las
herramientas que más usarás en análisis e ingeniería de datos y que suelen aparecer en entrevistas.

## 1. Comprensiones: transformar datos en una línea

Una comprensión crea una colección a partir de otra, filtrando y transformando a la vez.

```python
precios = [10, 25, 3, 40]
caros = [p for p in precios if p > 20]          # [25, 40]
con_iva = [round(p * 1.16, 2) for p in precios] # transforma cada valor
por_nombre = {n: len(n) for n in ["ana", "luis"]}  # comprensión de diccionario
unicos = {p % 10 for p in precios}              # comprensión de conjunto
```

Regla práctica: si la comprensión no cabe cómodamente en una línea o necesita dos `if` anidados, usa un `for` normal.

## 2. Diccionarios y conjuntos: tus estructuras favoritas

- `dict.get(clave, defecto)` evita `KeyError` y sirve para contar: `conteo[x] = conteo.get(x, 0) + 1`.
- `collections.Counter` y `collections.defaultdict` hacen lo mismo con menos código.
- Los `set` eliminan duplicados y comprueban pertenencia en tiempo casi constante: `x in conjunto`.

## 3. Funciones que se pueden probar

En datos, las funciones **puras** (misma entrada → misma salida, sin tocar variables globales) son más fáciles de
probar y de reutilizar en pipelines.

```python
def normalizar_nombre(texto: str) -> str:
    return " ".join(texto.strip().lower().split())
```

**Error clásico:** argumentos por defecto mutables (`def f(x, lista=[])`). La lista se crea una sola vez y se
comparte entre llamadas. Usa `None` y crea la lista dentro.

## 4. Leer y escribir archivos

```python
import csv, json, io

with open("ventas.csv", newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):       # cada fila es un diccionario
        print(fila["producto"], fila["monto"])

datos = json.loads('{"a": 1, "b": [1, 2]}')   # texto -> objetos Python
texto = json.dumps(datos, indent=2)           # objetos Python -> texto
```

`io.StringIO(texto)` te deja tratar un texto como si fuera un archivo: ideal para practicar sin tocar el disco.
Usa siempre `with` para que el archivo se cierre solo y especifica `encoding="utf-8"`.

## 5. Manejo de errores

Los datos reales vienen sucios. Captura **solo** los errores que sabes manejar.

```python
def a_float(valor):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None
```

Evita `except:` a secas: esconde errores de programación. Usa `raise` para propagar lo que no puedas resolver.

## Cómo sabes que dominas este tema

- Escribes comprensiones sin mirar la sintaxis.
- Cuentas frecuencias con `dict.get` y también con `Counter`.
- Lees un CSV con el módulo `csv` y conviertes tipos con seguridad.
- Explicas por qué `def f(x, lista=[])` es peligroso.

> **Consejo del coach:** apunta en la pestaña *Apuntes* los 3 errores que más cometas. Revisarlos antes de cada
> sesión es una de las formas más baratas de mejorar.
""",
        "exercises": [
            py(
                "py-comprension", "Cuadrados de los pares", "Python: comprensiones",
                "Escribe `cuadrados_pares(nums)` que devuelva una lista con el cuadrado de cada número **par** de `nums`, "
                "en el mismo orden.",
                starter="""
def cuadrados_pares(nums):
    # tu código aquí
    pass
""",
                solution="""
def cuadrados_pares(nums):
    return [n * n for n in nums if n % 2 == 0]
""",
                tests="""
assert cuadrados_pares([1, 2, 3, 4]) == [4, 16], "Con [1, 2, 3, 4] debería devolver [4, 16]"
assert cuadrados_pares([]) == [], "Con una lista vacía debería devolver []"
assert cuadrados_pares([5, 7]) == [], "Si no hay pares, debería devolver []"
assert cuadrados_pares([-2, 0]) == [4, 0], "El 0 y los negativos pares también cuentan"
""",
                hint="Una comprensión con condición: [expresión for n in nums if condición].",
            ),
            py(
                "py-frecuencias", "Contar palabras", "Python: diccionarios",
                "Escribe `frecuencias(palabras)` que reciba una lista de palabras y devuelva un diccionario "
                "con cuántas veces aparece cada una, **ignorando mayúsculas/minúsculas** (las claves en minúscula).",
                starter="""
def frecuencias(palabras):
    # tu código aquí
    pass
""",
                solution="""
def frecuencias(palabras):
    conteo = {}
    for palabra in palabras:
        palabra = palabra.lower()
        conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo
""",
                tests="""
assert frecuencias(["Hola", "hola", "Mundo"]) == {"hola": 2, "mundo": 1}, "Revisa el uso de lower() y el conteo"
assert frecuencias([]) == {}, "Una lista vacía debe dar {}"
assert frecuencias(["a", "A", "a"]) == {"a": 3}
""",
                hint="conteo[x] = conteo.get(x, 0) + 1",
            ),
            py(
                "py-csv", "Totales por categoría desde un CSV", "Python: archivos CSV/JSON",
                "Escribe `total_por_categoria(texto_csv)`. Recibe el contenido de un CSV con columnas `categoria,monto` "
                "(como texto) y devuelve un diccionario categoría → suma de montos (como `float`). "
                "**Ignora** las filas con el monto vacío.",
                starter="""
import csv
import io

def total_por_categoria(texto_csv):
    # pista: csv.DictReader(io.StringIO(texto_csv))
    pass
""",
                solution="""
import csv
import io

def total_por_categoria(texto_csv):
    totales = {}
    for fila in csv.DictReader(io.StringIO(texto_csv)):
        if not fila["monto"].strip():
            continue
        categoria = fila["categoria"]
        totales[categoria] = totales.get(categoria, 0) + float(fila["monto"])
    return totales
""",
                tests="""
datos = "categoria,monto\\ncomida,10.5\\ncomida,4.5\\ntech,100\\ntech,\\n"
resultado = total_por_categoria(datos)
assert resultado == {"comida": 15.0, "tech": 100.0}, "Esperaba {'comida': 15.0, 'tech': 100.0} y obtuve %r" % resultado
assert total_por_categoria("categoria,monto\\n") == {}, "Sin filas debe devolver {}"
""",
                hint="Recorre las filas, salta las de monto vacío y acumula con get(categoria, 0).",
            ),
            py(
                "py-errores", "Conversión segura a entero", "Python: manejo de errores",
                "Escribe `a_entero_seguro(valor, defecto=0)` que convierta `valor` a `int`. "
                "Si no se puede convertir (texto no numérico, `None`, etc.), devuelve `defecto`. "
                "Debe aceptar textos con espacios como `' 7 '`.",
                starter="""
def a_entero_seguro(valor, defecto=0):
    # tu código aquí
    pass
""",
                solution="""
def a_entero_seguro(valor, defecto=0):
    try:
        return int(valor)
    except (ValueError, TypeError):
        return defecto
""",
                tests="""
assert a_entero_seguro("12") == 12
assert a_entero_seguro("  7 ") == 7, "int() ya ignora los espacios alrededor"
assert a_entero_seguro("abc", -1) == -1
assert a_entero_seguro(None) == 0, "None provoca TypeError"
assert a_entero_seguro("3.5", 9) == 9, "int('3.5') lanza ValueError"
""",
                hint="Captura ValueError y TypeError, no uses except a secas.",
            ),
            quiz(
                "py-quiz-mutable", "El argumento por defecto mutable", "Python: funciones",
                "¿Qué imprime este código?\n\n```python\ndef agregar(x, lista=[]):\n    lista.append(x)\n    return lista\n\n"
                "agregar(1)\nprint(agregar(2))\n```",
                ["[2]", "[1, 2]", "Un error", "None"], 1,
                "La lista por defecto se crea **una sola vez** al definir la función y se comparte entre llamadas. "
                "La solución habitual es `def agregar(x, lista=None): lista = [] if lista is None else lista`.",
            ),
        ],
    },
]
