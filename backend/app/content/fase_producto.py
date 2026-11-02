from ._helpers import checklist, py, quiz, sql

TOPICS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "sys-python-pro",
        "phase": "producto",
        "title": "Python profesional: tipos, clases, módulos y pruebas",
        "summary": "Type hints, dataclasses, clases y excepciones propias, generadores, context managers, paquetes y pytest.",
        "hours": 10,
        "theory": r"""
# Python profesional: tipos, clases, módulos y pruebas

Para construir sistemas que duren no basta con que el código funcione: tiene que ser **legible, probable y fácil de cambiar**.
Este tema cubre las herramientas de Python que separan un script de un sistema.

## 1. Type hints (anotaciones de tipo)

```python
def total_pedido(precios: list[float], descuento: float = 0.0) -> float:
    return sum(precios) * (1 - descuento)
```

Python **no** las comprueba al ejecutar, pero tu editor y herramientas como `mypy` sí: detectan errores antes de producción y documentan el código.
FastAPI y Pydantic las usan para validar datos automáticamente.

## 2. Clases y dataclasses

Una clase agrupa **datos y comportamiento**. Si la clase es sobre todo datos, usa `@dataclass` y te ahorras escribir `__init__`, `__repr__` y `__eq__`:

```python
from dataclasses import dataclass, field

@dataclass
class Producto:
    nombre: str
    precio: float
    stock: int = 0
    etiquetas: list[str] = field(default_factory=list)   # nunca un [] directo como valor por defecto

    def valor_inventario(self) -> float:
        return self.precio * self.stock
```

`@property` expone un atributo calculado o de solo lectura. Mantén las clases **pequeñas y con una responsabilidad**.

## 3. Excepciones propias

Las reglas de negocio merecen errores con nombre: el código que llama puede distinguirlos.

```python
class SaldoInsuficiente(Exception):
    pass

if monto > self._saldo:
    raise SaldoInsuficiente(f"Saldo {self._saldo} menor que {monto}")
```

## 4. Generadores: procesar datos sin cargarlos todos

`yield` produce valores **uno a uno** y bajo demanda. Sirve para leer archivos enormes o paginar una API sin agotar la memoria.

```python
def leer_lineas(ruta):
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            yield linea.rstrip("\n")
```

## 5. Context managers (`with`)

Garantizan que algo se **libere o se deshaga** aunque haya un error: archivos, conexiones, transacciones, bloqueos.
Se crean con una clase (`__enter__` / `__exit__`) o con `@contextmanager`. Si `__exit__` recibe una excepción, puedes deshacer cambios.

## 6. Módulos, paquetes y entornos

- Un archivo `.py` es un módulo; una carpeta con módulos es un paquete. Organiza por **dominio** (`pedidos/`, `usuarios/`), no por tipo de archivo.
- Usa siempre un **entorno virtual** por proyecto y fija dependencias (`requirements.txt` o `pyproject.toml`).
- `if __name__ == "__main__":` separa el código que se ejecuta como script del que se importa.

## 7. Pruebas con pytest

```python
# test_inventario.py
import pytest
from inventario import Producto

def test_valor_inventario():
    assert Producto("Lápiz", 2.0, stock=10).valor_inventario() == 20.0

@pytest.mark.parametrize("cantidad", [0, -1, 11])
def test_vender_cantidad_invalida(cantidad):
    with pytest.raises(ValueError):
        Producto("Lápiz", 2.0, stock=10).vender(cantidad)
```

Ejecuta `pytest` y se descubren solas las funciones `test_*`. Escribe pruebas **para la lógica de negocio y los casos borde**; son tu red de seguridad para cambiar el código sin miedo.

## Cómo sabes que dominas este tema

- Modelas una entidad con `@dataclass`, métodos y excepciones propias.
- Usas generadores y context managers donde corresponden.
- Escribes pruebas con pytest, incluidas las de casos de error.
""",
        "exercises": [
            py("pro-dataclass", "Un producto con reglas de negocio", "Sistemas: Python profesional",
               "Completa la `@dataclass` `Producto` (`nombre`, `precio`, `stock` con valor por defecto 0). Añade `valor_inventario()` que devuelva `precio * stock` "
               "y `vender(cantidad)` que reste del stock. `vender` debe lanzar `ValueError` si la cantidad es menor o igual a 0 o mayor que el stock disponible.",
               starter="""
from dataclasses import dataclass

@dataclass
class Producto:
    # define los campos y los métodos
    pass
""",
               solution="""
from dataclasses import dataclass

@dataclass
class Producto:
    nombre: str
    precio: float
    stock: int = 0

    def valor_inventario(self) -> float:
        return self.precio * self.stock

    def vender(self, cantidad: int) -> None:
        if cantidad <= 0 or cantidad > self.stock:
            raise ValueError("Cantidad no valida")
        self.stock -= cantidad
""",
               tests="""
p = Producto("Lapiz", 2.0, stock=10)
assert p.valor_inventario() == 20.0, "2.0 x 10 = 20.0"
p.vender(3)
assert p.stock == 7, "Tras vender 3 deben quedar 7"
assert Producto("Goma", 1.0).stock == 0, "El stock por defecto es 0"
for cantidad in (0, -1, 8):
    try:
        p.vender(cantidad)
    except ValueError:
        pass
    else:
        raise AssertionError("vender(%d) debe lanzar ValueError" % cantidad)
assert p.stock == 7, "Una venta invalida no debe cambiar el stock"
""",
               hint="Declara los campos con tipo dentro de la clase: nombre: str, precio: float, stock: int = 0."),
            py("pro-excepcion", "Cuenta con excepción propia", "Sistemas: Python profesional",
               "Crea la excepción `SaldoInsuficiente` y la clase `Cuenta`: empieza con saldo 0, tiene `depositar(monto)` (lanza `ValueError` si el monto no es positivo), "
               "`retirar(monto)` (lanza `ValueError` si no es positivo y `SaldoInsuficiente` si supera el saldo) y una propiedad de solo lectura `saldo`.",
               starter="""
class SaldoInsuficiente(Exception):
    pass

class Cuenta:
    # tu código aquí
    pass
""",
               solution="""
class SaldoInsuficiente(Exception):
    pass

class Cuenta:
    def __init__(self):
        self._saldo = 0

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self._saldo += monto

    def retirar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self._saldo:
            raise SaldoInsuficiente("Saldo insuficiente")
        self._saldo -= monto
""",
               tests="""
c = Cuenta()
assert c.saldo == 0
c.depositar(100)
c.retirar(30)
assert c.saldo == 70, "100 - 30 = 70"
try:
    c.retirar(500)
except SaldoInsuficiente:
    pass
else:
    raise AssertionError("Retirar mas del saldo debe lanzar SaldoInsuficiente")
for operacion in (c.depositar, c.retirar):
    try:
        operacion(0)
    except ValueError:
        pass
    else:
        raise AssertionError("Montos no positivos deben lanzar ValueError")
try:
    c.saldo = 1000
except AttributeError:
    pass
else:
    raise AssertionError("saldo debe ser de solo lectura (usa @property)")
assert c.saldo == 70
""",
               hint="Guarda el saldo en self._saldo y exponlo con @property sin setter."),
            py("pro-generador", "Generador por lotes", "Sistemas: Python profesional",
               "Escribe el **generador** `por_lotes(iterable, n)` que entregue (con `yield`) listas de hasta `n` elementos, en orden. Debe funcionar con cualquier iterable, "
               "incluso uno infinito: no puede convertir todo el iterable en lista de golpe.",
               starter="""
def por_lotes(iterable, n):
    # tu código aquí (usa yield)
    pass
""",
               solution="""
def por_lotes(iterable, n):
    lote = []
    for elemento in iterable:
        lote.append(elemento)
        if len(lote) == n:
            yield lote
            lote = []
    if lote:
        yield lote
""",
               tests="""
import itertools
import types
assert isinstance(por_lotes([1, 2, 3], 2), types.GeneratorType), "Debe ser un generador (usa yield)"
assert list(por_lotes(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]
assert list(por_lotes([], 3)) == []
infinito = por_lotes(itertools.count(), 2)
assert next(infinito) == [0, 1] and next(infinito) == [2, 3], "Debe funcionar con un iterable infinito"
""",
               hint="Acumula en una lista; al llegar a n elementos haz yield y empieza una nueva. Al final, entrega lo que quede."),
            py("pro-contexto", "Context manager transaccional", "Sistemas: Python profesional",
               "Escribe la clase `Transaccion(datos)` para usar con `with`: si el bloque termina bien, los cambios hechos a `datos` (un diccionario) se conservan; "
               "si ocurre una excepción, `datos` vuelve a su estado original y la excepción se propaga. `__enter__` devuelve el propio diccionario.",
               starter="""
import copy

class Transaccion:
    def __init__(self, datos):
        self.datos = datos

    # implementa __enter__ y __exit__
""",
               solution="""
import copy

class Transaccion:
    def __init__(self, datos):
        self.datos = datos

    def __enter__(self):
        self._copia = copy.deepcopy(self.datos)
        return self.datos

    def __exit__(self, tipo, valor, traza):
        if tipo is not None:
            self.datos.clear()
            self.datos.update(self._copia)
        return False
""",
               tests="""
cuentas = {"ana": 100, "luis": 50}
with Transaccion(cuentas) as c:
    c["ana"] -= 30
    c["luis"] += 30
assert cuentas == {"ana": 70, "luis": 80}, "Si todo va bien, los cambios se conservan"
try:
    with Transaccion(cuentas) as c:
        c["ana"] -= 500
        c["nuevo"] = 1
        raise RuntimeError("fallo a mitad")
except RuntimeError:
    pass
else:
    raise AssertionError("La excepcion debe propagarse (devuelve False en __exit__)")
assert cuentas == {"ana": 70, "luis": 80}, "Tras un error, los datos deben volver al estado original; obtuve %r" % (cuentas,)
""",
               hint="Guarda una copia profunda en __enter__; en __exit__, si tipo no es None, restaura con clear() + update()."),
            quiz("pro-quiz-hints", "Type hints en ejecución", "Sistemas: Python profesional",
                 "Tienes `def f(x: int) -> int: return x * 2` y llamas `f(\"ab\")`. ¿Qué pasa?",
                 ["Python lanza TypeError por el type hint", "Devuelve \"abab\": Python no comprueba los type hints al ejecutar; los usan el editor y herramientas como mypy",
                  "Devuelve None", "Error de sintaxis"], 1,
                 "Las anotaciones son información para herramientas y personas. Para validar en ejecución se usan librerías como Pydantic (lo que hace FastAPI)."),
            quiz("pro-quiz-default", "Valores por defecto en dataclasses", "Sistemas: Python profesional",
                 "¿Cómo declaras en una dataclass un campo lista vacía por defecto?",
                 ["etiquetas: list = []", "etiquetas: list = field(default_factory=list)", "etiquetas: list = None siempre", "No se puede"], 1,
                 "Un `[]` directo se compartiría entre instancias (dataclasses lo prohíbe). `default_factory` crea una lista nueva para cada objeto."),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "sys-apis",
        "phase": "producto",
        "title": "Diseño de APIs REST con FastAPI",
        "summary": "HTTP, recursos REST, códigos de estado, validación, paginación, errores, idempotencia y versionado.",
        "hours": 10,
        "theory": r"""
# Diseño de APIs REST con FastAPI

La API es el **contrato** entre tu backend y quien lo usa (tu frontend, una app móvil, otros sistemas). Una API bien diseñada es predecible;
una mal diseñada genera errores y trabajo extra durante años.

## 1. HTTP en lo esencial

| Método | Uso | ¿Idempotente? |
|---|---|---|
| `GET` | Leer | Sí |
| `POST` | Crear o ejecutar una acción | **No** |
| `PUT` | Reemplazar un recurso completo | Sí |
| `PATCH` | Modificar parte de un recurso | Depende |
| `DELETE` | Eliminar | Sí |

**Idempotente** = repetir la petición deja el sistema igual que hacerla una vez. Importa porque las redes fallan y los clientes reintentan.

## 2. Recursos y rutas

Las rutas nombran **cosas** (sustantivos en plural), no acciones:

- Bien: `GET /pedidos`, `GET /pedidos/42`, `POST /pedidos`, `GET /clientes/7/pedidos`
- Mal: `GET /obtenerPedidos`, `POST /crearPedidoNuevo`

Filtros, orden y paginación van en la *query string*: `GET /pedidos?estado=pagado&pagina=2&por_pagina=20`.

## 3. Códigos de estado

| Código | Cuándo |
|---|---|
| `200 OK` | Lectura o actualización correcta |
| `201 Created` | Se creó un recurso (devuelve el recurso o su URL) |
| `204 No Content` | Correcto, sin cuerpo (por ejemplo, un DELETE) |
| `400 / 422` | Datos de entrada inválidos (FastAPI usa 422 para errores de validación) |
| `401` | No autenticado (no sabemos quién eres) |
| `403` | Autenticado pero sin permiso |
| `404` | No existe (o no debes saber que existe) |
| `409 Conflict` | Choca con el estado actual (email ya registrado, versión desactualizada) |
| `429` | Demasiadas peticiones |
| `500` | Error del servidor: un bug tuyo, nunca culpa del cliente |

## 4. FastAPI y validación

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class UsuarioNuevo(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    email: EmailStr
    edad: int | None = Field(default=None, ge=13, le=120)

@app.post("/usuarios", status_code=201)
def crear_usuario(datos: UsuarioNuevo):
    if repositorio.existe_email(datos.email):
        raise HTTPException(409, "Ese email ya está registrado")
    return repositorio.crear(datos)
```

**Valida todo lo que entra** (nunca confíes en el frontend) y devuelve errores con un formato consistente. FastAPI genera además la
documentación interactiva en `/docs` a partir de los tipos.

## 5. Paginación

Nunca devuelvas una colección sin límite: con el tiempo crecerá y tumbará tu API. Opciones:

- **Por páginas** (`pagina`, `por_pagina`): simple; devuelve también `total` y `paginas`.
- **Por cursor** (`despues_de=<id>`): estable aunque se inserten filas mientras navegas; mejor para listas grandes o en tiempo real.

Limita `por_pagina` (por ejemplo, máximo 100).

## 6. Idempotencia en operaciones críticas

Un `POST /pagos` que se reintenta por un timeout **puede cobrar dos veces**. La solución estándar: el cliente envía una
`Idempotency-Key` única; el servidor guarda el resultado asociado a esa clave y, si llega repetida, devuelve el mismo resultado sin volver a ejecutar.

## 7. Evolución del contrato

- **Versiona** cuando rompas compatibilidad (`/v1/...`, `/v2/...`). Añadir campos opcionales no rompe; quitar o renombrar, sí.
- Usa nombres de campos consistentes (`snake_case` o `camelCase`, pero uno solo) y fechas en ISO 8601 con zona horaria.

## 8. Lo que pasa por debajo: redes en lo esencial

La pregunta clásica de entrevista junior es *"¿qué pasa cuando escribes una URL en el navegador?"*. La respuesta corta:

1. **DNS:** el navegador pregunta qué dirección IP corresponde a `midominio.com` (un registro `A` del dominio apunta a la IP del servidor).
   La respuesta se guarda en caché un tiempo, por eso la segunda visita es más rápida.
2. **TCP:** abre una conexión fiable con esa IP. Los datos viajan en paquetes numerados; si uno se pierde, se reenvía y llegan en orden.
   **UDP** no garantiza entrega ni orden, pero es más rápido (video, voz, juegos).
3. **TLS:** con `https`, se cifra la conexión y se verifica el certificado del servidor.
4. **HTTP:** el navegador envía la petición (método, ruta, **cabeceras** y, a veces, **cuerpo**) y el servidor responde con un código de estado,
   cabeceras y cuerpo. Puedes verlo en la pestaña *Network* de las herramientas del navegador.

**Cómo enviar datos del servidor al cliente en tiempo real:**

| Técnica | Cómo funciona | Cuándo usarla |
|---|---|---|
| *Polling* | El cliente pregunta cada X segundos "¿hay algo nuevo?" | Casos simples y poco frecuentes; desperdicia peticiones |
| **SSE** (*Server-Sent Events*) | Una petición HTTP que el servidor mantiene abierta y por la que envía eventos | Un solo sentido, servidor → cliente: **la respuesta de un chatbot con streaming** |
| **WebSockets** | Conexión bidireccional que queda abierta | Los dos lados envían en cualquier momento: chat entre personas, colaboración en vivo |

Otros formatos que verás nombrados: **GraphQL** (el cliente pide exactamente los campos que quiere en una sola consulta) y **gRPC**
(comunicación rápida entre servicios con mensajes binarios). Para tus proyectos, REST + SSE cubre casi todo.

## Cómo sabes que dominas este tema

- Explicas qué pasa desde que escribes una URL hasta que ves la página.
- Diseñas las rutas y los códigos de estado de un recurso sin dudar.
- Validas la entrada y paginas cualquier colección.
- Explicas cómo evitar cobros duplicados con una clave de idempotencia.
""",
        "exercises": [
            py("api-validar", "Validar un usuario nuevo", "Sistemas: diseño de APIs",
               "Escribe `validar_usuario(datos)` que reciba un diccionario y devuelva un diccionario de errores `{campo: mensaje}` (vacío si todo está bien). Reglas: "
               "`nombre` obligatorio, texto de 2 a 50 caracteres tras quitar espacios; `email` obligatorio, debe contener una `@` con texto antes y un punto después de la `@`; "
               "`edad` es opcional, pero si viene debe ser un entero entre 13 y 120.",
               starter="""
def validar_usuario(datos):
    errores = {}
    # tu código aquí
    return errores
""",
               solution="""
def validar_usuario(datos):
    errores = {}
    nombre = datos.get("nombre")
    if not isinstance(nombre, str) or not 2 <= len(nombre.strip()) <= 50:
        errores["nombre"] = "Debe tener entre 2 y 50 caracteres"
    email = datos.get("email")
    if not isinstance(email, str) or "@" not in email:
        errores["email"] = "Email no valido"
    else:
        usuario, _, dominio = email.partition("@")
        if not usuario or "." not in dominio:
            errores["email"] = "Email no valido"
    if "edad" in datos and datos["edad"] is not None:
        edad = datos["edad"]
        if not isinstance(edad, int) or isinstance(edad, bool) or not 13 <= edad <= 120:
            errores["edad"] = "Debe ser un entero entre 13 y 120"
    return errores
""",
               tests="""
assert validar_usuario({"nombre": "Ana", "email": "ana@correo.com"}) == {}, "Un usuario valido no tiene errores"
assert validar_usuario({"nombre": "Ana", "email": "ana@correo.com", "edad": 30}) == {}
errores = validar_usuario({"nombre": " A ", "email": "ana.correo.com", "edad": 9})
assert set(errores) == {"nombre", "email", "edad"}, "Esperaba errores en nombre, email y edad; obtuve %r" % (errores,)
assert "email" in validar_usuario({"nombre": "Ana", "email": "@correo.com"}), "Falta el texto antes de la @"
assert "email" in validar_usuario({"nombre": "Ana", "email": "ana@correo"}), "Falta el punto despues de la @"
assert set(validar_usuario({})) == {"nombre", "email"}, "Sin datos faltan nombre y email (edad es opcional)"
assert "edad" in validar_usuario({"nombre": "Ana", "email": "a@b.co", "edad": "30"}), "La edad debe ser un entero, no texto"
"""),
            py("api-paginar", "Paginación con metadatos", "Sistemas: diseño de APIs",
               "Escribe `paginar(items, pagina=1, por_pagina=20)` que devuelva `{'items': [...], 'pagina': p, 'por_pagina': n, 'total': t, 'paginas': k}`. "
               "Las páginas empiezan en 1. Lanza `ValueError` si `pagina < 1` o si `por_pagina` no está entre 1 y 100. Una página fuera de rango devuelve `items` vacío.",
               starter="""
import math

def paginar(items, pagina=1, por_pagina=20):
    # tu código aquí
    pass
""",
               solution="""
import math

def paginar(items, pagina=1, por_pagina=20):
    if pagina < 1 or not 1 <= por_pagina <= 100:
        raise ValueError("Parametros de paginacion no validos")
    total = len(items)
    inicio = (pagina - 1) * por_pagina
    return {
        "items": items[inicio:inicio + por_pagina],
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total": total,
        "paginas": math.ceil(total / por_pagina),
    }
""",
               tests="""
datos = list(range(1, 46))
r = paginar(datos, pagina=3, por_pagina=20)
assert r["items"] == list(range(41, 46)), "La pagina 3 de 20 en 20 contiene del 41 al 45"
assert (r["total"], r["paginas"], r["pagina"], r["por_pagina"]) == (45, 3, 3, 20)
assert paginar(datos, pagina=9)["items"] == [], "Fuera de rango devuelve una lista vacia"
assert paginar([], 1)["paginas"] == 0
for mal in ({"pagina": 0}, {"por_pagina": 0}, {"por_pagina": 101}):
    try:
        paginar(datos, **mal)
    except ValueError:
        pass
    else:
        raise AssertionError("%r debe lanzar ValueError" % (mal,))
"""),
            py("api-idempotencia", "Pagos con clave de idempotencia", "Sistemas: diseño de APIs",
               "Escribe la clase `ProcesadorPagos` con `procesar(clave, monto)`: la primera vez con una clave nueva, registra el cobro (suma `monto` a `total_cobrado`) "
               "y devuelve un id de pago `'pago-1'`, `'pago-2'`, ...; si la clave ya se usó, devuelve **el mismo id** sin volver a cobrar. "
               "Si se reutiliza una clave con un monto distinto, lanza `ValueError`.",
               starter="""
class ProcesadorPagos:
    def __init__(self):
        self.total_cobrado = 0
        # tu código aquí

    def procesar(self, clave, monto):
        pass
""",
               solution="""
class ProcesadorPagos:
    def __init__(self):
        self.total_cobrado = 0
        self._por_clave = {}

    def procesar(self, clave, monto):
        if clave in self._por_clave:
            pago_id, monto_original = self._por_clave[clave]
            if monto != monto_original:
                raise ValueError("Clave reutilizada con otro monto")
            return pago_id
        pago_id = "pago-%d" % (len(self._por_clave) + 1)
        self.total_cobrado += monto
        self._por_clave[clave] = (pago_id, monto)
        return pago_id
""",
               tests="""
p = ProcesadorPagos()
assert p.procesar("abc", 50) == "pago-1"
assert p.procesar("abc", 50) == "pago-1", "Reintentar con la misma clave devuelve el mismo pago"
assert p.total_cobrado == 50, "Un reintento no debe cobrar dos veces"
assert p.procesar("xyz", 20) == "pago-2"
assert p.total_cobrado == 70
try:
    p.procesar("abc", 999)
except ValueError:
    pass
else:
    raise AssertionError("Reutilizar una clave con otro monto debe lanzar ValueError")
"""),
            quiz("api-quiz-codigo", "Código de estado", "Sistemas: diseño de APIs",
                 "Un cliente intenta registrarse con un email que ya existe. ¿Qué código devuelves?",
                 ["200 OK con un mensaje de error", "409 Conflict", "500 Internal Server Error", "404 Not Found"], 1,
                 "La petición es válida en forma, pero choca con el estado actual del sistema. Un 500 indicaría un fallo tuyo, y un 200 engañaría al cliente."),
            quiz("api-quiz-rutas", "Nombrar rutas", "Sistemas: diseño de APIs",
                 "¿Qué ruta sigue mejor las convenciones REST para listar los pedidos de un cliente?",
                 ["POST /obtenerPedidosCliente", "GET /clientes/7/pedidos", "GET /pedidos/listar?cliente=7&accion=ver", "GET /cliente_pedidos_7"], 1,
                 "Las rutas nombran recursos y su relación; el método HTTP indica la acción."),
            quiz("api-quiz-401", "401 o 403", "Sistemas: diseño de APIs",
                 "Un usuario con sesión válida pide `DELETE /proyectos/9`, pero el proyecto pertenece a otra persona. ¿Qué respondes?",
                 ["401 Unauthorized", "403 Forbidden (o 404 si no quieres revelar que existe)", "200 OK sin borrar nada", "500"], 1,
                 "401 significa 'no sé quién eres'. Aquí sabes quién es, pero no tiene permiso: 403. Algunas APIs devuelven 404 para no revelar recursos ajenos."),
            quiz("api-quiz-tiempo-real", "SSE o WebSockets", "Sistemas: diseño de APIs",
                 "Tu chatbot debe mostrar la respuesta del modelo a medida que se genera; el usuario solo envía un mensaje cada vez. ¿Qué usas?",
                 ["Polling cada 100 ms", "SSE: el servidor envía los fragmentos por una respuesta HTTP abierta",
                  "Una petición nueva por cada palabra", "UDP directamente desde el navegador"], 1,
                 "El flujo es de un solo sentido (servidor → cliente) mientras dura la respuesta: SSE es lo más simple. WebSockets se justifica cuando ambos lados envían en cualquier momento."),
            quiz("api-quiz-dns", "Qué hace el DNS", "Sistemas: diseño de APIs",
                 "Compraste un dominio para tu demo. ¿Qué tienes que configurar para que apunte a tu servidor?",
                 ["Un registro DNS (por ejemplo, tipo A con la IP o un CNAME al dominio que te da tu proveedor)", "El puerto TCP del navegador",
                  "Un certificado en el frontend", "Nada: los dominios se conectan solos"], 0,
                 "El DNS traduce el nombre del dominio a una dirección. Proveedores como Vercel te indican qué registro A o CNAME crear."),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "sys-bd-apps",
        "phase": "producto",
        "title": "Bases de datos para aplicaciones: transacciones, concurrencia e índices",
        "summary": "ACID, condiciones de carrera, bloqueo optimista, restricciones, el problema N+1, índices y migraciones.",
        "hours": 10,
        "theory": r"""
# Bases de datos para aplicaciones: transacciones, concurrencia e índices

En análisis casi solo lees datos. En una aplicación, **muchas personas escriben a la vez**, y ahí aparecen los errores más caros:
dinero duplicado, stock negativo, datos a medias. Este tema es lo que evita esos desastres.

## 1. Transacciones y ACID

Una transacción agrupa varias operaciones que deben ocurrir **todas o ninguna**:

```sql
BEGIN;
UPDATE cuentas SET saldo = saldo - 100 WHERE id = 1;
UPDATE cuentas SET saldo = saldo + 100 WHERE id = 2;
COMMIT;      -- o ROLLBACK si algo falla
```

**ACID:** Atomicidad (todo o nada), Consistencia (respeta las reglas), Aislamiento (las transacciones no se pisan), Durabilidad (lo confirmado sobrevive a un corte).

## 2. Condiciones de carrera: la "actualización perdida"

Dos peticiones leen `stock = 1` a la vez, ambas ven que hay stock y ambas venden. Resultado: stock −1. Soluciones:

- **Operación atómica en SQL:** `UPDATE productos SET stock = stock - 1 WHERE id = 7 AND stock >= 1` y comprobar cuántas filas cambió.
- **Bloqueo pesimista:** `SELECT ... FOR UPDATE` bloquea la fila hasta terminar la transacción.
- **Bloqueo optimista:** cada fila tiene una columna `version`; actualizas con `WHERE id = 7 AND version = 3` y, si no cambió ninguna fila, alguien se te adelantó: devuelves un **409** y el cliente reintenta.

## 3. Las restricciones son tu última línea de defensa

Valida en la aplicación, pero **declara las reglas también en la base**: `NOT NULL`, `UNIQUE` (email único), `FOREIGN KEY`, `CHECK (stock >= 0)`.
Si un bug o una carrera se cuela, la base lo rechaza en lugar de guardar datos corruptos.

## 4. El problema N+1

Con un ORM es fácil escribir sin darte cuenta:

```python
clientes = session.query(Cliente).all()          # 1 consulta
for c in clientes:
    print(c.nombre, len(c.pedidos))              # +1 consulta POR CLIENTE
```

Con 1000 clientes son 1001 consultas. La solución es pedir todo en una (un `JOIN` con `GROUP BY`, o la carga anticipada del ORM: `selectinload`, `joinedload`).
Activa el registro de consultas SQL en desarrollo para detectarlo.

## 5. Índices para aplicaciones

- Indexa las columnas por las que **buscas, unes y ordenas**: claves foráneas, `email`, `created_at`.
- **Índice compuesto:** `(cliente_id, created_at)` sirve para "pedidos de un cliente ordenados por fecha". El orden de las columnas importa: sirve para filtrar por `cliente_id` solo, pero no por `created_at` solo.
- Cada índice hace más lentas las escrituras: no indexes todo.
- `EXPLAIN ANALYZE` te dice si se usa.

## 6. Migraciones

El esquema evoluciona con el código. Usa **migraciones versionadas** (Alembic en Python): cada cambio es un archivo con su `upgrade` y `downgrade`, en Git y aplicado igual en todos los entornos.
Para no romper producción, haz cambios **compatibles hacia atrás**: primero añades la columna nueva, despliegas el código que la usa y solo después eliminas la vieja.

## 7. Otras prácticas

- Usa un **pool de conexiones**; no abras una conexión por petición.
- Guarda fechas con zona horaria (`timestamptz`) y dinero en enteros (centavos) o `NUMERIC`, nunca `float`.
- Haz copias de seguridad y **prueba restaurarlas**.

## Cómo sabes que dominas este tema

- Explicas una actualización perdida y tres formas de evitarla.
- Detectas un N+1 y lo reescribes en una consulta.
- Planificas una migración sin tiempo de inactividad.
""",
        "exercises": [
            sql("bd-n1", "Eliminar un N+1", "Sistemas: bases de datos para aplicaciones",
                "El código actual hace una consulta por cada cliente para contar sus pedidos. Escribe **una sola consulta** que devuelva `id`, `name` y `pedidos` "
                "(cuántos pedidos tiene, 0 si ninguno) de todos los clientes de `Chile`, ordenados por id.",
                "SELECT c.id, c.name, COUNT(o.id) AS pedidos FROM customers c LEFT JOIN orders o ON o.customer_id = c.id "
                "WHERE c.country = 'Chile' GROUP BY c.id, c.name ORDER BY c.id",
                starter="-- Antes: 1 consulta para los clientes + 1 por cada cliente\n-- Ahora: una sola consulta\nSELECT c.id, c.name,\nFROM customers c\n",
                ordered=True, hint="LEFT JOIN con orders, COUNT(o.id) y GROUP BY por cliente."),
            py("bd-transferir", "Transferencia atómica", "Sistemas: bases de datos para aplicaciones",
               "Escribe `transferir(cuentas, origen, destino, monto)`. `cuentas` es un diccionario `{nombre: saldo}`. Mueve `monto` de origen a destino. "
               "Lanza `ValueError` (sin modificar nada) si alguna cuenta no existe, si son la misma cuenta, si el monto no es positivo o si el saldo no alcanza.",
               starter="""
def transferir(cuentas, origen, destino, monto):
    # tu código aquí: valida TODO antes de modificar
    pass
""",
               solution="""
def transferir(cuentas, origen, destino, monto):
    if origen not in cuentas or destino not in cuentas:
        raise ValueError("Cuenta inexistente")
    if origen == destino:
        raise ValueError("Origen y destino iguales")
    if monto <= 0:
        raise ValueError("Monto no valido")
    if cuentas[origen] < monto:
        raise ValueError("Saldo insuficiente")
    cuentas[origen] -= monto
    cuentas[destino] += monto
""",
               tests="""
cuentas = {"ana": 100, "luis": 20}
transferir(cuentas, "ana", "luis", 30)
assert cuentas == {"ana": 70, "luis": 50}
for args in (("ana", "eva", 10), ("ana", "ana", 10), ("ana", "luis", 0), ("luis", "ana", 51)):
    antes = dict(cuentas)
    try:
        transferir(cuentas, *args)
    except ValueError:
        pass
    else:
        raise AssertionError("transferir%r debe lanzar ValueError" % (args,))
    assert cuentas == antes, "Una transferencia rechazada no debe modificar ninguna cuenta"
""",
               hint="Haz todas las validaciones primero; solo al final resta y suma."),
            py("bd-optimista", "Bloqueo optimista", "Sistemas: bases de datos para aplicaciones",
               "Escribe la excepción `ConflictoDeVersion` y la función `actualizar(registro, cambios, version_esperada)`. Si `registro['version']` no coincide con "
               "`version_esperada`, lanza `ConflictoDeVersion`. Si coincide, devuelve un **diccionario nuevo** con los cambios aplicados y la versión incrementada en 1 "
               "(sin modificar el original). Los cambios no pueden alterar `version` directamente.",
               starter="""
class ConflictoDeVersion(Exception):
    pass

def actualizar(registro, cambios, version_esperada):
    # tu código aquí
    pass
""",
               solution="""
class ConflictoDeVersion(Exception):
    pass

def actualizar(registro, cambios, version_esperada):
    if registro["version"] != version_esperada:
        raise ConflictoDeVersion("El registro cambio desde que lo leiste")
    nuevo = {**registro, **{k: v for k, v in cambios.items() if k != "version"}}
    nuevo["version"] = registro["version"] + 1
    return nuevo
""",
               tests="""
original = {"id": 7, "stock": 5, "version": 3}
nuevo = actualizar(original, {"stock": 4}, 3)
assert nuevo == {"id": 7, "stock": 4, "version": 4}, "Obtuve %r" % (nuevo,)
assert original == {"id": 7, "stock": 5, "version": 3}, "No modifiques el registro original"
try:
    actualizar(nuevo, {"stock": 1}, 3)
except ConflictoDeVersion:
    pass
else:
    raise AssertionError("Con una version desactualizada debe lanzar ConflictoDeVersion")
assert actualizar(nuevo, {"version": 99}, 4)["version"] == 5, "Los cambios no pueden fijar la version a mano"
"""),
            quiz("bd-quiz-carrera", "Evitar vender de más", "Sistemas: bases de datos para aplicaciones",
                 "Dos clientes compran la última unidad al mismo tiempo. ¿Qué consulta evita el stock negativo sin bloquear toda la tabla?",
                 ["SELECT stock y, si es mayor que 0, UPDATE stock = stock - 1 en otra consulta",
                  "UPDATE productos SET stock = stock - 1 WHERE id = 7 AND stock >= 1, y comprobar si cambió una fila",
                  "Borrar el producto al venderlo", "Usar un índice en stock"], 1,
                 "La comprobación y la resta ocurren en una sola operación atómica. Si no cambió ninguna fila, ya no había stock."),
            quiz("bd-quiz-indice", "Índice compuesto", "Sistemas: bases de datos para aplicaciones",
                 "Tienes un índice en `(cliente_id, created_at)`. ¿Qué consulta NO lo aprovecha bien?",
                 ["WHERE cliente_id = 5", "WHERE cliente_id = 5 ORDER BY created_at DESC", "WHERE created_at > '2026-01-01' (sin filtrar por cliente)", "WHERE cliente_id = 5 AND created_at > '2026-01-01'"], 2,
                 "Un índice compuesto se usa de izquierda a derecha. Sin filtrar por la primera columna, normalmente no sirve."),
            quiz("bd-quiz-dinero", "Guardar dinero", "Sistemas: bases de datos para aplicaciones",
                 "¿Qué tipo usarías para guardar precios y saldos?",
                 ["FLOAT", "NUMERIC(12, 2) o un entero en centavos", "TEXT", "DATE"], 1,
                 "Los float tienen errores de redondeo (0.1 + 0.2 ≠ 0.3). Para dinero se usa decimal exacto o enteros en la unidad mínima."),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "sys-seguridad",
        "phase": "producto",
        "title": "Autenticación y seguridad web",
        "summary": "Contraseñas, sesiones y JWT, permisos, inyección SQL, XSS, CSRF, secretos y las fallas más comunes (OWASP).",
        "hours": 10,
        "theory": r"""
# Autenticación y seguridad web

En una startup, una brecha de seguridad puede acabar con la confianza de tus clientes en un día. La buena noticia: **la mayoría de los ataques
explotan errores conocidos y evitables**. Este tema cubre los que más se repiten.

## 1. Autenticación vs autorización

- **Autenticación:** ¿quién eres? (inicio de sesión).
- **Autorización:** ¿qué puedes hacer? (permisos).

El fallo más común en aplicaciones reales es de **autorización**: comprobar que el usuario inició sesión, pero no que el recurso que pide es suyo
(`GET /facturas/1043` muestra la factura de otra persona). Se llama **IDOR**. Comprueba la propiedad **en cada endpoint**.

## 2. Contraseñas

- **Nunca** las guardes en texto plano ni con MD5/SHA-256 simple: se rompen en segundos con diccionarios.
- Usa un algoritmo **lento y con sal**: Argon2 o bcrypt (en Python, `argon2-cffi` o `passlib`); `PBKDF2` como alternativa estándar.
- La **sal** es aleatoria por usuario: dos contraseñas iguales producen hashes distintos.
- Compara con tiempo constante (`hmac.compare_digest`).
- Limita los intentos de inicio de sesión y ofrece 2FA para cuentas sensibles.

## 3. Sesiones o JWT

| | Cookie de sesión | JWT |
|---|---|---|
| Dónde vive el estado | En el servidor (o firmado en la cookie) | En el token |
| Revocar (cerrar sesión, robo) | Fácil | Difícil hasta que expire |
| Ideal para | Apps web propias | APIs entre servicios, móviles |

Si usas cookies: `HttpOnly` (JavaScript no puede leerla), `Secure` (solo HTTPS) y `SameSite=Lax` o `Strict` (mitiga CSRF).
Si usas JWT: expiración corta, refresh tokens y nunca datos sensibles dentro (se pueden leer).

## 4. Las vulnerabilidades más frecuentes

- **Inyección SQL:** nunca construyas SQL concatenando texto del usuario. Usa **consultas parametrizadas**:
  `cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))`. Los ORMs lo hacen por ti.
- **XSS:** si muestras texto del usuario como HTML sin escapar, puede ejecutar JavaScript en el navegador de otros. React escapa por defecto;
  cuidado con `dangerouslySetInnerHTML` y con generar HTML a mano.
- **CSRF:** otra web hace que tu navegador envíe una petición a tu app con tu cookie. `SameSite` y tokens anti-CSRF lo evitan.
- **Secretos expuestos:** claves en el código o en Git. Usa variables de entorno o un gestor de secretos, y revoca cualquier clave filtrada.
- **Dependencias vulnerables:** actualiza y usa herramientas como `pip-audit`, `npm audit` o Dependabot.

## 5. Defensa en profundidad

- HTTPS en todas partes.
- **Mínimo privilegio:** cada servicio y usuario de base de datos con solo los permisos que necesita.
- **Límite de peticiones** (rate limiting) en login y endpoints costosos.
- Registra eventos de seguridad (inicios fallidos, cambios de permisos) **sin** guardar contraseñas ni tokens en los logs.
- Valida y limita el tamaño de lo que se sube (archivos, JSON).

Referencia obligada: el **OWASP Top 10**, la lista de riesgos más comunes en aplicaciones web.

## Cómo sabes que dominas este tema

- Guardas y verificas contraseñas correctamente.
- Revisas cada endpoint con la pregunta "¿y si el recurso es de otra persona?".
- Explicas inyección SQL, XSS y CSRF y cómo prevenirlos.
""",
        "exercises": [
            py("seg-hash", "Hash de contraseñas con sal", "Sistemas: seguridad",
               "Escribe `hashear(contrasena, iteraciones=100_000, sal=None)` que use `hashlib.pbkdf2_hmac('sha256', ...)` con una sal aleatoria de 16 bytes "
               "(`os.urandom(16)`) si no se indica, y devuelva el texto `'iteraciones$sal_hex$hash_hex'`. Escribe también `verificar(contrasena, almacenado)` que recalcule "
               "el hash con la sal y las iteraciones guardadas y compare con `hmac.compare_digest`.",
               starter="""
import hashlib
import hmac
import os

def hashear(contrasena, iteraciones=100_000, sal=None):
    # tu código aquí
    pass

def verificar(contrasena, almacenado):
    # tu código aquí
    pass
""",
               solution="""
import hashlib
import hmac
import os

def hashear(contrasena, iteraciones=100_000, sal=None):
    sal = sal if sal is not None else os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), sal, iteraciones)
    return "%d$%s$%s" % (iteraciones, sal.hex(), digest.hex())

def verificar(contrasena, almacenado):
    iteraciones, sal_hex, hash_hex = almacenado.split("$")
    calculado = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), bytes.fromhex(sal_hex), int(iteraciones))
    return hmac.compare_digest(calculado.hex(), hash_hex)
""",
               tests="""
h = hashear("clave-segura", iteraciones=1000)
assert h.count("$") == 2 and h.startswith("1000$"), "Formato esperado: iteraciones$sal$hash"
assert "clave-segura" not in h, "El texto guardado no puede contener la contrasena"
assert verificar("clave-segura", h) is True
assert verificar("otra-clave", h) is False
assert hashear("igual", 1000) != hashear("igual", 1000), "Con sales aleatorias, la misma contrasena da hashes distintos"
sal = bytes(16)
assert hashear("x", 1000, sal) == hashear("x", 1000, sal), "Con la misma sal el resultado es reproducible"
""",
               hint="pbkdf2_hmac(nombre_hash, contrasena_en_bytes, sal, iteraciones) devuelve bytes; usa .hex() y bytes.fromhex()."),
            py("seg-sqli", "Consulta parametrizada", "Sistemas: seguridad",
               "Escribe `consulta_por_email(email)` que devuelva una tupla `(sql, parametros)` para buscar un usuario por email **sin concatenar** el valor en el SQL: "
               "`('SELECT id, nombre FROM usuarios WHERE email = %s', (email,))`.",
               starter="""
def consulta_por_email(email):
    # ¡No concatenes el email en el texto SQL!
    return "SELECT id, nombre FROM usuarios WHERE email = '" + email + "'", ()
""",
               solution="""
def consulta_por_email(email):
    return "SELECT id, nombre FROM usuarios WHERE email = %s", (email,)
""",
               tests="""
ataque = "x' OR '1'='1"
sql_texto, parametros = consulta_por_email(ataque)
assert ataque not in sql_texto, "El valor del usuario no debe aparecer dentro del SQL"
assert parametros == (ataque,), "El valor debe ir como parametro separado"
assert sql_texto == "SELECT id, nombre FROM usuarios WHERE email = %s"
""",
               hint="El SQL lleva un marcador %s y el valor viaja aparte en la tupla de parámetros."),
            py("seg-xss", "Escapar HTML", "Sistemas: seguridad",
               "Escribe `escapar_html(texto)` que reemplace `&`, `<`, `>`, `\"` y `'` por `&amp;`, `&lt;`, `&gt;`, `&quot;` y `&#x27;`. "
               "Cuidado con el orden: el `&` tiene que ir primero.",
               starter="""
def escapar_html(texto):
    # tu código aquí (sin usar el módulo html)
    pass
""",
               solution="""
def escapar_html(texto):
    return (texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#x27;"))
""",
               tests="""
assert escapar_html("<script>alert('x')</script>") == "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;"
assert escapar_html('Tom & "Jerry"') == "Tom &amp; &quot;Jerry&quot;"
assert escapar_html("&lt;") == "&amp;lt;", "Si el & no va primero, se escapan mal las entidades"
assert escapar_html("hola") == "hola"
"""),
            py("seg-idor", "Autorización por recurso", "Sistemas: seguridad",
               "Escribe `puede_ver(usuario, factura)`. `usuario` es `{'id': ..., 'rol': 'cliente' | 'admin'}` y `factura` es `{'id': ..., 'cliente_id': ...}`. "
               "Un admin puede ver cualquier factura; un cliente, solo las suyas. Si el usuario es `None` (sin sesión), devuelve `False`.",
               starter="""
def puede_ver(usuario, factura):
    # ¡estar autenticado no basta!
    return usuario is not None
""",
               solution="""
def puede_ver(usuario, factura):
    if usuario is None:
        return False
    if usuario.get("rol") == "admin":
        return True
    return usuario.get("id") == factura.get("cliente_id")
""",
               tests="""
factura = {"id": 1043, "cliente_id": 7}
assert puede_ver({"id": 7, "rol": "cliente"}, factura) is True
assert puede_ver({"id": 8, "rol": "cliente"}, factura) is False, "Un cliente no puede ver facturas ajenas (IDOR)"
assert puede_ver({"id": 1, "rol": "admin"}, factura) is True
assert puede_ver(None, factura) is False
"""),
            quiz("seg-quiz-hash", "Guardar contraseñas", "Sistemas: seguridad",
                 "¿Cuál es la forma correcta de guardar contraseñas?",
                 ["En texto plano en una tabla protegida", "Con SHA-256 sin sal", "Con un algoritmo lento y con sal (Argon2, bcrypt o PBKDF2)", "Cifradas con una clave guardada en el código"], 2,
                 "Los hashes rápidos se rompen con fuerza bruta y tablas precalculadas. Un algoritmo lento con sal por usuario lo hace inviable."),
            quiz("seg-quiz-cookie", "Atributos de la cookie de sesión", "Sistemas: seguridad",
                 "¿Qué combinación de atributos es la más segura para una cookie de sesión de una web propia?",
                 ["Ninguno, para que funcione en todos lados", "HttpOnly, Secure y SameSite=Lax", "Solo Secure", "Guardarla en localStorage"], 1,
                 "HttpOnly la protege de XSS, Secure evita enviarla sin HTTPS y SameSite mitiga CSRF. localStorage es legible desde cualquier script."),
            quiz("seg-quiz-jwt", "Revocar un JWT", "Sistemas: seguridad",
                 "Roban el JWT de un usuario y el token expira en 30 días. ¿Cuál es el problema principal?",
                 ["Ninguno", "Un JWT es válido hasta que expira: sin una lista de revocación, el atacante puede usarlo todo ese tiempo", "El JWT se borra solo", "El servidor detecta el robo automáticamente"], 1,
                 "Por eso los JWT deben expirar pronto (minutos) y renovarse con refresh tokens que sí puedas revocar."),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "sys-arquitectura",
        "phase": "producto",
        "title": "Arquitectura de software",
        "summary": "Separación en capas, inyección de dependencias, monolito modular vs microservicios, configuración y decisiones documentadas.",
        "hours": 8,
        "theory": r"""
# Arquitectura de software

La arquitectura es el conjunto de **decisiones difíciles de cambiar después**: cómo se divide el código, cómo se comunican las partes y dónde vive
cada responsabilidad. Una buena arquitectura hace que añadir funcionalidades siga siendo fácil al año de empezar.

## 1. Separar responsabilidades: capas

Una estructura sencilla y probada para un backend:

```
rutas / controladores   -> reciben la petición HTTP, validan la forma y llaman al servicio
servicios (dominio)     -> reglas de negocio: "no se puede cancelar un pedido enviado"
repositorios            -> acceso a datos (SQL, ORM, APIs externas)
```

Las reglas de negocio **no** deberían saber si los datos vienen de PostgreSQL o de un archivo, ni si la petición llegó por HTTP o por un script.
Así puedes probarlas sin base de datos y cambiar la infraestructura sin reescribirlas.

## 2. Inyección de dependencias

En vez de que una clase cree sus dependencias, **se las pasan**:

```python
class ServicioPedidos:
    def __init__(self, repositorio, notificador):
        self.repositorio = repositorio
        self.notificador = notificador
```

En producción le pasas el repositorio real; en las pruebas, uno falso en memoria. FastAPI tiene `Depends` para esto.

## 3. Monolito modular primero

Los **microservicios** resuelven problemas de **organizaciones grandes** (muchos equipos que despliegan por separado, partes que escalan distinto).
A cambio traen redes que fallan, datos distribuidos, despliegues complejos y mucha más operación.

Para una startup o un equipo pequeño: **un monolito modular** (una aplicación, bien dividida en módulos por dominio: `usuarios`, `pagos`, `pedidos`)
es casi siempre la mejor opción. Si un módulo de verdad necesita separarse más adelante, la buena división te lo pondrá fácil.

## 4. Acoplamiento y cohesión

- **Alta cohesión:** lo que cambia junto, vive junto.
- **Bajo acoplamiento:** un módulo usa a otro por una interfaz pequeña y clara, sin conocer sus detalles internos.
- Señal de alarma: cambiar algo pequeño obliga a tocar diez archivos de módulos distintos.

## 5. Configuración (12-factor app)

- Configuración y secretos en **variables de entorno**, no en el código.
- El mismo código se despliega en desarrollo, pruebas y producción; solo cambia la configuración.
- Logs a la salida estándar, procesos sin estado (el estado vive en la base, en Redis o en almacenamiento de objetos).

## 6. Decide con criterio y documenta

- **KISS** (mantenlo simple) y **YAGNI** (no lo vas a necesitar): no construyas para el millón de usuarios cuando tienes diez.
- Toda decisión es un **trade-off**: escríbelo. Un **ADR** (Architecture Decision Record) es un documento corto: contexto, decisión, alternativas y consecuencias.
  Dentro de un año explicará por qué el sistema es como es.

## Cómo sabes que dominas este tema

- Separas rutas, servicios y repositorios en tus proyectos.
- Pruebas la lógica de negocio con dependencias falsas.
- Defiendes por qué tu startup empieza con un monolito modular.
""",
        "exercises": [
            py("arq-servicio", "Servicio con dependencias inyectadas", "Sistemas: arquitectura",
               "Completa `ServicioPedidos(repositorio, notificador)`. `crear_pedido(cliente_id, total)` debe: lanzar `ValueError` si `total <= 0`; guardar el pedido con "
               "`repositorio.guardar({'cliente_id': ..., 'total': ..., 'estado': 'pendiente'})`, que devuelve el id; avisar con "
               "`notificador.enviar(cliente_id, 'Pedido <id> recibido')`; y devolver el id. Las pruebas usan un repositorio y un notificador falsos.",
               starter="""
class ServicioPedidos:
    def __init__(self, repositorio, notificador):
        self.repositorio = repositorio
        self.notificador = notificador

    def crear_pedido(self, cliente_id, total):
        # tu código aquí
        pass
""",
               solution="""
class ServicioPedidos:
    def __init__(self, repositorio, notificador):
        self.repositorio = repositorio
        self.notificador = notificador

    def crear_pedido(self, cliente_id, total):
        if total <= 0:
            raise ValueError("El total debe ser positivo")
        pedido_id = self.repositorio.guardar({"cliente_id": cliente_id, "total": total, "estado": "pendiente"})
        self.notificador.enviar(cliente_id, "Pedido %s recibido" % pedido_id)
        return pedido_id
""",
               tests="""
class RepoFalso:
    def __init__(self):
        self.guardados = []
    def guardar(self, pedido):
        self.guardados.append(pedido)
        return len(self.guardados)

class NotificadorFalso:
    def __init__(self):
        self.mensajes = []
    def enviar(self, cliente_id, texto):
        self.mensajes.append((cliente_id, texto))

repo, noti = RepoFalso(), NotificadorFalso()
servicio = ServicioPedidos(repo, noti)
assert servicio.crear_pedido(7, 50) == 1
assert repo.guardados == [{"cliente_id": 7, "total": 50, "estado": "pendiente"}]
assert noti.mensajes == [(7, "Pedido 1 recibido")], "Obtuve %r" % (noti.mensajes,)
try:
    servicio.crear_pedido(7, 0)
except ValueError:
    pass
else:
    raise AssertionError("Un total no positivo debe lanzar ValueError")
assert len(repo.guardados) == 1 and len(noti.mensajes) == 1, "Si la validacion falla, no se guarda ni se notifica"
"""),
            py("arq-repo", "Repositorio en memoria", "Sistemas: arquitectura",
               "Escribe `RepositorioMemoria` con: `guardar(entidad)` que asigna un id incremental (1, 2, 3...), guarda una **copia** con la clave `'id'` y devuelve el id; "
               "`obtener(id)` que devuelve una copia o `None`; y `listar(**filtros)` que devuelve copias de las entidades cuyos campos coinciden con todos los filtros, ordenadas por id.",
               starter="""
class RepositorioMemoria:
    def __init__(self):
        self._datos = {}

    # implementa guardar, obtener y listar
""",
               solution="""
class RepositorioMemoria:
    def __init__(self):
        self._datos = {}

    def guardar(self, entidad):
        nuevo_id = len(self._datos) + 1
        self._datos[nuevo_id] = {**entidad, "id": nuevo_id}
        return nuevo_id

    def obtener(self, entidad_id):
        entidad = self._datos.get(entidad_id)
        return dict(entidad) if entidad is not None else None

    def listar(self, **filtros):
        return [dict(e) for _, e in sorted(self._datos.items())
                if all(e.get(k) == v for k, v in filtros.items())]
""",
               tests="""
repo = RepositorioMemoria()
datos = {"nombre": "Ana", "plan": "pro"}
assert repo.guardar(datos) == 1 and repo.guardar({"nombre": "Luis", "plan": "free"}) == 2
assert "id" not in datos, "No modifiques el diccionario que te pasan"
assert repo.obtener(1) == {"nombre": "Ana", "plan": "pro", "id": 1}
assert repo.obtener(9) is None
copia = repo.obtener(1)
copia["plan"] = "hackeado"
assert repo.obtener(1)["plan"] == "pro", "obtener debe devolver una copia"
assert [e["id"] for e in repo.listar(plan="free")] == [2]
assert len(repo.listar()) == 2
"""),
            quiz("arq-quiz-micro", "¿Microservicios?", "Sistemas: arquitectura",
                 "Eres el único desarrollador de una startup en fase de MVP. ¿Qué arquitectura eliges?",
                 ["Diez microservicios con Kubernetes desde el día 1", "Un monolito modular bien dividido por dominios",
                  "Un único archivo de 5000 líneas", "Funciones serverless independientes para cada endpoint sin estructura común"], 1,
                 "Los microservicios añaden mucha complejidad operativa que un equipo pequeño no necesita. Un monolito modular permite avanzar rápido y separar después si hace falta."),
            quiz("arq-quiz-capa", "¿Dónde va la regla?", "Sistemas: arquitectura",
                 "La regla 'un pedido enviado no se puede cancelar' debe vivir en...",
                 ["El componente de React del botón", "La capa de servicios (dominio), independiente de HTTP y de la base de datos",
                  "Un trigger de la base de datos únicamente", "El archivo de rutas, mezclada con el parseo de la petición"], 1,
                 "Las reglas de negocio en el dominio se pueden probar y reutilizar (API, tareas programadas, scripts). El frontend puede ayudar, pero no es la fuente de verdad."),
            quiz("arq-quiz-config", "Configuración", "Sistemas: arquitectura",
                 "¿Dónde pones la URL de la base de datos y la clave de la API de pagos?",
                 ["En constantes dentro del código", "En variables de entorno (y un gestor de secretos en producción)", "En el README", "En el frontend"], 1,
                 "Así el mismo código sirve para cada entorno y los secretos no acaban en Git."),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "sys-diseno",
        "phase": "producto",
        "title": "Diseño de sistemas: escalar, caché, colas y fiabilidad",
        "summary": "Escalado horizontal, caché, colas y tareas en segundo plano, reintentos, límites de peticiones, observabilidad y cómo abordar un diseño.",
        "hours": 10,
        "theory": r"""
# Diseño de sistemas: escalar, caché, colas y fiabilidad

Diseñar sistemas es decidir **cómo se comporta tu producto cuando crece y cuando algo falla**. No necesitas la arquitectura de una gran plataforma,
pero sí conocer las piezas y cuándo usar cada una.

## 1. Escalar

- **Vertical:** una máquina más grande. Simple, con límite.
- **Horizontal:** más copias de tu aplicación detrás de un **balanceador de carga**. Requiere que la app sea **sin estado**:
  nada importante en memoria del proceso (sesiones, archivos subidos); eso va a la base, a Redis o a almacenamiento de objetos (S3).
- La base de datos suele ser el cuello de botella: índices, consultas eficientes, **réplicas de lectura** y, solo al final, particionar.

## 2. Caché

Guardar el resultado de algo costoso para reutilizarlo.

- **Dónde:** en el navegador o CDN (archivos estáticos), en la aplicación, en Redis (compartida entre servidores).
- **Patrón cache-aside:** busca en caché; si no está, consulta la base y guarda el resultado con un **TTL** (tiempo de vida).
- **Invalidación:** el problema difícil. Usa TTL cortos o borra la entrada al actualizar el dato.
- **Política de expulsión:** cuando se llena, se descarta lo menos usado recientemente (**LRU**).

## 3. Colas y trabajo en segundo plano

Lo que no necesita responder al usuario en el momento (enviar correos, generar reportes, procesar imágenes, llamar a APIs lentas) va a una **cola**
(Redis, RabbitMQ, SQS) y lo procesan **workers**. La petición responde rápido y el sistema absorbe picos.

## 4. Fallar bien

Todo lo que está en la red falla tarde o temprano.

- **Timeouts** en cada llamada externa: sin ellos, un servicio lento bloquea el tuyo.
- **Reintentos con espera exponencial** (0,5 s, 1 s, 2 s, 4 s... con un máximo) y algo de aleatoriedad, solo en operaciones **idempotentes**.
- **Circuit breaker:** si un servicio falla una y otra vez, deja de llamarlo un tiempo.
- **Rate limiting** (por ejemplo, *token bucket*): protege tu API de abusos y de clientes con errores. Responde **429**.
- **Degradación elegante:** si falla la recomendación, muestra la página sin recomendaciones en vez de un error.

## 5. Observabilidad

No puedes arreglar lo que no ves:

- **Logs** estructurados (JSON) con un id de petición.
- **Métricas:** latencia (p50, p95, p99), tasa de errores, peticiones por segundo, uso de recursos.
- **Trazas** para seguir una petición entre servicios.
- **Alertas** sobre síntomas que afectan al usuario (errores, latencia), no sobre cada detalle.

## 6. Cómo abordar un diseño (también en entrevistas)

Una entrevista de diseño de sistemas dura 45-60 minutos y el enunciado es **ambiguo a propósito** ("diseña un chat"). Sin un método,
el tiempo se va en detalles y el entrevistador no puede seguir tu razonamiento. Reparto orientativo:

| Paso | Tiempo | Qué haces |
|---|---|---|
| Presentación | 5 min | Te presentas y escuchas el problema |
| 1. Alcance | 5-10 min | Requisitos y estimaciones |
| 2. Diseño de alto nivel | ~20 min | API, diagrama y modelo de datos |
| 3. Profundización | ~15 min | 2-3 cuellos de botella |
| Cierre | 5 min | Resumen y tus preguntas |

**1. Alcance (no dibujes nada todavía).**

- **Requisitos funcionales:** qué debe hacer, para quién y por qué. "Un chat" puede ser WhatsApp (1 a 1), Slack (equipos) o Discord
  (comunidades), y cada uno se diseña distinto. Acuerda con el entrevistador las 3-4 funciones principales.
- **Requisitos no funcionales:** escala, latencia, disponibilidad, consistencia. Son los que hacen difícil el problema.
- **Estimaciones rápidas** (*back of the envelope*): 100 000 usuarios diarios × 20 peticiones ≈ 2 millones al día ≈ 23 por segundo de media,
  quizá 100 en el pico. Basta con acertar el orden de magnitud.

**2. Diseño de alto nivel, de arriba abajo.**

- Empieza por la **API**: los endpoints, sus entradas y salidas. Es el contrato con el cliente y comprueba que cubres los requisitos.
- Dibuja el **diagrama**: cliente → balanceador o API gateway → servicios → almacenamiento (y caché o colas si hacen falta).
- Define el **modelo de datos** y los patrones de acceso: ¿se lee mucho más de lo que se escribe? Eso decide índices, caché y tipo de base.
- Recorre cada requisito de principio a fin sobre el diagrama. Anota aparte lo que quieras profundizar, sin desviarte todavía.

**3. Profundización: para cada cuello de botella.**

1. **Expón el problema** con números ("1 millón de escrituras por segundo no caben en una sola base de datos").
2. **Propón dos soluciones** (reducir la frecuencia de envío / particionar o usar una base pensada para muchas escrituras).
3. **Compara pros y contras**, con estimaciones si puedes.
4. **Elige y justifica**, y pregunta al entrevistador si está de acuerdo. Atento a sus señales: si insiste en un punto, ve ahí.

**Cierre:** resume el diseño, menciona qué mejorarías con más tiempo y haz tus preguntas sobre el equipo.

Para un junior, lo que más pesa es **preguntar antes de diseñar, razonar en voz alta y explicar los trade-offs**, no conocer cada tecnología.

## 7. Bases de datos a escala

Cuando una sola base de datos no da abasto, estas son las herramientas, en este orden:

1. **Optimizar primero:** índices, consultas sin N+1, caché y un pool de conexiones. Resuelve la mayoría de los casos.
2. **Réplicas de lectura:** copias de la base que reciben los cambios del servidor principal y atienden lecturas. Ojo con el **retraso de replicación**:
   si un usuario guarda algo y justo después lee de una réplica, puede no ver su propio cambio. Solución habitual: leer del principal justo después de escribir.
3. **Particionado (sharding):** repartir los datos entre varias bases según una clave (por ejemplo, `hash(cliente_id) % n`). Escala las escrituras,
   pero complica las consultas que cruzan particiones y los cambios en el número de particiones (para eso existe el *hashing consistente*).

**Consistencia:** en sistemas distribuidos no puedes tenerlo todo cuando la red falla (teorema **CAP**): o respondes con datos posiblemente desactualizados
(disponibilidad) o rechazas la petición hasta asegurar datos correctos (consistencia). El saldo de una cuenta exige consistencia; un contador de "me gusta" tolera la eventualidad.

## 8. Contenido estático y CDN

Una **CDN** guarda copias de archivos estáticos (imágenes, JS, CSS, videos) en servidores repartidos por el mundo, cerca de los usuarios: menos latencia y menos carga
para tu servidor. Usa nombres de archivo con versión o hash (`app.3f9a.js`) para poder cachearlos mucho tiempo sin servir versiones viejas.

## 9. GraphQL, en una línea

Alternativa a REST donde el cliente pide exactamente los campos que necesita en una sola consulta. Útil con muchos clientes distintos (web, móvil) y datos muy relacionados;
añade complejidad en caché, permisos y rendimiento. Para empezar, REST bien diseñado es suficiente.

## Cómo sabes que dominas este tema

- Explicas cuándo usar caché, cola o réplica de lectura.
- Implementas reintentos con backoff y un limitador de peticiones.
- Haces una estimación rápida de carga y propones un diseño razonable.
""",
        "exercises": [
            py("dis-lru", "Caché LRU", "Sistemas: diseño de sistemas",
               "Escribe `CacheLRU(capacidad)` con `obtener(clave)` (devuelve el valor o `None`, y marca la clave como usada recientemente) y `guardar(clave, valor)`. "
               "Al superar la capacidad, elimina la clave **usada hace más tiempo**. Puedes usar `collections.OrderedDict`.",
               starter="""
from collections import OrderedDict

class CacheLRU:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self._datos = OrderedDict()

    # implementa obtener y guardar
""",
               solution="""
from collections import OrderedDict

class CacheLRU:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self._datos = OrderedDict()

    def obtener(self, clave):
        if clave not in self._datos:
            return None
        self._datos.move_to_end(clave)
        return self._datos[clave]

    def guardar(self, clave, valor):
        self._datos[clave] = valor
        self._datos.move_to_end(clave)
        if len(self._datos) > self.capacidad:
            self._datos.popitem(last=False)
""",
               tests="""
c = CacheLRU(2)
c.guardar("a", 1)
c.guardar("b", 2)
assert c.obtener("a") == 1, "a se usa ahora: pasa a ser la mas reciente"
c.guardar("c", 3)
assert c.obtener("b") is None, "b era la menos usada y debe salir"
assert c.obtener("a") == 1 and c.obtener("c") == 3
c.guardar("a", 10)
c.guardar("d", 4)
assert c.obtener("c") is None and c.obtener("a") == 10, "Actualizar una clave tambien la marca como reciente"
""",
               hint="move_to_end marca como reciente; popitem(last=False) quita la más antigua."),
            py("dis-ttl", "Caché con tiempo de vida", "Sistemas: diseño de sistemas",
               "Escribe `CacheTTL(ttl, reloj=time.monotonic)` con `guardar(clave, valor)` y `obtener(clave)`. Un valor caduca cuando han pasado `ttl` segundos o más desde que se guardó: "
               "entonces `obtener` devuelve `None` y lo elimina. El reloj se inyecta para poder probarlo sin esperar.",
               starter="""
import time

class CacheTTL:
    def __init__(self, ttl, reloj=time.monotonic):
        self.ttl = ttl
        self.reloj = reloj
        # tu código aquí
""",
               solution="""
import time

class CacheTTL:
    def __init__(self, ttl, reloj=time.monotonic):
        self.ttl = ttl
        self.reloj = reloj
        self._datos = {}

    def guardar(self, clave, valor):
        self._datos[clave] = (valor, self.reloj() + self.ttl)

    def obtener(self, clave):
        entrada = self._datos.get(clave)
        if entrada is None:
            return None
        valor, expira = entrada
        if self.reloj() >= expira:
            del self._datos[clave]
            return None
        return valor
""",
               tests="""
ahora = [100.0]
c = CacheTTL(10, reloj=lambda: ahora[0])
c.guardar("usuario:7", {"nombre": "Ana"})
ahora[0] = 109.9
assert c.obtener("usuario:7") == {"nombre": "Ana"}, "A los 9.9 s sigue vigente"
ahora[0] = 110.0
assert c.obtener("usuario:7") is None, "A los 10 s ya caduco"
assert c.obtener("nunca") is None
"""),
            py("dis-tokens", "Limitador de peticiones (token bucket)", "Sistemas: diseño de sistemas",
               "Escribe `Limitador(capacidad, por_segundo, reloj=time.monotonic)`. Empieza lleno con `capacidad` fichas; se recargan `por_segundo` fichas por segundo, sin superar la capacidad. "
               "`permitir()` devuelve `True` y gasta una ficha si hay al menos una; si no, devuelve `False`.",
               starter="""
import time

class Limitador:
    def __init__(self, capacidad, por_segundo, reloj=time.monotonic):
        self.capacidad = capacidad
        self.por_segundo = por_segundo
        self.reloj = reloj
        # tu código aquí

    def permitir(self):
        pass
""",
               solution="""
import time

class Limitador:
    def __init__(self, capacidad, por_segundo, reloj=time.monotonic):
        self.capacidad = capacidad
        self.por_segundo = por_segundo
        self.reloj = reloj
        self._fichas = float(capacidad)
        self._ultimo = reloj()

    def permitir(self):
        ahora = self.reloj()
        self._fichas = min(self.capacidad, self._fichas + (ahora - self._ultimo) * self.por_segundo)
        self._ultimo = ahora
        if self._fichas >= 1:
            self._fichas -= 1
            return True
        return False
""",
               tests="""
t = [0.0]
lim = Limitador(3, 1, reloj=lambda: t[0])
assert [lim.permitir() for _ in range(4)] == [True, True, True, False], "Empieza con 3 fichas"
t[0] = 1.0
assert lim.permitir() is True and lim.permitir() is False, "Tras 1 s se recarga 1 ficha"
t[0] = 100.0
assert sum(lim.permitir() for _ in range(5)) == 3, "Nunca acumula mas que la capacidad"
"""),
            py("dis-backoff", "Reintentos con espera exponencial", "Sistemas: diseño de sistemas",
               "Escribe `reintentar(funcion, intentos=4, base=0.5, maximo=8, dormir=time.sleep)`: llama a `funcion()`; si lanza una excepción, espera "
               "`min(base * 2**n, maximo)` segundos (n = 0, 1, 2...) usando `dormir` y vuelve a intentar. Si fallan todos los intentos, relanza la última excepción. "
               "Devuelve el resultado en cuanto una llamada funcione.",
               starter="""
import time

def reintentar(funcion, intentos=4, base=0.5, maximo=8, dormir=time.sleep):
    # tu código aquí
    pass
""",
               solution="""
import time

def reintentar(funcion, intentos=4, base=0.5, maximo=8, dormir=time.sleep):
    for n in range(intentos):
        try:
            return funcion()
        except Exception:
            if n == intentos - 1:
                raise
            dormir(min(base * 2 ** n, maximo))
""",
               tests="""
esperas = []
llamadas = {"n": 0}
def inestable():
    llamadas["n"] += 1
    if llamadas["n"] < 3:
        raise ConnectionError("fallo temporal")
    return "ok"
assert reintentar(inestable, dormir=esperas.append) == "ok"
assert esperas == [0.5, 1.0], "Esperas esperadas [0.5, 1.0]; obtuve %r" % (esperas,)
esperas.clear()
def siempre_falla():
    raise TimeoutError("caido")
try:
    reintentar(siempre_falla, intentos=6, base=1, maximo=4, dormir=esperas.append)
except TimeoutError:
    pass
else:
    raise AssertionError("Si todos fallan, debe relanzar la ultima excepcion")
assert esperas == [1, 2, 4, 4, 4], "La espera no debe superar el maximo; obtuve %r" % (esperas,)
"""),
            py("dis-shard", "Elegir la partición de un cliente", "Sistemas: diseño de sistemas",
               "Escribe `particion(clave, n)` que devuelva el número de partición (0 a n-1) para una clave de texto usando `int(hashlib.md5(clave.encode()).hexdigest(), 16) % n`. "
               "Debe ser **determinista** (la misma clave siempre va a la misma partición) y lanzar `ValueError` si `n < 1`. No uses `hash()`, que cambia entre ejecuciones de Python.",
               starter="""
import hashlib

def particion(clave, n):
    return hash(clave) % n
""",
               solution="""
import hashlib

def particion(clave, n):
    if n < 1:
        raise ValueError("Debe haber al menos una particion")
    return int(hashlib.md5(clave.encode()).hexdigest(), 16) % n
""",
               tests="""
import hashlib
assert particion("cliente-42", 4) == int(hashlib.md5(b"cliente-42").hexdigest(), 16) % 4, "Usa md5, no hash() (que cambia en cada ejecucion)"
assert all(particion("cliente-%d" % i, 4) == particion("cliente-%d" % i, 4) for i in range(50)), "Debe ser determinista"
conteo = [0] * 4
for i in range(4000):
    conteo[particion("cliente-%d" % i, 4)] += 1
assert all(800 < c < 1200 for c in conteo), "El reparto debe ser aproximadamente uniforme: %r" % (conteo,)
try:
    particion("x", 0)
except ValueError:
    pass
else:
    raise AssertionError("n < 1 debe lanzar ValueError")
""",
               hint="hashlib.md5(clave.encode()).hexdigest() da un hexadecimal; conviértelo con int(..., 16)."),
            quiz("dis-quiz-replica", "Retraso de replicación", "Sistemas: diseño de sistemas",
                 "Un usuario cambia su foto de perfil, recarga la página y sigue viendo la foto vieja. Las lecturas van a réplicas. ¿Qué ocurre y qué haces?",
                 ["Un bug del navegador", "Retraso de replicación: tras escribir, lee de la base principal (al menos para ese usuario durante unos segundos)",
                  "Hay que borrar las réplicas", "Hay que usar GraphQL"], 1,
                 "Las réplicas reciben los cambios con algo de retraso. 'Leer tus propias escrituras' desde el principal es la solución habitual."),
            quiz("dis-quiz-cola", "Enviar el correo de bienvenida", "Sistemas: diseño de sistemas",
                 "Al registrarse un usuario, envías un correo con un proveedor externo que a veces tarda 5 segundos. ¿Qué haces?",
                 ["Enviarlo dentro de la petición de registro y que el usuario espere", "Poner la tarea en una cola y que un worker la envíe en segundo plano, con reintentos",
                  "No enviar correos", "Enviarlo desde el navegador del usuario"], 1,
                 "El registro responde al instante y, si el proveedor falla, el worker reintenta sin afectar al usuario."),
            quiz("dis-quiz-estado", "Escalar horizontalmente", "Sistemas: diseño de sistemas",
                 "Pasas de 1 a 3 servidores detrás de un balanceador y los usuarios pierden la sesión al azar. ¿Por qué?",
                 ["El balanceador está roto", "Las sesiones se guardaban en la memoria de cada servidor; hay que moverlas a un almacén compartido (base, Redis) o usar cookies firmadas",
                  "Hacen falta más servidores", "La base de datos es lenta"], 1,
                 "Para escalar horizontalmente la aplicación debe ser sin estado: cualquier servidor debe poder atender cualquier petición."),
            quiz("dis-quiz-estimacion", "Estimación rápida", "Sistemas: diseño de sistemas",
                 "Tu app tiene 50 000 usuarios activos diarios y cada uno hace unas 40 peticiones al día. ¿Cuántas peticiones por segundo hay de media, aproximadamente?",
                 ["≈ 2", "≈ 23", "≈ 2000", "≈ 50 000"], 1,
                 "50 000 × 40 = 2 millones al día; un día tiene 86 400 segundos → ≈ 23 por segundo de media (el pico puede ser varias veces mayor)."),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "sys-calidad",
        "phase": "producto",
        "title": "Pruebas, CI/CD y operación en producción",
        "summary": "Pirámide de pruebas, pytest, integración continua, despliegues seguros, logs estructurados, monitoreo, copias de seguridad e incidentes.",
        "hours": 8,
        "theory": r"""
# Pruebas, CI/CD y operación en producción

Lanzar es el principio. Un buen sistema es el que **puedes cambiar sin miedo** y que **te avisa cuando algo va mal** antes que tus clientes.

## 1. La pirámide de pruebas

- **Muchas pruebas unitarias:** rápidas, de funciones y servicios aislados (con dependencias falsas).
- **Algunas de integración:** tu código con una base de datos real (por ejemplo, PostgreSQL en Docker) o con la API.
- **Pocas de extremo a extremo (E2E):** el flujo completo en un navegador (Playwright). Son lentas y frágiles: solo para los caminos críticos (registro, pago).

Prueba sobre todo **la lógica de negocio y los casos borde**: vacíos, límites, errores, redondeos. Un buen test describe un comportamiento:
`test_no_se_puede_cancelar_un_pedido_enviado`.

```python
import pytest

@pytest.fixture
def servicio():
    return ServicioPedidos(RepositorioMemoria(), NotificadorFalso())

@pytest.mark.parametrize("total", [0, -5])
def test_rechaza_totales_no_positivos(servicio, total):
    with pytest.raises(ValueError):
        servicio.crear_pedido(1, total)
```

## 2. Integración continua (CI)

En cada *push* o Pull Request, un servicio (GitHub Actions) instala dependencias, ejecuta linters y pruebas. Si algo falla, no se mezcla.

```yaml
# .github/workflows/tests.yml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt pytest
      - run: pytest -q
```

## 3. Despliegue continuo (CD) y despliegues seguros

- Entornos separados: **desarrollo → pruebas (staging) → producción**, con la misma configuración salvo las variables.
- Despliega **a menudo y en cambios pequeños**: es más fácil encontrar qué rompió algo.
- **Migraciones compatibles hacia atrás** antes de desplegar el código que las usa.
- Ten un **plan de vuelta atrás** (rollback) y, si puedes, *feature flags* para activar funcionalidades sin desplegar.

## 4. Operar en producción

- **Logs estructurados** (JSON) con nivel, mensaje y contexto (id de petición, usuario). **Nunca** contraseñas, tokens ni datos de tarjetas.
- **Monitoreo y alertas:** errores por minuto, latencia p95, disponibilidad (*uptime*). Un servicio de errores como Sentry te muestra el traceback y a cuántos usuarios afecta.
- **Copias de seguridad automáticas** y, sobre todo, **prueba restaurarlas**: una copia que nunca restauraste no es una copia.
- **Incidentes:** primero mitiga (rollback), luego investiga. Después escribe un **post-mortem sin culpables**: qué pasó, por qué, cómo se detectó y qué cambias para que no se repita.

## 5. Calidad del código

Formateador y linter automáticos (`ruff`, `black`), revisión de código en Pull Requests (aunque sea con un asistente de IA si trabajas solo) y
un `README` que permita levantar el proyecto en minutos.

## Cómo sabes que dominas este tema

- Tus proyectos tienen pruebas que corren en CI en cada push.
- Despliegas en pasos pequeños y sabes volver atrás.
- Tienes logs útiles, alertas básicas y copias probadas.
""",
        "exercises": [
            py("cal-repartir", "Repartir dinero sin perder centavos", "Sistemas: pruebas y operación",
               "Escribe `repartir(total_centavos, partes)` que divida un importe entero de centavos en `partes` enteros que **sumen exactamente** el total y difieran "
               "como máximo en 1 centavo, con los mayores primero. Lanza `ValueError` si `partes < 1`. Es el típico bug que solo aparece con buenas pruebas de casos borde.",
               starter="""
def repartir(total_centavos, partes):
    # versión ingenua: pierde centavos con los redondeos
    return [round(total_centavos / partes)] * partes
""",
               solution="""
def repartir(total_centavos, partes):
    if partes < 1:
        raise ValueError("Debe haber al menos una parte")
    base, resto = divmod(total_centavos, partes)
    return [base + 1] * resto + [base] * (partes - resto)
""",
               tests="""
assert repartir(1000, 3) == [334, 333, 333], "10,00 entre 3 = 3,34 + 3,33 + 3,33"
for total, partes in ((1000, 3), (1, 4), (999, 7), (0, 5), (12345, 1)):
    r = repartir(total, partes)
    assert sum(r) == total, "La suma debe ser exactamente el total (%d entre %d dio %r)" % (total, partes, r)
    assert len(r) == partes and max(r) - min(r) <= 1
try:
    repartir(100, 0)
except ValueError:
    pass
else:
    raise AssertionError("Con 0 partes debe lanzar ValueError")
""",
               hint="divmod(total, partes) da la base y cuántas partes llevan un centavo extra."),
            py("cal-log", "Log estructurado sin secretos", "Sistemas: pruebas y operación",
               "Escribe `log_json(nivel, mensaje, **campos)` que devuelva una línea JSON con `nivel`, `mensaje` y los campos extra. Cualquier campo cuyo nombre contenga "
               "`password`, `token` o `secret` (sin importar mayúsculas) debe aparecer con el valor `'***'`.",
               starter="""
import json

def log_json(nivel, mensaje, **campos):
    # tu código aquí
    pass
""",
               solution="""
import json

SENSIBLES = ("password", "token", "secret")

def log_json(nivel, mensaje, **campos):
    limpio = {k: ("***" if any(s in k.lower() for s in SENSIBLES) else v) for k, v in campos.items()}
    return json.dumps({"nivel": nivel, "mensaje": mensaje, **limpio}, ensure_ascii=False)
""",
               tests="""
import json
linea = log_json("info", "login correcto", usuario_id=7, password="1234", AccessToken="abc", ruta="/login")
datos = json.loads(linea)
assert datos == {"nivel": "info", "mensaje": "login correcto", "usuario_id": 7, "password": "***", "AccessToken": "***", "ruta": "/login"}, "Obtuve %r" % (datos,)
assert "1234" not in linea and "abc" not in linea, "Los secretos no pueden aparecer en el log"
assert json.loads(log_json("error", "fallo"))["nivel"] == "error"
"""),
            quiz("cal-quiz-piramide", "Qué pruebas escribir más", "Sistemas: pruebas y operación",
                 "¿Qué tipo de prueba debería ser la más numerosa en tu proyecto?",
                 ["Pruebas E2E en el navegador", "Pruebas unitarias de la lógica de negocio", "Pruebas manuales antes de cada despliegue", "Ninguna, con revisar el código basta"], 1,
                 "Son rápidas, estables y señalan el fallo con precisión. Las E2E se reservan para unos pocos flujos críticos."),
            quiz("cal-quiz-backup", "Copias de seguridad", "Sistemas: pruebas y operación",
                 "Tu proveedor hace copias automáticas de la base cada noche. ¿Qué te falta?",
                 ["Nada", "Probar periódicamente que puedes restaurarlas (y cuánto tardas)", "Hacer copias cada minuto", "Guardarlas en el mismo servidor"], 1,
                 "Muchas empresas descubren durante un desastre que sus copias estaban incompletas o no sabían restaurarlas."),
            quiz("cal-quiz-incidente", "Durante un incidente", "Sistemas: pruebas y operación",
                 "Tras un despliegue, los pagos empiezan a fallar. ¿Qué haces primero?",
                 ["Buscar al culpable", "Mitigar: volver a la versión anterior (rollback) y luego investigar", "Escribir el post-mortem", "Esperar a ver si se arregla solo"], 1,
                 "Primero se restaura el servicio; el análisis viene después, en un post-mortem sin culpables."),
            checklist("cal-check", "Tu proyecto, listo para producción", "Sistemas: pruebas y operación",
                      "Aplícalo a tu proyecto actual.",
                      ["Tiene pruebas unitarias de la lógica principal", "GitHub Actions ejecuta las pruebas en cada push",
                       "La configuración y los secretos vienen de variables de entorno", "Hay logs estructurados sin datos sensibles",
                       "Tengo monitoreo de errores (por ejemplo, Sentry) y una alerta básica", "Probé restaurar una copia de la base de datos"]),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "startup-mvp",
        "phase": "producto",
        "title": "Startup: del problema al MVP",
        "summary": "Elegir un problema, entrevistar clientes sin sesgos, construir el MVP más pequeño posible, métricas de producto y cobrar.",
        "hours": 8,
        "theory": r"""
# Startup: del problema al MVP

La razón más citada por la que fracasan las startups no es técnica: **construyen algo que no suficientes personas necesitan**.
Este tema es para que tu capacidad de construir se use en el problema correcto.

## 1. Empieza por el problema, no por la solución

Un buen problema para empezar:

- Lo **sufre un grupo concreto** de personas o empresas que puedes contactar.
- Es **frecuente o costoso** (tiempo, dinero, riesgo).
- Ya intentan resolverlo con algo improvisado (hojas de cálculo, WhatsApp, procesos manuales): es una señal fuerte.
- Idealmente, **lo conoces de cerca** (tu trabajo, tu entorno, tu sector).

## 2. Entrevistas de descubrimiento

Habla con 15-20 personas **antes de programar**. Reglas para no engañarte:

- Pregunta por **hechos pasados**, no por opiniones ni hipótesis. Mal: "¿usarías una app que...?". Bien: "¿Cuándo fue la última vez que te pasó? ¿Qué hiciste? ¿Cuánto te costó?"
- **No presentes tu idea** al principio: la gente es amable y te dirá que es genial.
- Busca **compromisos**, no cumplidos: tiempo para una segunda reunión, acceso a sus datos, una carta de intención, un **pago anticipado**.
- Anota textual lo que dicen; los patrones aparecen a partir de la décima entrevista.

## 3. El MVP: el experimento más pequeño

El MVP (producto mínimo viable) no es una versión reducida de tu producto soñado: es **la forma más barata de comprobar tu hipótesis más arriesgada**.

| Tipo | Ejemplo |
|---|---|
| Landing page | Describes el producto, precio y un botón "Quiero acceso": mides el interés real |
| Concierge | Haces el servicio a mano para los primeros clientes |
| Mago de Oz | El cliente ve un producto; detrás lo resuelves tú manualmente |
| Producto mínimo | Una sola funcionalidad que resuelve el problema central, bien hecha |

Regla: si tardas más de **4-6 semanas** en tener algo en manos de usuarios reales, el alcance es demasiado grande.

## 4. Métricas que importan

- **Activación:** % de registrados que llegan al momento de valor ("creó su primera factura").
- **Retención por cohortes:** de los que empezaron la semana X, ¿cuántos siguen activos 1, 4, 8 semanas después? **Es la métrica más honesta de que resuelves algo.**
- **Ingresos:** MRR (ingreso recurrente mensual), churn, LTV y CAC (los viste en la fase de BI).
- Los registros totales y las visitas son métricas de vanidad si nadie vuelve.

## 5. Cobrar desde el principio

Cobrar valida mejor que cualquier encuesta. Empieza con un precio simple (uno o dos planes) y ajusta hablando con clientes.
Si vendes a empresas, el valor suele expresarse en **tiempo o dinero ahorrado**.

Desde Venezuela: comprueba **qué pasarelas de pago aceptan tu país** (muchas no operan directamente) y cómo recibirás el dinero; es frecuente
vender a clientes internacionales y estudiar opciones como plataformas que actúan como revendedor (*merchant of record*) o una entidad en otro país.
Infórmate bien y, si hace falta, con asesoría legal y contable.

## 6. Ritmo con un empleo

Con un trabajo de por medio: un problema a la vez, **una hipótesis por semana**, y conversaciones con clientes cada semana.
Pon una fecha límite para decidir si continúas, cambias de problema o lo dejas: emprender también es saber parar.

## Cómo sabes que dominas este tema

- Puedes describir el problema, quién lo sufre y cómo lo resuelve hoy, con evidencia de entrevistas.
- Tu MVP se puede construir en semanas, no en meses.
- Mides activación y retención, no solo registros.
""",
        "exercises": [
            py("st-retencion", "Retención de una cohorte", "Startup: producto y validación",
               "Escribe `retencion(actividad, semana)`. `actividad` es un diccionario `{usuario: conjunto de semanas en que estuvo activo}`, donde la semana 0 es la de registro "
               "(todos la tienen). Devuelve la fracción de usuarios activos en `semana`. Con un diccionario vacío, devuelve `0.0`.",
               starter="""
def retencion(actividad, semana):
    # tu código aquí
    pass
""",
               solution="""
def retencion(actividad, semana):
    if not actividad:
        return 0.0
    activos = sum(1 for semanas in actividad.values() if semana in semanas)
    return activos / len(actividad)
""",
               tests="""
cohorte = {"ana": {0, 1, 2, 4}, "luis": {0, 1}, "eva": {0}, "jose": {0, 2, 4}}
assert retencion(cohorte, 0) == 1.0, "En la semana 0 todos estan activos"
assert retencion(cohorte, 1) == 0.5
assert retencion(cohorte, 4) == 0.5
assert retencion(cohorte, 3) == 0.0
assert retencion({}, 1) == 0.0
"""),
            py("st-mrr", "Ingreso recurrente mensual (MRR)", "Startup: producto y validación",
               "Escribe `mrr(suscripciones)`. Cada suscripción es un diccionario con `plan` (`'mensual'` o `'anual'`), `precio` y `activa` (booleano). "
               "Suma solo las activas; las anuales cuentan como `precio / 12`. Redondea el resultado a 2 decimales.",
               starter="""
def mrr(suscripciones):
    # tu código aquí
    pass
""",
               solution="""
def mrr(suscripciones):
    total = 0.0
    for s in suscripciones:
        if not s["activa"]:
            continue
        total += s["precio"] / 12 if s["plan"] == "anual" else s["precio"]
    return round(total, 2)
""",
               tests="""
subs = [
    {"plan": "mensual", "precio": 20, "activa": True},
    {"plan": "anual", "precio": 180, "activa": True},
    {"plan": "mensual", "precio": 20, "activa": False},
    {"plan": "anual", "precio": 100, "activa": True},
]
assert mrr(subs) == 43.33, "20 + 180/12 + 100/12 = 43.33; obtuve %r" % (mrr(subs),)
assert mrr([]) == 0
"""),
            quiz("st-quiz-pregunta", "Una buena pregunta de entrevista", "Startup: producto y validación",
                 "¿Cuál de estas preguntas te da información más fiable en una entrevista de descubrimiento?",
                 ["¿Pagarías 10 dólares al mes por una app que resuelva esto?", "¿Te parece buena mi idea?",
                  "Cuéntame la última vez que te ocurrió este problema: ¿qué hiciste y cuánto te costó?", "¿Qué funcionalidades te gustaría que tuviera?"], 2,
                 "Los hechos pasados revelan el comportamiento real; las hipótesis y opiniones sobre el futuro suelen ser demasiado optimistas."),
            quiz("st-quiz-mvp", "Elegir el MVP", "Startup: producto y validación",
                 "Quieres ayudar a pequeñas clínicas a reducir las citas a las que los pacientes no se presentan. ¿Cuál es el mejor primer experimento?",
                 ["Construir durante 6 meses una plataforma completa con app móvil", "Enviar tú los recordatorios por WhatsApp a mano para 3 clínicas durante un mes y medir las ausencias",
                  "Lanzar una campaña de publicidad antes de hablar con nadie", "Diseñar el logo y la marca"], 1,
                 "Un MVP concierge prueba si el recordatorio reduce las ausencias y si las clínicas lo valoran, sin escribir casi código."),
            quiz("st-quiz-metrica", "La métrica honesta", "Startup: producto y validación",
                 "Tu producto pasó de 100 a 1000 registros este mes, pero solo el 3 % sigue activo tras dos semanas. ¿Qué concluyes?",
                 ["Va muy bien: los registros se multiplicaron por 10", "La adquisición funciona, pero el producto no retiene: hay que entender por qué abandonan antes de invertir en crecer",
                  "Hay que gastar más en publicidad", "La retención no importa en esta etapa"], 1,
                 "Sin retención, cada usuario nuevo se pierde. Primero hay que lograr que el producto resuelva el problema para un grupo que vuelva."),
            checklist("st-check", "Valida tu idea", "Startup: producto y validación",
                      "Antes de escribir código para tu startup:",
                      ["Describí el problema y a quién afecta en un párrafo", "Hice al menos 15 entrevistas sobre hechos pasados, sin presentar mi idea al principio",
                       "Encontré cómo lo resuelven hoy y cuánto les cuesta", "Definí la hipótesis más arriesgada y un MVP para probarla en menos de 6 semanas",
                       "Conseguí al menos un compromiso real (pago anticipado, piloto o carta de intención)", "Definí las métricas de activación y retención que voy a medir"]),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "proyecto-mvp",
        "phase": "producto",
        "title": "Proyecto: tu MVP en producción",
        "summary": "Construye y lanza un producto real pequeño: backend con FastAPI, base de datos, autenticación, pruebas, despliegue y usuarios reales.",
        "hours": 20,
        "theory": r"""
# Proyecto: tu MVP en producción

Este proyecto une todo lo de la ruta y es la mejor pieza de portafolio para un perfil de producto: **un sistema real, en producción, con usuarios**.
Si además resuelve un problema que validaste en el tema anterior, puede ser el inicio de tu startup.

## 1. Alcance

- **Una sola funcionalidad central** que resuelva el problema, bien hecha.
- Registro e inicio de sesión (o enlace mágico por correo).
- Un panel con la métrica que le importa al usuario.
- Nada de "nice to have" hasta tener usuarios.

## 2. Requisitos técnicos

- **Backend:** FastAPI organizado en capas (rutas → servicios → repositorios) y con validación de entrada.
- **Base de datos:** PostgreSQL con restricciones, índices en las búsquedas frecuentes y **migraciones** (Alembic).
- **Seguridad:** contraseñas con hash (Argon2 o bcrypt) o login sin contraseña, comprobación de permisos por recurso, secretos en variables de entorno, rate limiting en el login.
- **Calidad:** pruebas unitarias de la lógica central y GitHub Actions corriendo en cada push.
- **Operación:** despliegue (Vercel, Railway, Render o Fly.io), logs estructurados, monitoreo de errores y copias de seguridad.
- **Si usas IA:** un caso de uso concreto, con verificación de resultados y sin enviar datos sensibles.

## 3. Requisitos de producto

- **5-10 usuarios reales** usándolo (no solo amigos que lo prueban una vez).
- Mides **activación y retención** (aunque sea con una tabla de eventos y una consulta SQL).
- Recoges comentarios y haces al menos **una iteración** basada en ellos.

## 4. Plan sugerido (≈ 20 horas)

| Horas | Etapa |
|---|---|
| 2 | Alcance, modelo de datos y diseño de la API (escríbelo en un ADR corto) |
| 6 | Backend, base de datos y autenticación |
| 4 | Frontend mínimo (React o plantillas) |
| 3 | Pruebas, CI y despliegue |
| 2 | Monitoreo, eventos y métricas |
| 3 | Usuarios reales, entrevistas y una iteración |

## 5. Entrega

Repositorio público con README (problema, arquitectura con diagrama, decisiones y trade-offs, cómo ejecutarlo, capturas), el enlace del producto en vivo y
un post en LinkedIn contando qué aprendiste de los usuarios. En una entrevista de ingeniería de producto, poder decir "lo usan 8 personas cada semana y
cambié X porque me dijeron Y" vale más que cualquier certificado.
""",
        "exercises": [
            quiz("mvp-quiz-alcance", "Recortar el alcance", "Proyecto: MVP",
                 "Llevas 3 semanas y aún no lanzas porque quieres añadir pagos, modo oscuro, app móvil y notificaciones. ¿Qué haces?",
                 ["Terminar todo antes de lanzar", "Lanzar ya la funcionalidad central a unos pocos usuarios y decidir lo demás según lo que digan",
                  "Empezar de cero con otra tecnología", "Contratar a alguien para que lo termine"], 1,
                 "Cada semana sin usuarios es una semana sin aprender si vas en la dirección correcta."),
            checklist("mvp-entregables", "Entregables del proyecto", "Proyecto: MVP",
                      "Marca cada punto cuando esté listo.",
                      ["El alcance es una sola funcionalidad central documentada en un ADR", "Backend en capas con validación y migraciones",
                       "Autenticación segura y permisos comprobados por recurso", "Pruebas de la lógica central ejecutándose en GitHub Actions",
                       "Desplegado en producción con logs, monitoreo de errores y copias de seguridad", "Mido activación y retención",
                       "Tengo al menos 5 usuarios reales y una iteración basada en sus comentarios",
                       "README con arquitectura, decisiones y enlace en vivo; post en LinkedIn publicado"]),
        ],
    },
]
