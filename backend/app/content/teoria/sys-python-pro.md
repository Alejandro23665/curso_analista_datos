# Python profesional: tipos, clases, módulos y pruebas

Hasta ahora has escrito funciones sueltas. Eso basta para un script de 50 líneas, pero un sistema real (la API de tu chatbot, el
backend de un cliente, tu MVP) tiene miles de líneas que escriben y cambian varias personas durante meses. Para que ese código siga
siendo comprensible y no se rompa con cada cambio, los equipos profesionales usan un conjunto de herramientas que vas a aprender aquí:

- **Anotaciones de tipo** (*type hints*): documentar y verificar qué tipo de dato espera cada cosa.
- **Clases y dataclasses**: agrupar datos con el comportamiento que les corresponde.
- **Propiedades y excepciones propias**: proteger las reglas de negocio.
- **Generadores**: procesar datos enormes sin agotar la memoria.
- **Context managers** (`with`): garantizar que los recursos se liberen pase lo que pase.
- **Módulos, paquetes y entornos virtuales**: organizar un proyecto.
- **Pruebas con pytest**: la red de seguridad que te deja cambiar código sin miedo.

FastAPI, Pydantic, SQLAlchemy y los SDK de los modelos de IA usan todas estas piezas. Cuando las leas en su documentación, sabrás qué
estás viendo.

---

## 1. Anotaciones de tipo (type hints)

Una anotación de tipo indica **qué tipo de valor** espera un parámetro y qué tipo devuelve una función:

```python
def precio_final(precio: float, descuento: float = 0.0) -> float:
    return precio * (1 - descuento)
```

- `precio: float` → el parámetro `precio` debería ser un `float`.
- `-> float` → la función devuelve un `float`.

También se pueden anotar variables: `edad: int = 30`.

### Tipos compuestos

```python
def promedio(notas: list[float]) -> float: ...
def contar(palabras: list[str]) -> dict[str, int]: ...
def coordenada() -> tuple[float, float]: ...
def buscar(email: str) -> dict | None: ...      # puede devolver un dict o None
```

- `list[str]`: una lista de textos. `dict[str, int]`: un diccionario de texto a entero.
- `X | None`: "un X o `None`". Verás también la forma antigua, `Optional[X]`, que significa lo mismo.
- Una función que no devuelve nada se anota `-> None`.

### Lo más importante: Python NO las comprueba al ejecutar

```python
def doble(x: int) -> int:
    return x * 2

print(doble("ab"))    # abab   (ningún error)
```

Las anotaciones son **información**, no reglas que Python haga cumplir. Entonces, ¿para qué sirven?

1. **Documentan**: quien lee `def enviar(mensaje: str, reintentos: int = 3) -> bool` entiende la función sin leer su cuerpo.
2. **Tu editor** las usa para autocompletar y subrayar errores mientras escribes.
3. **Herramientas como `mypy`** revisan todo el proyecto antes de ejecutarlo y detectan llamadas incorrectas.
4. **Librerías como FastAPI y Pydantic sí las usan en ejecución**: leen las anotaciones para validar los datos que llegan a tu API. Si
   un endpoint declara `edad: int` y el cliente manda `"hola"`, FastAPI responde con un error 422 automáticamente.

A partir de aquí, anota tus funciones. Es una costumbre que se nota mucho en una prueba técnica.

---

## 2. Clases desde cero

Una **clase** es un molde para crear objetos que **agrupan datos y las funciones que trabajan con esos datos**. Ya usaste muchos
objetos: un texto es un objeto de la clase `str`, y `.upper()` es una de sus funciones (llamadas **métodos**).

### Definir una clase

```python
class Reserva:
    def __init__(self, huesped, noches, precio_noche):
        self.huesped = huesped
        self.noches = noches
        self.precio_noche = precio_noche

    def total(self):
        return self.noches * self.precio_noche
```

### Crear objetos (instancias) y usarlos

```python
r1 = Reserva("Ana", 3, 40.0)
r2 = Reserva("Luis", 1, 55.0)

print(r1.huesped)     # Ana
print(r1.total())     # 120.0
print(r2.total())     # 55.0
```

`r1` y `r2` son dos **instancias** de la misma clase: tienen la misma estructura pero sus propios datos.

### Las piezas que confunden

- **`__init__`** es el método que Python ejecuta automáticamente al crear un objeto (`Reserva("Ana", 3, 40.0)`). Ahí se guardan los
  datos iniciales.
- **`self`** es el propio objeto. Cuando llamas `r1.total()`, Python ejecuta `Reserva.total(r1)`: `self` es `r1`. Por eso todos los
  métodos llevan `self` como primer parámetro, y por eso dentro de ellos se accede a los datos como `self.noches`.
- **`self.noches = noches`**: a la izquierda, un **atributo** del objeto (vive mientras viva el objeto); a la derecha, el **parámetro**
  (desaparece al terminar `__init__`). Tienen el mismo nombre por convención, pero son cosas distintas.

### Métodos que modifican el objeto

```python
class Reserva:
    def __init__(self, huesped, noches, precio_noche):
        self.huesped = huesped
        self.noches = noches
        self.precio_noche = precio_noche

    def total(self):
        return self.noches * self.precio_noche

    def extender(self, noches_extra):
        self.noches += noches_extra

r = Reserva("Ana", 3, 40.0)
r.extender(2)
print(r.noches, r.total())    # 5 200.0
```

### Mostrar y comparar objetos

Si imprimes un objeto de una clase normal, verás algo poco útil como `<__main__.Reserva object at 0x7f...>`, y dos reservas con los
mismos datos **no** se consideran iguales con `==`. Para arreglarlo habría que escribir los métodos especiales `__repr__` y `__eq__`.
En la práctica, para clases que son sobre todo datos, existe una forma mucho más cómoda: las dataclasses.

---

## 3. Dataclasses: clases de datos sin repetir código

```python
from dataclasses import dataclass

@dataclass
class Reserva:
    huesped: str
    noches: int
    precio_noche: float

    def total(self) -> float:
        return self.noches * self.precio_noche
```

El decorador `@dataclass` (la línea con `@` encima de la clase) lee las anotaciones de los atributos y **genera automáticamente**
`__init__`, `__repr__` y `__eq__`:

```python
r = Reserva("Ana", 3, 40.0)
print(r)                                   # Reserva(huesped='Ana', noches=3, precio_noche=40.0)
print(r == Reserva("Ana", 3, 40.0))        # True
print(Reserva(huesped="Luis", noches=1, precio_noche=55.0).total())   # 55.0
```

### Valores por defecto

```python
@dataclass
class Reserva:
    huesped: str
    noches: int
    precio_noche: float
    desayuno: bool = False           # valor por defecto
```

Igual que en las funciones, los campos con valor por defecto van **después** de los que no lo tienen.

### Listas y diccionarios como valor por defecto: `field(default_factory=...)`

¿Recuerdas la trampa del valor por defecto mutable del capítulo anterior? En una dataclass, Python directamente **no te deja** escribir
`= []`:

```python
@dataclass
class Grupo:
    nombre: str
    miembros: list[str] = []
```

```
ValueError: mutable default <class 'list'> for field miembros is not allowed: use default_factory
```

La forma correcta es `field(default_factory=list)`: le dices "para cada objeto nuevo, llama a `list()` y crea una lista nueva":

```python
from dataclasses import dataclass, field

@dataclass
class Grupo:
    nombre: str
    miembros: list[str] = field(default_factory=list)

a = Grupo("Python")
b = Grupo("SQL")
a.miembros.append("Ana")
print(b.miembros)     # []   (cada grupo tiene su propia lista)
```

### Validar al crear: `__post_init__`

Si necesitas comprobar los datos al crear el objeto, la dataclass llama a `__post_init__` justo después de su `__init__` automático:

```python
@dataclass
class Reserva:
    huesped: str
    noches: int
    precio_noche: float

    def __post_init__(self):
        if self.noches <= 0:
            raise ValueError("Una reserva necesita al menos una noche")
```

### Objetos inmutables: `frozen=True`

`@dataclass(frozen=True)` impide modificar los atributos después de crear el objeto. Útil para valores que no deben cambiar, como una
coordenada o una configuración.

---

## 4. Encapsulación y propiedades

Una regla de negocio (por ejemplo, "el stock nunca puede ser negativo") solo se respeta si nadie puede saltársela cambiando el atributo
directamente. Python no tiene atributos realmente privados, pero sí **convenciones** y **herramientas**.

### La convención del guion bajo

Un atributo que empieza con `_` significa: *"esto es interno, no lo toques desde fuera"*. Python no lo impide, pero cualquier
programador lo entiende y lo respeta.

### `@property`: un atributo calculado o de solo lectura

```python
class Termostato:
    def __init__(self):
        self._temperatura = 20.0

    @property
    def temperatura(self):
        return self._temperatura

    def subir(self, grados):
        if grados <= 0:
            raise ValueError("Los grados deben ser positivos")
        self._temperatura += grados

t = Termostato()
t.subir(2)
print(t.temperatura)    # 22.0  (se lee como un atributo, sin paréntesis)
t.temperatura = 99      # AttributeError: no tiene setter
```

`@property` convierte un método en algo que **se lee como un atributo**. Como no hay forma de asignarle un valor, la única manera de
cambiar la temperatura es a través de `subir`, que valida. Así la regla de negocio queda protegida.

Una propiedad también sirve para valores **calculados**:

```python
@dataclass
class Rectangulo:
    ancho: float
    alto: float

    @property
    def area(self) -> float:
        return self.ancho * self.alto

print(Rectangulo(3, 4).area)    # 12
```

---

## 5. Herencia y composición, en lo justo

**Herencia:** una clase puede basarse en otra y heredar sus atributos y métodos:

```python
class Notificacion:
    def __init__(self, destino):
        self.destino = destino

    def enviar(self, texto):
        raise NotImplementedError

class Email(Notificacion):
    def enviar(self, texto):
        print(f"Email a {self.destino}: {texto}")

class SMS(Notificacion):
    def enviar(self, texto):
        print(f"SMS a {self.destino}: {texto[:160]}")

for aviso in [Email("ana@correo.com"), SMS("+58 412 0000000")]:
    aviso.enviar("Tu pedido salió")
```

Cada subclase implementa `enviar` a su manera, y el código que las usa no necesita saber cuál es cuál.

**Composición:** en lugar de heredar, un objeto **contiene** a otros (`Pedido` tiene una lista de `LineaPedido`). Es más flexible y es
lo que se usa la mayoría de las veces. Regla práctica: usa herencia cuando la relación sea claramente "es un tipo de" (un `Email` *es
una* `Notificacion`) y composición cuando sea "tiene" (un `Pedido` *tiene* líneas).

Lo que más vas a usar de la herencia, sin embargo, es lo de la siguiente sección: crear tus propias excepciones.

---

## 6. Excepciones propias

Las excepciones de Python (`ValueError`, `KeyError`...) son genéricas. Las reglas de negocio merecen **errores con nombre propio**,
porque el código que llama puede distinguirlos y reaccionar a cada uno de forma distinta.

### Crear una excepción

Basta con una clase que herede de `Exception`:

```python
class CupoAgotado(Exception):
    pass
```

### Lanzarla

```python
class Curso:
    def __init__(self, nombre, cupo):
        self.nombre = nombre
        self.cupo = cupo
        self._inscritos = []

    def inscribir(self, alumno):
        if len(self._inscritos) >= self.cupo:
            raise CupoAgotado(f"El curso {self.nombre} ya tiene {self.cupo} alumnos")
        self._inscritos.append(alumno)
```

El mensaje entre paréntesis aparece en el traceback y explica qué pasó. Escríbelo pensando en quien tendrá que depurarlo.

### Capturarla de forma específica

```python
curso = Curso("Python", cupo=1)
curso.inscribir("Ana")
try:
    curso.inscribir("Luis")
except CupoAgotado as error:
    print("Lista de espera:", error)
```

`except CupoAgotado as error` guarda la excepción en la variable `error`; al imprimirla, muestra su mensaje.

### Cuándo usar cuál

- **`ValueError`**: el valor recibido no tiene sentido (cantidad negativa, texto vacío). Es un error de quien llamó.
- **Tu excepción propia**: una regla del negocio impide la operación aunque los datos sean válidos (no hay cupo, no hay saldo, el pedido
  ya se envió).
- **`TypeError`**: el tipo es incorrecto (Python suele lanzarla solo).

---

## 7. Iteradores y generadores

### Qué hace un `for` por dentro

Un `for` funciona con cualquier objeto **iterable** (listas, textos, diccionarios, archivos, `range`...). Por dentro, Python pide un
**iterador** con `iter()` y le va pidiendo el siguiente elemento con `next()` hasta que se agota:

```python
iterador = iter(["a", "b"])
print(next(iterador))    # a
print(next(iterador))    # b
print(next(iterador))    # StopIteration: ya no quedan
```

### Generadores: funciones que producen valores de uno en uno

Una función con `yield` en lugar de `return` es un **generador**. No calcula todos los resultados de golpe: entrega **un valor cada vez
que se le pide** y se queda en pausa hasta la siguiente petición.

```python
def cuenta_regresiva(desde):
    while desde > 0:
        yield desde
        desde -= 1

for n in cuenta_regresiva(3):
    print(n)
```

```
3
2
1
```

Qué pasa paso a paso: el `for` pide un valor; la función se ejecuta hasta el primer `yield` y entrega `3`; se **pausa** recordando
dónde estaba. El `for` pide otro; la función continúa justo después del `yield`, resta 1, vuelve al `while` y entrega `2`. Y así hasta
que la función termina, lo que pone fin al bucle.

### Por qué importan: memoria y datos infinitos

Una lista guarda **todos** sus elementos en memoria. Un generador solo guarda **dónde va**. Eso permite:

- Procesar un archivo de 50 GB línea a línea (un archivo abierto ya es un iterador).
- Recorrer páginas de una API una a una.
- Representar secuencias **infinitas**:

```python
def numeros_pares():
    n = 0
    while True:          # nunca termina por sí solo...
        yield n
        n += 2

for p in numeros_pares():
    if p > 6:
        break            # ...pero quien lo usa decide cuándo parar
    print(p)             # 0 2 4 6
```

Nunca intentes `list(numeros_pares())`: intentaría guardar infinitos números y el programa se colgaría. Con generadores, la regla es
**consumir solo lo que necesitas**.

### Tomar solo unos cuantos: `itertools.islice`

El módulo `itertools` tiene herramientas para trabajar con iteradores. `islice(iterable, n)` toma como mucho `n` elementos sin
consumir el resto:

```python
from itertools import islice

primeros = list(islice(numeros_pares(), 4))
print(primeros)     # [0, 2, 4, 6]
```

Ojo: `islice` **avanza** el iterador que le pasas. Si llamas varias veces a `islice` sobre el **mismo iterador** (no sobre la lista
original), cada llamada continúa donde se quedó la anterior. Para conseguir eso, convierte primero el iterable en iterador con `iter()`.

### Expresiones generadoras

Como una comprensión de lista pero con paréntesis: produce los valores bajo demanda.

```python
total = sum(x * x for x in range(1_000_000))   # no crea una lista de un millón de elementos
```

---

## 8. Context managers: `with`

Ya usaste `with open(...)`. Un **context manager** es cualquier objeto que sabe hacer algo **al entrar** en un bloque `with` y algo
**al salir**, salga como salga: normalmente, por un `return` o por una excepción. Se usa para todo lo que hay que **liberar o deshacer**:
archivos, conexiones a bases de datos, transacciones, bloqueos.

### Crear uno con una clase

```python
import time

class Cronometro:
    def __enter__(self):
        self.inicio = time.perf_counter()
        return self                         # lo que se asigna con "as"

    def __exit__(self, tipo, valor, traza):
        duracion = time.perf_counter() - self.inicio
        print(f"Tardó {duracion:.3f} s")
        return False                        # no "tragarse" la excepción, si la hubo

with Cronometro():
    sum(range(1_000_000))
```

- `__enter__` se ejecuta al entrar. Lo que devuelve es lo que recibes en `with ... as variable`.
- `__exit__` se ejecuta **siempre** al salir. Recibe tres valores: si el bloque terminó bien, los tres son `None`; si hubo una
  excepción, reciben su tipo, la excepción y la traza.
- Si `__exit__` devuelve `False` (o nada), la excepción **sigue propagándose** después de ejecutar tu código de limpieza. Si devolviera
  `True`, la excepción se "tragaría" y el programa seguiría como si nada, algo que casi nunca quieres.

Así puedes reaccionar distinto según haya habido error o no:

```python
class Registro:
    def __enter__(self):
        print("Inicio de la operación")
        return self

    def __exit__(self, tipo, valor, traza):
        if tipo is None:
            print("Terminó bien")
        else:
            print(f"Falló con {tipo.__name__}: {valor}")
        return False

with Registro():
    int("abc")
```

```
Inicio de la operación
Falló con ValueError: invalid literal for int() with base 10: 'abc'
Traceback (most recent call last): ...
```

### La forma corta: `@contextmanager`

Para casos sencillos, el módulo `contextlib` permite escribir un context manager como un generador: lo de antes del `yield` es la
entrada; lo de después, la salida.

```python
from contextlib import contextmanager

@contextmanager
def seccion(nombre):
    print(f"--- {nombre} ---")
    try:
        yield
    finally:
        print(f"--- fin de {nombre} ---")
```

### Copias superficiales y profundas

Si un context manager (o cualquier código) necesita **guardar una foto** de unos datos para poder restaurarlos después, cuidado con las
copias. `d.copy()` hace una copia **superficial**: si el diccionario contiene listas, la copia y el original comparten esas listas.
`copy.deepcopy(d)` copia también todo lo que hay dentro:

```python
import copy

original = {"tags": ["a"]}
superficial = original.copy()
profunda = copy.deepcopy(original)
original["tags"].append("b")
print(superficial["tags"])   # ['a', 'b']   (comparte la lista)
print(profunda["tags"])      # ['a']        (independiente)
```

Y para **restaurar** un diccionario "en su sitio" (de modo que quien tenga una referencia a él vea el cambio), no reasignes la variable:
vacíalo con `d.clear()` y vuelve a llenarlo con `d.update(foto)`.

---

## 9. Módulos, paquetes y entornos

### Módulos y paquetes

- Un **módulo** es un archivo `.py`. Si tienes `precios.py` con una función `con_iva`, desde otro archivo de la misma carpeta haces
  `from precios import con_iva`.
- Un **paquete** es una carpeta de módulos (tradicionalmente con un archivo `__init__.py`). Permite `from tienda.precios import
  con_iva`.

Organiza los proyectos **por dominio**, no por tipo de archivo:

```
mi_api/
├── pedidos/
│   ├── modelos.py
│   ├── servicio.py
│   └── rutas.py
├── usuarios/
│   └── ...
└── tests/
    └── test_pedidos.py
```

### `if __name__ == "__main__":`

Cuando Python ejecuta un archivo directamente, la variable especial `__name__` vale `"__main__"`. Cuando el archivo se **importa**,
vale el nombre del módulo. Esto permite que un archivo sea a la vez una librería importable y un script ejecutable:

```python
def con_iva(precio):
    return precio * 1.16

if __name__ == "__main__":
    print(con_iva(100))    # solo se ejecuta con: python precios.py
```

### Entornos virtuales y dependencias

Cada proyecto necesita sus propias librerías en versiones concretas. Un **entorno virtual** es una carpeta con un Python aislado para
ese proyecto:

```bash
python -m venv .venv                 # crear el entorno (una vez)
.venv\Scripts\activate               # activarlo en Windows (en Linux/Mac: source .venv/bin/activate)
pip install fastapi pytest           # instalar dentro del entorno
pip freeze > requirements.txt        # guardar las versiones exactas
pip install -r requirements.txt      # reinstalarlas en otro equipo
```

Reglas: **un entorno por proyecto**, nunca subas la carpeta `.venv` a Git (va en el `.gitignore`) y **sí** sube el `requirements.txt`
(o `pyproject.toml`), para que cualquiera pueda reproducir tu entorno.

---

## 10. Pruebas automáticas con pytest

Una **prueba** es código que ejecuta tu código con una entrada conocida y comprueba que el resultado es el esperado. Los ejercicios de
esta plataforma funcionan exactamente así: tu función se ejecuta contra unas pruebas escondidas. Ahora vas a escribir las tuyas.

### La prueba más simple

```python
# archivo: reservas.py
def total(noches, precio_noche):
    return noches * precio_noche
```

```python
# archivo: test_reservas.py
from reservas import total

def test_total_varias_noches():
    assert total(3, 40.0) == 120.0

def test_total_cero_noches():
    assert total(0, 40.0) == 0
```

```bash
pytest
```

pytest busca automáticamente los archivos `test_*.py` y, dentro, las funciones `test_*`, las ejecuta y te dice cuáles pasaron. `assert
condición` hace fallar la prueba si la condición es falsa, y pytest te muestra qué valores tenía cada lado.

### La estructura de una buena prueba: preparar, actuar, comprobar

```python
def test_extender_reserva_suma_noches():
    reserva = Reserva("Ana", 3, 40.0)       # preparar
    reserva.extender(2)                     # actuar
    assert reserva.noches == 5              # comprobar
```

Una prueba = un comportamiento. El nombre debe decir qué comportamiento se prueba: cuando falle, sabrás qué se rompió sin abrirla.

### Probar que algo falla cuando debe

Las reglas de negocio se prueban también por el lado del error:

```python
import pytest

def test_inscribir_sin_cupo_lanza_error():
    curso = Curso("Python", cupo=1)
    curso.inscribir("Ana")
    with pytest.raises(CupoAgotado):
        curso.inscribir("Luis")
```

`pytest.raises` (que es un context manager) hace que la prueba **pase solo si** el bloque lanza esa excepción.

### Muchos casos, una prueba: `parametrize`

```python
@pytest.mark.parametrize("noches", [0, -1, -10])
def test_reserva_noches_invalidas(noches):
    with pytest.raises(ValueError):
        Reserva("Ana", noches, 40.0)
```

pytest ejecuta la prueba una vez por cada valor de la lista.

### Qué probar

1. **El caso normal** (el que todos prueban).
2. **Los casos borde**: vacío, cero, uno, negativos, el límite exacto (`cupo` justo lleno).
3. **Los errores**: que se lancen las excepciones correctas con datos inválidos.

No hace falta probar que Python sabe sumar. Prueba **tu lógica**: tus reglas y tus decisiones. Con pruebas, cuando cambias el código
(o cuando lo cambia un agente de IA), ejecutas `pytest` y sabes en segundos si rompiste algo.

---

## 11. Errores típicos de este capítulo

| Síntoma | Causa | Solución |
|---|---|---|
| `TypeError: __init__() takes 3 positional arguments but 4 were given` | Olvidaste `self` en un método | Todos los métodos llevan `self` primero |
| `NameError: name 'noches' is not defined` dentro de un método | Usaste `noches` en lugar de `self.noches` | Los atributos se leen con `self.` |
| `ValueError: mutable default ... use default_factory` | `= []` en una dataclass | `field(default_factory=list)` |
| `AttributeError: can't set attribute` | Asignaste a una `@property` sin setter | Usa el método que valida |
| Tu generador no hace nada | Llamaste a la función pero no recorriste el resultado | Recórrelo con `for`, `next()` o `list()` |
| El programa se cuelga | `list()` sobre un generador infinito | Consume solo lo necesario (`islice`, `break`) |
| La excepción desaparece | `__exit__` devuelve `True` | Devuelve `False` para propagarla |
| La "foto" de los datos cambió | Copia superficial de datos anidados | `copy.deepcopy` |
| `ModuleNotFoundError` | Librería no instalada o entorno sin activar | Activa el entorno y `pip install` |

---

## Resumen del capítulo

| Herramienta | Para qué | Clave |
|---|---|---|
| Type hints | Documentar y verificar tipos | Python no las comprueba; mypy, el editor y FastAPI sí |
| Clase | Agrupar datos y comportamiento | `__init__`, `self`, atributos, métodos |
| `@dataclass` | Clases de datos sin código repetido | `field(default_factory=list)`, `__post_init__` |
| `@property` | Atributos calculados o de solo lectura | Proteger reglas de negocio |
| Excepción propia | Errores de negocio con nombre | `class X(Exception)`, `raise X("mensaje")` |
| Generador | Producir valores bajo demanda | `yield`; no cargues todo en memoria |
| Context manager | Liberar o deshacer siempre | `__enter__` / `__exit__`; devolver `False` propaga |
| Paquetes y venv | Organizar y aislar proyectos | Por dominio; `requirements.txt` |
| pytest | Red de seguridad | `assert`, `pytest.raises`, `parametrize` |

## Autoevaluación final

1. ¿Qué pasa si llamas a `def f(x: int)` con un texto?
2. ¿Qué es `self` en un método?
3. ¿Qué genera automáticamente `@dataclass`?
4. ¿Por qué no se puede escribir `etiquetas: list = []` en una dataclass y qué se usa en su lugar?
5. ¿Para qué sirve `@property`?
6. ¿Qué diferencia hay entre `return` y `yield`?
7. ¿Qué recibe `__exit__` cuando el bloque termina sin errores? ¿Y qué pasa si devuelve `True`?
8. ¿Cómo compruebas con pytest que una función lanza una excepción?

**Respuestas:** 1) Se ejecuta igual: Python no comprueba las anotaciones. 2) El propio objeto sobre el que se llama el método.
3) `__init__`, `__repr__` y `__eq__`. 4) Porque la lista se compartiría entre todos los objetos; se usa `field(default_factory=list)`.
5) Para exponer un valor calculado o de solo lectura como si fuera un atributo. 6) `return` termina la función y entrega un valor;
`yield` entrega un valor y pausa la función, que continúa en la siguiente petición. 7) Recibe `None` en sus tres parámetros; si devuelve
`True`, cualquier excepción del bloque se suprime. 8) Con `with pytest.raises(TipoDeExcepcion):` alrededor de la llamada.

En la práctica vas a construir una dataclass con reglas de negocio, una clase con su propia excepción y una propiedad de solo lectura,
un generador que funcione incluso con iterables infinitos y un context manager que deshaga los cambios si algo falla.
