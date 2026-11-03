# Leer, depurar y revisar código (también el generado por IA)

Escribir código es cada vez más barato: un asistente de IA genera en segundos una función que antes costaba una hora. Lo que se ha
vuelto valioso es todo lo demás:

- **Leer** código que no escribiste y entender qué hace.
- **Encontrar por qué falla** un programa (depurar).
- **Decidir si un cambio es correcto** antes de aceptarlo (revisar).

En tu primer empleo pasarás más tiempo leyendo y depurando que escribiendo desde cero. En una entrevista asistida por IA, esto es
exactamente lo que evalúan. Y en tus proyectos freelance, es lo que separa una entrega que funciona de una que falla delante del cliente.

---

## 1. Leer código que no escribiste

Leer código es una habilidad que se entrena, igual que leer en otro idioma. No se lee de arriba abajo como una novela: se lee **de fuera
hacia dentro**.

### Estrategia para leer una función

1. **El nombre y la firma**: `def calcular_envio(pedido: dict, zona: str) -> float`. Antes de mirar el cuerpo ya sabes qué recibe y qué
   devuelve.
2. **Los `return`**: ¿qué devuelve y en qué casos? A menudo hay varios.
3. **Las condiciones**: ¿qué caminos distintos puede seguir?
4. **Los bucles**: ¿qué recorre y qué acumula?
5. **Ejecútala mentalmente con un ejemplo pequeño**, apuntando cómo cambian las variables.

### Trazar a mano: la técnica más útil

**Trazar** es seguir el programa línea a línea con unos datos concretos, anotando el valor de cada variable. Es lo que hace un
depurador, pero en papel, y te obliga a entender cada línea.

```python
def promedio_positivos(numeros):
    total = 0
    cantidad = 0
    for n in numeros:
        if n > 0:
            total += n
            cantidad += 1
    return total / cantidad
```

Traza con `[4, -2, 6]`:

| Paso | `n` | ¿`n > 0`? | `total` | `cantidad` |
|---|---|---|---|---|
| inicio | | | 0 | 0 |
| vuelta 1 | 4 | sí | 4 | 1 |
| vuelta 2 | -2 | no | 4 | 1 |
| vuelta 3 | 6 | sí | 10 | 2 |
| `return` | | | 10 / 2 = **5.0** | |

Ahora traza con `[-1, -3]`: `cantidad` termina en 0 y `total / cantidad` lanza `ZeroDivisionError`. Trazando con un caso borde
encontraste un bug sin ejecutar nada. **Siempre traza al menos un caso normal y un caso borde** (vacío, todo negativo, un solo
elemento).

### Leer un proyecto nuevo

Cuando entras a un repositorio que no conoces (en un trabajo nuevo o en el proyecto de un cliente):

1. **El README**: qué hace el proyecto y cómo se ejecuta.
2. **El punto de entrada**: dónde empieza (`main.py`, `app/main.py`, el `CMD` del Dockerfile).
3. **Las pruebas**: muestran cómo se supone que se usa cada pieza y qué casos importan.
4. **Sigue un caso de uso completo**: por ejemplo, qué pasa desde que llega una petición `POST /pedidos` hasta que se guarda en la base de
   datos.
5. **Ejecútalo** y prueba cosas. Leer sin ejecutar es mucho más lento.

---

## 2. Tracebacks a fondo

En el capítulo de fundamentos aprendiste a leer un traceback de abajo arriba. Ahora veamos casos más realistas.

### Un traceback con varias llamadas

```
Traceback (most recent call last):
  File "main.py", line 22, in <module>
    informe = generar_informe(pedidos)
  File "main.py", line 15, in generar_informe
    envio = calcular_envio(p)
  File "envios.py", line 8, in calcular_envio
    return pedido["peso_kg"] * TARIFA
KeyError: 'peso_kg'
```

Cada bloque `File ..., line ..., in ...` es una **llamada**, de la más externa (arriba) a la más interna (abajo), donde ocurrió el error.
Léelo así:

1. **Qué pasó** (última línea): un diccionario no tiene la clave `'peso_kg'`.
2. **Dónde** (bloque de abajo): `envios.py`, línea 8, dentro de `calcular_envio`.
3. **Cómo se llegó ahí** (hacia arriba): `generar_informe` llamó a `calcular_envio` con un pedido `p`, y a su vez la llamó el programa
   principal.

La pregunta de depuración ya no es "¿qué falla?" sino **"¿por qué ese pedido llegó sin `peso_kg`?"**. La causa real suele estar más
arriba que la línea que explota: en los datos o en quien construyó ese diccionario.

### Cuando el error ocurre dentro de una librería

Si las últimas líneas del traceback están en archivos de una librería (`site-packages/...`), el error casi nunca es de la librería: es lo
que **tú** le pasaste. Busca hacia arriba **la última línea que sea de tu código**: ahí está la llamada con datos incorrectos.

### Excepciones encadenadas

```
ValueError: invalid literal for int() with base 10: 'N/A'

During handling of the above exception, another exception occurred:
...
```

Si ves *"During handling of the above exception"*, hubo **dos** errores: uno dentro de un bloque `except` que intentaba manejar el
primero. Normalmente el que importa es **el primero**, que es la causa original.

### Excepciones que verás a diario

| Excepción | Significado | Pregunta que debes hacerte |
|---|---|---|
| `KeyError: 'x'` | El diccionario no tiene esa clave | ¿De dónde viene ese diccionario y por qué le falta? |
| `IndexError` | Posición fuera de la lista | ¿La lista estaba vacía? ¿Me pasé por uno? |
| `AttributeError: 'NoneType' object has no attribute 'x'` | Algo que esperabas que fuera un objeto es `None` | ¿Qué función devolvió `None`? (a menudo, falta un `return`) |
| `TypeError: unsupported operand type(s)` | Operación entre tipos incompatibles | ¿Ese valor era texto (de un CSV, de un formulario)? |
| `ValueError` | Tipo correcto, valor inválido | ¿Qué valor exacto llegó? |
| `ZeroDivisionError` | División entre cero | ¿Puede estar vacío el conjunto del que calculo el promedio? |

El `AttributeError` con `NoneType` merece atención especial: es probablemente el error más frecuente de Python. Significa que una
variable vale `None` cuando esperabas otra cosa. Busca la función que la produjo: casi siempre le falta un `return` o devuelve `None` en
algún caso que no previste.

---

## 3. El método para depurar

Depurar no es cambiar cosas al azar hasta que funcione. Es un método, parecido al científico:

### Paso 1: reproducir

Consigue que el fallo ocurra **cuando tú quieras**. Si no puedes reproducirlo, no puedes saber si lo arreglaste. Anota los pasos y los
datos exactos.

### Paso 2: reducir

Busca **el caso más pequeño** que todavía falla. Si falla con un CSV de 10 000 filas, ¿falla con 10? ¿Con 1? ¿Con qué fila concreta?
Cuanto más pequeño, más fácil ver la causa.

### Paso 3: formular una hipótesis

Una explicación concreta y comprobable: *"creo que la página 1 muestra los elementos de la 2 porque el índice inicial se calcula como si
las páginas empezaran en 0"*. No "algo está mal en la paginación".

### Paso 4: comprobar la hipótesis

Con datos, no con intuición: imprime las variables clave, usa el depurador, ejecuta con un ejemplo cuyo resultado conoces. Si la
hipótesis era falsa, descártala y formula otra.

### Paso 5: corregir y escribir una prueba

Corrige la causa (no el síntoma) y escribe una **prueba que falle sin tu corrección y pase con ella**. Así ese error no vuelve nunca, ni
aunque alguien (o un agente de IA) toque ese código dentro de seis meses.

### Paso 6: preguntarte "¿dónde más?"

Si cometiste este error aquí, ¿lo cometiste en otro sitio? Los bugs vienen en familias.

---

## 4. Herramientas para comprobar hipótesis

### `print`, bien usado

El método más antiguo y todavía útil. Dos trucos:

```python
total = 42
nombre = "Ana"
print(f"{total=}, {nombre=}")      # total=42, nombre='Ana'   (el = muestra nombre y valor)
print(f"{type(total)=}")           # type(total)=<class 'int'>
```

Imprime en los **puntos de decisión**: antes de un `if`, en cada vuelta de un bucle, justo antes del `return`. Y **bórralos** cuando
termines: un `print` de depuración olvidado en producción da mala imagen.

### `logging`: prints que se quedan

En aplicaciones reales se usa el módulo `logging`, que permite niveles (`DEBUG`, `INFO`, `WARNING`, `ERROR`) y activar o desactivar el
detalle sin tocar el código:

```python
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info("Procesando %d pedidos", 120)
log.warning("Pedido %s sin peso, uso 1 kg", 1042)
```

### `breakpoint()`: detener el programa y explorar

Escribe `breakpoint()` en una línea y ejecuta el programa: se detendrá ahí y te dará una consola interactiva (el depurador `pdb`) donde
puedes inspeccionar todo:

| Comando | Qué hace |
|---|---|
| `p variable` | Muestra el valor de una variable |
| `n` | Ejecuta la siguiente línea (*next*) |
| `s` | Entra dentro de la función que se llama en esta línea (*step*) |
| `c` | Continúa hasta el siguiente `breakpoint` (*continue*) |
| `l` | Muestra el código alrededor (*list*) |
| `q` | Sale (*quit*) |

Los editores como VS Code tienen un depurador visual que hace lo mismo con clics: pones un punto rojo junto a una línea, ejecutas en modo
depuración y ves todas las variables en un panel. Aprende a usarlo pronto: ahorra horas.

### `assert`: comprobar lo que crees que es verdad

```python
def aplicar_descuento(precio, porcentaje):
    assert 0 <= porcentaje <= 100, f"porcentaje fuera de rango: {porcentaje}"
    return precio * (1 - porcentaje / 100)
```

Si la condición es falsa, el programa se detiene con un `AssertionError` y tu mensaje. Útil para detectar pronto supuestos que no se
cumplen. (No lo uses para validar datos de usuarios en producción: los `assert` se pueden desactivar; para eso, `raise ValueError`.)

---

## 5. Aislar el fallo cuando no sabes dónde está

### Dividir por la mitad

Si un programa largo falla y no sabes dónde, comprueba el estado de los datos **a mitad del proceso**. ¿Ya está mal ahí? El error está en
la primera mitad; si no, en la segunda. Repite. En pocas rondas acotas el problema a unas líneas.

### `git bisect`: ¿qué commit lo rompió?

Si algo funcionaba la semana pasada y hoy no, Git puede encontrar el commit culpable por búsqueda binaria:

```bash
git bisect start
git bisect bad                 # el commit actual está mal
git bisect good a1b2c3d        # este commit antiguo estaba bien
# Git te lleva a un commit intermedio; lo pruebas y le dices:
git bisect good                # o: git bisect bad
# ...repites hasta que Git te dice cuál fue el primer commit malo
git bisect reset
```

Con 100 commits entre "bien" y "mal", lo encuentras en unas 7 pruebas. Es otra razón para hacer commits pequeños: el culpable será un
cambio pequeño y fácil de entender.

---

## 6. Catálogo de errores clásicos

Estos errores aparecen una y otra vez, en código humano y en código generado por IA. Aprende a reconocerlos por su **síntoma**.

### Fuera por uno (*off-by-one*)

**Síntoma:** falta o sobra el primer o el último elemento; un rango se queda corto; "la página 1 muestra la página 2".

**Causa:** confundir dónde empieza el conteo (0 o 1) o si un límite se incluye. Recuerda: los índices empiezan en 0, `range(a, b)` no
incluye `b` y `lista[a:b]` tampoco. Cuando un humano habla de "la página 1" o "el primer elemento", el código suele necesitar la
posición 0.

**Cómo detectarlo:** traza los **extremos**: el primer elemento, el último, la primera página.

### Valor por defecto mutable

**Síntoma:** una función "recuerda" datos de llamadas anteriores.

**Causa:** `def f(x, lista=[])`: la lista se crea una sola vez y se comparte entre llamadas (lo viste en *Python para datos*).

### Modificar una lista mientras se recorre

**Síntoma:** el bucle se salta elementos, sin dar ningún error.

**Causa:** al borrar un elemento, los siguientes se desplazan una posición, y el bucle avanza a la siguiente sin haber mirado el que
ocupó el hueco. Pasa sobre todo con elementos **consecutivos** que hay que borrar.

**Regla:** no modifiques (añadiendo o borrando) la colección que estás recorriendo. Construye una nueva.

### Dos nombres para la misma lista

**Síntoma:** una lista "cambia sola" o una función modifica datos que no debía.

**Causa:** `b = a` o pasar una lista a una función no copia nada.

### Slicing con cero o negativos

**Síntoma:** pides "los últimos 0 elementos" y te devuelve todos.

**Causa:** `lista[-n:]` con `n = 0` es `lista[-0:]`, y `-0` es `0`, así que es `lista[0:]`: la lista entera. Los índices negativos
tienen sus propias reglas en los bordes; prueba siempre `n = 0`.

### Operadores que parecen correctos

**Síntoma:** un acumulador termina con el último valor en lugar de la suma.

**Causa:** `total =+ p` en lugar de `total += p`. Python lo acepta, porque significa `total = (+p)`: asigna `p` con signo positivo. No
da error; simplemente hace otra cosa. Lo mismo con `=` en lugar de `==` en lugares donde ambos son válidos.

### Porcentajes al revés

**Síntoma:** un "10 % de descuento" deja el 10 % del precio.

**Causa:** multiplicar por `0.10` en lugar de por `0.90` (o por `1 - 0.10`). Pruébalo siempre con un número redondo: 100 con 10 % de
descuento tiene que dar 90.

### `return` en el sitio equivocado

**Síntoma:** una función que debía procesar toda la lista solo procesa el primer elemento.

**Causa:** el `return` está indentado **dentro** del bucle, así que la función termina en la primera vuelta.

### Funciones que devuelven `None`

**Síntoma:** `AttributeError: 'NoneType' object has no attribute ...` o una variable que vale `None`.

**Causa:** falta un `return`, hay un camino del `if` sin `return`, o guardaste el resultado de un método que modifica en su sitio
(`lista = lista.sort()`).

### Tipos que parecen números

**Síntoma:** `"10" + "5"` da `"105"`; ordenar `["10", "9"]` da `["10", "9"]` porque compara texto.

**Causa:** el valor vino de un CSV, un formulario o una API como texto. Convierte al leer.

### Pisar nombres de Python

**Síntoma:** `TypeError: 'list' object is not callable` al hacer `list(...)`.

**Causa:** antes escribiste `list = [1, 2, 3]` y "tapaste" la función `list`. No uses como nombres de variable `list`, `dict`, `str`,
`sum`, `max`, `id`, `input`.

### Comparar decimales con `==`

**Síntoma:** `0.1 + 0.2 == 0.3` es `False`.

**Causa:** la representación binaria de los decimales. Compara con una tolerancia: `abs(a - b) < 1e-9`, o usa `round`.

---

## 7. Revisar código generado por IA

El código de un asistente **suele funcionar en el caso feliz** (el ejemplo típico) y fallar en los bordes. Además, escribe con mucha
seguridad incluso cuando se equivoca. Revisarlo bien es tu trabajo, y en una entrevista asistida por IA, la principal señal que te
evalúan.

### Lista de revisión

1. **¿Hace exactamente lo que se pidió?** Compara con el requisito, punto por punto. Los asistentes a veces "mejoran" cosas que no les
   pediste o se saltan un requisito.
2. **Casos borde**: vacío, cero, uno, negativos, duplicados, `None`, textos con espacios o mayúsculas, el primer y el último elemento.
3. **Seguridad**:
   - SQL construido con f-strings o concatenación (`f"... WHERE email = '{email}'"`): permite **inyección SQL**. Los valores van siempre
     como **parámetros** aparte (`cur.execute("... WHERE email = %s", (email,))`).
   - Secretos escritos en el código.
   - Datos del usuario usados sin validar.
4. **Dependencias**: ¿existe de verdad ese paquete? ¿Hacía falta? Los modelos a veces inventan nombres de librerías, y hay atacantes que
   publican paquetes con esos nombres inventados.
5. **Manejo de errores**: ¿captura excepciones con `except:` a secas y esconde problemas? ¿Qué pasa si la API externa falla?
6. **Rendimiento**: ¿un bucle dentro de otro bucle sobre datos grandes? ¿Una consulta a la base de datos dentro de un bucle?
7. **Pruebas**: ¿las pruebas comprueban de verdad el comportamiento, o solo que "no explota"? Que las pruebas pasen **no** significa que
   el código sea correcto ni seguro: solo que cumple lo que esas pruebas miran.
8. **¿Puedes explicarlo línea por línea?** Si no, todavía no es tuyo. Pide al asistente que te lo explique o reescríbelo.

### Cómo pedirle a un asistente que revise

Un truco útil: después de que genere código, pídele explícitamente *"busca errores, casos borde no tratados y problemas de seguridad en
el código que acabas de escribir"*. Una segunda pasada con ese foco encuentra muchos problemas. Pero la decisión final es tuya.

---

## 8. Requisitos vagos y reportes de bugs

### Muchos bugs son malentendidos

Un requisito como "que el reporte salga bien" o "que la paginación funcione" se puede programar de diez formas. Antes de escribir
código, convierte el requisito en **ejemplos concretos de entrada y salida**:

> "Con 10 elementos y 3 por página: la página 1 son los elementos 1 a 3, la página 4 tiene solo el elemento 10 y la página 5 está vacía.
> ¿Y la página 0? ¿Error o lista vacía?"

Esos ejemplos se convierten luego en tus pruebas.

### Cómo reportar un bug (o pedir ayuda)

Cuando reportes un fallo a un compañero, a un cliente o en un foro, incluye:

1. **Qué hiciste**: los pasos exactos para reproducirlo.
2. **Qué esperabas** que pasara.
3. **Qué pasó en realidad**, con el mensaje de error completo (copiado como texto, no una foto).
4. **El entorno**: versión de Python, sistema operativo, versión de la librería.
5. **El caso mínimo** que lo reproduce, si lo tienes.

Un buen reporte suele resolverse en minutos; uno malo ("no funciona"), en días. Escribirlo bien, además, a menudo te hace encontrar la
solución por ti mismo mientras lo redactas.

---

## Resumen del capítulo

| Habilidad | Lo esencial |
|---|---|
| Leer código | De fuera hacia dentro: firma, `return`, condiciones, bucles; traza un caso normal y uno borde |
| Tracebacks | Última línea: qué pasó; bloque de abajo: dónde; hacia arriba: cómo se llegó. Busca tu última línea |
| Método | Reproducir, reducir, hipótesis, comprobar, corregir con prueba, buscar casos similares |
| Herramientas | `print(f"{x=}")`, `logging`, `breakpoint()`, depurador del editor, `assert`, `git bisect` |
| Errores clásicos | Fuera por uno, valor por defecto mutable, modificar al recorrer, alias, `=+`, `return` mal indentado, `None` |
| Revisar IA | Requisitos, bordes, seguridad (SQL parametrizado), dependencias, errores, rendimiento, pruebas, explicarlo |
| Comunicación | Requisitos como ejemplos; reportes con pasos, esperado, obtenido, entorno |

## Autoevaluación final

1. En un traceback largo, ¿dónde está normalmente la causa del error?
2. ¿Qué significa `AttributeError: 'NoneType' object has no attribute 'append'`?
3. ¿Cuáles son los pasos del método de depuración?
4. ¿Qué hace `total =+ precio` y por qué no da error?
5. ¿Por qué `lista[-n:]` falla cuando `n` es 0?
6. Un asistente genera una consulta SQL con un f-string y las pruebas pasan. ¿Es aceptable?
7. ¿Qué debe tener la prueba que escribes al corregir un bug?
8. ¿Qué cinco cosas incluye un buen reporte de bug?

**Respuestas:** 1) Muchas veces antes de la línea que explota: en los datos o en quien los preparó; empieza por la última línea de tu
código. 2) Que la variable sobre la que llamaste `.append` vale `None`: alguna función no devolvió lo esperado. 3) Reproducir, reducir,
formular una hipótesis, comprobarla, corregir con una prueba y buscar casos parecidos. 4) Asigna `+precio` (el mismo valor) en lugar de
sumarlo; es sintaxis válida. 5) Porque `-0` es `0` y `lista[0:]` es la lista completa. 6) No: permite inyección SQL; los valores van como
parámetros. 7) Que falle sin la corrección y pase con ella. 8) Pasos, resultado esperado, resultado obtenido (con el error completo),
entorno y un caso mínimo.

En la práctica vas a recibir funciones con errores realistas (algunas "escritas por un asistente") y tendrás que encontrarlos y
corregirlos. Usa el método: traza con un ejemplo pequeño y con los casos borde antes de cambiar nada.
