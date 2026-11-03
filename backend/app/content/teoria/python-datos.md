# Python esencial para trabajar con datos

Con los dos capítulos anteriores ya sabes escribir funciones y manejar listas y diccionarios. Este capítulo da el salto a lo que hace
un programador en un trabajo real: **leer datos de un archivo, limpiarlos, resumirlos y guardar el resultado**. Es exactamente lo que
harás al procesar los documentos de un cliente, los mensajes de un chatbot o la respuesta de una API.

Vas a aprender:

- **Comprensiones**: transformar y filtrar colecciones en una línea.
- **Contar y agrupar** con las herramientas de la librería estándar (`Counter`, `defaultdict`).
- **Limpiar texto** que viene sucio.
- **Funciones puras** y la trampa de los valores por defecto mutables.
- **Archivos, CSV y JSON**: leer y escribir los formatos de datos más comunes.
- **Excepciones**: que un dato malo no tumbe todo el programa.

Al final juntamos todo en un pequeño *pipeline* (una cadena de pasos que procesa datos de principio a fin).

---

## 1. Comprensiones: transformar y filtrar en una línea

Ya viste la idea en el capítulo anterior. Aquí la dominamos, porque la verás en todo el código Python profesional.

### Comprensión de lista

La estructura general es:

```
[ expresión   for elemento in colección   if condición ]
   qué guardo     de dónde lo saco          (opcional) cuáles me quedo
```

```python
temperaturas = [18, 25, 31, 22, 35]

# Solo transformar
en_fahrenheit = [t * 9 / 5 + 32 for t in temperaturas]
# [64.4, 77.0, 87.8, 71.6, 95.0]

# Solo filtrar
calurosas = [t for t in temperaturas if t > 30]
# [31, 35]

# Filtrar y transformar a la vez
calurosas_f = [t * 9 / 5 + 32 for t in temperaturas if t > 30]
# [87.8, 95.0]
```

Léela en voz alta como una frase: *"dame `t` en Fahrenheit, para cada `t` de `temperaturas`, si `t` es mayor que 30"*. El orden en
que se ejecuta es: primero el `for`, luego el `if` (decide si el elemento pasa) y por último la expresión del principio.

Equivale exactamente a este bucle:

```python
calurosas_f = []
for t in temperaturas:
    if t > 30:
        calurosas_f.append(t * 9 / 5 + 32)
```

### `if` para filtrar frente a `if ... else` para elegir

Son dos cosas distintas y van en sitios distintos:

```python
notas = [8, 15, 11, 6]

# if AL FINAL: filtra (quita elementos)
aprobadas = [n for n in notas if n >= 10]                     # [15, 11]

# if ... else AL PRINCIPIO: elige qué valor poner (no quita ninguno)
estados = ["aprobado" if n >= 10 else "reprobado" for n in notas]
# ['reprobado', 'aprobado', 'aprobado', 'reprobado']
```

### Comprensiones de diccionario y de conjunto

Con llaves y `clave: valor` construyes un diccionario; con llaves y un solo valor, un conjunto:

```python
productos = ["café", "pan", "leche"]

longitudes = {p: len(p) for p in productos}
# {'café': 4, 'pan': 3, 'leche': 5}

precios = {"café": 4.5, "pan": 1.2, "leche": 2.0}
con_descuento = {p: round(precio * 0.9, 2) for p, precio in precios.items()}
# {'café': 4.05, 'pan': 1.08, 'leche': 1.8}

iniciales = {p[0] for p in productos}
# {'c', 'p', 'l'}  (sin repetidos)
```

### Cuándo NO usar una comprensión

- Si no cabe cómodamente en una línea.
- Si necesitas más de una condición compleja o varias operaciones por elemento.
- Si dentro necesitas `print`, `try/except` o modificar otras variables.

En esos casos un `for` normal es más legible, y la legibilidad gana siempre. Una comprensión es para **construir una colección**, no para
"ahorrar líneas".

### Comprueba que entendiste

**Pregunta:** ¿qué produce `[len(p) for p in ["sol", "mar", "montaña"] if len(p) > 3]`?

**Respuesta:** `[7]`. Solo "montaña" pasa el filtro (`len > 3`), y de ella se guarda su longitud.

---

## 2. Contar y agrupar sin reinventar la rueda

En el capítulo anterior contaste con `d.get(clave, 0) + 1`. Es importante que entiendas ese patrón, pero Python trae herramientas que lo
hacen por ti en el módulo `collections`.

### Importar un módulo

Un **módulo** es un archivo de código con funciones listas para usar. La "librería estándar" son los módulos que vienen con Python, sin
instalar nada. Se cargan con `import`:

```python
from collections import Counter, defaultdict
import csv
import json
```

`from X import Y` trae solo `Y`; `import X` trae el módulo entero y usas `X.algo`.

### `Counter`: contar en una línea

```python
from collections import Counter

colores = ["rojo", "azul", "rojo", "verde", "rojo", "azul"]
conteo = Counter(colores)
print(conteo)                    # Counter({'rojo': 3, 'azul': 2, 'verde': 1})
print(conteo["rojo"])            # 3
print(conteo["negro"])           # 0   (no da KeyError: lo que no está cuenta 0)
print(conteo.most_common(2))     # [('rojo', 3), ('azul', 2)]  los 2 más frecuentes
```

Un `Counter` se comporta como un diccionario: puedes recorrerlo con `.items()` o convertirlo con `dict(conteo)`.

### `defaultdict`: diccionarios con valor inicial automático

Al agrupar, siempre había que preguntar "¿existe ya esta clave?" antes de añadir. `defaultdict` crea el valor inicial automáticamente la
primera vez que usas una clave:

```python
from collections import defaultdict

compras = [("Ana", 20), ("Luis", 15), ("Ana", 5)]

# Agrupar en listas: el valor inicial es una lista vacía
por_cliente = defaultdict(list)
for cliente, monto in compras:
    por_cliente[cliente].append(monto)
print(dict(por_cliente))      # {'Ana': [20, 5], 'Luis': [15]}

# Sumar: el valor inicial es 0
gasto = defaultdict(int)
for cliente, monto in compras:
    gasto[cliente] += monto
print(dict(gasto))            # {'Ana': 25, 'Luis': 15}
```

`defaultdict(list)` empieza cada clave con `[]`; `defaultdict(int)` con `0`; `defaultdict(float)` con `0.0`.

### Ordenar por un criterio: `key`

Para ordenar diccionarios o tuplas por un campo concreto, `sorted` acepta `key`, una función que dice **por qué valor ordenar**:

```python
gasto = {"Ana": 25, "Luis": 15, "Eva": 40}
ranking = sorted(gasto.items(), key=lambda par: par[1], reverse=True)
print(ranking)      # [('Eva', 40), ('Ana', 25), ('Luis', 15)]
```

`lambda par: par[1]` es una función pequeña sin nombre: recibe un par `(nombre, monto)` y devuelve el monto. Es lo mismo que:

```python
def por_monto(par):
    return par[1]

ranking = sorted(gasto.items(), key=por_monto, reverse=True)
```

También funciona con `max` y `min`: `max(gasto, key=gasto.get)` devuelve la clave con el valor más alto (`'Eva'`).

### Comprueba que entendiste

**Pregunta:** ¿qué devuelve `Counter("banana").most_common(1)`?

**Respuesta:** `[('a', 3)]`. Un texto se recorre letra a letra y la "a" aparece 3 veces.

---

## 3. Limpiar texto sucio

Los datos que escriben las personas o que llegan de sistemas distintos casi nunca vienen limpios: espacios de más, mayúsculas
mezcladas, tildes en unos sitios sí y en otros no. Si no los normalizas, `"Café"`, `"café "` y `"CAFE"` cuentan como tres productos
distintos.

Herramientas clave (todas devuelven un texto **nuevo**):

| Operación | Código | Ejemplo |
|---|---|---|
| Quitar espacios de los extremos | `t.strip()` | `"  pan  "` → `"pan"` |
| Unificar mayúsculas | `t.lower()` | `"PaN"` → `"pan"` |
| Colapsar espacios internos | `" ".join(t.split())` | `"pan   dulce"` → `"pan dulce"` |
| Reemplazar | `t.replace(",", ".")` | `"3,5"` → `"3.5"` |
| Título | `t.title()` | `"ana pérez"` → `"Ana Pérez"` |

`t.split()` **sin argumento** corta por cualquier cantidad de espacios, tabuladores o saltos de línea, y descarta los vacíos. Por eso
`" ".join(t.split())` es el truco estándar para dejar exactamente un espacio entre palabras.

Encadenar operaciones es normal, porque cada una devuelve un texto:

```python
def normalizar(texto):
    return " ".join(texto.strip().lower().split())

print(normalizar("   Pan    DULCE  "))    # pan dulce
```

Y para contar ignorando mayúsculas, normaliza **antes** de contar:

```python
respuestas = ["Sí", "si ", "NO", "sí"]
limpias = [r.strip().lower() for r in respuestas]
print(Counter(limpias))      # Counter({'sí': 2, 'si': 1, 'no': 1})
```

Fíjate en que `"sí"` y `"si"` siguen siendo distintos: la tilde es otro carácter. Quitar tildes requiere el módulo `unicodedata`; lo
verás cuando lo necesites. Lo importante ahora es la idea: **decide una forma canónica y convierte todo a ella antes de comparar**.

---

## 4. Funciones puras y la trampa del valor por defecto mutable

### Funciones puras

Una función es **pura** cuando:

1. Para la misma entrada devuelve siempre la misma salida.
2. No modifica nada de fuera (ni variables globales, ni las listas que recibe, ni archivos).

```python
# Pura: solo depende de sus parámetros y devuelve un valor nuevo
def con_impuesto(precios, tasa):
    return [p * (1 + tasa) for p in precios]

# No pura: modifica la lista que recibe
def aplicar_impuesto(precios, tasa):
    for i in range(len(precios)):
        precios[i] = precios[i] * (1 + tasa)
```

Las funciones puras son fáciles de **probar** (le das una entrada y miras la salida) y de **reutilizar** (no tienen efectos
sorpresa). En procesamiento de datos, escribe tus pasos como funciones puras siempre que puedas.

### La trampa del valor por defecto mutable

Esta es una de las preguntas favoritas de las entrevistas de Python. Mira este código:

```python
def registrar(evento, historial=[]):
    historial.append(evento)
    return historial

print(registrar("login"))     # ['login']
print(registrar("compra"))    # ['login', 'compra']   ¿¿por qué??
```

Esperarías `['compra']` en la segunda llamada, pero sale `['login', 'compra']`. La razón: **el valor por defecto se crea una sola vez,
cuando Python lee el `def`**, no en cada llamada. Todas las llamadas que no pasan `historial` comparten **la misma lista**, que va
acumulando datos de llamadas anteriores.

Con valores inmutables (números, textos, `None`, tuplas) no hay problema, porque no se pueden modificar. El problema aparece solo con
valores **mutables**: listas, diccionarios y conjuntos.

La solución estándar es usar `None` como valor por defecto y crear la lista dentro:

```python
def registrar(evento, historial=None):
    if historial is None:
        historial = []           # una lista nueva en CADA llamada
    historial.append(evento)
    return historial

print(registrar("login"))     # ['login']
print(registrar("compra"))    # ['compra']
```

`is None` es la forma correcta de preguntar si algo es `None` (más preciso que `== None`).

---

## 5. Leer y escribir archivos

### Abrir un archivo con `with`

```python
with open("notas.txt", encoding="utf-8") as archivo:
    contenido = archivo.read()          # todo el archivo como un solo texto
print(contenido)
```

- `open(ruta, modo, encoding=...)` abre el archivo. El modo por defecto es `"r"` (leer).
- **`encoding="utf-8"`**: indícalo siempre. Sin él, en Windows los caracteres como "ñ" o "é" pueden leerse mal.
- **`with`** cierra el archivo automáticamente al salir del bloque, incluso si ocurre un error. Olvidar cerrar un archivo puede dejar
  datos sin guardar o bloquear el archivo.

### Leer línea a línea

Para archivos grandes, no los cargues enteros: recórrelos línea a línea.

```python
with open("registro.log", encoding="utf-8") as archivo:
    for numero, linea in enumerate(archivo, start=1):
        linea = linea.rstrip("\n")      # cada línea trae su salto de línea al final
        if "ERROR" in linea:
            print(numero, linea)
```

### Escribir

```python
with open("resumen.txt", "w", encoding="utf-8") as archivo:
    archivo.write("Total de ventas: 1500\n")
    archivo.write("Clientes: 42\n")
```

| Modo | Qué hace |
|---|---|
| `"r"` | Leer (por defecto). Error si el archivo no existe. |
| `"w"` | Escribir. **Borra** el contenido anterior o crea el archivo. |
| `"a"` | Añadir al final sin borrar. |

`write` no añade saltos de línea: ponlos tú con `\n`.

### Archivos que no existen

```python
open("no_existe.txt", encoding="utf-8")
```

```
FileNotFoundError: [Errno 2] No such file or directory: 'no_existe.txt'
```

Las rutas relativas (`"datos/ventas.csv"`) se buscan desde la carpeta en la que **se ejecuta** el programa, no desde donde está el
archivo `.py`. Es una fuente frecuente de este error.

### Tratar un texto como si fuera un archivo: `io.StringIO`

Muchas funciones esperan un archivo, pero a veces tienes los datos en una variable de texto (por ejemplo, el contenido de un archivo
subido a una API, o en los ejercicios de esta plataforma). `io.StringIO` envuelve un texto para que se comporte como un archivo abierto:

```python
import io

texto = "linea uno\nlinea dos\n"
archivo_falso = io.StringIO(texto)
for linea in archivo_falso:
    print(linea.strip())
```

---

## 6. CSV: datos en forma de tabla

Un CSV (*comma-separated values*) es un archivo de texto donde cada línea es una fila y las columnas se separan con comas. La primera
línea suele tener los nombres de las columnas:

```
producto,ciudad,unidades
café,Caracas,12
pan,Valencia,30
café,Valencia,
```

Podrías separar cada línea con `split(",")`, pero falla en cuanto un valor contiene una coma entre comillas (`"Pérez, Ana"`). El módulo
`csv` maneja esos casos correctamente.

### `csv.DictReader`: cada fila como diccionario

```python
import csv
import io

texto = """producto,ciudad,unidades
café,Caracas,12
pan,Valencia,30
café,Valencia,
"""

lector = csv.DictReader(io.StringIO(texto))
for fila in lector:
    print(fila)
```

```
{'producto': 'café', 'ciudad': 'Caracas', 'unidades': '12'}
{'producto': 'pan', 'ciudad': 'Valencia', 'unidades': '30'}
{'producto': 'café', 'ciudad': 'Valencia', 'unidades': ''}
```

Tres cosas importantísimas:

1. **Todos los valores llegan como texto**, incluso los números: `'12'`, no `12`. Para hacer cuentas, conviértelos con `int()` o
   `float()`.
2. **Los valores vacíos llegan como texto vacío `''`**, y `int('')` da `ValueError`. Hay que decidir qué hacer con ellos: saltar la
   fila, usar 0 o marcarla como error.
3. La primera línea (los nombres de las columnas) la usa `DictReader` como claves; no aparece como fila.

Para leer un archivo real en lugar de un texto, pasa el archivo abierto (con `newline=""`, que el módulo `csv` recomienda):

```python
with open("ventas.csv", newline="", encoding="utf-8") as archivo:
    for fila in csv.DictReader(archivo):
        ...
```

### Ejemplo: unidades por ciudad, saltando filas incompletas

```python
from collections import defaultdict

unidades_por_ciudad = defaultdict(int)
for fila in csv.DictReader(io.StringIO(texto)):
    if not fila["unidades"].strip():     # vacío o solo espacios: la saltamos
        continue
    unidades_por_ciudad[fila["ciudad"]] += int(fila["unidades"])

print(dict(unidades_por_ciudad))    # {'Caracas': 12, 'Valencia': 30}
```

### Escribir un CSV

```python
filas = [
    {"ciudad": "Caracas", "unidades": 12},
    {"ciudad": "Valencia", "unidades": 30},
]
with open("resumen.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=["ciudad", "unidades"])
    escritor.writeheader()       # escribe la fila de nombres
    escritor.writerows(filas)    # escribe todas las filas
```

---

## 7. JSON: el formato de las APIs

**JSON** es el formato de texto con el que se comunican casi todas las APIs del mundo, incluidas las de los modelos de IA. Se parece
muchísimo a los diccionarios y listas de Python:

```json
{
  "cliente": "Ana",
  "activo": true,
  "pedidos": [
    {"id": 1, "total": 25.5},
    {"id": 2, "total": null}
  ]
}
```

Diferencias con Python: `true`/`false`/`null` en minúscula (en Python, `True`/`False`/`None`), y las claves siempre entre comillas
dobles.

### De texto a Python y de Python a texto

```python
import json

texto = '{"cliente": "Ana", "activo": true, "pedidos": [{"id": 1, "total": 25.5}]}'

datos = json.loads(texto)            # loads = "load string": texto JSON -> objetos Python
print(datos["cliente"])              # Ana
print(datos["activo"])               # True
print(datos["pedidos"][0]["total"])  # 25.5

resumen = {"clientes": 42, "ciudades": ["Caracas", "Mérida"]}
salida = json.dumps(resumen, ensure_ascii=False, indent=2)   # objetos Python -> texto JSON
print(salida)
```

```
{
  "clientes": 42,
  "ciudades": [
    "Caracas",
    "Mérida"
  ]
}
```

- `indent=2` lo hace legible para personas.
- `ensure_ascii=False` deja las tildes tal cual (sin él verías `Mérida`).

### Con archivos

```python
with open("config.json", encoding="utf-8") as archivo:
    config = json.load(archivo)          # sin "s": lee de un archivo

with open("salida.json", "w", encoding="utf-8") as archivo:
    json.dump(resumen, archivo, ensure_ascii=False, indent=2)
```

Regla mnemotécnica: con **s** (`loads`, `dumps`) trabajas con un **s**tring; sin s, con un archivo.

Si el texto no es JSON válido, `json.loads` lanza `json.JSONDecodeError`. Pasa mucho cuando un modelo de IA responde con texto alrededor
del JSON; verás cómo manejarlo en los temas de IA.

---

## 8. Excepciones: que un dato malo no tumbe el programa

Cuando algo falla, Python **lanza una excepción** (los errores que ya conoces: `ValueError`, `KeyError`...). Si nadie la maneja, el
programa se detiene. Con `try/except` puedes **capturarla** y decidir qué hacer.

### Estructura básica

```python
texto = "doce"
try:
    unidades = int(texto)
except ValueError:
    print(f"'{texto}' no es un número; uso 0")
    unidades = 0
print(unidades)
```

1. Python intenta ejecutar el bloque `try`.
2. Si ocurre un `ValueError`, salta al bloque `except` (y el resto del `try` no se ejecuta).
3. Si no ocurre nada, el `except` se ignora.

### Capturar solo lo que sabes manejar

```python
# MAL: atrapa cualquier error, incluso los que son fallos de tu código
try:
    total = calcular_total(datos)
except:
    total = 0
```

Un `except:` sin tipo esconde errores de programación (un nombre mal escrito, un `TypeError` por un bug) y te deja con resultados
incorrectos sin saber por qué. **Captura siempre tipos concretos.** Si un mismo bloque puede fallar de varias formas esperadas, puedes
listarlas:

```python
def a_decimal(valor):
    try:
        return float(str(valor).replace(",", "."))
    except (ValueError, TypeError):
        return None

print(a_decimal("3,5"))     # 3.5
print(a_decimal("abc"))     # None
print(a_decimal(None))      # None  (str(None) es el texto "None", y float("None") da ValueError)
```

### `else` y `finally`

```python
try:
    archivo = open("datos.txt", encoding="utf-8")
except FileNotFoundError:
    print("No encontré el archivo")
else:
    print("Lo abrí bien")          # solo si NO hubo excepción
    archivo.close()
finally:
    print("Esto se ejecuta siempre")
```

### Lanzar tus propias excepciones: `raise`

Cuando tu función recibe datos que no tienen sentido, lo correcto suele ser **avisar con un error claro** en lugar de devolver algo
inventado:

```python
def porcentaje(parte, total):
    if total == 0:
        raise ValueError("El total no puede ser 0")
    return parte / total * 100
```

¿Cuándo capturar y cuándo lanzar? **Captura** cuando sabes qué hacer con el problema (usar un valor por defecto, saltar la fila,
reintentar). **Lanza** (o deja que la excepción suba) cuando no sabes qué hacer: así quien llamó a la función decide. Devolver `None` o 0
"por si acaso" esconde los problemas.

### Comprueba que entendiste

**Pregunta:** ¿qué imprime este código?

```python
try:
    print("A")
    x = int("7")
    print("B")
except ValueError:
    print("C")
print("D")
```

**Respuesta:** `A`, `B` y `D`. `int("7")` funciona, así que no hay excepción y el `except` no se ejecuta.

---

## 9. Todo junto: un pequeño pipeline de datos

Vamos a procesar un CSV de inscripciones a cursos. El objetivo: **cuántos alumnos válidos tiene cada curso**, con los nombres de curso
normalizados, y guardar el resultado en JSON. Los datos vienen sucios a propósito.

```python
import csv
import io
import json
from collections import Counter

texto = """alumno,curso,edad
Ana,  Python ,22
Luis,python,abc
Eva,SQL,30
,SQL,25
Mar, sql ,19
"""

def normalizar(texto):
    return " ".join(texto.strip().lower().split())

def edad_valida(valor):
    try:
        edad = int(valor)
    except ValueError:
        return False
    return 15 <= edad <= 99

def alumnos_por_curso(texto_csv):
    conteo = Counter()
    for fila in csv.DictReader(io.StringIO(texto_csv)):
        if not fila["alumno"].strip():         # sin nombre: fila inválida
            continue
        if not edad_valida(fila["edad"]):      # edad no numérica o absurda
            continue
        conteo[normalizar(fila["curso"])] += 1
    return dict(conteo)

resultado = alumnos_por_curso(texto)
print(resultado)                                   # {'python': 1, 'sql': 2}
print(json.dumps(resultado, ensure_ascii=False))   # {"python": 1, "sql": 2}
```

Recorre el razonamiento:

- Ana cuenta para `python` (los espacios y mayúsculas se normalizan).
- Luis se descarta porque su edad no es un número.
- Eva cuenta para `sql`.
- La fila sin nombre se descarta.
- Mar cuenta para `sql`.

Fíjate en la estructura: **funciones pequeñas y puras** (`normalizar`, `edad_valida`) y una función principal que las combina. Cada
pieza se puede probar por separado. Así se escriben los pipelines de datos de verdad, desde un script de 30 líneas hasta un sistema
que procesa millones de filas.

---

## 10. Errores típicos de este capítulo

| Síntoma | Causa | Solución |
|---|---|---|
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | Sumaste un valor de un CSV sin convertirlo | Convierte con `int()`/`float()` |
| `ValueError: invalid literal for int() with base 10: ''` | Una celda vacía en el CSV | Comprueba si está vacía antes de convertir, o usa `try` |
| Palabras iguales cuentan como distintas | Mayúsculas o espacios distintos | Normaliza antes de contar |
| Una lista guarda datos de llamadas anteriores | Valor por defecto mutable (`=[]`) | Usa `=None` y crea la lista dentro |
| Caracteres raros (`Ã©` en lugar de `é`) | Falta `encoding="utf-8"` | Indica siempre la codificación |
| `FileNotFoundError` | Ruta incorrecta o relativa a otra carpeta | Revisa desde dónde ejecutas el programa |
| `json.JSONDecodeError` | El texto no es JSON válido | Revisa el texto; captura la excepción si puede pasar |
| Errores que "desaparecen" y resultados raros | Un `except:` sin tipo | Captura solo excepciones concretas |

---

## Resumen del capítulo

| Herramienta | Para qué | Ejemplo |
|---|---|---|
| Comprensión de lista | Transformar o filtrar | `[x * 2 for x in xs if x > 0]` |
| Comprensión de diccionario | Construir un diccionario | `{k: v * 2 for k, v in d.items()}` |
| `Counter` | Contar frecuencias | `Counter(lista).most_common(3)` |
| `defaultdict` | Agrupar o acumular sin comprobar claves | `defaultdict(list)`, `defaultdict(int)` |
| `sorted(..., key=...)` | Ordenar por un criterio | `sorted(d.items(), key=lambda p: p[1])` |
| Normalizar texto | Comparar textos sucios | `" ".join(t.strip().lower().split())` |
| `with open(...)` | Leer y escribir archivos que se cierran solos | `encoding="utf-8"` siempre |
| `csv.DictReader` | Leer un CSV fila a fila como diccionarios | Todo llega como texto |
| `json.loads` / `json.dumps` | JSON ↔ Python | `ensure_ascii=False`, `indent=2` |
| `try/except Tipo` | Manejar errores esperados | Nunca `except:` a secas |
| `raise` | Avisar de datos inválidos | `raise ValueError("...")` |

## Autoevaluación final

1. ¿Qué diferencia hay entre `[x for x in xs if c]` y `[a if c else b for x in xs]`?
2. ¿Qué devuelve `Counter(["a", "b", "a"])["z"]`?
3. ¿Por qué `def f(x, datos=[])` es peligroso y cómo se arregla?
4. Lees un CSV con `DictReader`. ¿De qué tipo es el valor de una columna numérica?
5. ¿Qué diferencia hay entre `json.load` y `json.loads`?
6. ¿Qué modo de `open` borra el contenido anterior del archivo?
7. ¿Por qué es mala idea `except:` sin tipo?
8. ¿Cómo dejas exactamente un espacio entre las palabras de un texto?

**Respuestas:** 1) La primera filtra (quita elementos que no cumplen); la segunda elige un valor para cada elemento sin quitar ninguno.
2) `0`. 3) La lista por defecto se crea una sola vez y se comparte entre llamadas; usa `datos=None` y crea la lista dentro. 4) Texto
(`str`). 5) `load` lee de un archivo; `loads` de un texto. 6) `"w"`. 7) Porque también atrapa los errores de programación y los
esconde. 8) `" ".join(texto.split())`.

En la práctica vas a combinar estas herramientas: una comprensión con filtro, contar ignorando mayúsculas, sumar por categoría desde un
CSV saltando valores vacíos, y convertir valores sin que el programa se caiga.
