# Lógica I: seguir el código a mano

Mucha gente cree que "la lógica" es un talento: o lo tienes o no. No es así. La lógica de programación es, sobre todo, **una forma
ordenada de leer código**, y se entrena como cualquier otra habilidad. El primer paso, y el más importante, es aprender a **ejecutar un
programa en tu cabeza**: saber qué valor tiene cada variable en cada momento.

Si sientes que olvidas rápido lo que aprendes o que te pierdes cuando un programa tiene bucles y condiciones, casi siempre es por lo mismo:
estás leyendo el código como un texto ("aquí hay un bucle que suma") en vez de **seguirlo paso a paso**. Este capítulo te enseña la
herramienta que usan los buenos programadores para eso: la **tabla de variables**.

---

## 1. Por qué seguir código a mano

Seguir el código a mano (en inglés, *tracing*) sirve para tres cosas:

1. **Entender** qué hace un programa que no escribiste tú (o que generó una IA).
2. **Encontrar errores**: el error está en la línea donde el valor real se separa del que esperabas.
3. **Escribir código correcto**: si puedes simular tu programa en la cabeza, lo escribes bien a la primera más a menudo.

Además, en las entrevistas técnicas es muy común la pregunta "¿qué imprime este código?". Y cuando un agente de IA te propone un cambio,
leerlo de verdad, simulándolo, es lo que te permite detectar que está mal.

---

## 2. La tabla de variables

La idea es simple: una **columna por variable** y **una fila cada vez que algo cambia**. Así nunca tienes que recordar valores: están
escritos.

```python
precio = 20
cantidad = 3
total = precio * cantidad
descuento = 0
if total > 50:
    descuento = 10
total = total - descuento
print(total)
```

| Línea | precio | cantidad | total | descuento | Comentario |
|---|---|---|---|---|---|
| 1 | 20 | | | | |
| 2 | 20 | 3 | | | |
| 3 | 20 | 3 | 60 | | 20 × 3 |
| 4 | 20 | 3 | 60 | 0 | |
| 5 | | | | | ¿60 > 50? Sí: entra al `if` |
| 6 | 20 | 3 | 60 | 10 | |
| 7 | 20 | 3 | 50 | 10 | 60 − 10 |
| 8 | | | | | Imprime **50** |

Reglas para que funcione:

- **Una línea cada vez**, en el orden en que se ejecuta (no en el orden en que está escrita: los bucles y los `if` saltan).
- **Escribe las condiciones** y su resultado (verdadero o falso). Ahí está la mitad de los errores.
- **Cuando una variable cambia, tacha el valor antiguo** y escribe el nuevo. Una variable solo tiene un valor en cada momento.
- Usa **ejemplos pequeños**: 3 o 4 elementos bastan. Con 100 te perderías.

Hazlo en papel o en un archivo de texto. Al principio parece lento; después de unos cuantos ejercicios lo haces en la cabeza.

### La asignación no es una igualdad

`total = total - descuento` no es una ecuación matemática (que sería imposible). Se lee así: **"calcula lo de la derecha con los valores
actuales y guarda el resultado en la variable de la izquierda"**. Primero la derecha, después la flecha hacia la izquierda:

```
total = total - descuento
        └──── 60 - 10 = 50 ────┘ → total pasa a valer 50
```

---

## 3. Seguir un bucle `for`

En un bucle, la tabla tiene **una fila por vuelta**. Ejemplo:

```python
palabras = ["sol", "mar", "luna"]
letras = 0
for p in palabras:
    letras = letras + len(p)
print(letras)
```

| Vuelta | p | len(p) | letras (después) |
|---|---|---|---|
| antes del bucle | | | 0 |
| 1 | "sol" | 3 | 3 |
| 2 | "mar" | 3 | 6 |
| 3 | "luna" | 4 | 10 |
| después del bucle | | | imprime **10** |

Dos preguntas que debes hacerte siempre con un `for`:

1. **¿Qué valores toma la variable del bucle?** Con una lista, cada elemento en orden. Con `range`, cuidado con los límites:

| Expresión | Valores |
|---|---|
| `range(4)` | 0, 1, 2, 3 (empieza en 0, el 4 **no** se incluye) |
| `range(2, 6)` | 2, 3, 4, 5 |
| `range(0, 10, 3)` | 0, 3, 6, 9 (de 3 en 3) |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 (hacia atrás) |

2. **¿Qué está dentro del bucle y qué fuera?** En Python lo decide la **sangría**. Una línea con sangría se repite en cada vuelta; una sin
   sangría (después del bucle) se ejecuta una sola vez al final. Un `print` dentro del bucle imprime en cada vuelta; fuera, solo una vez.

```python
for i in range(3):
    print("dentro", i)     # se imprime 3 veces
print("fuera", i)          # se imprime 1 vez, con el último valor de i: 2
```

---

## 4. Seguir condiciones: `if`, `elif`, `else`

Lo más importante de una cadena `if / elif / else`: **solo se ejecuta una rama, la primera cuya condición es verdadera**. Las demás ni se
comprueban.

```python
temperatura = 35
if temperatura > 30:
    print("calor")
elif temperatura > 20:
    print("agradable")
else:
    print("frío")
```

Imprime solo `calor`, aunque 35 también es mayor que 20: como la primera condición ya se cumplió, el `elif` ni se mira. Por eso **el orden
de las condiciones importa**: si pusieras `temperatura > 20` primero, 35 imprimiría "agradable".

Compáralo con varios `if` independientes:

```python
n = 12
if n % 2 == 0:
    print("par")
if n % 3 == 0:
    print("múltiplo de 3")
```

Aquí se imprimen **las dos** líneas: cada `if` es una pregunta separada. Elegir entre `if`+`elif` (excluyentes) o varios `if`
(independientes) es una decisión de lógica, no de estilo.

### Condiciones compuestas: `and`, `or`, `not`

| Expresión | Es verdadera cuando... |
|---|---|
| `a and b` | las **dos** son verdaderas |
| `a or b` | **al menos una** es verdadera |
| `not a` | `a` es falsa |

Truco para seguirlas: **evalúa cada parte por separado** y escribe el resultado.

```python
edad = 17
con_permiso = True
puede_entrar = edad >= 18 or con_permiso
```

`edad >= 18` → `False`; `con_permiso` → `True`; `False or True` → **`True`**.

El operador `%` (módulo, el resto de la división) aparece muchísimo en estas condiciones: `n % 2 == 0` significa "n es par" (el resto de
dividir entre 2 es 0), y `n % 5 == 0`, "n es múltiplo de 5".

---

## 5. Seguir un bucle `while`

El `while` repite **mientras** la condición sea verdadera, y la comprueba **antes de cada vuelta**. Para seguirlo, en cada vuelta:

1. Evalúa la condición con los valores actuales.
2. Si es falsa, el bucle termina (y no se ejecuta nada de dentro).
3. Si es verdadera, ejecuta el cuerpo y vuelve al paso 1.

```python
saldo = 100
meses = 0
while saldo < 150:
    saldo = saldo * 1.2
    meses += 1
print(meses, round(saldo))
```

| Vuelta | ¿saldo < 150? | saldo (después) | meses |
|---|---|---|---|
| inicio | | 100 | 0 |
| 1 | 100 < 150 → sí | 120 | 1 |
| 2 | 120 < 150 → sí | 144 | 2 |
| 3 | 144 < 150 → sí | 172.8 | 3 |
| fin | 172.8 < 150 → **no** | | imprime **3 173** |

Dos errores típicos que la tabla detecta enseguida:

- **Bucle infinito**: si nada dentro del bucle cambia la condición (olvidaste `meses += 1` o el `saldo` no crece), el bucle no termina nunca.
- **Una vuelta de más o de menos**: `<` frente a `<=`. Con la tabla ves exactamente cuándo para.

### Condiciones con `and` en un `while`

Una situación frecuente es recorrer una lista **hasta encontrar algo**, con un índice:

```python
i = 0
while i < len(lista) and lista[i] != objetivo:
    i += 1
```

El orden de las dos condiciones importa: Python evalúa de izquierda a derecha y, en un `and`, **si la primera es falsa ya no mira la
segunda**. Así, cuando `i` llega al final de la lista, `i < len(lista)` es falsa y nunca se intenta leer `lista[i]` (que daría un error
de índice). Si las escribes al revés, el programa falla cuando el objetivo no está.

---

## 6. Seguir funciones

Cuando el código llama a una función, imagina que **saltas** a la función con los valores que le pasas, la ejecutas con su propia tabla
y **vuelves** con el valor que devuelve.

```python
def area(base, altura):
    resultado = base * altura / 2
    return resultado

a = area(6, 4)
b = area(a, 2)
print(a, b)
```

1. `area(6, 4)`: dentro, `base = 6`, `altura = 4`, `resultado = 12.0`, devuelve 12.0 → `a = 12.0`.
2. `area(a, 2)` = `area(12.0, 2)`: `resultado = 12.0`, → `b = 12.0`.
3. Imprime `12.0 12.0`.

Dos ideas clave:

- **Las variables de dentro son locales**: `resultado`, `base` y `altura` solo existen durante esa llamada. Cada llamada tiene su propia
  tabla.
- **Cambiar un número o un texto dentro de una función no cambia la variable de fuera.** Si la función hace `x = x * 2`, la variable con
  la que la llamaste sigue igual. (Las listas y los diccionarios son distintos: si la función los *modifica* con `append` o asignando un
  elemento, el cambio sí se ve fuera, porque es el mismo objeto.)

### `return` frente a `print`

`print` **muestra** un valor en pantalla; `return` **devuelve** un valor a quien llamó a la función para que lo use. Una función sin
`return` devuelve `None`:

```python
def doble_mal(x):
    print(x * 2)

y = doble_mal(5)    # imprime 10
print(y)            # imprime None: la función no devolvió nada
```

Es uno de los errores más frecuentes al empezar: "mi función funciona, imprime el resultado", pero luego el resultado no se puede usar.

---

## 7. Usar `print` como tabla automática

Cuando el código es largo, puedes dejar que Python escriba la tabla por ti, añadiendo `print` temporales:

```python
for i, nota in enumerate(notas):
    print("vuelta", i, "nota", nota, "suma", suma)   # depuración: quítalo después
    suma = suma + nota
```

Y una forma muy cómoda de imprimir variables con su nombre: el `=` dentro de un f-string.

```python
x = 5
print(f"{x=}")       # x=5
```

Herramientas más avanzadas: el **depurador** de tu editor (VS Code) permite parar en una línea (*breakpoint*) y avanzar paso a paso
viendo todas las variables. Es exactamente la tabla de variables, pero automática. Aprende a usarlo cuando domines la tabla a mano: sin
la costumbre de pensar paso a paso, el depurador solo muestra números.

Y una herramienta web muy útil para aprender: **Python Tutor** (pythontutor.com) dibuja la ejecución de un programa paso a paso. Úsala para
comprobar tus tablas.

---

## 8. Los errores de lógica más comunes (y cómo los delata la tabla)

| Error | Síntoma | Qué ves en la tabla |
|---|---|---|
| Variable inicializada **dentro** del bucle | El total solo tiene el último valor | La variable vuelve a 0 en cada vuelta |
| `print` o `return` **dentro** del bucle | Sale después de la primera vuelta | El bucle se corta en la vuelta 1 |
| `range` mal (`range(1, n)` en vez de `range(n)`) | Falta el primer o el último elemento | Faltan o sobran filas |
| `<` en vez de `<=` | Una vuelta de menos | La última fila no aparece |
| `elif` en vez de `if` | Solo se aplica una regla | La segunda condición no se comprueba |
| Bandera que se "resetea" | Solo cuenta el último elemento | El valor cambia en los dos sentidos |
| `print` en vez de `return` | El resultado es `None` | La función no devuelve nada |

Cuando un programa falla, **no cambies cosas al azar** esperando que funcione. Haz la tabla con un ejemplo pequeño, escribe al lado lo que
*esperabas* en cada paso y busca la primera fila donde no coinciden.

---

## 9. Cómo practicar

- **Cada día, un "¿qué imprime?"**: los ejercicios de esta plataforma, ejercicios de entrevistas o cualquier código que leas. Primero
  predice, después ejecuta y compara.
- **Antes de pulsar "Comprobar"** en un ejercicio de Python, sigue tu propio código con el ejemplo del enunciado. Encontrarás muchos errores
  antes de que lo haga la prueba.
- **Cuando la IA te dé código**, elige una función y síguela con la tabla. Si no puedes, todavía no la entiendes.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Tabla de variables | Una columna por variable, una fila por cambio, condiciones escritas |
| Asignación | Primero se calcula la derecha, después se guarda a la izquierda |
| `for` | Una fila por vuelta; cuidado con los límites de `range` y con la sangría |
| `if/elif/else` | Solo la primera rama verdadera; el orden importa |
| `while` | La condición se comprueba antes de cada vuelta; algo debe cambiarla |
| `and` | Se evalúa de izquierda a derecha y para en cuanto encuentra un falso |
| Funciones | Tabla propia por llamada; `return` devuelve, `print` muestra |
| Depurar | Busca la primera fila donde el valor real se separa del esperado |

## Autoevaluación final

1. ¿Qué valores toma `i` en `for i in range(3, 9, 2)`?
2. `x = 4`, luego `x = x * x - x`. ¿Cuánto vale `x`?
3. En una cadena `if / elif`, si las dos condiciones son verdaderas, ¿cuántas ramas se ejecutan?
4. ¿Por qué en `while i < len(lista) and lista[i] != 0` importa el orden de las condiciones?
5. Una función hace `print(resultado)` pero no tiene `return`. ¿Qué vale `y = funcion(3)`?
6. Tu suma da siempre el último número de la lista. ¿Qué error de lógica sospechas primero?

**Respuestas:** 1) 3, 5 y 7. 2) 12 (se calcula 4 × 4 − 4 con el valor anterior y se guarda). 3) Solo una: la primera verdadera. 4) Porque
el `and` para en la primera condición falsa: si el índice ya está fuera de la lista, no se llega a leer `lista[i]` (que daría error).
5) `None`. 6) Que la variable de la suma se pone a 0 dentro del bucle en lugar de antes.
