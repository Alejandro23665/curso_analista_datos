# Lógica III: cómo resolver un problema que no sabes resolver

Lees un enunciado, entiendes cada palabra, sabes qué es un bucle y un diccionario... y aun así te quedas en blanco delante del editor.
Es la experiencia más común al aprender a programar, y no significa que "no tengas lógica". Significa que estás intentando **saltar
directamente del enunciado al código**, y ese salto es demasiado grande para cualquiera.

Los programadores con experiencia no lo dan de un salto: siguen un **método**, a menudo sin darse cuenta. Este capítulo te lo enseña paso
a paso. Es el mismo método que usarás en las entrevistas técnicas, en los ejercicios de esta plataforma y en tus proyectos con clientes.

---

## 1. El método en seis pasos

| Paso | Pregunta | Resultado |
|---|---|---|
| **1. Entender** | ¿Qué entra, qué sale y qué reglas hay? | El enunciado con tus palabras |
| **2. Ejemplos a mano** | ¿Sé resolverlo sin ordenador? | 2-3 ejemplos resueltos, con un caso borde |
| **3. Descomponer** | ¿En qué partes más pequeñas se divide? | Una lista de subproblemas |
| **4. Pseudocódigo** | ¿Qué pasos sigo, en orden? | Los pasos en lenguaje natural |
| **5. Programar paso a paso** | ¿Funciona cada parte? | Código probado por partes |
| **6. Probar los casos borde** | ¿Y si está vacío, es uno solo, hay empate? | Confianza en que funciona |

Parece lento, pero es al revés: los minutos que dedicas a los pasos 1 a 4 te ahorran la hora de cambiar código al azar.

---

## 2. Paso 1: entender el problema

Antes de pensar en cómo, asegúrate de saber **qué**. Escribe tres cosas:

- **Entrada**: qué recibe, de qué tipo y con qué forma (*una lista de diccionarios con las claves `nombre` y `edad`*).
- **Salida**: qué devuelve exactamente (*una lista de nombres, ordenada*), y qué devuelve en los casos raros (*lista vacía si no hay
  ninguno*).
- **Reglas**: las condiciones del enunciado, una por línea.

Ejemplo de enunciado: *"Escribe `inscribir(personas)` que devuelva los nombres de las personas que pueden inscribirse en un taller: deben
ser mayores de edad y haber dado un correo. Devuélvelos en orden alfabético."*

```
Entrada: lista de diccionarios {"nombre": texto, "edad": número, "correo": texto (puede estar vacío)}
Salida:  lista de nombres (textos), en orden alfabético; [] si nadie cumple
Reglas:  - edad >= 18 ("mayor de edad": ¿18 cuenta? sí)
         - correo no vacío
         - las dos a la vez (y)
```

Fíjate en que al escribirlo aparecen **preguntas**: ¿18 años cuenta como mayor de edad? ¿qué es "haber dado un correo": un texto no vacío?
En una entrevista, esas preguntas se hacen en voz alta. Aquí, el enunciado y las pruebas te dan la respuesta.

**Palabras del enunciado que cambian la lógica**: "y" frente a "o"; "al menos" (`>=`) frente a "más de" (`>`); "el primero" frente a
"todos"; "ordenado"; "sin repetir"; "si no hay ninguno".

---

## 3. Paso 2: resolver ejemplos a mano

Esta es la regla de oro: **si no puedes resolverlo a mano con un ejemplo pequeño, todavía no puedes programarlo**. Y si puedes, los pasos
que hiciste **son el algoritmo**.

```
personas = [
  {"nombre": "Luis", "edad": 17, "correo": "luis@mail.com"},
  {"nombre": "Ana",  "edad": 25, "correo": "ana@mail.com"},
  {"nombre": "Eva",  "edad": 30, "correo": ""},
  {"nombre": "Bea",  "edad": 18, "correo": "bea@mail.com"},
]
```

A mano: Luis no (17). Ana sí. Eva no (sin correo). Bea sí (18 cuenta). Quedan Ana y Bea; ordenadas: **["Ana", "Bea"]**.

¿Qué hiciste? Miraste a cada persona una por una (un **bucle**), comprobaste dos condiciones (un **if con and**), apuntaste a las que
cumplían (un **acumulador en lista**) y al final ordenaste (**después** del bucle). Ese es el programa.

Haz siempre al menos un **caso borde**: lista vacía (debería dar `[]`), nadie cumple (`[]`), todos cumplen.

---

## 4. Paso 3: descomponer

Los problemas grandes se resuelven como problemas pequeños en fila. **Descomponer** es dividir el problema en partes que puedas resolver
(y probar) por separado.

Ejemplo de un problema más grande: *"Genera el resumen de una factura: el subtotal de las líneas, un descuento del 5 % si el subtotal
supera 200, el IVA del 16 % sobre el importe con descuento y el total."*

```
Subproblema A: subtotal = suma de cantidad × precio de cada línea          (acumulador)
Subproblema B: descuento = 5 % del subtotal si subtotal > 200, si no 0    (una condición)
Subproblema C: base = subtotal - descuento
Subproblema D: iva = 16 % de la base
Subproblema E: total = base + iva
Subproblema F: juntar todo en un diccionario y redondear a 2 decimales
```

Cada subproblema es pequeño y casi obvio. La dificultad del problema original estaba en que eran seis cosas a la vez.

### Cómo saber por dónde cortar

- **Cada regla del enunciado** suele ser un subproblema.
- **Cada dato que hay que calcular** para el resultado es un subproblema.
- Si un subproblema todavía te parece difícil, **divídelo otra vez**.
- Busca **subproblemas independientes**: los que no dependen unos de otros se pueden resolver en cualquier orden. En la factura, A va
  antes que B, pero en una validación de varias reglas cada regla es independiente de las demás.

### Funciones auxiliares

Cuando un subproblema es claro, conviértelo en una **función pequeña con un nombre que explique qué hace**:

```python
def subtotal(lineas):
    total = 0
    for linea in lineas:
        total += linea["cantidad"] * linea["precio"]
    return total

def descuento(importe):
    return importe * 0.05 if importe > 200 else 0
```

La función principal queda como una lectura del pseudocódigo, y cada pieza se puede probar sola:

```python
def resumen_factura(lineas):
    sub = subtotal(lineas)
    base = sub - descuento(sub)
    iva = base * 0.16
    return {"subtotal": round(sub, 2), "base": round(base, 2), "iva": round(iva, 2), "total": round(base + iva, 2)}
```

---

## 5. Paso 4: pseudocódigo

El **pseudocódigo** es el algoritmo escrito en lenguaje natural, con la estructura del código (bucles, condiciones) pero sin preocuparte de
la sintaxis. Es el puente entre "lo sé hacer a mano" y "lo sé programar".

Para el ejemplo del taller:

```
inscritos = lista vacía
para cada persona en personas:
    si su edad es 18 o más Y su correo no está vacío:
        añadir su nombre a inscritos
ordenar inscritos
devolver inscritos
```

Ahora la traducción a Python es casi línea a línea:

```python
def inscribir(personas):
    inscritos = []
    for persona in personas:
        if persona["edad"] >= 18 and persona["correo"]:
            inscritos.append(persona["nombre"])
    return sorted(inscritos)
```

(Un texto vacío `""` se considera falso en una condición, así que `persona["correo"]` ya significa "el correo no está vacío".)

Reglas para un buen pseudocódigo:

- **Un paso por línea**, con la sangría de los bloques (qué va dentro del bucle y qué después).
- **Sin sintaxis**: "añadir a la lista", no `lista.append(x)`. Si te atascas pensando en la sintaxis, pierdes el hilo del algoritmo.
- **Nombra las variables** igual que en el código, para que la traducción sea directa.

### Condiciones independientes o excluyentes

Al escribir el pseudocódigo decide si las reglas se excluyen o no:

- "Si es **A**, haz X; si no, **si es B**, haz Y" → excluyentes: `if` / `elif`.
- "Comprueba A; **además**, comprueba B" → independientes: dos `if` separados.

Ejemplo de reglas **independientes**: validar el formulario de un evento y devolver **todos** los problemas que tiene.

```python
def problemas_formulario(f):
    problemas = []
    if not f["nombre"].strip():
        problemas.append("falta el nombre")
    if f["edad"] < 18:
        problemas.append("menor de edad")
    if "@" not in f["correo"]:
        problemas.append("correo inválido")
    return problemas
```

Con `elif` solo se informaría del **primer** problema, y un formulario con tres errores mostraría uno solo.

### Herramientas que acortan comprobaciones: `any` y `all`

Muchas reglas son "¿hay algún carácter / elemento que...?" o "¿todos...?". Python tiene dos funciones para eso:

```python
any(c.isdigit() for c in "abc3")         # True: hay algún dígito
all(c.isalpha() for c in "abc3")         # False: no todos son letras
any(n < 0 for n in [4, 7, 1])            # False: ningún negativo
```

Métodos de texto útiles para este tipo de reglas: `c.isdigit()` (es un dígito), `c.isalpha()` (es una letra), `c.isupper()` / `c.islower()`
(mayúscula / minúscula), `c.isspace()` (espacio), `texto.strip()` (sin espacios a los lados).

---

## 6. Paso 5: programar paso a paso

No escribas toda la función y la ejecutes al final. **Programa un subproblema, pruébalo y sigue.**

```python
def resumen_factura(lineas):
    sub = subtotal(lineas)
    print("subtotal:", sub)          # comprobación temporal
    ...
```

Con un ejemplo que resolviste a mano, compara cada valor intermedio con el tuyo. Si el subtotal ya está mal, no tiene sentido mirar el IVA.

Cuando algo falla, vuelve a la **tabla de variables** del capítulo *Seguir el código a mano*: busca la primera línea en la que el valor
real se separa del que calculaste a mano.

### Empieza por el caso más fácil

Muchas veces conviene escribir primero el **caso especial** (la lista vacía) y después el general:

```python
def mejor_vendedor(ventas):
    if not ventas:          # caso especial resuelto y fuera de la vista
        return None
    ...                     # ahora el caso general, sabiendo que hay al menos una venta
```

---

## 7. Paso 6: probar los casos borde

Los casos borde son las entradas "raras" donde suelen esconderse los errores. Esta lista cubre casi todos:

- **Vacío**: lista, texto o diccionario vacío.
- **Un solo elemento.**
- **Empates**: dos elementos con el mismo valor máximo; ¿cuál gana?
- **Límites exactos**: si la regla es "18 o más", prueba con 17, 18 y 19.
- **Todos cumplen / ninguno cumple.**
- **Valores especiales**: cero, negativos, textos con espacios o mayúsculas.

Y una técnica para **empates con orden alfabético** (un enunciado típico: "si hay empate, el primero en orden alfabético"): recorre las
claves **ya ordenadas** y quédate con el primero que alcanza el máximo (usando `>` estricto, como viste en el patrón máximo). Ejemplo con
otro dato:

```python
stock = {"tornillos": 40, "clavos": 40, "tuercas": 10}
mas_stock = None
for producto in sorted(stock):                  # "clavos", "tornillos", "tuercas"
    if mas_stock is None or stock[producto] > stock[mas_stock]:
        mas_stock = producto
# "clavos": empata con "tornillos" a 40, pero va antes alfabéticamente
```

### Redondear y dividir

Dos detalles que fallan a menudo en las pruebas:

- **`round(valor, 1)`** redondea a un decimal: `round(6.666, 1)` da `6.7`. Redondea **al final**, no en los pasos intermedios, para no
  acumular error.
- **Dividir entre una cantidad que puede ser 0**: comprueba antes (el caso vacío).

---

## 8. Un ejemplo completo, de principio a fin

**Enunciado:** *"Escribe `resumen_gastos(gastos)` que reciba una lista de tuplas `(categoria, importe)` y devuelva el total gastado, la
categoría con más gasto acumulado y cuántos gastos superan 50."*

**1. Entender.** Entrada: lista de tuplas (texto, número). Salida: un diccionario con tres datos. Casos raros: lista vacía → total 0,
categoría `None`, 0 gastos grandes.

**2. Ejemplo a mano.** `[("comida", 30), ("ocio", 60), ("comida", 45), ("ocio", 10)]`: total 145; por categoría, comida 75 y ocio 70 →
comida; gastos de más de 50: solo el de 60 → 1.

**3. Descomponer.** A) total (acumulador). B) gasto por categoría (agrupar) y la mayor (máximo). C) cuántos superan 50 (contador).

**4. Pseudocódigo.**

```
si no hay gastos: devolver total 0, categoría ninguna, grandes 0
total = 0, grandes = 0, por_categoria = diccionario vacío
para cada (categoria, importe):
    sumar importe al total
    si importe > 50: sumar 1 a grandes
    sumar importe a por_categoria[categoria] (creándola si no existe)
mayor = la categoría con más gasto en por_categoria
devolver los tres datos
```

**5. Programar.**

```python
def resumen_gastos(gastos):
    if not gastos:
        return {"total": 0, "mayor": None, "grandes": 0}
    total, grandes, por_categoria = 0, 0, {}
    for categoria, importe in gastos:
        total += importe
        if importe > 50:
            grandes += 1
        por_categoria[categoria] = por_categoria.get(categoria, 0) + importe
    mayor = None
    for categoria in por_categoria:
        if mayor is None or por_categoria[categoria] > por_categoria[mayor]:
            mayor = categoria
    return {"total": total, "mayor": mayor, "grandes": grandes}
```

**6. Probar.** El ejemplo da `{"total": 145, "mayor": "comida", "grandes": 1}`. Lista vacía: el caso especial. Un gasto de exactamente 50
no cuenta como grande (la regla dice "superan"). Fíjate en que el programa combina **cuatro patrones** del capítulo anterior: acumulador,
contador, agrupar y máximo.

---

## 9. Cuando te atascas

- **Vuelve un paso atrás.** Si no sabes programarlo, revisa el pseudocódigo. Si no sabes escribir el pseudocódigo, resuelve otro ejemplo a
  mano. Si no sabes resolverlo a mano, relee el enunciado.
- **Simplifica el problema.** Resuelve primero una versión más fácil (sin la regla del empate, con una sola categoría) y después añade la
  parte que falta.
- **Habla en voz alta** (o escríbelo): explicar el problema te obliga a ordenar las ideas. Es la técnica "del patito de goma".
- **Descansa.** Muchas soluciones aparecen después de una pausa: el cerebro sigue trabajando. Para eso está el temporizador.
- **Usa la pista antes que la solución.** Mirar la solución completa te da la respuesta pero te quita el entrenamiento.
- **Con la IA, pide pistas, no código.** "¿Qué patrón me sirve para esto?" o "¿qué caso borde se me escapa?" te hace avanzar sin
  resolverlo por ti.

---

## Resumen del capítulo

| Paso | Lo esencial |
|---|---|
| Entender | Entrada, salida y reglas por escrito; palabras que cambian la lógica |
| Ejemplos a mano | Si no lo resuelves a mano, no lo puedes programar; los pasos son el algoritmo |
| Descomponer | Una regla o un dato = un subproblema; funciones pequeñas con buen nombre |
| Pseudocódigo | Un paso por línea, con sangría, sin sintaxis; `if/elif` excluyentes, varios `if` independientes |
| Programar | Un subproblema cada vez, comprobado con `print`; primero el caso especial |
| Probar | Vacío, uno solo, empates, límites exactos, todos y ninguno |

## Autoevaluación final

1. ¿Qué tres cosas escribes en el paso "entender"?
2. ¿Por qué resolver ejemplos a mano antes de programar?
3. Tienes tres reglas de validación y debes informar de **todos** los fallos. ¿`if` y `elif` o varios `if`?
4. ¿Qué devuelve `any(c.isupper() for c in "hola")`?
5. Una regla dice "18 o más". ¿Con qué valores la pruebas?
6. Te atascas al programar. ¿A qué paso vuelves primero?

**Respuestas:** 1) La entrada, la salida (incluidos los casos raros) y las reglas. 2) Porque si no puedes resolverlo a mano todavía no lo
entiendes, y si puedes, los pasos que seguiste son el algoritmo. 3) Varios `if`: son reglas independientes y con `elif` solo saldría el
primer fallo. 4) `False`: no hay ninguna mayúscula. 5) Con 17, 18 y 19 (justo por debajo, en el límite y por encima). 6) Al pseudocódigo; y
si tampoco lo tienes claro, a resolver otro ejemplo a mano.
