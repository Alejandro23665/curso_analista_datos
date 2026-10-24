from ._helpers import py, quiz

TOPICS = [
    {
        "slug": "python-fundamentos",
        "phase": "python",
        "title": "Fundamentos de Python desde cero",
        "summary": "Variables, tipos, operadores, texto, condicionales y bucles, explicados paso a paso y con ejercicios muy cortos.",
        "hours": 8,
        "theory": r"""
# Fundamentos de Python desde cero

Si la sintaxis te resulta confusa, es normal: casi todo el mundo se atasca en los mismos cinco puntos. Aquí los vemos uno por uno,
despacio. **No avances hasta que puedas explicar cada ejemplo con tus palabras.**

> **Cómo estudiar este tema:** escribe cada ejemplo a mano (no copies y pegues), cámbiale un valor y predice qué va a pasar *antes* de ejecutarlo.
> Para ver el código ejecutarse línea por línea, pega ejemplos en **pythontutor.com**.

## 1. Variables: cajas con nombre

Una variable es un **nombre** que apunta a un valor. El signo `=` significa **"guarda esto en ese nombre"**, no "es igual a".

```python
edad = 30            # guarda el número 30 en el nombre "edad"
nombre = "Ana"       # guarda el texto "Ana"
edad = edad + 1      # lee edad (30), le suma 1 y guarda 31 de nuevo en "edad"
print(edad)          # muestra 31
```

Reglas de nombres: letras, números y guion bajo; no empiezan por número; distinguen mayúsculas (`edad` y `Edad` son distintas).
Usa nombres que expliquen el contenido: `precio_total` es mejor que `x`.

## 2. Tipos de datos básicos

| Tipo | Ejemplo | Para qué |
|---|---|---|
| `int` | `7`, `-3` | Números enteros |
| `float` | `3.14`, `0.5` | Números con decimales |
| `str` | `"hola"`, `'hola'` | Texto |
| `bool` | `True`, `False` | Verdadero o falso |
| `None` | `None` | "No hay valor" |

`type(valor)` te dice el tipo. Error muy común: `"5" + 3` falla porque `"5"` es texto. Conviértelo con `int("5") + 3`.

## 3. Operadores

```python
7 + 2     # 9      suma
7 - 2     # 5      resta
7 * 2     # 14     multiplicación
7 / 2     # 3.5    división (siempre da float)
7 // 2    # 3      división entera
7 % 2     # 1      resto (muy útil: n % 2 == 0 significa "n es par")
7 ** 2    # 49     potencia
```

Comparaciones (dan `True` o `False`): `==` igual, `!=` distinto, `<`, `>`, `<=`, `>=`.
Lógicos: `and` (ambas), `or` (alguna), `not` (invierte).

**La confusión nº 1:** `=` guarda un valor; `==` **pregunta** si dos valores son iguales.

## 4. Texto (str)

```python
nombre = "Ana"
saludo = "Hola, " + nombre + "!"          # unir textos
saludo = f"Hola, {nombre}! Tienes {30} años."   # f-string: lo más cómodo
len(nombre)            # 3      cantidad de caracteres
nombre.upper()         # "ANA"
"  hola ".strip()      # "hola" quita espacios de los lados
"a,b,c".split(",")     # ["a", "b", "c"]
nombre[0]              # "A"    primer carácter (se empieza a contar en 0)
```

## 5. Decisiones: if / elif / else

```python
edad = 16
if edad < 13:
    print("niño")
elif edad < 18:
    print("adolescente")
else:
    print("adulto")
```

Tres cosas que importan:

1. Después de la condición va **dos puntos** `:`.
2. Lo que está dentro se **indenta** (4 espacios). **La indentación ES la sintaxis en Python.**
3. Solo se ejecuta **la primera rama** cuya condición sea verdadera.

## 6. Repetir: for y while

```python
for numero in range(1, 4):     # range(1, 4) produce 1, 2, 3 (el final NO se incluye)
    print(numero)

total = 0
for n in [10, 20, 30]:         # recorre una lista elemento a elemento
    total = total + n          # patrón "acumulador"
print(total)                   # 60
```

El patrón **acumulador** (empezar en 0 y sumar en cada vuelta) lo usarás toda tu carrera. `while` repite *mientras* una condición sea verdadera;
cuida que la condición llegue a ser falsa o el programa no termina nunca.

## 7. Leer errores sin miedo

Un error (*traceback*) se lee **de abajo hacia arriba**: la última línea dice qué pasó y la anterior dónde.

| Mensaje | Significa |
|---|---|
| `SyntaxError` | Escribiste algo que Python no entiende (falta `:`, paréntesis sin cerrar...) |
| `IndentationError` | La indentación es incorrecta |
| `NameError` | Usaste un nombre que no existe (error de escritura o no lo definiste antes) |
| `TypeError` | Operación con tipos incompatibles (`"5" + 3`) |
| `ZeroDivisionError` | Dividiste entre cero |

## Cómo sabes que dominas este tema

- Explicas la diferencia entre `=` y `==`.
- Escribes un `if/elif/else` y un `for` con acumulador sin mirar ejemplos.
- Lees un error y dices qué línea y qué problema señala.

> **Consejo del coach:** si te atascas, no mires la solución enseguida. Escribe en *Apuntes* qué intentaste y qué error te dio; esa es la práctica que de verdad enseña.
""",
        "exercises": [
            py("fund-area", "Área de un rectángulo", "Python: fundamentos",
               "Escribe la función `area_rectangulo(base, altura)` que **devuelva** (con `return`) el área: base por altura.",
               starter="""
def area_rectangulo(base, altura):
    # tu código aquí (usa return)
    pass
""",
               solution="""
def area_rectangulo(base, altura):
    return base * altura
""",
               tests="""
assert area_rectangulo(3, 4) == 12, "3 x 4 debe dar 12"
assert area_rectangulo(2.5, 2) == 5.0
assert area_rectangulo(0, 9) == 0
""",
               hint="return base * altura. Recuerda: print muestra en pantalla, return entrega el valor."),
            py("fund-saludo", "Saludo con f-string", "Python: fundamentos",
               "Escribe `saludo(nombre, edad)` que devuelva exactamente el texto `'Hola, Ana. Tienes 30 años.'` (con el nombre y la edad que reciba). Usa un f-string.",
               starter="""
def saludo(nombre, edad):
    # tu código aquí
    pass
""",
               solution="""
def saludo(nombre, edad):
    return f"Hola, {nombre}. Tienes {edad} años."
""",
               tests="""
assert saludo("Ana", 30) == "Hola, Ana. Tienes 30 años.", "Obtuve %r" % (saludo("Ana", 30),)
assert saludo("Luis", 5) == "Hola, Luis. Tienes 5 años."
""",
               hint='f"Hola, {nombre}. Tienes {edad} años."'),
            py("fund-par", "¿Es par?", "Python: operadores",
               "Escribe `es_par(n)` que devuelva `True` si `n` es par y `False` si no. Pista: el operador `%` da el resto de una división.",
               starter="""
def es_par(n):
    # tu código aquí
    pass
""",
               solution="""
def es_par(n):
    return n % 2 == 0
""",
               tests="""
assert es_par(4) is True, "4 es par"
assert es_par(7) is False, "7 es impar"
assert es_par(0) is True, "0 es par"
assert es_par(-2) is True, "los negativos pares tambien cuentan"
""",
               hint="Un número es par si al dividirlo entre 2 el resto es 0: n % 2 == 0."),
            py("fund-edad", "Clasificar una edad", "Python: condicionales",
               "Escribe `clasificar_edad(edad)` que devuelva `'niño'` si `edad < 13`, `'adolescente'` si `edad < 18` y `'adulto'` en cualquier otro caso. Usa `if / elif / else`.",
               starter="""
def clasificar_edad(edad):
    # tu código aquí
    pass
""",
               solution="""
def clasificar_edad(edad):
    if edad < 13:
        return "niño"
    elif edad < 18:
        return "adolescente"
    else:
        return "adulto"
""",
               tests="""
assert clasificar_edad(5) == "niño"
assert clasificar_edad(12) == "niño", "12 todavia es niño"
assert clasificar_edad(13) == "adolescente", "13 ya es adolescente"
assert clasificar_edad(17) == "adolescente"
assert clasificar_edad(18) == "adulto"
assert clasificar_edad(60) == "adulto"
""",
               hint="No olvides los dos puntos después de cada condición y la indentación de 4 espacios."),
            py("fund-suma", "Sumar de 1 hasta n", "Python: bucles",
               "Escribe `suma_hasta(n)` que devuelva la suma de los números del 1 al `n` (ambos incluidos) usando un bucle `for` y un acumulador. Si `n` es 0, devuelve 0.",
               starter="""
def suma_hasta(n):
    total = 0
    # tu bucle aquí
    return total
""",
               solution="""
def suma_hasta(n):
    total = 0
    for numero in range(1, n + 1):
        total = total + numero
    return total
""",
               tests="""
assert suma_hasta(4) == 10, "1+2+3+4 = 10"
assert suma_hasta(1) == 1
assert suma_hasta(0) == 0, "Con n = 0 no hay nada que sumar"
assert suma_hasta(100) == 5050
""",
               hint="range(1, n + 1) incluye al n, porque el final de range no se incluye."),
            py("fund-vocales", "Contar vocales", "Python: bucles",
               "Escribe `contar_vocales(texto)` que cuente cuántas vocales (`a e i o u`, sin tildes, mayúsculas o minúsculas) tiene el texto. Recorre el texto con un `for`.",
               starter="""
def contar_vocales(texto):
    cantidad = 0
    # tu bucle aquí
    return cantidad
""",
               solution="""
def contar_vocales(texto):
    cantidad = 0
    for letra in texto.lower():
        if letra in "aeiou":
            cantidad = cantidad + 1
    return cantidad
""",
               tests="""
assert contar_vocales("hola") == 2
assert contar_vocales("PYTHON") == 1
assert contar_vocales("rhythm") == 0
assert contar_vocales("") == 0
assert contar_vocales("Murcielago") == 5
""",
               hint='Pasa el texto a minúsculas con .lower() y pregunta: if letra in "aeiou".'),
            py("fund-fizzbuzz", "FizzBuzz", "Python: bucles",
               "Escribe `fizzbuzz(n)` que devuelva una lista con los números del 1 al `n`, pero: múltiplos de 3 → `'Fizz'`, múltiplos de 5 → `'Buzz'`, "
               "múltiplos de 3 y de 5 → `'FizzBuzz'`. Es un clásico de entrevistas. Cuidado con el orden de las condiciones.",
               starter="""
def fizzbuzz(n):
    resultado = []
    # tu bucle aquí
    return resultado
""",
               solution="""
def fizzbuzz(n):
    resultado = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            resultado.append("FizzBuzz")
        elif i % 3 == 0:
            resultado.append("Fizz")
        elif i % 5 == 0:
            resultado.append("Buzz")
        else:
            resultado.append(i)
    return resultado
""",
               tests="""
assert fizzbuzz(5) == [1, 2, "Fizz", 4, "Buzz"], "Obtuve %r" % (fizzbuzz(5),)
esperado = [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz", 11, "Fizz", 13, 14, "FizzBuzz"]
assert fizzbuzz(15) == esperado, "Revisa el orden: primero hay que preguntar por el 15 (3 y 5 a la vez)"
assert fizzbuzz(0) == []
""",
               hint="Pregunta primero si es múltiplo de 15 (o de 3 y 5 a la vez); si no, el 3 se 'comería' al FizzBuzz."),
            quiz("fund-quiz-igual", "= o ==", "Python: fundamentos",
                 "¿Qué hace la línea `x = 5`?",
                 ["Pregunta si x vale 5", "Guarda el valor 5 en el nombre x", "Compara x con 5 y devuelve True", "Es un error de sintaxis"], 1,
                 "`=` es asignación: guarda un valor en una variable. Para preguntar si dos cosas son iguales se usa `==`."),
            quiz("fund-quiz-range", "Qué produce range", "Python: bucles",
                 "¿Qué números recorre `for i in range(1, 4):`?",
                 ["1, 2, 3, 4", "0, 1, 2, 3", "1, 2, 3", "2, 3, 4"], 2,
                 "`range(inicio, fin)` incluye el inicio pero **no** el fin. Por eso para llegar hasta n se escribe `range(1, n + 1)`."),
            quiz("fund-quiz-error", "Leer un error", "Python: fundamentos",
                 "Al ejecutar tu código ves `TypeError: can only concatenate str (not \"int\") to str`. ¿Qué pasó?",
                 ["Falta un paréntesis", "Intentaste sumar un texto con un número", "El archivo no existe", "Dividiste entre cero"], 1,
                 "Pasa con cosas como `\"Edad: \" + 30`. Convierte el número con `str(30)` o usa un f-string: `f\"Edad: {30}\"`."),
        ],
    },
    {
        "slug": "python-estructuras",
        "phase": "python",
        "title": "Funciones, listas y diccionarios paso a paso",
        "summary": "Cómo definir funciones y guardar datos en listas, tuplas, diccionarios y conjuntos, con ejemplos pequeños.",
        "hours": 8,
        "theory": r"""
# Funciones, listas y diccionarios paso a paso

Con esto ya puedes escribir casi cualquier programa pequeño. Es la base de todo lo que viene (pandas, ETL, APIs).

## 1. Funciones: un trozo de código con nombre

```python
def calcular_iva(precio, tasa=0.16):    # def + nombre + (parámetros) + dos puntos
    iva = precio * tasa                  # el cuerpo va indentado
    return precio + iva                  # return ENTREGA el resultado

total = calcular_iva(100)                # llama a la función -> 116.0
total = calcular_iva(100, 0.10)          # cambia la tasa -> 110.0
```

- **Parámetros** son los nombres que usa la función; **argumentos** son los valores que le pasas.
- `tasa=0.16` es un valor **por defecto**: si no lo das, se usa ese.
- **`print` muestra, `return` devuelve.** Si olvidas el `return`, la función devuelve `None`. Es el error más común de quien empieza.
- Las variables creadas dentro de una función no existen fuera de ella.

## 2. Listas: colecciones ordenadas y modificables

```python
frutas = ["manzana", "pera", "uva"]
frutas[0]            # "manzana"   (se empieza a contar en 0)
frutas[-1]           # "uva"       (el último)
frutas.append("kiwi")        # añade al final
len(frutas)                  # 4
"pera" in frutas             # True
frutas[1:3]                  # ["pera", "uva"]  slicing: del 1 al 3 (el 3 NO se incluye)
frutas[::-1]                 # la lista al revés
```

Recorrer: `for fruta in frutas:`. Con índice: `for i, fruta in enumerate(frutas):`.

**Cuidado con las copias:** `b = a` NO copia la lista, hace que `b` y `a` sean **la misma**. Para copiar usa `b = a.copy()` o `b = list(a)`.

## 3. Tuplas: listas que no cambian

`punto = (3, 4)`. No se pueden modificar. Se usan para agrupar valores fijos y para devolver varios valores de una función: `return minimo, maximo`.

## 4. Diccionarios: pares clave → valor

```python
persona = {"nombre": "Ana", "edad": 30}
persona["nombre"]               # "Ana"
persona["ciudad"] = "Caracas"   # añade o modifica
persona.get("pais", "sin dato") # lee sin error si no existe
"edad" in persona               # True (pregunta por las CLAVES)

for clave, valor in persona.items():
    print(clave, valor)
```

Leer una clave inexistente con `persona["pais"]` da `KeyError`; con `.get()` no.
Los diccionarios son **la** estructura de datos del análisis: un registro de una base de datos, un JSON de una API o una fila de un CSV se leen como diccionarios.

Patrón para **contar**:

```python
conteo = {}
for palabra in ["a", "b", "a"]:
    conteo[palabra] = conteo.get(palabra, 0) + 1     # {"a": 2, "b": 1}
```

## 5. Conjuntos (set): sin repetidos

```python
numeros = {1, 2, 2, 3}      # {1, 2, 3}
list(set([1, 1, 2]))        # quitar duplicados (pierde el orden)
```

## 6. ¿Cuál uso?

| Necesito... | Uso |
|---|---|
| Una secuencia ordenada que cambia | lista `[]` |
| Valores fijos agrupados | tupla `()` |
| Buscar por nombre/clave | diccionario `{}` |
| Valores únicos | conjunto `set()` |

## 7. Errores típicos

- **`IndexError`**: pediste una posición que no existe (`lista[10]` en una lista de 3).
- **`KeyError`**: clave inexistente en un diccionario.
- Modificar una lista mientras la recorres.
- Olvidar el `return`.

## Cómo sabes que dominas este tema

- Escribes una función con parámetros, un valor por defecto y `return`.
- Sabes sacar el primer y el último elemento y hacer slicing.
- Cuentas elementos con un diccionario sin buscar el patrón.
""",
        "exercises": [
            py("estr-iva", "Función con valor por defecto", "Python: funciones",
               "Escribe `precio_con_iva(precio, tasa=0.16)` que devuelva el precio más su IVA. Si no se indica la tasa, usa 0.16.",
               starter="""
def precio_con_iva(precio, tasa=0.16):
    # tu código aquí
    pass
""",
               solution="""
def precio_con_iva(precio, tasa=0.16):
    return precio + precio * tasa
""",
               tests="""
assert abs(precio_con_iva(100) - 116.0) < 1e-9, "100 con 16% de IVA = 116"
assert abs(precio_con_iva(100, 0.10) - 110.0) < 1e-9
assert precio_con_iva(0) == 0
""",
               hint="return precio + precio * tasa"),
            py("estr-extremos", "Primero y último", "Python: listas",
               "Escribe `primero_y_ultimo(lista)` que devuelva una tupla `(primero, ultimo)`. Si la lista está vacía, devuelve `(None, None)`.",
               starter="""
def primero_y_ultimo(lista):
    # tu código aquí
    pass
""",
               solution="""
def primero_y_ultimo(lista):
    if not lista:
        return None, None
    return lista[0], lista[-1]
""",
               tests="""
assert primero_y_ultimo([4, 5, 6]) == (4, 6)
assert primero_y_ultimo(["a"]) == ("a", "a"), "Con un solo elemento, el primero y el ultimo son el mismo"
assert primero_y_ultimo([]) == (None, None)
""",
               hint="lista[0] es el primero y lista[-1] el último. Comprueba primero si la lista está vacía."),
            py("estr-invertir", "Invertir un texto", "Python: listas",
               "Escribe `invertir(texto)` que devuelva el texto al revés. Hazlo con slicing (`[::-1]`).",
               starter="""
def invertir(texto):
    # tu código aquí
    pass
""",
               solution="""
def invertir(texto):
    return texto[::-1]
""",
               tests="""
assert invertir("hola") == "aloh"
assert invertir("") == ""
assert invertir("a") == "a"
""",
               hint="texto[::-1]"),
            py("estr-mayor", "El número más grande", "Python: listas",
               "Escribe `mayor(nums)` que devuelva el mayor número de la lista **sin usar `max`**: recorre la lista y ve guardando el mayor encontrado. Si la lista está vacía, devuelve `None`.",
               starter="""
def mayor(nums):
    # tu código aquí
    pass
""",
               solution="""
def mayor(nums):
    if not nums:
        return None
    el_mayor = nums[0]
    for n in nums:
        if n > el_mayor:
            el_mayor = n
    return el_mayor
""",
               tests="""
assert mayor([3, 9, 2]) == 9
assert mayor([-5, -1, -8]) == -1, "Con negativos tambien debe funcionar"
assert mayor([7]) == 7
assert mayor([]) is None
""",
               hint="Empieza con el primer elemento como 'el mayor hasta ahora' y compara con cada uno."),
            py("estr-carrito", "Total de un carrito", "Python: diccionarios",
               "Escribe `total_carrito(carrito)`. `carrito` es un diccionario `{producto: (precio, cantidad)}`. Devuelve la suma de `precio * cantidad` de todos los productos.",
               starter="""
def total_carrito(carrito):
    # tu código aquí
    pass
""",
               solution="""
def total_carrito(carrito):
    total = 0
    for producto, (precio, cantidad) in carrito.items():
        total = total + precio * cantidad
    return total
""",
               tests="""
carrito = {"pan": (2.0, 3), "leche": (1.5, 2)}
assert total_carrito(carrito) == 9.0, "2.0*3 + 1.5*2 = 9.0"
assert total_carrito({}) == 0, "Un carrito vacio cuesta 0"
""",
               hint="for producto, (precio, cantidad) in carrito.items(): ..."),
            py("estr-unicos", "Quitar repetidos manteniendo el orden", "Python: diccionarios",
               "Escribe `sin_repetidos(lista)` que devuelva una lista nueva con los elementos sin repetir, **en el orden en que aparecieron por primera vez**. "
               "Ayuda: usa un `set` de elementos ya vistos.",
               starter="""
def sin_repetidos(lista):
    # tu código aquí
    pass
""",
               solution="""
def sin_repetidos(lista):
    vistos = set()
    resultado = []
    for elemento in lista:
        if elemento not in vistos:
            vistos.add(elemento)
            resultado.append(elemento)
    return resultado
""",
               tests="""
assert sin_repetidos([3, 1, 3, 2, 1]) == [3, 1, 2], "Obtuve %r" % (sin_repetidos([3, 1, 3, 2, 1]),)
assert sin_repetidos([]) == []
assert sin_repetidos(["a", "a"]) == ["a"]
""",
               hint="Recorre la lista; si el elemento no está en 'vistos', agrégalo a 'vistos' y al resultado."),
            quiz("estr-quiz-copia", "Copiar una lista", "Python: listas",
                 "¿Qué imprime este código?\n\n```python\na = [1, 2]\nb = a\nb.append(3)\nprint(a)\n```",
                 ["[1, 2]", "[1, 2, 3]", "[3]", "Un error"], 1,
                 "`b = a` no crea una copia: `a` y `b` son dos nombres para **la misma lista**. Para copiar usa `a.copy()`."),
            quiz("estr-quiz-keyerror", "Clave que no existe", "Python: diccionarios",
                 "Tienes `d = {'a': 1}`. ¿Qué hace `d.get('b', 0)`?",
                 ["Da un KeyError", "Devuelve 0", "Devuelve None", "Añade la clave 'b'"], 1,
                 "`.get(clave, defecto)` devuelve el valor por defecto cuando la clave no existe, sin lanzar error. `d['b']` sí daría `KeyError`."),
            quiz("estr-quiz-return", "print o return", "Python: funciones",
                 "Una función termina con `print(resultado)` en lugar de `return resultado`. Al hacer `x = mi_funcion()`, ¿qué vale `x`?",
                 ["El resultado calculado", "None", "0", "Un texto vacío"], 1,
                 "`print` solo muestra el valor en pantalla. Sin `return`, la función devuelve `None`, y `x` no recibe nada útil."),
        ],
    },
]
