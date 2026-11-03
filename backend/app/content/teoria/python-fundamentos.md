# Fundamentos de Python desde cero

Este capítulo es la base de todo lo demás: pandas, APIs, chatbots y agentes de IA se escriben con estas mismas piezas. Si alguna te
resulta confusa, es normal; casi todo el mundo se atasca en los mismos puntos, y aquí los vamos a ver uno por uno, despacio y con muchos
ejemplos.

**Cómo estudiar este capítulo:**

1. Lee una sección entera antes de pasar a la siguiente.
2. Copia **a mano** cada ejemplo en cualquier ejercicio de la pestaña *Práctica* (el editor tiene el botón **Ejecutar**, que no corrige,
   solo ejecuta) y cámbiale un valor.
3. **Antes de ejecutar, predice** qué va a salir. Si aciertas, entendiste; si no, ahí está lo que tienes que repasar.
4. Al final de cada sección hay preguntas de comprobación con su respuesta. Contéstalas sin mirar.

---

## 1. Qué es un programa y cómo lo lee Python

Un programa es una lista de **instrucciones** que el ordenador ejecuta **en orden, de arriba abajo, una línea tras otra**. Python no
"entiende" lo que quieres hacer: hace exactamente lo que escribiste, ni más ni menos. Por eso los detalles (un paréntesis, dos puntos,
un espacio) importan tanto.

La primera instrucción que todo el mundo aprende es `print`, que **muestra algo en pantalla**:

```python
print("Hola")
print("Estoy aprendiendo Python")
print(2 + 3)
```

Salida:

```
Hola
Estoy aprendiendo Python
5
```

Fíjate en tres cosas:

- Lo que va entre comillas (`"Hola"`) es **texto** y se muestra tal cual.
- `2 + 3` no lleva comillas: Python **calcula** el resultado y muestra `5`.
- Cada `print` escribe en una línea nueva.

### Comentarios

Todo lo que va después de `#` en una línea es un **comentario**: Python lo ignora. Sirve para explicar el código a las personas
(incluido tu yo del futuro).

```python
# Esto es un comentario: Python no lo ejecuta
print("Esto sí se ejecuta")   # y esto también es un comentario
```

### Comprueba que entendiste

**Pregunta:** ¿qué muestra `print("2 + 3")`? ¿Y `print(2 + 3)`?

**Respuesta:** el primero muestra el texto `2 + 3` tal cual, porque está entre comillas. El segundo calcula la suma y muestra `5`.

---

## 2. Variables: nombres que guardan valores

Una **variable** es un **nombre** que apunta a un valor guardado en la memoria. Se crea con el signo `=`:

```python
edad = 30
nombre = "Ana"
print(nombre)
print(edad)
```

Salida:

```
Ana
30
```

**Lo más importante de esta sección:** en Python, `=` **no significa "es igual a"**. Significa **"calcula lo que hay a la derecha
y guárdalo en el nombre de la izquierda"**. Se lee de derecha a izquierda.

Por eso esto, que en matemáticas sería absurdo, en Python es perfectamente normal:

```python
edad = 30
edad = edad + 1
print(edad)    # 31
```

Paso a paso:

| Línea | Qué hace Python | Valor de `edad` después |
|---|---|---|
| `edad = 30` | Guarda 30 en `edad` | 30 |
| `edad = edad + 1` | Lee `edad` (30), calcula 30 + 1 = 31 y lo guarda en `edad` | 31 |
| `print(edad)` | Muestra el valor actual | 31 |

Una variable guarda **un solo valor a la vez**: al asignarle uno nuevo, el anterior se pierde.

### Reglas para los nombres

- Pueden tener letras, números y guion bajo `_`. **No pueden empezar por un número** (`2precio` no vale; `precio2` sí).
- **Distinguen mayúsculas:** `edad`, `Edad` y `EDAD` son tres variables distintas.
- No pueden tener espacios: en Python se usa `snake_case`, palabras en minúscula unidas por guion bajo: `precio_total`, `nombre_cliente`.
- No pueden ser palabras reservadas del lenguaje, como `if`, `for`, `def`, `return`, `True`, `class`.
- Usa **nombres que expliquen el contenido**. `precio_total` se entiende solo; `x` o `pt` obligan a adivinar.

### El error más común: usar una variable antes de crearla

```python
print(total)
total = 100
```

```
NameError: name 'total' is not defined
```

Python lee de arriba abajo: cuando llega a `print(total)`, todavía no existe ninguna variable `total`. El mismo error aparece si
escribes mal un nombre (`nombre` frente a `nomrbe`).

### Comprueba que entendiste

**Pregunta:** ¿cuánto vale `x` al final?

```python
x = 5
y = x
x = 10
```

**Respuesta:** `x` vale 10. (Y `y` vale 5: en la segunda línea `y` recibió el valor que tenía `x` en ese momento; cambiar `x` después no
cambia `y`.)

---

## 3. Tipos de datos

Cada valor tiene un **tipo**, que decide qué puedes hacer con él. Los cinco básicos:

| Tipo | Nombre | Ejemplos | Para qué |
|---|---|---|---|
| `int` | entero | `7`, `-3`, `0`, `2026` | Contar cosas, edades, cantidades |
| `float` | decimal | `3.14`, `0.5`, `-2.0` | Precios, medidas, porcentajes |
| `str` | texto (*string*) | `"hola"`, `'Ana'`, `""` | Nombres, mensajes, cualquier texto |
| `bool` | booleano | `True`, `False` | Respuestas sí/no |
| `NoneType` | nada | `None` | "No hay valor todavía" |

Detalles que causan errores:

- Los decimales se escriben con **punto**, no con coma: `3.5`, nunca `3,5`.
- El texto va entre comillas dobles o simples, da igual cuáles, pero tienen que cerrar con las mismas: `"hola"` o `'hola'`.
- `True` y `False` van con **mayúscula inicial** y sin comillas. `"True"` con comillas es un texto, no un booleano.
- `"5"` (texto) y `5` (número) **no son lo mismo**.

### Preguntar el tipo: `type()`

```python
print(type(7))        # <class 'int'>
print(type(7.0))      # <class 'float'>
print(type("7"))      # <class 'str'>
print(type(True))     # <class 'bool'>
```

### Convertir entre tipos

| Función | Convierte a | Ejemplo | Resultado |
|---|---|---|---|
| `int()` | entero | `int("42")` | `42` |
| `int()` | entero (corta los decimales) | `int(3.9)` | `3` |
| `float()` | decimal | `float("2.5")` | `2.5` |
| `str()` | texto | `str(30)` | `"30"` |
| `round()` | redondea | `round(3.14159, 2)` | `3.14` |

Si conviertes algo que no tiene sentido, Python se queja:

```python
int("hola")
```

```
ValueError: invalid literal for int() with base 10: 'hola'
```

**Por qué importa:** todo lo que llega "desde fuera" (lo que escribe un usuario, una línea de un archivo, un dato de una web) suele
llegar como **texto**, aunque parezca un número. Antes de hacer cuentas, hay que convertirlo.

```python
cantidad_texto = "3"
precio = 2.5
total = int(cantidad_texto) * precio
print(total)    # 7.5
```

### Una rareza de los decimales

```python
print(0.1 + 0.2)    # 0.30000000000000004
```

No es un error de Python: los ordenadores guardan los decimales en binario y algunos no se pueden representar de forma exacta. Para
mostrarlos, redondea (`round(0.1 + 0.2, 2)` da `0.3`). Para dinero en sistemas reales se usan otras herramientas (`Decimal`), que verás
más adelante.

### Comprueba que entendiste

**Pregunta:** ¿qué tipo tiene cada uno? `"3.5"`, `3.5`, `False`, `"False"`.

**Respuesta:** `str`, `float`, `bool`, `str`. Todo lo que va entre comillas es texto.

---

## 4. Operadores aritméticos

| Operador | Significado | Ejemplo | Resultado |
|---|---|---|---|
| `+` | suma | `7 + 2` | `9` |
| `-` | resta | `7 - 2` | `5` |
| `*` | multiplicación | `7 * 2` | `14` |
| `/` | división | `7 / 2` | `3.5` |
| `//` | división entera | `7 // 2` | `3` |
| `%` | resto (módulo) | `7 % 2` | `1` |
| `**` | potencia | `7 ** 2` | `49` |

### Orden de las operaciones

Igual que en matemáticas: primero `**`, después `*`, `/`, `//` y `%`, y por último `+` y `-`. Los paréntesis cambian el orden.

```python
print(2 + 3 * 4)      # 14  (primero 3 * 4)
print((2 + 3) * 4)    # 20  (primero el paréntesis)
```

Si dudas, **pon paréntesis**: hacen el código más claro y nunca sobran.

### División: `/`, `//` y `%`

- `/` siempre da un decimal, incluso si la división es exacta: `10 / 2` da `5.0`.
- `//` da solo la parte entera: cuántas veces cabe completo.
- `%` da **lo que sobra** de esa división entera.

Ejemplo práctico: convertir 135 minutos a horas y minutos.

```python
minutos = 135
horas = minutos // 60      # 2   (60 cabe 2 veces en 135)
resto = minutos % 60       # 15  (sobran 15 minutos)
print(horas, "h y", resto, "min")    # 2 h y 15 min
```

El operador `%` es más útil de lo que parece:

- `n % 2` vale `0` si `n` es par y `1` si es impar.
- `n % 10` da la última cifra de un número: `347 % 10` es `7`.
- `a % b == 0` significa "a es múltiplo de b" (la división es exacta, no sobra nada): `12 % 4 == 0` es `True`.

### Operadores de asignación abreviados

Como "actualizar una variable con su propio valor" es tan frecuente, existe una forma corta:

| Forma larga | Forma corta |
|---|---|
| `total = total + 5` | `total += 5` |
| `vidas = vidas - 1` | `vidas -= 1` |
| `precio = precio * 2` | `precio *= 2` |

### Dividir entre cero

```python
print(10 / 0)
```

```
ZeroDivisionError: division by zero
```

Cuando el divisor puede ser cero (por ejemplo, un promedio de una lista vacía), compruébalo antes con un `if` (lo verás en la sección 7).

### Comprueba que entendiste

**Pregunta:** ¿cuánto valen `17 // 5` y `17 % 5`?

**Respuesta:** `17 // 5` es `3` (el 5 cabe 3 veces en 17) y `17 % 5` es `2` (3 × 5 = 15, sobran 2).

---

## 5. Comparaciones y lógica

Las comparaciones **hacen una pregunta** y responden con `True` o `False`:

| Operador | Pregunta | Ejemplo | Resultado |
|---|---|---|---|
| `==` | ¿son iguales? | `5 == 5` | `True` |
| `!=` | ¿son distintos? | `5 != 3` | `True` |
| `<` | ¿menor que? | `3 < 5` | `True` |
| `>` | ¿mayor que? | `3 > 5` | `False` |
| `<=` | ¿menor o igual? | `5 <= 5` | `True` |
| `>=` | ¿mayor o igual? | `4 >= 5` | `False` |

**La confusión número uno de todo principiante:**

- `=` **guarda** un valor: `x = 5` significa "guarda 5 en x".
- `==` **pregunta**: `x == 5` significa "¿x vale 5?" y responde `True` o `False`.

También se pueden comparar textos: `"ana" == "ana"` es `True`, pero `"ana" == "Ana"` es `False`, porque las mayúsculas cuentan.

### Combinar condiciones: `and`, `or`, `not`

- `and`: es `True` solo si **las dos** partes son verdaderas.
- `or`: es `True` si **al menos una** es verdadera.
- `not`: invierte (`not True` es `False`).

| A | B | `A and B` | `A or B` |
|---|---|---|---|
| True | True | True | True |
| True | False | False | True |
| False | True | False | True |
| False | False | False | False |

```python
edad = 25
tiene_entrada = True
print(edad >= 18 and tiene_entrada)    # True: las dos se cumplen
print(edad < 18 or tiene_entrada)      # True: basta con una
print(not tiene_entrada)               # False
```

Python permite encadenar comparaciones como en matemáticas: `0 <= nota <= 20` significa "nota está entre 0 y 20".

### Verdadero y falso "por su valor"

En un `if`, Python también acepta valores que no son booleanos. Se consideran **falsos**: `0`, `0.0`, el texto vacío `""`, la lista
vacía `[]`, el diccionario vacío `{}` y `None`. Todo lo demás se considera verdadero. Por eso verás `if not lista:` para preguntar
"¿la lista está vacía?". Lo usarás mucho a partir del siguiente capítulo.

### Comprueba que entendiste

**Pregunta:** si `x = 7`, ¿qué dan `x > 5 and x < 10`, `x > 5 and x > 10` y `x > 5 or x > 10`?

**Respuesta:** `True`, `False`, `True`.

---

## 6. Trabajar con texto

### Crear y unir textos

```python
nombre = "Ana"
apellido = "Pérez"
completo = nombre + " " + apellido     # unir con +
print(completo)                        # Ana Pérez
print("-" * 10)                        # ---------- (repetir)
```

`+` solo une texto con texto. Esto falla:

```python
edad = 30
print("Tengo " + edad + " años")
```

```
TypeError: can only concatenate str (not "int") to str
```

Hay dos soluciones: convertir el número (`"Tengo " + str(edad) + " años"`) o, mucho mejor, usar un **f-string**.

### f-strings: la forma cómoda de construir textos

Pon una `f` justo antes de las comillas y escribe las variables entre llaves `{}`:

```python
producto = "café"
precio = 4.5
cantidad = 3
print(f"Compraste {cantidad} de {producto} por {precio * cantidad} dólares")
```

```
Compraste 3 de café por 13.5 dólares
```

Dentro de las llaves puedes poner cualquier expresión (`{precio * cantidad}`). También puedes darle formato:

```python
total = 13.5
print(f"Total: {total:.2f}")     # Total: 13.50  (siempre 2 decimales)
porcentaje = 0.256
print(f"{porcentaje:.1%}")       # 25.6%
```

### Longitud, posiciones y trozos

Un texto es una **secuencia de caracteres**, y cada uno tiene una **posición** (índice). **Se empieza a contar en 0.**

```
 texto:    P   y   t   h   o   n
 índice:   0   1   2   3   4   5
 negativo: -6  -5  -4  -3  -2  -1
```

```python
lenguaje = "Python"
print(len(lenguaje))      # 6   cantidad de caracteres
print(lenguaje[0])        # P   el primero
print(lenguaje[5])        # n   el último (posición len - 1)
print(lenguaje[-1])       # n   el último, contando desde el final
print(lenguaje[0:3])      # Pyt trozo: de la posición 0 a la 3, SIN incluir la 3
print(lenguaje[2:])       # thon desde la 2 hasta el final
```

Pedir una posición que no existe da error: `lenguaje[10]` produce `IndexError: string index out of range`.

### Métodos útiles

Un **método** es una función que pertenece a un valor y se llama con un punto: `texto.metodo()`.

| Método | Qué hace | Ejemplo | Resultado |
|---|---|---|---|
| `.upper()` | todo en mayúsculas | `"hola".upper()` | `"HOLA"` |
| `.lower()` | todo en minúsculas | `"HoLa".lower()` | `"hola"` |
| `.strip()` | quita espacios de los extremos | `"  hola  ".strip()` | `"hola"` |
| `.replace(a, b)` | cambia a por b | `"1,5".replace(",", ".")` | `"1.5"` |
| `.split(sep)` | corta en una lista | `"a;b;c".split(";")` | `["a", "b", "c"]` |
| `.startswith(x)` | ¿empieza por x? | `"Python".startswith("Py")` | `True` |
| `.count(x)` | cuántas veces aparece x | `"banana".count("a")` | `3` |

Y el operador `in` pregunta si un texto contiene a otro: `"th" in "Python"` es `True`; `"z" in "Python"` es `False`.

**Los textos no cambian (son inmutables).** Los métodos no modifican el texto original: **devuelven uno nuevo**. Si quieres conservar
el resultado, guárdalo:

```python
saludo = "hola"
saludo.upper()            # crea "HOLA", pero no se guarda en ningún sitio
print(saludo)             # hola
saludo = saludo.upper()   # ahora sí
print(saludo)             # HOLA
```

Un truco muy usado: para comparar textos sin que importen las mayúsculas, pasa los dos a minúsculas. `"SÍ".lower() == "sí"` es `True`.

### Comprueba que entendiste

**Pregunta:** si `ciudad = "Caracas"`, ¿qué dan `ciudad[1]`, `ciudad[-2]`, `ciudad[0:4]` y `len(ciudad)`?

**Respuesta:** `"a"`, `"a"`, `"Cara"` y `7`.

---

## 7. Tomar decisiones: `if`, `elif`, `else`

Hasta ahora el programa ejecutaba todas las líneas. Con `if` decide **qué líneas ejecutar según una condición**.

```python
temperatura = 31

if temperatura > 30:
    print("Hace calor")
    print("Bebe agua")
print("Fin del programa")
```

Salida:

```
Hace calor
Bebe agua
Fin del programa
```

### La sintaxis, pieza por pieza

1. `if`, luego la condición, y al final **dos puntos `:`**. Olvidarlos es un `SyntaxError`.
2. Las líneas que dependen de la condición van **indentadas** (desplazadas a la derecha) **4 espacios**. Ese grupo se llama **bloque**.
3. Cuando vuelves al margen izquierdo, el bloque terminó: `print("Fin del programa")` se ejecuta siempre.

**En Python la indentación no es decoración: es la sintaxis.** Es como el lenguaje sabe qué líneas están "dentro" del `if`. Si la
indentación es incoherente, aparece `IndentationError`.

### `else`: qué hacer si no se cumple

```python
saldo = 40
precio = 55

if saldo >= precio:
    print("Compra aprobada")
else:
    print("Saldo insuficiente")
```

### `elif`: varias opciones en orden

```python
temperatura = 22

if temperatura >= 30:
    print("calor")
elif temperatura >= 20:
    print("templado")
elif temperatura >= 10:
    print("fresco")
else:
    print("frío")
```

Salida: `templado`.

**Regla clave:** Python comprueba las condiciones **de arriba abajo** y ejecuta **solo la primera que se cumpla**; las demás ni se
miran. Por eso **el orden importa**. Observa este error:

```python
temperatura = 35

if temperatura >= 10:
    print("fresco")       # se cumple primero (35 >= 10) y se queda aquí
elif temperatura >= 30:
    print("calor")        # nunca llega
```

Con 35 grados imprime `fresco`, porque la primera condición ya es verdadera. Cuando las condiciones se solapan, **pon primero la más
específica o la más exigente**.

### Condiciones combinadas e `if` anidados

```python
edad = 20
tiene_carnet = False

if edad >= 18 and tiene_carnet:
    print("Puede conducir")
elif edad >= 18:
    print("Tiene edad, pero le falta el carnet")
else:
    print("Todavía no tiene edad")
```

También se puede poner un `if` dentro de otro (cada nivel añade 4 espacios), pero si hay muchos niveles el código se vuelve difícil de
leer; normalmente se puede reescribir con `and` o con `elif`.

### Comprueba que entendiste

**Pregunta:** con `nota = 15`, ¿qué imprime este código?

```python
if nota >= 10:
    print("aprobado")
if nota >= 14:
    print("notable")
else:
    print("sin mención")
```

**Respuesta:** imprime `aprobado` y `notable`. Son **dos `if` independientes** (no hay `elif`), así que Python evalúa los dos.

---

## 8. Repetir con `for`

Un bucle `for` repite un bloque **una vez por cada elemento** de una secuencia.

```python
for fruta in ["manzana", "pera", "uva"]:
    print("Me gusta la", fruta)
```

```
Me gusta la manzana
Me gusta la pera
Me gusta la uva
```

En cada vuelta, la variable `fruta` toma el siguiente valor de la lista. El nombre lo eliges tú; usa uno que describa cada elemento.

También se puede recorrer un texto, letra por letra:

```python
for letra in "sol":
    print(letra)
```

```
s
o
l
```

### `range()`: repetir con números

`range` genera una secuencia de números. Es la fuente de errores más frecuente del principiante, así que vale la pena memorizarlo:

| Expresión | Números que produce | Regla |
|---|---|---|
| `range(5)` | 0, 1, 2, 3, 4 | Empieza en 0, termina **antes** del 5 |
| `range(2, 6)` | 2, 3, 4, 5 | Incluye el inicio, **no** el final |
| `range(0, 10, 3)` | 0, 3, 6, 9 | El tercer número es el salto |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 | Con salto negativo cuenta hacia atrás |

**El final nunca se incluye.** Si quieres llegar hasta un número `n` incluido, el final tiene que ser `n + 1`.

```python
for i in range(1, 4):
    print(i, "al cuadrado es", i ** 2)
```

```
1 al cuadrado es 1
2 al cuadrado es 4
3 al cuadrado es 9
```

### Patrón 1: el acumulador

Para calcular un total a lo largo de un bucle: crea una variable **antes** del bucle con un valor inicial y actualízala **dentro**.

```python
precios = [12.5, 8.0, 4.5]
total = 0                     # 1. valor inicial, ANTES del bucle
for precio in precios:
    total = total + precio    # 2. se actualiza en cada vuelta
print(total)                  # 3. se usa DESPUÉS del bucle -> 25.0
```

Así cambia `total` en cada vuelta:

| Vuelta | `precio` | `total` antes | `total` después |
|---|---|---|---|
| 1 | 12.5 | 0 | 12.5 |
| 2 | 8.0 | 12.5 | 20.5 |
| 3 | 4.5 | 20.5 | 25.0 |

Errores típicos con el acumulador:

- **Inicializarlo dentro del bucle:** se reinicia a 0 en cada vuelta y al final solo vale el último elemento.
- **Hacer el `print` (o el `return`) dentro del bucle:** muestra resultados parciales o termina en la primera vuelta. Fíjate en la
  indentación: lo que va después del bucle se escribe al nivel del `for`, no dentro.

El acumulador no tiene por qué sumar. Puede multiplicar (empezando en 1), construir un texto (empezando en `""`) o una lista
(empezando en `[]`).

### Patrón 2: el contador

Un caso especial del acumulador: sumar 1 cada vez que algo se cumple.

```python
temperaturas = [28, 33, 35, 29, 31]
dias_calurosos = 0
for t in temperaturas:
    if t > 30:
        dias_calurosos += 1
print(dias_calurosos)    # 3
```

Fíjate en que el `if` está **dentro** del `for` (8 espacios para lo que está dentro de los dos).

### Patrón 3: construir una lista resultado

```python
nombres = ["ana", "luis", "eva"]
en_mayusculas = []                       # lista vacía
for n in nombres:
    en_mayusculas.append(n.upper())      # .append añade al final
print(en_mayusculas)                     # ['ANA', 'LUIS', 'EVA']
```

### `break` y `continue`

- `break` **sale** del bucle inmediatamente.
- `continue` **salta** al siguiente elemento sin ejecutar el resto del bloque.

```python
for n in [4, 7, -1, 9]:
    if n < 0:
        print("Encontré un negativo, paro")
        break
    print("Procesando", n)
```

```
Procesando 4
Procesando 7
Encontré un negativo, paro
```

### Comprueba que entendiste

**Pregunta:** ¿qué imprime este código y por qué no da 6?

```python
for n in [1, 2, 3]:
    total = 0
    total = total + n
print(total)
```

**Respuesta:** imprime `3`. `total = 0` está **dentro** del bucle, así que se reinicia en cada vuelta y al final solo queda el último
número. Hay que moverlo antes del `for`.

---

## 9. Repetir con `while`

`while` repite un bloque **mientras** una condición sea verdadera. Se usa cuando no sabes de antemano cuántas vueltas habrá.

```python
ahorro = 0
semana = 0
while ahorro < 100:
    ahorro += 30
    semana += 1
print(f"Llegas a {ahorro} en {semana} semanas")    # Llegas a 120 en 4 semanas
```

Cómo funciona: antes de cada vuelta Python comprueba la condición; si es verdadera, ejecuta el bloque y vuelve a comprobar; si es falsa,
sigue con lo que hay después.

**Peligro: el bucle infinito.** Si nada dentro del bloque hace que la condición llegue a ser falsa, el programa no termina nunca:

```python
contador = 0
while contador < 5:
    print(contador)
    # falta contador += 1: imprime 0 para siempre
```

Si te pasa al ejecutar en la plataforma, recarga la página.

**¿`for` o `while`?** Si recorres una colección o sabes cuántas vueltas hay, usa `for` (es más difícil equivocarse). Usa `while` cuando
la repetición depende de algo que cambia durante el proceso ("hasta que el usuario acierte", "mientras queden datos").

---

## 10. Funciones: `def` y `return`

Casi todos los ejercicios de la plataforma te piden **escribir una función**. Aquí tienes lo esencial; el siguiente capítulo profundiza.

Una **función** es un bloque de código con nombre que **recibe datos, hace algo con ellos y devuelve un resultado**. Ya usaste varias:
`print()`, `len()`, `type()`. Ahora vas a crear las tuyas.

```python
def precio_final(precio, descuento):
    resultado = precio - precio * descuento
    return resultado
```

Pieza por pieza:

- `def` indica que vas a **definir** una función.
- `precio_final` es su nombre (mismas reglas que las variables).
- Entre paréntesis van los **parámetros**: los nombres con los que la función llamará a los datos que reciba.
- Dos puntos `:` y el cuerpo **indentado**, igual que en un `if`.
- `return` **entrega el resultado** a quien llamó a la función, y **termina** la función en ese momento.

Definir una función **no la ejecuta**: solo la guarda. Se ejecuta cuando la **llamas**:

```python
total = precio_final(100, 0.2)     # llama a la función con precio=100 y descuento=0.2
print(total)                       # 80.0
print(precio_final(50, 0.1))       # 45.0
```

Cuando llamas a `precio_final(100, 0.2)`, Python hace `precio = 100` y `descuento = 0.2`, ejecuta el cuerpo y el `return` devuelve
`80.0`, que se guarda en `total`.

### `return` frente a `print`: la diferencia que más importa

- `print` **muestra** un valor en pantalla para que lo lea una persona. El valor no se puede usar después.
- `return` **devuelve** el valor al código que llamó a la función, para seguir usándolo.

```python
def doble_con_print(n):
    print(n * 2)

def doble_con_return(n):
    return n * 2

a = doble_con_print(5)      # muestra 10 en pantalla...
print(a)                    # ...pero a vale None

b = doble_con_return(5)     # no muestra nada...
print(b + 1)                # ...pero b vale 10 y se puede usar: 11
```

Una función **sin `return` devuelve `None`**. Los ejercicios de la plataforma comprueban lo que **devuelve** tu función, así que si
usas `print` en lugar de `return`, la prueba fallará aunque en pantalla veas el número correcto.

### `return` dentro de un `if`

Una función puede tener varios `return`; se ejecuta solo el primero al que llegue:

```python
def signo(n):
    if n > 0:
        return "positivo"
    elif n < 0:
        return "negativo"
    else:
        return "cero"

print(signo(-4))    # negativo
```

### Cómo probar tu función mientras la escribes

Debajo de la función, llámala con valores cuyo resultado conoces y muestra lo que devuelve:

```python
def promedio(a, b):
    return (a + b) / 2

print(promedio(4, 6))     # espero 5.0
print(promedio(0, 0))     # espero 0.0
```

Si lo que sale no coincide con lo que esperabas, ya sabes dónde buscar. Esta costumbre de **probar con ejemplos pequeños** es la
habilidad más valiosa de este capítulo.

### Comprueba que entendiste

**Pregunta:** ¿qué valor tiene `x`?

```python
def mitad(n):
    n / 2

x = mitad(10)
```

**Respuesta:** `None`. La función calcula `n / 2` pero no lo devuelve: falta `return`.

---

## 11. Leer los errores sin miedo

Los errores no son un fracaso: son **la forma que tiene Python de decirte qué pasa**. Un programador con experiencia no comete menos
errores; los **lee** mejor.

### Anatomía de un mensaje de error (*traceback*)

```
Traceback (most recent call last):
  File "main.py", line 4, in <module>
    total = precio * cantidad
NameError: name 'cantidad' is not defined
```

Se lee **de abajo hacia arriba**:

1. **Última línea:** el tipo de error (`NameError`) y la explicación (`'cantidad' no está definida`).
2. **Las líneas de arriba:** dónde ocurrió: el archivo, la **línea 4** y el código de esa línea.

### Los errores que verás más a menudo

| Error | Qué significa | Ejemplo que lo causa | Cómo arreglarlo |
|---|---|---|---|
| `SyntaxError` | Algo está mal escrito y Python no puede leerlo | `if x > 3` (faltan los `:`) o un paréntesis sin cerrar | Revisa la línea señalada y la anterior |
| `IndentationError` | La indentación no es coherente | Un bloque con 3 espacios y otro con 4 | Usa siempre 4 espacios por nivel |
| `NameError` | Usas un nombre que no existe | Una variable mal escrita o usada antes de crearla | Revisa la ortografía y el orden |
| `TypeError` | Operación entre tipos incompatibles | `"Edad: " + 30` | Convierte con `str()` o usa f-strings |
| `ValueError` | El tipo es correcto pero el valor no sirve | `int("hola")` | Comprueba el dato antes de convertir |
| `IndexError` | Posición que no existe | `"abc"[5]` | Recuerda que el último índice es `len - 1` |
| `ZeroDivisionError` | División entre cero | `total / 0` | Comprueba el divisor con un `if` |

Un detalle sobre `SyntaxError`: a veces la línea que señala es la **siguiente** a la que tiene el problema (por ejemplo, cuando no
cerraste un paréntesis en la línea anterior). Si la línea señalada parece correcta, mira la de arriba.

### Errores que no producen mensaje

Los más traicioneros son los **errores de lógica**: el programa funciona, pero el resultado es incorrecto. Por ejemplo, un `range` que
se queda corto, un acumulador dentro del bucle o un `elif` en el orden equivocado. Para encontrarlos:

1. Prueba con un ejemplo pequeño cuyo resultado sepas calcular a mano.
2. Añade `print` temporales para ver cómo cambian las variables: `print("vuelta", i, "total", total)`.
3. Compara lo que ves con lo que esperabas, línea a línea. La primera diferencia es el error.

---

## 12. Cómo enfrentarte a un ejercicio

Un método que funciona con cualquier ejercicio de esta plataforma (y en una entrevista):

1. **Lee el enunciado dos veces** y subraya qué recibe la función y qué tiene que **devolver** (tipo y forma: ¿un número, un texto,
   una lista?).
2. **Resuelve un ejemplo a mano**, en papel, sin código. Si no sabes hacerlo a mano, todavía no puedes programarlo.
3. **Piensa en los casos borde:** ¿y si la lista está vacía?, ¿y si el número es 0 o negativo?, ¿y si el texto tiene mayúsculas?
4. **Escribe el esqueleto:** la función, el valor inicial, el bucle o el `if`, el `return`.
5. **Pruébalo con Ejecutar** usando `print(mi_funcion(...))` con tu ejemplo del paso 2.
6. **Comprobar** solo cuando tus propias pruebas funcionen. Si falla, lee el mensaje de la prueba: suele decir qué caso no pasó.

Ejemplo del método (un problema distinto a los de la práctica): *"Escribe `cuantos_negativos(numeros)` que devuelva cuántos números
negativos hay en una lista."*

1. Recibe una lista de números; devuelve un **entero**.
2. A mano: en `[3, -1, -5, 2]` hay 2 negativos.
3. Casos borde: lista vacía → 0; el 0 no es negativo.
4. Es un **contador**: empieza en 0, recorre la lista, suma 1 si el número es menor que 0.

```python
def cuantos_negativos(numeros):
    cantidad = 0
    for n in numeros:
        if n < 0:
            cantidad += 1
    return cantidad

print(cuantos_negativos([3, -1, -5, 2]))    # espero 2
print(cuantos_negativos([]))                # espero 0
print(cuantos_negativos([0, 4]))            # espero 0
```

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Variables | `nombre = valor`; `=` guarda, se lee de derecha a izquierda |
| Tipos | `int`, `float`, `str`, `bool`, `None`; convertir con `int()`, `float()`, `str()` |
| Operadores | `//` división entera, `%` resto (par: `n % 2 == 0`; múltiplo: `a % b == 0`) |
| Comparaciones | `==` pregunta, `=` guarda; `and`, `or`, `not` |
| Texto | f-strings `f"Hola {nombre}"`; índices desde 0; `[-1]` es el último; los métodos devuelven texto nuevo |
| `if/elif/else` | Dos puntos, 4 espacios; solo se ejecuta la primera rama verdadera, el orden importa |
| `for` | Una vuelta por elemento; `range(a, b)` no incluye `b` |
| Patrones | Acumulador (valor inicial antes del bucle), contador, lista resultado |
| `while` | Repite mientras se cumpla; cuidado con el bucle infinito |
| Funciones | `def nombre(parámetros):` y `return`; sin `return` devuelve `None` |
| Errores | Se leen de abajo arriba: tipo de error y línea |

## Autoevaluación final

Responde sin mirar el capítulo y después comprueba.

1. ¿Qué diferencia hay entre `x = 3` y `x == 3`?
2. ¿Qué produce `range(3, 7)`?
3. ¿Cuánto vale `25 % 7`?
4. ¿Por qué falla `"Total: " + 10` y cómo se arregla?
5. En un `if/elif`, si se cumplen dos condiciones, ¿cuáles se ejecutan?
6. ¿Qué devuelve una función que no tiene `return`?
7. ¿Dónde se inicializa un acumulador y dónde se devuelve?
8. ¿Qué significa `IndentationError`?

**Respuestas:** 1) la primera guarda 3 en `x`; la segunda pregunta si `x` vale 3. 2) `3, 4, 5, 6`. 3) `4` (7 × 3 = 21, sobran 4).
4) No se puede unir texto con número: usa `"Total: " + str(10)` o `f"Total: {10}"`. 5) Solo la primera que se cumpla. 6) `None`.
7) Antes del bucle se inicializa; el `return` va después del bucle, al nivel del `for`. 8) Que los espacios al principio de las líneas
no son coherentes con los bloques.

Si respondiste bien al menos 6 de 8, pasa a la práctica. Si no, vuelve a las secciones de las preguntas que fallaste: es exactamente
lo que la práctica va a pedirte.
