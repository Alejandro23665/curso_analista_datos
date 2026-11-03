# Algoritmos y estructuras de datos para entrevistas

En muchas entrevistas técnicas de backend y de IA aplicada hay una parte de *live coding*: te dan un problema pequeño y lo resuelves
mientras explicas lo que piensas. No buscan genios de las competiciones: buscan que **elijas la estructura de datos adecuada**, que
**razones sobre la eficiencia** y que **comuniques** con claridad.

La buena noticia es que la gran mayoría de los problemas de nivel junior se resuelven con **media docena de patrones**. Este capítulo te
enseña a medir la eficiencia (Big O) y esos patrones, cada uno con ejemplos resueltos, para que al ver un problema nuevo reconozcas qué
herramienta usar.

---

## 1. Big O: cómo crece el trabajo

La notación **Big O** describe cómo crece el número de operaciones de un algoritmo cuando crece el tamaño de la entrada (`n`). No mide
segundos: mide **la forma del crecimiento**.

| Notación | Nombre | Ejemplo | Con n = 1 000 000 |
|---|---|---|---|
| O(1) | Constante | Acceder a `lista[5]`, buscar en un `dict` o `set` | 1 paso |
| O(log n) | Logarítmica | Búsqueda binaria | ~20 pasos |
| O(n) | Lineal | Recorrer una lista una vez | 1 000 000 |
| O(n log n) | Casi lineal | Ordenar (`sorted`) | ~20 000 000 |
| O(n²) | Cuadrática | Dos bucles anidados sobre la misma lista | 1 000 000 000 000 |

La diferencia entre O(n) y O(n²) no es académica: con un millón de elementos, uno tarda una fracción de segundo y el otro, horas.

### Cómo calcularlo a ojo

- Un bucle sobre `n` elementos: **O(n)**.
- Dos bucles anidados sobre `n`: **O(n²)**.
- Dos bucles **seguidos** (uno después del otro): O(n) + O(n) = **O(n)**. Las constantes no importan.
- Algo que divide el problema a la mitad en cada paso: **O(log n)**.
- Se toma el término que más crece: O(n² + n) = O(n²).

### El costo oculto de las operaciones de Python

Esta tabla es la que más preguntas de entrevista resuelve:

| Operación | Costo |
|---|---|
| `x in lista` | **O(n)**: recorre la lista |
| `x in conjunto` / `clave in diccionario` | **O(1)** en promedio |
| `lista.append(x)` / `lista.pop()` (al final) | O(1) |
| `lista.insert(0, x)` / `lista.pop(0)` (al principio) | O(n): desplaza todo |
| `lista.index(x)`, `lista.count(x)`, `min`, `max`, `sum` | O(n) |
| `sorted(lista)` / `lista.sort()` | O(n log n) |
| Corte `lista[a:b]` | O(b − a): copia los elementos |

Un ejemplo clásico de error: comprobar 100 000 veces si un correo está en una **lista** de un millón de correos son
100 000 × 1 000 000 operaciones. Convertir la lista en un `set` **una vez** (O(n)) hace que cada comprobación sea O(1).

### Espacio

Big O también se usa para la **memoria** extra. Muchas soluciones rápidas cambian memoria por tiempo: guardar cosas en un diccionario
(O(n) de espacio) para no tener que volver a recorrer la lista. En la entrevista, menciona los dos: "es O(n) en tiempo y O(n) en espacio".

---

## 2. Cómo abordar un problema en la entrevista

El proceso importa tanto como la solución:

1. **Repite el problema con tus palabras** y pregunta por los casos dudosos: ¿la lista puede estar vacía? ¿hay negativos? ¿duplicados?
   ¿qué devuelvo si no hay solución?
2. **Haz un ejemplo a mano**, pequeño, y uno de caso borde.
3. **Di primero la solución obvia** (normalmente la de fuerza bruta) y su Big O. Demuestra que entiendes el problema.
4. **Mejórala**: "¿qué estoy repitiendo? ¿qué estructura me evitaría recorrer otra vez?".
5. **Escribe el código** explicando mientras lo haces.
6. **Pruébalo** recorriendo tu ejemplo a mano, y con los casos borde.
7. **Di el Big O final** de tiempo y espacio.

Si te atascas, piensa en voz alta. Un entrevistador puede darte una pista si sabe en qué estás pensando; si estás en silencio, no.

---

## 3. Patrón 1: diccionario o conjunto para recordar lo visto

**Cuándo:** el problema pide buscar algo **relacionado con otros elementos** de la lista (un par, un duplicado, un complemento) y la
solución obvia es un bucle dentro de otro.

**La idea:** recorrer la lista **una vez** guardando en un `set` o `dict` lo que ya viste, para responder "¿he visto antes X?" en O(1).

### Ejemplo: ¿hay algún elemento repetido?

Fuerza bruta: comparar cada par, O(n²).

```python
def tiene_duplicados_lento(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False
```

Con un conjunto, O(n):

```python
def tiene_duplicados(nums):
    vistos = set()
    for x in nums:
        if x in vistos:          # O(1)
            return True
        vistos.add(x)
    return False

tiene_duplicados([3, 1, 4, 1, 5])   # True
tiene_duplicados([])                 # False
```

### Ejemplo: la primera posición donde se repite un valor

Cuando además de saber **si** lo viste necesitas saber **dónde**, usa un diccionario `valor → índice`:

```python
def primera_repeticion(palabras):
    """Devuelve (indice_primera_vez, indice_repeticion) de la primera palabra que se repite."""
    posicion = {}
    for i, p in enumerate(palabras):
        if p in posicion:
            return (posicion[p], i)
        posicion[p] = i
    return None

primera_repeticion(["sol", "mar", "luna", "mar", "sol"])   # (1, 3)
```

Fíjate en el **orden** dentro del bucle: primero se **consulta** y después se **guarda**. Si guardaras antes de consultar, cada elemento
"se encontraría a sí mismo". Este detalle aparece en muchos problemas: piensa qué debe estar ya en el diccionario en el momento de
consultar.

Esta misma idea se generaliza: en lugar de buscar el mismo valor, puedes buscar **el valor que te falta** para cumplir una condición
(un complemento). La pregunta clave es: "para el elemento actual, ¿qué otro elemento necesitaría haber visto antes?".

---

## 4. Patrón 2: contar frecuencias

**Cuándo:** el problema habla de "cuántas veces", "el más frecuente", "aparece una sola vez", "anagramas".

**La idea:** una pasada para contar con un diccionario (o `collections.Counter`), y después usar los conteos.

```python
from collections import Counter

Counter("banana")                  # Counter({'a': 3, 'n': 2, 'b': 1})
Counter("banana")["a"]             # 3
Counter("banana")["z"]             # 0 (no da error)
Counter("banana").most_common(1)   # [('a', 3)]
```

### Ejemplo: ¿son anagramas?

Dos palabras son anagramas si tienen las mismas letras con las mismas frecuencias:

```python
def son_anagramas(a, b):
    return Counter(a) == Counter(b)

son_anagramas("roma", "amor")   # True
son_anagramas("roma", "ramos")  # False
```

O(n), frente a O(n log n) de comparar `sorted(a) == sorted(b)`.

### Ejemplo: la última palabra que aparece más de una vez

Un patrón muy útil es **contar primero y recorrer después**: la primera pasada calcula los conteos de todo; la segunda recorre en el
orden que necesitas consultando los conteos.

```python
def ultima_repetida(palabras):
    conteo = Counter(palabras)
    for p in reversed(palabras):       # segunda pasada, en el orden que pide el problema
        if conteo[p] > 1:
            return p
    return None

ultima_repetida(["a", "b", "c", "b", "d"])   # 'b'
```

Dos pasadas seguidas siguen siendo O(n). La razón de separarlas: mientras cuentas, todavía no sabes si un elemento volverá a aparecer más
adelante.

---

## 5. Patrón 3: la pila

Una **pila** (*stack*) es una estructura "el último en entrar es el primero en salir", como una pila de platos. En Python se usa una lista
con `append` (apilar) y `pop()` (desapilar), ambos O(1). `pila[-1]` consulta la cima sin sacarla.

**Cuándo:** cosas que se **abren y se cierran** en orden anidado, "deshacer", o comparar cada elemento con el **último pendiente**.

### Ejemplo: eliminar pares de letras iguales adyacentes

Dado `"abbaca"`: se eliminan las `bb` adyacentes → `"aaca"`; luego las `aa` → `"ca"`. Con una pila, en una pasada:

```python
def quitar_adyacentes(s):
    pila = []
    for c in s:
        if pila and pila[-1] == c:    # la cima es igual: se anulan
            pila.pop()
        else:
            pila.append(c)
    return "".join(pila)

quitar_adyacentes("abbaca")   # 'ca'
```

Fíjate en `if pila and ...`: antes de mirar la cima, se comprueba que la pila **no esté vacía**. `pila[-1]` sobre una lista vacía lanza
`IndexError`. Es el error más común con pilas.

### Ejemplo: etiquetas que se abren y se cierran

Las estructuras anidadas (etiquetas, bloques, paréntesis) son el uso típico de la pila: cada apertura se apila; cada cierre debe
corresponder **a la última apertura pendiente**. Ejemplo con una lista de etiquetas tipo HTML:

```python
def etiquetas_bien_anidadas(etiquetas):
    pila = []
    for e in etiquetas:
        if not e.startswith("/"):          # apertura: "b", "i"
            pila.append(e)
        else:                               # cierre: "/b", "/i"
            if not pila or pila.pop() != e[1:]:
                return False
    return not pila                         # al final no debe quedar nada abierto

etiquetas_bien_anidadas(["b", "i", "/i", "/b"])   # True
etiquetas_bien_anidadas(["b", "i", "/b", "/i"])   # False: se cierra b antes que i
etiquetas_bien_anidadas(["b"])                     # False: b queda abierta
```

Los tres casos de fallo que hay que cubrir siempre: un cierre **sin apertura** (pila vacía), un cierre que **no corresponde** a la última
apertura, y aperturas que **quedan sin cerrar** al final. Un diccionario de "pareja de cada cierre" (`{")": "(", ...}`) es una forma
cómoda de comprobar la correspondencia cuando los símbolos son distintos.

---

## 6. Patrón 4: dos punteros

**Cuándo:** listas o textos **ordenados**, o problemas que comparan los extremos.

**La idea:** dos índices que avanzan según una regla, en lugar de probar todos los pares.

### Ejemplo: ¿es un palíndromo?

```python
def es_palindromo(s):
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True

es_palindromo("reconocer")   # True
```

### Ejemplo: fusionar dos listas ordenadas

```python
def fusionar(a, b):
    i = j = 0
    resultado = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            resultado.append(a[i]); i += 1
        else:
            resultado.append(b[j]); j += 1
    resultado.extend(a[i:])       # lo que quede de cada una
    resultado.extend(b[j:])
    return resultado

fusionar([1, 4, 9], [2, 3, 10])   # [1, 2, 3, 4, 9, 10]
```

O(n + m), sin volver a ordenar.

---

## 7. Patrón 5: ventana deslizante

**Cuándo:** el problema habla de **subarreglos o subcadenas consecutivas** ("k elementos seguidos", "el tramo más largo que...").

**La idea:** en lugar de recalcular cada ventana desde cero, **actualizarla** al moverla: añadir lo que entra y quitar lo que sale.

### Ejemplo: el promedio de cada ventana de tamaño k

Fuerza bruta: para cada posición, sumar los `k` elementos → O(n·k).

```python
def promedios_moviles_lento(nums, k):
    return [sum(nums[i:i + k]) / k for i in range(len(nums) - k + 1)]
```

Con ventana deslizante → O(n):

```python
def promedios_moviles(nums, k):
    if k < 1 or k > len(nums):
        return []
    suma = sum(nums[:k])                 # la primera ventana, una sola vez
    resultado = [suma / k]
    for i in range(k, len(nums)):
        suma += nums[i] - nums[i - k]    # entra nums[i], sale nums[i - k]
        resultado.append(suma / k)
    return resultado

promedios_moviles([2, 4, 6, 8, 10], 3)   # [4.0, 6.0, 8.0]
```

Recorre el ejemplo a mano: la primera ventana es `[2, 4, 6]` (suma 12). Al mover, entra el 8 y sale el 2: suma 18, ventana `[4, 6, 8]`.
Luego entra el 10 y sale el 4: suma 24. El índice del que **sale** es siempre `i - k`.

Fíjate también en la validación del principio: ¿qué tiene sentido devolver si `k` es 0, negativo o mayor que la lista? El enunciado de
cada problema lo define; pregúntalo en la entrevista si no lo dice.

### Ventana de tamaño variable

Otra variante: la ventana **crece** por la derecha y **se encoge** por la izquierda cuando deja de cumplir una condición. Ejemplo: la
subcadena más larga sin caracteres repetidos.

```python
def mas_larga_sin_repetir(s):
    inicio = 0
    ultima_vez = {}
    mejor = 0
    for i, c in enumerate(s):
        if c in ultima_vez and ultima_vez[c] >= inicio:
            inicio = ultima_vez[c] + 1        # encoger: saltar después de la repetición
        ultima_vez[c] = i
        mejor = max(mejor, i - inicio + 1)
    return mejor

mas_larga_sin_repetir("abcabcbb")   # 3 ('abc')
```

Combina dos patrones: ventana deslizante y diccionario de lo visto.

---

## 8. Patrón 6: búsqueda binaria

**Cuándo:** los datos están **ordenados** (o la respuesta es un número dentro de un rango y puedes comprobar si "es demasiado grande o
demasiado pequeño").

**La idea:** mirar el elemento del medio y **descartar la mitad** en cada paso. Con un millón de elementos bastan unas 20 comparaciones
(2²⁰ ≈ 1 000 000): eso es O(log n).

```
Buscar 23 en [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
               0  1  2   3   4   5   6   7   8   9

paso 1: lo=0, hi=9, medio=4 → 16 < 23 → descartar la izquierda: lo=5
paso 2: lo=5, hi=9, medio=7 → 56 > 23 → descartar la derecha:   hi=6
paso 3: lo=5, hi=6, medio=5 → 23 == 23 → encontrado en el índice 5
```

### Ejemplo: raíz cuadrada entera

La búsqueda binaria no solo sirve para buscar en listas: sirve para buscar **una respuesta** en un rango. La raíz cuadrada entera de `n`
es el mayor `r` tal que `r * r <= n`:

```python
def raiz_entera(n):
    lo, hi = 0, n
    respuesta = 0
    while lo <= hi:
        medio = (lo + hi) // 2
        if medio * medio <= n:
            respuesta = medio         # medio es válido; ¿habrá uno mayor?
            lo = medio + 1
        else:
            hi = medio - 1            # demasiado grande
    return respuesta

raiz_entera(30)    # 5   (5*5 = 25 <= 30, 6*6 = 36 > 30)
raiz_entera(1)     # 1
```

### Los detalles donde todos se equivocan

- **La condición del bucle**: con `lo <= hi` el rango incluye los dos extremos; el bucle termina cuando el rango queda vacío.
- **Mover más allá del medio**: `lo = medio + 1` y `hi = medio - 1`. Si escribes `lo = medio`, cuando `lo` y `hi` son vecinos el medio
  vuelve a ser `lo` y el bucle **nunca termina**.
- **División entera** `//` para el índice del medio.
- **Qué devolver si no está**: cuando el bucle termina sin encontrarlo, el valor no existe.
- Comprueba siempre: lista vacía, un elemento, el valor en el primer índice, en el último, y un valor que no está (menor que todos, mayor
  que todos y en medio).

En Python real existe el módulo `bisect` para esto; en la entrevista suelen pedir que lo escribas tú.

---

## 9. Otras estructuras que conviene conocer

| Estructura | En Python | Para qué |
|---|---|---|
| Cola (el primero en entrar sale primero) | `collections.deque` (`append`, `popleft` en O(1)) | Procesar en orden de llegada, recorridos por niveles |
| Montículo (*heap*) | `heapq` | Los k mayores o menores sin ordenar todo: O(n log k) |
| Conjunto | `set` | Pertenencia O(1), quitar duplicados, intersecciones |
| Diccionario con valor por defecto | `collections.defaultdict(list)` | Agrupar |

```python
import heapq
heapq.nlargest(3, [5, 1, 9, 3, 7])   # [9, 7, 5]
```

---

## 10. Cómo practicar

- **Por patrones, no al azar**: 5-10 problemas de cada patrón hasta que lo reconozcas al leer el enunciado.
- **Cronometrado**: 20-30 minutos por problema, como en la entrevista.
- **En voz alta**: explica mientras escribes, aunque estés solo. Es una habilidad que se entrena.
- **Sin el asistente de IA** mientras practicas: el objetivo es que el patrón quede en tu cabeza. Después, compara tu solución con otras.
- Plataformas: LeetCode (filtra por "Easy" y por etiqueta: *Hash Table*, *Stack*, *Two Pointers*, *Sliding Window*, *Binary Search*),
  HackerRank, NeetCode (listas organizadas por patrón).

---

## Resumen del capítulo

| Patrón | Señal en el enunciado | Herramienta | Costo típico |
|---|---|---|---|
| Recordar lo visto | Pares, duplicados, complementos | `set` / `dict`; consultar antes de guardar | O(n) |
| Frecuencias | "Cuántas veces", "una sola vez", anagramas | `Counter`; contar y luego recorrer | O(n) |
| Pila | Abrir/cerrar, anidado, deshacer | Lista con `append`/`pop`; comprobar si está vacía | O(n) |
| Dos punteros | Ordenado, extremos, fusionar | Dos índices | O(n) |
| Ventana deslizante | "k seguidos", "subcadena" | Sumar lo que entra, restar lo que sale | O(n) |
| Búsqueda binaria | Ordenado, "buscar en un rango" | `lo`, `hi`, medio; `±1` al mover | O(log n) |

## Autoevaluación final

1. ¿Cuál es el Big O de comprobar `x in lista` dentro de un bucle sobre otra lista del mismo tamaño? ¿Cómo lo mejorarías?
2. En el patrón de "recordar lo visto", ¿por qué se consulta el diccionario **antes** de guardar el elemento actual?
3. ¿Por qué el patrón "contar primero y recorrer después" usa dos pasadas y sigue siendo O(n)?
4. ¿Qué tres situaciones hacen que una secuencia de aperturas y cierres esté mal formada?
5. ¿Qué error se produce al hacer `pila[-1]` con la pila vacía y cómo se evita?
6. En una ventana deslizante de tamaño k, al llegar al índice `i`, ¿qué elemento sale de la ventana?
7. ¿Cuántas comparaciones necesita como máximo una búsqueda binaria en un millón de elementos?
8. ¿Qué pasa si en la búsqueda binaria escribes `lo = medio` en lugar de `lo = medio + 1`?

**Respuestas:** 1) O(n²); convirtiendo la segunda lista en un `set` una vez, queda O(n). 2) Para no encontrar el propio elemento:
solo debe estar lo visto **antes**. 3) Porque mientras cuentas aún no sabes las frecuencias finales; dos pasadas seguidas son O(n) + O(n)
= O(n). 4) Un cierre sin apertura pendiente, un cierre que no corresponde a la última apertura, y aperturas que quedan sin cerrar.
5) `IndexError`; comprobando antes que la pila no esté vacía (`if pila and ...`). 6) El de índice `i - k`. 7) Unas 20 (log₂ de un
millón). 8) Cuando `lo` y `hi` son vecinos, el medio vuelve a ser `lo` y el bucle puede no terminar nunca.
