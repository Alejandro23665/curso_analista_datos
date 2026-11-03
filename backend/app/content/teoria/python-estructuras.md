# Funciones, listas y diccionarios paso a paso

En el capítulo anterior trabajaste con valores sueltos: un número, un texto. Los programas reales manejan **muchos datos a la vez**
(los productos de una tienda, los mensajes de un chat, las filas de una tabla) y repiten las mismas operaciones una y otra vez. Para
eso existen dos herramientas que vas a usar todos los días durante el resto de tu carrera:

- **Funciones**, para empaquetar un trozo de lógica con nombre y reutilizarlo.
- **Estructuras de datos** (listas, tuplas, diccionarios y conjuntos), para guardar y organizar muchos valores.

Todo lo que viene después (pandas, APIs con FastAPI, el JSON que devuelve un modelo de IA) está hecho de estas piezas. Un JSON, por
ejemplo, no es más que diccionarios y listas anidados.

Igual que antes: copia los ejemplos, cámbialos, **predice el resultado antes de ejecutar** y responde las preguntas de comprobación.

---

## 1. Funciones a fondo

En el capítulo anterior viste lo básico: `def`, parámetros y `return`. Ahora vamos a ver por qué las funciones son tan importantes y
todas las formas de usarlas.

### Por qué usar funciones

Imagina que calculas el precio con descuento en cinco sitios distintos de tu programa. Si un día cambia la regla del descuento, tendrías
que cambiar cinco sitios (y olvidarás alguno). Con una función, la regla vive en **un solo lugar**:

```python
def aplicar_descuento(precio, porcentaje):
    return precio * (1 - porcentaje / 100)

print(aplicar_descuento(200, 10))    # 180.0
print(aplicar_descuento(80, 25))     # 60.0
```

Ventajas: **reutilizas** el código, le das un **nombre** que explica qué hace, y puedes **probarlo por separado**.

### Parámetros y argumentos

- **Parámetros:** los nombres que aparecen en la definición (`precio`, `porcentaje`).
- **Argumentos:** los valores concretos que pasas al llamar (`200`, `10`).

Al llamar a la función, Python asigna cada argumento a su parámetro **por posición**: el primero al primero, el segundo al segundo.

### Valores por defecto

Puedes darle a un parámetro un valor que se usará **si no lo pasan**:

```python
def saludar(nombre, saludo="Hola"):
    return f"{saludo}, {nombre}"

print(saludar("Ana"))                # Hola, Ana          (usa el valor por defecto)
print(saludar("Ana", "Buenos días")) # Buenos días, Ana   (lo sustituye)
```

Regla: los parámetros con valor por defecto van **después** de los que no lo tienen. `def f(a=1, b):` es un `SyntaxError`.

### Argumentos por nombre

También puedes pasar los argumentos indicando a qué parámetro van. Así el orden da igual y la llamada se entiende mejor:

```python
def crear_usuario(nombre, edad, pais="Venezuela"):
    return f"{nombre} ({edad}) de {pais}"

print(crear_usuario(edad=25, nombre="Luis"))          # Luis (25) de Venezuela
print(crear_usuario("Eva", 31, pais="Chile"))         # Eva (31) de Chile
```

Esto es muy común al usar librerías: verás llamadas como `round(3.14159, ndigits=2)` o, más adelante,
`client.messages.create(model=..., max_tokens=...)`.

### Devolver varios valores

Una función puede devolver varios valores separados por comas. En realidad devuelve una **tupla** (lo verás en la sección 4), que puedes
"desempaquetar" en varias variables:

```python
def estadisticas(a, b):
    suma = a + b
    promedio = suma / 2
    return suma, promedio

s, p = estadisticas(4, 8)
print(s)    # 12
print(p)    # 6.0
```

### Ámbito: las variables de una función viven dentro de ella

Las variables que creas **dentro** de una función (incluidos los parámetros) solo existen mientras la función se ejecuta. Fuera de
ella no existen:

```python
def calcular():
    resultado = 42
    return resultado

calcular()
print(resultado)
```

```
NameError: name 'resultado' is not defined
```

`resultado` existió dentro de `calcular` y desapareció al terminar. Por eso las funciones se comunican con el exterior **solo** a
través de los parámetros (lo que entra) y el `return` (lo que sale). Esa disciplina es una ventaja: una función no puede estropear por
accidente las variables del resto del programa.

### Funciones que llaman a otras funciones

Las funciones se combinan como piezas de Lego. Divide un problema grande en funciones pequeñas, cada una con una sola tarea:

```python
def subtotal(precio, cantidad):
    return precio * cantidad

def con_impuesto(monto, tasa=0.16):
    return monto * (1 + tasa)

def total_linea(precio, cantidad):
    return con_impuesto(subtotal(precio, cantidad))

print(total_linea(10, 3))    # 34.8
```

### Documentar una función

Es buena práctica explicar qué hace una función en una línea de texto justo debajo del `def` (se llama *docstring*):

```python
def area_circulo(radio):
    'Devuelve el área de un círculo a partir de su radio.'
    return 3.14159 * radio ** 2
```

### Comprueba que entendiste

**Pregunta:** ¿qué imprime `print(saludar("Mar", saludo="Hey"))` con la función `saludar` de arriba? ¿Y qué pasa con `saludar()`?

**Respuesta:** imprime `Hey, Mar`. `saludar()` da un `TypeError` porque falta el argumento obligatorio `nombre` (solo `saludo` tiene
valor por defecto).

---

## 2. Listas: colecciones ordenadas

Una **lista** guarda varios valores **en orden**. Se escribe entre corchetes, con los elementos separados por comas:

```python
precios = [12.5, 8.0, 4.5, 20.0]
nombres = ["Ana", "Luis", "Eva"]
mezcla = [1, "dos", 3.0, True]       # puede mezclar tipos (aunque no es lo habitual)
vacia = []                           # lista vacía
```

### Acceder por posición (índice)

Igual que con los textos, **se cuenta desde 0**, y los índices negativos cuentan desde el final:

```
 nombres:    "Ana"   "Luis"   "Eva"
 índice:       0        1        2
 negativo:    -3       -2       -1
```

```python
print(nombres[0])     # Ana
print(nombres[2])     # Eva
print(nombres[-1])    # Eva   (el último, sin importar cuántos haya)
print(len(nombres))   # 3
```

Pedir un índice que no existe da `IndexError: list index out of range`. En una lista de 3 elementos, el último índice válido es 2.

### Slicing: sacar un trozo

La sintaxis completa es `lista[inicio:fin:paso]`. El inicio se incluye, el **fin no**, y cualquiera de los tres se puede omitir:

```python
numeros = [10, 20, 30, 40, 50, 60]
print(numeros[1:4])     # [20, 30, 40]     posiciones 1, 2 y 3
print(numeros[:3])      # [10, 20, 30]     desde el principio
print(numeros[3:])      # [40, 50, 60]     hasta el final
print(numeros[-2:])     # [50, 60]         los dos últimos
print(numeros[::2])     # [10, 30, 50]     de 2 en 2
print(numeros[::-1])    # [60, 50, 40, 30, 20, 10]   al revés
```

El slicing **no modifica** la lista original: crea una nueva. Funciona igual con los textos: `"Python"[::2]` da `"Pto"`.

### Modificar una lista

A diferencia de los textos, las listas **sí se pueden modificar** (son *mutables*):

```python
tareas = ["estudiar", "comer"]
tareas[1] = "almorzar"          # cambia un elemento: ['estudiar', 'almorzar']
tareas.append("dormir")         # añade al final: ['estudiar', 'almorzar', 'dormir']
tareas.insert(0, "despertar")   # inserta en una posición: ['despertar', 'estudiar', 'almorzar', 'dormir']
tareas.remove("almorzar")       # quita la primera aparición de ese valor
ultima = tareas.pop()           # quita y devuelve el último: 'dormir'
primera = tareas.pop(0)         # quita y devuelve el de la posición 0: 'despertar'
print(tareas)                   # ['estudiar']
```

| Método | Qué hace | ¿Devuelve algo? |
|---|---|---|
| `.append(x)` | Añade `x` al final | No (`None`) |
| `.insert(i, x)` | Inserta `x` en la posición `i` | No |
| `.remove(x)` | Quita la primera aparición de `x` (error si no está) | No |
| `.pop()` / `.pop(i)` | Quita el último (o el de posición `i`) | **Sí**, el elemento quitado |
| `.sort()` | Ordena la lista en su sitio | No |
| `.reverse()` | Invierte la lista en su sitio | No |
| `.index(x)` | Posición de la primera aparición de `x` | Sí |
| `.count(x)` | Cuántas veces aparece `x` | Sí |

**Trampa clásica:** los métodos que modifican la lista devuelven `None`. Esto **borra** tu lista:

```python
numeros = [3, 1, 2]
numeros = numeros.sort()    # sort ordena en su sitio y devuelve None...
print(numeros)              # None
```

Lo correcto es `numeros.sort()` a secas, o usar la **función** `sorted(numeros)`, que no toca la original y **devuelve** una lista
nueva ordenada:

```python
numeros = [3, 1, 2]
ordenados = sorted(numeros)                 # [1, 2, 3]
de_mayor_a_menor = sorted(numeros, reverse=True)   # [3, 2, 1]
print(numeros)                              # [3, 1, 2]  (la original sigue igual)
```

### Funciones que reciben una lista

```python
notas = [14, 18, 9, 16]
print(len(notas))                  # 4
print(sum(notas))                  # 57
print(min(notas), max(notas))      # 9 18
print(sum(notas) / len(notas))     # 14.25  (promedio)
print(16 in notas)                 # True   (¿está el 16?)
print(20 not in notas)             # True
```

Cuidado: `sum(lista) / len(lista)` con una lista **vacía** da `ZeroDivisionError`. Compruébalo antes con `if lista:`.

### Recorrer una lista

```python
for nota in notas:
    print(nota)
```

Si además necesitas la **posición**, usa `enumerate`, que te da el índice y el valor a la vez:

```python
for i, nombre in enumerate(["Ana", "Luis", "Eva"]):
    print(i, nombre)
```

```
0 Ana
1 Luis
2 Eva
```

(`enumerate(lista, start=1)` empieza a contar en 1, útil para mostrar listas numeradas a personas.)

Para recorrer **dos listas a la vez**, emparejando elementos, usa `zip`:

```python
productos = ["café", "pan"]
precios = [4.5, 1.2]
for producto, precio in zip(productos, precios):
    print(f"{producto}: {precio}")
```

### Buscar el "mejor" elemento recorriendo la lista

Hay problemas en los que no basta con `max()`: quieres el elemento que gana según un criterio propio, o simplemente entender cómo
funciona `max()` por dentro. El patrón consiste en guardar un **candidato** y compararlo con cada elemento. Por ejemplo, la palabra
más larga:

```python
palabras = ["sol", "montaña", "mar", "río"]
mas_larga = palabras[0]                 # empezamos suponiendo que la primera es la mejor
for palabra in palabras:
    if len(palabra) > len(mas_larga):   # ¿esta gana a la que tenía?
        mas_larga = palabra             # entonces es la nueva candidata
print(mas_larga)                        # montaña
```

Por qué se empieza con `palabras[0]` y no con un valor inventado: con números, empezar en `0` falla si todos los números son negativos
(ninguno sería mayor que 0). Empezar con un elemento real de la lista siempre funciona... siempre que la lista no esté vacía, así que ese
caso hay que comprobarlo antes.

### Listas por comprensión

Una forma compacta de construir una lista a partir de otra. Estas dos versiones hacen lo mismo:

```python
precios = [10, 20, 30]

con_iva = []
for p in precios:
    con_iva.append(p * 1.16)

con_iva = [p * 1.16 for p in precios]      # versión por comprensión
```

Y con una condición, para filtrar:

```python
notas = [14, 8, 18, 9]
aprobadas = [n for n in notas if n >= 10]   # [14, 18]
```

Léelo así: "dame `n` para cada `n` en `notas` si `n >= 10`". Úsalas cuando la transformación sea sencilla; si necesitas varias
líneas de lógica, el `for` normal se lee mejor.

### Listas dentro de listas

Una lista puede contener otras listas, por ejemplo una tabla:

```python
tabla = [
    [1, 2, 3],
    [4, 5, 6],
]
print(tabla[1])       # [4, 5, 6]   la segunda fila
print(tabla[1][2])    # 6           fila 1, columna 2
```

### Comprueba que entendiste

**Pregunta:** con `letras = ["a", "b", "c", "d", "e"]`, ¿qué dan `letras[1:3]`, `letras[-3:]` y `letras[::-2]`?

**Respuesta:** `["b", "c"]`, `["c", "d", "e"]` y `["e", "c", "a"]`.

---

## 3. Copias y referencias: el error que confunde a todos

Esta sección explica uno de los errores más desconcertantes de Python. Léela despacio.

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)    # [1, 2, 3, 4]   ¡a también cambió!
```

`b = a` **no copia la lista**. Hace que `b` sea **otro nombre para la misma lista**. Imagina la lista como una caja y las variables como
etiquetas pegadas a ella: `b = a` pega una segunda etiqueta en la misma caja. Lo que hagas a través de una etiqueta se ve a través de la
otra.

Para tener una **copia independiente**:

```python
a = [1, 2, 3]
b = a.copy()     # o list(a), o a[:]
b.append(4)
print(a)         # [1, 2, 3]       intacta
print(b)         # [1, 2, 3, 4]
```

Esto mismo pasa al **pasar una lista a una función**: la función recibe la misma lista, no una copia. Si la función la modifica (con
`append`, `remove`, `pop`...), el cambio se ve fuera:

```python
def agregar_bono(salarios):
    salarios.append(100)

mis_salarios = [500, 600]
agregar_bono(mis_salarios)
print(mis_salarios)    # [500, 600, 100]
```

La recomendación profesional: **que tus funciones no modifiquen las listas que reciben**, salvo que ese sea justamente su propósito.
Construye una lista nueva y devuélvela; así nadie se lleva sorpresas.

¿Y con números y textos? No hay problema, porque son **inmutables**: no existe ninguna operación que los cambie "en su sitio".
`x = x + 1` crea un número nuevo y mueve la etiqueta.

---

## 4. Tuplas: grupos fijos de valores

Una **tupla** es como una lista que **no se puede modificar**. Se escribe con paréntesis:

```python
coordenada = (10.5, -66.9)
color_rgb = (255, 128, 0)
print(coordenada[0])     # 10.5
coordenada[0] = 3        # TypeError: 'tuple' object does not support item assignment
```

Se usan para agrupar valores que **van juntos y no deben cambiar**: una coordenada, una fecha (año, mes, día), un par (precio, cantidad).

### Empaquetar y desempaquetar

```python
punto = 3, 4            # empaquetar: Python crea la tupla (3, 4)
x, y = punto            # desempaquetar: x = 3, y = 4
print(x, y)             # 3 4
```

El número de variables a la izquierda tiene que coincidir con el número de elementos, o aparece `ValueError: too many values to
unpack`.

Un truco que solo es posible gracias a esto: **intercambiar** dos variables en una línea.

```python
a, b = 1, 2
a, b = b, a
print(a, b)    # 2 1
```

Y esto es lo que pasa cuando una función hace `return suma, promedio`: devuelve una tupla, y `s, p = estadisticas(4, 8)` la
desempaqueta.

Detalle: una tupla de un solo elemento necesita una coma final: `(5,)`. Sin la coma, `(5)` es simplemente el número 5 entre paréntesis.

---

## 5. Diccionarios: buscar por clave

Una lista te da un valor **por posición** (`lista[2]`). Un **diccionario** te da un valor **por nombre**. Guarda pares
**clave → valor**:

```python
persona = {
    "nombre": "Ana",
    "edad": 30,
    "ciudad": "Maracaibo",
}
print(persona["nombre"])    # Ana
print(persona["edad"])      # 30
```

- Se escribe con llaves `{}`, y cada par es `clave: valor`, separados por comas.
- Las claves suelen ser textos (también pueden ser números o tuplas), y **no se repiten**.
- Los valores pueden ser de cualquier tipo, incluidas listas u otros diccionarios.

**Por qué los diccionarios son tan importantes:** un usuario en una base de datos, la respuesta JSON de una API, el mensaje que envías a
un modelo de IA, la configuración de un programa... todo eso son diccionarios. Si dominas los diccionarios, dominas la mitad del trabajo
con datos.

### Leer valores sin errores

```python
persona["telefono"]
```

```
KeyError: 'telefono'
```

Pedir una clave que no existe con corchetes da `KeyError`. Hay dos formas seguras:

```python
print("telefono" in persona)                  # False   (in pregunta por las CLAVES)
print(persona.get("telefono"))                # None    (no da error)
print(persona.get("telefono", "sin dato"))    # sin dato (valor por defecto)
```

Usa `[]` cuando la clave **tiene** que existir (si no está, es un error real y quieres enterarte). Usa `.get()` cuando puede faltar.

### Añadir, cambiar y borrar

```python
persona["email"] = "ana@correo.com"   # la clave no existía: se añade
persona["edad"] = 31                  # la clave existía: se reemplaza el valor
del persona["ciudad"]                 # borra el par
quitado = persona.pop("email")        # borra y devuelve el valor
print(persona)                        # {'nombre': 'Ana', 'edad': 31}
```

### Recorrer un diccionario

```python
stock = {"café": 12, "pan": 30, "leche": 0}

for producto in stock:                     # recorre las CLAVES
    print(producto)

for cantidad in stock.values():            # recorre los VALORES
    print(cantidad)

for producto, cantidad in stock.items():   # recorre los PARES: lo más útil
    print(f"{producto}: {cantidad}")
```

`.items()` devuelve pares `(clave, valor)`, que el `for` desempaqueta en dos variables.

### Valores compuestos y desempaquetado anidado

Muchas veces el valor es a su vez una tupla o una lista. Puedes desempaquetarlo directamente en el `for`:

```python
# alumno -> (nota del primer parcial, nota del segundo parcial)
notas = {"Ana": (15, 18), "Luis": (10, 12)}

for alumno, (p1, p2) in notas.items():
    promedio = (p1 + p2) / 2
    print(f"{alumno}: {promedio}")
```

```
Ana: 16.5
Luis: 11.0
```

Los paréntesis en `(p1, p2)` le dicen a Python: "el valor es un par; separa sus dos partes".

### Patrón: contar con un diccionario

Es uno de los patrones más usados en programación. Para contar cuántas veces aparece cada cosa:

```python
votos = ["sí", "no", "sí", "sí", "abstención"]
conteo = {}
for voto in votos:
    conteo[voto] = conteo.get(voto, 0) + 1
print(conteo)    # {'sí': 3, 'no': 1, 'abstención': 1}
```

Cómo funciona `conteo.get(voto, 0) + 1`: si el voto ya está en el diccionario, toma su cuenta actual y le suma 1; si no está, toma 0 y le
suma 1. Así no hace falta un `if` para el primer caso.

### Patrón: agrupar

Parecido, pero guardando listas:

```python
ventas = [("Caracas", 120), ("Valencia", 80), ("Caracas", 50)]
por_ciudad = {}
for ciudad, monto in ventas:
    if ciudad not in por_ciudad:
        por_ciudad[ciudad] = []
    por_ciudad[ciudad].append(monto)
print(por_ciudad)    # {'Caracas': [120, 50], 'Valencia': [80]}
```

### Datos anidados: así se ve un JSON

```python
pedido = {
    "id": 1042,
    "cliente": {"nombre": "Eva", "email": "eva@correo.com"},
    "productos": [
        {"nombre": "café", "precio": 4.5, "cantidad": 2},
        {"nombre": "pan", "precio": 1.2, "cantidad": 5},
    ],
}
print(pedido["cliente"]["nombre"])            # Eva
print(pedido["productos"][1]["nombre"])       # pan
print(len(pedido["productos"]))               # 2
```

Para leer un dato anidado, **ve de fuera hacia dentro**, un paso cada vez: `pedido["productos"]` es una lista; `[1]` es su segundo
elemento, que es un diccionario; `["nombre"]` es un valor de ese diccionario. Cuando trabajes con APIs y LLMs leerás estructuras así
constantemente.

### Comprueba que entendiste

**Pregunta:** con el `pedido` de arriba, ¿cómo obtienes el precio del café? ¿Y qué devuelve `pedido.get("descuento", 0)`?

**Respuesta:** `pedido["productos"][0]["precio"]` (vale `4.5`). `pedido.get("descuento", 0)` devuelve `0`, porque la clave no existe.

---

## 6. Conjuntos (set): valores únicos

Un **conjunto** guarda valores **sin repetir** y **sin orden**:

```python
colores = {"rojo", "verde", "rojo", "azul"}
print(colores)          # {'rojo', 'verde', 'azul'}  (el orden puede variar)
print(len(colores))     # 3
vacio = set()           # ojo: {} crea un diccionario vacío, no un conjunto
```

### Para qué sirven

1. **Quitar duplicados** de una lista:

```python
ciudades = ["Caracas", "Mérida", "Caracas", "Coro"]
unicas = set(ciudades)            # {'Caracas', 'Mérida', 'Coro'}
print(len(unicas))                # 3 ciudades distintas
```

Atención: al pasar por un conjunto **se pierde el orden original**. Si el orden te importa, necesitas otra estrategia (combinar una
lista resultado con un conjunto que recuerde lo que ya viste es la idea; la práctica te pedirá construirla).

2. **Preguntar si algo está, muy rápido.** `x in conjunto` es casi instantáneo aunque el conjunto tenga millones de elementos, mientras
que `x in lista` revisa la lista elemento por elemento.

```python
vistos = set()
vistos.add("ana@correo.com")      # añadir un elemento
print("ana@correo.com" in vistos)  # True
print("luis@correo.com" in vistos) # False
```

3. **Operaciones entre grupos:**

```python
curso_python = {"Ana", "Luis", "Eva"}
curso_sql = {"Luis", "Eva", "Mar"}
print(curso_python & curso_sql)    # {'Luis', 'Eva'}             en los dos (intersección)
print(curso_python | curso_sql)    # {'Ana', 'Luis', 'Eva', 'Mar'} en alguno (unión)
print(curso_python - curso_sql)    # {'Ana'}                     solo en Python (diferencia)
```

---

## 7. ¿Qué estructura uso?

| Necesito... | Estructura | Ejemplo |
|---|---|---|
| Una secuencia ordenada que puede cambiar | lista `[]` | Mensajes de un chat, filas leídas de un archivo |
| Valores fijos que van juntos | tupla `()` | Coordenada, (precio, cantidad) |
| Buscar un valor por su nombre o identificador | diccionario `{}` | Usuario por email, configuración, un JSON |
| Valores únicos o comprobar pertenencia rápido | conjunto `set()` | Emails ya procesados, etiquetas distintas |

Y muchas veces se combinan: **una lista de diccionarios** es la forma más común de representar una tabla (cada diccionario es una
fila); **un diccionario de listas** sirve para agrupar.

---

## 8. Errores típicos de este capítulo

| Síntoma | Causa probable | Solución |
|---|---|---|
| La función devuelve `None` | Falta `return` (o usaste `print`) | Devuelve el resultado con `return` |
| `TypeError: f() missing 1 required positional argument` | Llamaste a la función con menos argumentos de los necesarios | Revisa los parámetros obligatorios |
| `IndexError: list index out of range` | Índice mayor o igual que `len(lista)`, o lista vacía | El último índice es `len - 1`; comprueba si está vacía |
| `KeyError: 'x'` | La clave no existe en el diccionario | Usa `in` o `.get()` |
| Tu lista se volvió `None` | Hiciste `lista = lista.sort()` | Usa `lista.sort()` solo, o `sorted(lista)` |
| Una lista "cambia sola" | Dos variables apuntan a la misma lista | Copia con `.copy()` |
| `ValueError: too many values to unpack` | El número de variables no coincide con el de elementos | Ajusta el desempaquetado |
| Un bucle se salta elementos | Modificaste la lista mientras la recorrías | Construye una lista nueva |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Funciones | Reutilizar lógica; parámetros con valor por defecto (`tasa=0.16`) van al final; argumentos por nombre |
| `return` | Puede devolver varios valores (una tupla); las variables internas no existen fuera |
| Listas | Índices desde 0, `[-1]` el último; slicing `[inicio:fin:paso]` sin incluir el fin; `[::-1]` invierte |
| Métodos de lista | `append`, `insert`, `remove`, `pop`, `sort`; los que modifican devuelven `None` |
| Funciones útiles | `len`, `sum`, `min`, `max`, `sorted`, `in`, `enumerate`, `zip` |
| Copias | `b = a` no copia; usa `a.copy()` |
| Tuplas | Inmutables; desempaquetar `x, y = punto` |
| Diccionarios | `d[clave]` (error si falta) frente a `d.get(clave, defecto)`; recorrer con `.items()` |
| Patrones | Contar con `d.get(k, 0) + 1`; agrupar en listas; buscar el mejor guardando un candidato |
| Conjuntos | Sin repetidos ni orden; `in` muy rápido; `&`, `|`, `-` |

## Autoevaluación final

1. ¿Qué devuelve una función que termina con `print(x)` en lugar de `return x`?
2. ¿Por qué `def f(a=1, b):` da error?
3. ¿Qué devuelve `[5, 6, 7, 8][1:3]`?
4. Tienes `a = [1, 2]` y haces `b = a` y luego `b.append(3)`. ¿Qué vale `a`?
5. ¿Qué diferencia hay entre `lista.sort()` y `sorted(lista)`?
6. ¿Qué hace `d.get("x", 0)` si `"x"` no está en `d`?
7. ¿Qué tres cosas da cada vuelta de `for k, v in d.items()`? (pista: es una pregunta trampa)
8. ¿Para qué usarías un conjunto en lugar de una lista?

**Respuestas:** 1) `None`. 2) Los parámetros con valor por defecto deben ir después de los obligatorios. 3) `[6, 7]`. 4) `[1, 2, 3]`,
porque `a` y `b` son la misma lista. 5) `sort()` ordena la lista original y devuelve `None`; `sorted()` devuelve una lista nueva
ordenada sin tocar la original. 6) Devuelve `0` sin dar error. 7) Son dos, no tres: la clave (`k`) y el valor (`v`). 8) Para quitar
duplicados o comprobar muy rápido si un valor ya está.

Si respondiste bien al menos 6 de 8, pasa a la práctica. Los ejercicios combinan estas piezas: funciones con valor por defecto, slicing,
recorrer listas guardando un candidato, recorrer diccionarios con `.items()` y conjuntos para recordar lo que ya viste.
