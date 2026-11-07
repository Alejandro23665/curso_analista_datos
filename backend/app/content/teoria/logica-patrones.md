# Lógica II: los patrones que se repiten

Cuando ves a alguien resolver rápido un ejercicio con bucles, parece que se le ocurre la solución de la nada. En realidad, casi siempre
está **reconociendo un patrón** que ya usó muchas veces. La gran mayoría de los ejercicios con listas se resuelven combinando **cinco
recetas**: el contador, el acumulador, el máximo (o mínimo), la bandera y la búsqueda. A ellas se suma una sexta muy útil: agrupar con
un diccionario.

Este capítulo te enseña cada patrón con su **plantilla**, sus **errores típicos** y cómo **reconocerlo en un enunciado**. Cuando los
tengas automatizados, dejarás de empezar cada ejercicio desde cero, y lo aprendido se te olvidará mucho menos, porque estará organizado en
pocas ideas en lugar de en cientos de ejercicios sueltos.

---

## 1. La estructura común: antes, durante, después

Todos los patrones tienen la misma forma en tres partes:

```python
# ANTES del bucle: preparar la variable que guardará el resultado
resultado = valor_inicial

# DURANTE: recorrer y actualizar
for elemento in coleccion:
    if condicion(elemento):
        resultado = actualizar(resultado, elemento)

# DESPUÉS: usar el resultado (devolverlo o imprimirlo)
return resultado
```

Las tres preguntas que debes responder para cualquier patrón:

1. **¿Con qué valor empieza el resultado?** (0, una lista vacía, `False`, el primer elemento...)
2. **¿Cuándo y cómo se actualiza** en cada vuelta?
3. **¿Qué se devuelve** al final, y qué pasa si la colección está vacía?

La mayoría de los errores de lógica están en la respuesta a una de estas tres preguntas.

---

## 2. Patrón contador: ¿cuántos cumplen algo?

**Señal en el enunciado:** "cuántos", "número de", "cuenta los".

```python
def contar_aprobados(notas):
    contador = 0                  # antes: empieza en cero
    for nota in notas:
        if nota >= 5:             # durante: solo los que cumplen
            contador += 1         # suma uno, no el valor
    return contador               # después

contar_aprobados([4, 7, 5, 2])    # 2
```

Detalles:

- Se suma **1**, no el elemento. Si sumas el elemento, tienes un acumulador (siguiente patrón).
- `contador += 1` es lo mismo que `contador = contador + 1`.
- Con la colección vacía, el bucle no da ninguna vuelta y se devuelve 0, que es lo correcto. Este patrón no necesita caso especial.
- **Cuidado con los límites de la condición**: "5 o más" es `>= 5`; "más de 5" es `> 5`. Lee el enunciado palabra por palabra.

En Python existe un atajo (`sum(1 for n in notas if n >= 5)`), pero conviene dominar primero la versión con bucle: es la que te permite
añadir más lógica cuando el problema se complica.

---

## 3. Patrón acumulador: sumar, juntar o construir

**Señal:** "total", "suma", "promedio", "lista de los que", "texto con".

El acumulador es un contador generalizado: en lugar de sumar 1, **añade algo del elemento**.

```python
# Acumular un número
total = 0
for precio in [12.5, 8, 30]:
    total += precio            # 50.5

# Acumular en una lista
caros = []
for precio in [12.5, 8, 30]:
    if precio > 10:
        caros.append(precio)   # [12.5, 30]

# Acumular texto
iniciales = ""
for nombre in ["Ana", "Luis", "Eva"]:
    iniciales += nombre[0]     # "ALE"
```

| Qué acumulas | Valor inicial | Actualización |
|---|---|---|
| Una suma | `0` | `total += x` |
| Un producto | `1` (¡no 0!) | `producto *= x` |
| Una lista | `[]` | `lista.append(x)` |
| Un texto | `""` | `texto += x` |
| Un conjunto | `set()` | `conjunto.add(x)` |

### El promedio: dos acumuladores

Un promedio es una suma dividida entre una cantidad. Si solo cuentan algunos elementos (por ejemplo, "el promedio de los positivos"),
necesitas **acumular y contar a la vez**, y dividir **después** del bucle:

```python
suma, cuenta = 0, 0
for t in [3, -1, 5, -2, 4]:
    if t > 0:
        suma += t
        cuenta += 1
promedio = suma / cuenta if cuenta else 0     # (3 + 5 + 4) / 3 = 4.0
```

Fíjate en el `if cuenta else 0`: si ningún elemento cumple, `cuenta` es 0 y dividir daría `ZeroDivisionError`. **Siempre que dividas,
pregúntate si el divisor puede ser cero.**

### El error más común del acumulador

```python
for precio in precios:
    total = 0          # MAL: se reinicia en cada vuelta
    total += precio
```

El resultado es siempre el último precio. Es la primera sospecha cuando "la suma da el último número".

---

## 4. Patrón máximo y mínimo: el mejor hasta ahora

**Señal:** "el mayor", "el más caro", "el más largo", "el que más", "el menor".

La idea: recorres guardando **el mejor visto hasta ahora** y lo reemplazas cuando aparece uno mejor.

```python
def mas_largo(palabras):
    if not palabras:
        return None                  # colección vacía: no hay "más largo"
    mejor = palabras[0]              # empezar con el PRIMER elemento
    for palabra in palabras[1:]:
        if len(palabra) > len(mejor):
            mejor = palabra
    return mejor

mas_largo(["sol", "montaña", "río"])    # "montaña"
```

Las tres decisiones de diseño de este patrón:

1. **Valor inicial: el primer elemento, no 0.** Si empiezas con `mejor = 0` para buscar el mayor número, falla cuando todos los números
   son negativos (ninguno supera al 0). Para el mínimo es peor: empezar en 0 devuelve 0 aunque no esté en la lista.
2. **¿Qué pasa con la lista vacía?** No hay primer elemento: hay que decidir qué devolver (`None` es lo habitual) y comprobarlo **antes**.
3. **¿Qué pasa con los empates?** Con `>` se queda el **primero** que alcanzó el máximo (los siguientes iguales no lo reemplazan); con
   `>=` se queda el **último**. Elige según lo que pida el enunciado.

### Máximo de elementos compuestos

A menudo los datos son tuplas o diccionarios y hay que comparar **por un campo**, pero devolver **el elemento completo**:

```python
ciudades = [("Caracas", 31), ("Mérida", 22), ("Maracaibo", 35)]

mas_calida = ciudades[0]
for ciudad in ciudades[1:]:
    if ciudad[1] > mas_calida[1]:      # comparar por la temperatura (posición 1)
        mas_calida = ciudad            # guardar la tupla entera
# ("Maracaibo", 35)
```

Python tiene `max()` y `min()` (también con `key=`), y conviene usarlos en el trabajo real. Pero en entrevistas y en esta plataforma a
menudo te pedirán el patrón a mano, precisamente para comprobar que entiendes las tres decisiones de arriba.

---

## 5. Patrón bandera: ¿alguno cumple? ¿todos cumplen?

**Señal:** "si hay algún", "si existe", "si todos", "si ninguno", "comprueba que".

Una **bandera** es una variable booleana que empieza en un valor y **solo cambia en un sentido** cuando ocurre algo.

### "¿Hay alguno...?"

Empieza en `False`; si encuentras uno, pasa a `True`.

```python
hay_agotado = False
for stock in [5, 3, 0, 8]:
    if stock == 0:
        hay_agotado = True
# True
```

### "¿Todos cumplen...?"

Empieza en `True`; si encuentras uno que **no** cumple, pasa a `False`. Es la versión al revés: para saber si todos cumplen, buscas un
contraejemplo.

```python
todos_positivos = True
for x in [4, 7, -1, 3]:
    if x <= 0:
        todos_positivos = False
# False
```

### El error clásico: la bandera que vuelve atrás

```python
for stock in stocks:
    if stock == 0:
        hay_agotado = True
    else:
        hay_agotado = False     # MAL: el siguiente elemento borra lo encontrado
```

Con un `else` que la devuelve a su valor inicial, la bandera solo refleja el **último** elemento. **Una bandera nunca tiene `else`**
dentro del bucle.

### Salir antes: `return` dentro del bucle

Dentro de una función, en cuanto sabes la respuesta puedes devolverla y dejar de recorrer:

```python
def todos_positivos(numeros):
    for x in numeros:
        if x <= 0:
            return False        # ya hay un contraejemplo: no hace falta seguir
    return True                 # el bucle terminó sin encontrar ninguno
```

Fíjate dónde está cada `return`: el `return False` **dentro** del `if` y el `return True` **después** del bucle, fuera. Si pones el
`return True` dentro del bucle (en un `else`), la función respondería mirando solo el primer elemento.

Y un detalle de lógica: con una lista **vacía**, "¿todos cumplen?" es `True` (no hay ninguno que no cumpla) y "¿alguno cumple?" es
`False`. Las versiones con bandera y con `return` dan eso automáticamente.

Python tiene `any()` y `all()` para esto mismo: `any(s == 0 for s in stocks)` y `all(x > 0 for x in numeros)`.

---

## 6. Patrón búsqueda: encontrar el primero que...

**Señal:** "el primero que", "la posición de", "encuentra", "devuelve el índice".

Es una bandera que, además de decir si lo encontró, **guarda qué o dónde**:

```python
def primera_vocal(texto):
    for i, letra in enumerate(texto):
        if letra in "aeiou":
            return i                # posición de la primera vocal
    return -1                       # convención habitual: -1 si no hay

primera_vocal("xyzab")    # 3
primera_vocal("xyz")      # -1
```

- `enumerate` da a la vez la **posición** y el **elemento**.
- Decide qué devolver si no se encuentra: `-1` para posiciones, `None` para elementos. Pero **decídelo y documéntalo**: que la función
  no devuelva nada por accidente es un error.

### Buscar comparando con lo ya visto

Algunos problemas preguntan por relaciones entre elementos: "el primer duplicado", "¿hay dos que suman X?". La técnica es **recordar lo
visto en un conjunto o diccionario** mientras recorres. Ejemplo con otra pregunta: ¿qué palabra ya apareció con otra mayúscula?

```python
def repetida_sin_mayusculas(palabras):
    vistas = set()
    for p in palabras:
        clave = p.lower()
        if clave in vistas:         # primero se consulta...
            return p
        vistas.add(clave)           # ...y después se guarda
    return None

repetida_sin_mayusculas(["Hola", "mundo", "HOLA"])    # "HOLA"
```

El orden "consultar y después guardar" es esencial: si guardaras primero, cada palabra se encontraría a sí misma. Buscar en un `set` es
casi instantáneo, mucho más que buscar en una lista (lo verás en *Algoritmos y estructuras de datos*).

---

## 7. Patrón agrupar: un contador o acumulador por categoría

**Señal:** "por cada", "por categoría", "cuántos de cada", "agrupa".

Es un contador (o acumulador), pero con **uno por clave**, guardados en un diccionario:

```python
ventas = [("lunes", 20), ("martes", 15), ("lunes", 5)]
por_dia = {}
for dia, importe in ventas:
    if dia not in por_dia:
        por_dia[dia] = 0            # crear la clave la primera vez
    por_dia[dia] += importe
# {"lunes": 25, "martes": 15}
```

La parte que se olvida es **crear la clave antes de sumar**: `por_dia[dia] += importe` con una clave nueva da `KeyError`. Dos formas
equivalentes más cortas:

```python
por_dia[dia] = por_dia.get(dia, 0) + importe     # get con valor por defecto
```

```python
from collections import defaultdict
por_dia = defaultdict(int)                        # las claves nuevas empiezan en 0
por_dia[dia] += importe
```

Para agrupar en listas (por ejemplo, los nombres de cada departamento), el valor inicial de cada clave es `[]` y se usa `append`.

---

## 8. Cómo reconocer el patrón en un enunciado

| El enunciado dice... | Patrón | Valor inicial |
|---|---|---|
| "cuántos..." | Contador | `0` |
| "total", "suma", "promedio" | Acumulador | `0` (y un contador si hay promedio) |
| "lista de los que..." | Acumulador en lista | `[]` |
| "el mayor / menor / más..." | Máximo / mínimo | El primer elemento (y comprobar vacío) |
| "si hay algún..." | Bandera | `False` |
| "si todos..." | Bandera inversa | `True` |
| "el primero que... / la posición de..." | Búsqueda | Devolver al encontrar; valor por defecto al final |
| "por cada categoría..." | Agrupar | `{}` |

Muchos problemas **combinan** patrones. "El promedio de las notas aprobadas y el nombre del mejor alumno" son un acumulador con
contador y un máximo, en el mismo bucle o en dos bucles separados (dos bucles seguidos suelen ser más claros, y para listas pequeñas la
diferencia de velocidad no importa).

---

## 9. Casos borde que debes probar siempre

Antes de dar un ejercicio por terminado, pruébalo mentalmente (o con `print`) con:

| Caso | Por qué |
|---|---|
| Colección **vacía** | ¿El máximo devuelve `None`? ¿El promedio divide entre cero? |
| **Un solo** elemento | ¿El máximo empieza y termina en él? |
| **Todos iguales** / empates | ¿Gana el primero o el último? |
| **Negativos** o cero | ¿Empezaste el máximo en 0 por error? |
| El elemento buscado **al principio** y **al final** | ¿El bucle llega hasta el último? |
| **Ninguno** cumple la condición | ¿Qué se devuelve? |

Son exactamente los casos que comprueban las pruebas de los ejercicios. Si los piensas antes, aciertas a la primera más a menudo.

---

## Resumen del capítulo

| Patrón | Plantilla | Error típico |
|---|---|---|
| Contador | `n = 0` → `if ...: n += 1` | Sumar el elemento en vez de 1 |
| Acumulador | `total = 0` / `[]` / `""` → añadir | Inicializar dentro del bucle; dividir entre cero |
| Máximo / mínimo | `mejor = lista[0]` → reemplazar si es mejor | Empezar en 0; no comprobar la lista vacía |
| Bandera | `False` (alguno) / `True` (todos) → cambia en un sentido | Un `else` que la devuelve atrás |
| Búsqueda | `return` al encontrar; valor por defecto al final | `return` por defecto dentro del bucle |
| Agrupar | `{}` → crear la clave → actualizar | `KeyError` por no crear la clave |

## Autoevaluación final

1. Para contar cuántas palabras empiezan por "a", ¿qué se suma en cada vuelta?
2. ¿Con qué valor empieza un acumulador de **producto** y por qué?
3. Buscas la temperatura máxima de `[-3, -8, -1]` empezando con `maximo = 0`. ¿Qué devuelve y por qué está mal?
4. En el patrón máximo, ¿qué comparación hace que en un empate gane el primero?
5. ¿Qué devuelve "¿todos son pares?" con una lista vacía?
6. ¿Por qué una bandera no debe tener `else` dentro del bucle?
7. Al agrupar en un diccionario, ¿qué error aparece si haces `conteo[clave] += 1` con una clave nueva?

**Respuestas:** 1) 1 (el contador suma uno por cada palabra que cumple). 2) Con 1: si empezara en 0, cualquier producto daría 0.
3) Devuelve 0, que ni siquiera está en la lista: ningún valor supera al 0 inicial. El valor inicial debe ser el primer elemento
(que daría −1). 4) `>` (estrictamente mayor): uno igual no reemplaza al que ya estaba. 5) `True`: no hay ningún elemento que
lo incumpla. 6) Porque el `else` la devolvería a su valor inicial con el siguiente elemento, y solo reflejaría el último. 7) `KeyError`:
hay que crear la clave antes (o usar `get` o `defaultdict`).
