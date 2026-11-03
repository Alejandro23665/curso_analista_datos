# Diseño de APIs REST con FastAPI

Una **API** (*Application Programming Interface*) es la puerta por la que otros programas hablan con el tuyo. Cuando el frontend de tu
chatbot envía la pregunta del usuario, cuando la app de un cliente consulta su inventario o cuando tu código llama a un modelo de IA,
lo hacen a través de una API.

En este capítulo vas a aprender:

- Cómo funciona **HTTP**, el protocolo sobre el que viajan casi todas las APIs.
- Cómo se **diseña** una API REST: rutas, métodos, códigos de estado, errores, paginación, idempotencia y versionado.
- Cómo se **construye** con **FastAPI**, el framework de Python que usan muchas empresas de IA (y el backend de esta misma plataforma).
- Qué pasa **por debajo** (DNS, TCP, TLS) y cómo enviar datos en tiempo real (SSE, WebSockets).

Diseñar bien una API importa mucho: es un **contrato**. Una vez que un frontend, una app móvil o un cliente dependen de ella, cambiarla
rompe cosas. Una API predecible ahorra errores y trabajo durante años.

---

## 1. HTTP en lo esencial

HTTP funciona con **peticiones** y **respuestas**. El cliente (un navegador, una app, tu script) envía una petición; el servidor
responde.

### Una petición

```
POST /pedidos HTTP/1.1
Host: api.mitienda.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOi...

{"producto_id": 7, "cantidad": 2}
```

| Parte | Qué es |
|---|---|
| **Método** (`POST`) | Qué quieres hacer |
| **Ruta** (`/pedidos`) | Sobre qué recurso |
| **Cabeceras** (*headers*) | Metadatos: formato del cuerpo, credenciales, idioma... |
| **Cuerpo** (*body*) | Los datos que envías (normalmente JSON). Las peticiones `GET` no llevan cuerpo |

### Una respuesta

```
HTTP/1.1 201 Created
Content-Type: application/json

{"id": 1042, "producto_id": 7, "cantidad": 2, "estado": "pendiente"}
```

Un **código de estado** (`201`), cabeceras y, normalmente, un cuerpo JSON.

### Los métodos

| Método | Uso | ¿Idempotente? |
|---|---|---|
| `GET` | Leer | Sí |
| `POST` | Crear un recurso o ejecutar una acción | **No** |
| `PUT` | Reemplazar un recurso completo | Sí |
| `PATCH` | Modificar parte de un recurso | Depende |
| `DELETE` | Eliminar | Sí |

**Idempotente** significa que repetir la petición deja el sistema igual que hacerla una vez. Borrar el pedido 42 dos veces deja el mismo
resultado (el pedido 42 no existe). Crear un pedido dos veces crea **dos** pedidos. Esto importa porque **las redes fallan** y los
clientes reintentan: volveremos a ello en la sección 7.

`GET` además debe ser **seguro**: no debe cambiar nada en el servidor. Nunca hagas que un `GET /borrar?id=5` borre cosas: los navegadores,
los buscadores y las cachés hacen peticiones `GET` por su cuenta.

### Ver HTTP con tus ojos

Abre las herramientas del navegador (F12) → pestaña **Network** (Red) y recarga cualquier página, por ejemplo esta plataforma. Verás cada
petición a `/api/...` con su método, código de estado, cabeceras y respuesta. Es la mejor forma de entender HTTP y de depurar tu
frontend.

---

## 2. Diseñar los recursos y las rutas

En una API REST, las rutas nombran **cosas** (recursos), con **sustantivos en plural**. La acción la indica el **método**:

| Petición | Significado |
|---|---|
| `GET /pedidos` | Listar pedidos |
| `GET /pedidos/42` | Obtener el pedido 42 |
| `POST /pedidos` | Crear un pedido |
| `PATCH /pedidos/42` | Modificar parte del pedido 42 |
| `DELETE /pedidos/42` | Borrar el pedido 42 |
| `GET /clientes/7/pedidos` | Listar los pedidos del cliente 7 (relación) |

Errores típicos de diseño: `GET /obtenerPedidos`, `POST /crearPedidoNuevo`, `GET /pedidos/borrar/42`. El verbo ya está en el método.

### Parámetros de ruta y de consulta

- **De ruta** (`/pedidos/42`): identifican **un** recurso concreto.
- **De consulta** o *query string* (`/pedidos?estado=pagado&pagina=2`): filtran, ordenan o paginan una colección. Van después de `?`,
  separados por `&`.

### Acciones que no son CRUD

A veces hay acciones que no encajan en crear/leer/modificar/borrar, como "cancelar un pedido" o "reenviar un correo". Se suelen modelar
como un sub-recurso con `POST`: `POST /pedidos/42/cancelacion`. Lo importante es ser **consistente** en toda la API.

---

## 3. Códigos de estado

El código de estado le dice al cliente **qué pasó** sin tener que leer el cuerpo. Usar el correcto permite que el frontend reaccione bien.

| Código | Significado | Cuándo |
|---|---|---|
| `200 OK` | Todo bien | Lecturas y actualizaciones correctas |
| `201 Created` | Se creó algo | Tras un `POST` que crea un recurso (devuelve el recurso creado) |
| `204 No Content` | Bien, sin cuerpo | Típico de `DELETE` |
| `400 Bad Request` | La petición está mal formada | JSON roto, parámetros incoherentes |
| `401 Unauthorized` | No sé quién eres | Falta el token o es inválido |
| `403 Forbidden` | Sé quién eres, pero no puedes | Sin permiso sobre ese recurso |
| `404 Not Found` | No existe | O no debes saber que existe |
| `409 Conflict` | Choca con el estado actual | Email ya registrado, pedido ya enviado |
| `422 Unprocessable Entity` | Datos inválidos | Errores de validación (FastAPI lo usa automáticamente) |
| `429 Too Many Requests` | Demasiadas peticiones | Límite de uso superado |
| `500 Internal Server Error` | Error del servidor | Un bug tuyo; **nunca** es culpa del cliente |
| `503 Service Unavailable` | Servicio no disponible | Base de datos caída, mantenimiento |

Las familias: **2xx** éxito, **4xx** error del cliente (puede corregir su petición), **5xx** error del servidor.

Dos dudas frecuentes:

- **401 o 403:** 401 cuando no hay identidad válida ("inicia sesión"); 403 cuando la identidad es válida pero no tiene permiso. Si
  revelar que un recurso existe ya es un problema (el proyecto privado de otra persona), muchas APIs devuelven 404.
- **Nunca devuelvas `200` con un mensaje de error en el cuerpo** (`{"error": "email duplicado"}` con 200). El cliente que solo mira el
  código creerá que todo fue bien.

---

## 4. FastAPI desde cero

**FastAPI** es un framework para construir APIs en Python. Sus ventajas: usa las **anotaciones de tipo** para validar automáticamente los
datos, genera documentación interactiva y es rápido.

### Instalar y arrancar

```bash
pip install fastapi uvicorn
```

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/salud")
def salud():
    return {"estado": "ok"}
```

```bash
uvicorn main:app --reload
```

- `app = FastAPI()` crea la aplicación.
- `@app.get("/salud")` es un **decorador**: registra la función de debajo como la que responde a `GET /salud`.
- Lo que devuelve la función (un diccionario) se convierte automáticamente en JSON.
- `uvicorn` es el servidor que ejecuta la app; `--reload` la reinicia al guardar cambios (solo en desarrollo).

Abre `http://localhost:8000/salud` y verás `{"estado": "ok"}`. Abre `http://localhost:8000/docs` y verás la **documentación interactiva**
que FastAPI genera sola, donde puedes probar cada endpoint.

### Parámetros de ruta

```python
@app.get("/pedidos/{pedido_id}")
def obtener_pedido(pedido_id: int):
    return {"id": pedido_id}
```

`{pedido_id}` en la ruta se pasa a la función. Como está anotado `int`, FastAPI **convierte y valida**: `/pedidos/42` funciona;
`/pedidos/abc` responde automáticamente `422` con una explicación del error.

### Parámetros de consulta

Los parámetros de la función que **no** están en la ruta se leen de la query string:

```python
@app.get("/pedidos")
def listar_pedidos(estado: str | None = None, pagina: int = 1, por_pagina: int = 20):
    return {"estado": estado, "pagina": pagina, "por_pagina": por_pagina}
```

`GET /pedidos?estado=pagado&pagina=2` → `estado="pagado"`, `pagina=2`, `por_pagina=20` (el valor por defecto).

### El cuerpo de la petición: modelos de Pydantic

Para recibir JSON se define un **modelo** con Pydantic (la librería de validación que usa FastAPI):

```python
from pydantic import BaseModel, Field

class PedidoNuevo(BaseModel):
    producto_id: int
    cantidad: int = Field(gt=0, le=100)          # mayor que 0, como mucho 100
    nota: str | None = Field(default=None, max_length=200)

@app.post("/pedidos", status_code=201)
def crear_pedido(pedido: PedidoNuevo):
    # aquí pedido.producto_id, pedido.cantidad y pedido.nota ya están validados
    return {"id": 1042, **pedido.model_dump()}
```

Si el cliente envía `{"producto_id": 7, "cantidad": 0}`, FastAPI responde **422** sin que llegue a ejecutarse tu función, con un cuerpo
que dice exactamente qué campo falló y por qué. Tu función **solo recibe datos válidos**.

`Field(...)` añade reglas: `gt`/`ge` (mayor / mayor o igual), `lt`/`le`, `min_length`/`max_length`, `pattern` (expresión regular).
`model_dump()` convierte el modelo en diccionario.

### Modelos de respuesta

También puedes declarar **qué devuelve** un endpoint. FastAPI filtrará la respuesta para que solo salgan esos campos, algo muy útil para
no filtrar datos internos por accidente (como el hash de una contraseña):

```python
class UsuarioPublico(BaseModel):
    id: int
    nombre: str
    email: str

@app.get("/usuarios/{usuario_id}", response_model=UsuarioPublico)
def obtener_usuario(usuario_id: int):
    usuario = repositorio.buscar(usuario_id)   # puede tener más campos, como password_hash
    return usuario                              # solo salen id, nombre y email
```

### Errores: HTTPException

```python
from fastapi import HTTPException

@app.get("/pedidos/{pedido_id}")
def obtener_pedido(pedido_id: int):
    pedido = repositorio.buscar(pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido
```

`raise HTTPException(...)` corta la ejecución y responde con ese código y `{"detail": "..."}`. Usa siempre el mismo formato de error en
toda la API, para que el frontend pueda mostrarlos de forma uniforme.

---

## 5. Validar todo lo que entra

**Nunca confíes en el cliente.** Aunque tu frontend valide los formularios, cualquiera puede enviar peticiones directamente a tu API
(con `curl`, con un script, saltándose tu interfaz). La validación del servidor es la única que cuenta.

Pydantic hace gran parte del trabajo, pero entender qué hace por dentro te prepara para validar donde no hay Pydantic (un script, un
webhook, datos de un archivo). Validar consiste en:

1. **Presencia**: ¿están los campos obligatorios? ¿Qué hago con los opcionales ausentes?
2. **Tipo**: ¿es un número, un texto, un booleano? Cuidado: en Python `True` es también un `int` (`isinstance(True, int)` es `True`), un
   detalle que puede colarse en validaciones hechas a mano.
3. **Normalización**: quitar espacios antes de medir un texto, pasar emails a minúsculas.
4. **Reglas**: longitudes, rangos, formatos (un email con algo antes y después de la `@` y un punto en el dominio).
5. **Informar todos los errores a la vez**, por campo, no solo el primero. Un formulario que te dice los errores de uno en uno es
   frustrante.

Un formato de respuesta habitual para errores de validación es un diccionario `{campo: mensaje}`:

```json
{
  "detail": {
    "nombre": "Debe tener entre 2 y 50 caracteres",
    "email": "No es un email válido"
  }
}
```

Y la validación de **reglas de negocio** que dependen del estado (¿ya existe ese email?) va después de la validación de formato, y suele
responder `409`.

---

## 6. Paginación

**Nunca devuelvas una colección sin límite.** Hoy tienes 50 pedidos; dentro de un año, 2 millones, y un `GET /pedidos` sin límite tumbará
tu servidor y el navegador del cliente.

### Paginación por páginas

El cliente pide `?pagina=2&por_pagina=20` y la respuesta incluye los elementos y **metadatos** para construir la navegación:

```json
{
  "items": [ ... ],
  "pagina": 2,
  "por_pagina": 20,
  "total": 137,
  "paginas": 7
}
```

Las cuentas que hay detrás:

- Si las páginas empiezan en 1, la página `p` empieza en la posición `(p - 1) * por_pagina`. (La página 1 empieza en 0.)
- El número de páginas es el total dividido entre el tamaño **redondeando hacia arriba**: 137 elementos de 20 en 20 son 7 páginas (la
  última con 17). En Python, `math.ceil(137 / 20)` o el truco entero `-(-137 // 20)`.
- Una página más allá del final no es un error: devuelve una lista vacía.
- **Valida** los parámetros: `pagina` mínima 1 y un `por_pagina` con máximo (por ejemplo 100). Sin máximo, alguien pedirá `por_pagina=1000000`.

En SQL se traduce en `LIMIT por_pagina OFFSET (pagina - 1) * por_pagina`, con un `ORDER BY` estable.

### Paginación por cursor

En lugar de "la página 3", el cliente dice "dame los 20 siguientes **después del id 1042**" (`?despues_de=1042&limite=20`), y la consulta es
`WHERE id > 1042 ORDER BY id LIMIT 20`. Ventajas: es estable aunque se inserten filas mientras navegas (con páginas, un elemento nuevo
desplaza todo y puedes ver duplicados) y es más rápida con tablas enormes. Es lo que usan los feeds y las APIs de mensajes.

---

## 7. Idempotencia en operaciones críticas

Imagina este escenario: tu app envía `POST /pagos` para cobrar 50 dólares. El servidor cobra, pero la respuesta se pierde por un corte de
red. La app no sabe si se cobró, y **reintenta**. Resultado: el cliente paga 100 dólares.

La solución estándar (la usan Stripe, PayPal y casi todas las pasarelas de pago) es la **clave de idempotencia**:

1. El cliente genera un identificador único para **esa operación** (por ejemplo, un UUID) y lo envía en una cabecera:
   `Idempotency-Key: 6f1c...`. Si reintenta, envía **la misma clave**.
2. El servidor, antes de ejecutar, comprueba si ya procesó esa clave:
   - Si **no**: ejecuta la operación, **guarda el resultado asociado a la clave** y responde.
   - Si **sí**: no ejecuta nada otra vez; devuelve **el mismo resultado** que la primera vez.
3. Si llega una clave ya usada pero con **datos distintos** (otro monto), es un error del cliente: se rechaza en lugar de devolver un
   resultado que no corresponde.

Así, reintentar es seguro: pase lo que pase con la red, el cobro ocurre una sola vez. En un sistema real las claves se guardan en la base
de datos (con un índice único) y caducan pasado un tiempo.

Esta idea aparece en entrevistas de backend con frecuencia ("¿cómo evitarías cobros duplicados?") y en el trabajo con cualquier
operación que no deba repetirse: enviar un correo, crear una factura, descontar stock.

---

## 8. Evolución y buenas prácticas del contrato

- **Versiona** cuando rompas la compatibilidad: `/v1/pedidos`, `/v2/pedidos`. **Añadir** un campo opcional no rompe a nadie; **quitar o
  renombrar** un campo, o cambiar su tipo, sí.
- **Consistencia**: un solo estilo de nombres (`snake_case` o `camelCase`, no ambos), el mismo formato de errores en todos los endpoints,
  los mismos nombres de parámetros de paginación.
- **Fechas** en formato ISO 8601 con zona horaria: `2026-11-02T14:30:00Z`.
- **Dinero**: nunca en `float` (recuerda `0.1 + 0.2`). Usa enteros en céntimos o decimales.
- **Documenta**: FastAPI genera `/docs`; añade descripciones y ejemplos a tus modelos.

---

## 9. Organizar una API que crece

Cuando la API tiene muchos endpoints, no los pongas todos en `main.py`. FastAPI permite **routers** para separar por dominio:

```python
# pedidos/rutas.py
from fastapi import APIRouter

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get("")
def listar(): ...

@router.post("", status_code=201)
def crear(pedido: PedidoNuevo): ...
```

```python
# main.py
from fastapi import FastAPI
from pedidos.rutas import router as pedidos_router

app = FastAPI()
app.include_router(pedidos_router)
```

Y separa en capas (lo verás en *Arquitectura de software*):

- **Rutas**: reciben la petición HTTP, validan y devuelven la respuesta. Nada de lógica de negocio.
- **Servicios**: la lógica de negocio ("no se puede cancelar un pedido ya enviado"), sin saber nada de HTTP.
- **Repositorios**: el acceso a la base de datos.

### Dependencias

FastAPI tiene un sistema de **dependencias** (`Depends`) para reutilizar lógica común en muchos endpoints: obtener la sesión de base de
datos, comprobar el usuario autenticado, leer la configuración.

```python
from fastapi import Depends

def usuario_actual(token: str = Depends(leer_token)):
    usuario = verificar(token)
    if usuario is None:
        raise HTTPException(401, "Sesión no válida")
    return usuario

@app.get("/mis-pedidos")
def mis_pedidos(usuario = Depends(usuario_actual)):
    return repositorio.pedidos_de(usuario.id)
```

Cualquier endpoint que declare `Depends(usuario_actual)` exige un usuario válido, sin repetir el código.

### Probar la API

FastAPI incluye un cliente de pruebas que hace peticiones a tu app sin arrancar un servidor:

```python
from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)

def test_crear_pedido_valida_cantidad():
    respuesta = cliente.post("/pedidos", json={"producto_id": 7, "cantidad": 0})
    assert respuesta.status_code == 422

def test_salud():
    assert cliente.get("/salud").json() == {"estado": "ok"}
```

---

## 10. CORS: cuando el frontend está en otro dominio

Si tu frontend está en `https://mi-demo.vercel.app` y tu API en `https://mi-api.onrender.com`, el navegador **bloquea** por defecto las
peticiones del uno al otro (es una protección de seguridad llamada *same-origin policy*). Para permitirlas, la API debe declarar qué
orígenes acepta, con **CORS**:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mi-demo.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

En producción, lista **solo** los dominios de tu frontend; `allow_origins=["*"]` permite que cualquier web llame a tu API desde el
navegador de sus usuarios. El error típico que verás en la consola del navegador cuando falta CORS es *"has been blocked by CORS policy"*.

---

## 11. Lo que pasa por debajo: redes en lo esencial

La pregunta clásica de entrevista junior es *"¿qué pasa cuando escribes una URL en el navegador?"*. La respuesta, por capas:

1. **DNS**: el navegador pregunta qué dirección IP corresponde a `midominio.com`. Un **registro A** del dominio apunta a una IP; un
   **CNAME** apunta a otro nombre (lo que te piden configurar servicios como Vercel). La respuesta se guarda en caché un tiempo, por eso la
   segunda visita es más rápida y los cambios de DNS tardan en propagarse.
2. **TCP**: abre una conexión fiable con esa IP. Los datos viajan en paquetes numerados; si uno se pierde, se reenvía y llegan en orden.
   **UDP**, la alternativa, no garantiza entrega ni orden, pero es más rápido (video, voz, juegos).
3. **TLS**: con `https`, se cifra la conexión y se verifica el **certificado** del servidor (que demuestra que es quien dice ser).
4. **HTTP**: se envía la petición (método, ruta, cabeceras, cuerpo) y el servidor responde con código, cabeceras y cuerpo.
5. **Renderizado**: el navegador procesa el HTML, pide el CSS, el JavaScript y las imágenes (más peticiones HTTP) y dibuja la página.

---

## 12. Datos en tiempo real: polling, SSE y WebSockets

HTTP es "pregunta y respuesta": el servidor no puede hablar si el cliente no pregunta. Para que el servidor envíe datos según los tiene,
hay tres técnicas:

| Técnica | Cómo funciona | Cuándo usarla |
|---|---|---|
| *Polling* | El cliente pregunta cada X segundos "¿hay algo nuevo?" | Casos simples y poco frecuentes; desperdicia peticiones |
| **SSE** (*Server-Sent Events*) | Una petición HTTP que el servidor mantiene abierta y por la que envía eventos | Un solo sentido, servidor → cliente: **la respuesta de un chatbot con streaming** |
| **WebSockets** | Conexión bidireccional que queda abierta | Los dos lados envían en cualquier momento: chat entre personas, colaboración en vivo |

Para tu chatbot, **SSE** es lo natural: el usuario envía una pregunta (una petición normal) y el servidor va enviando los fragmentos de la
respuesta del modelo a medida que se generan. En FastAPI:

```python
from fastapi.responses import StreamingResponse

def generar_respuesta(pregunta: str):
    for fragmento in modelo.stream(pregunta):       # cada trozo que produce el LLM
        yield f"data: {fragmento}\n\n"              # formato SSE: "data: ..." y una línea en blanco
    yield "data: [DONE]\n\n"

@app.post("/chat")
def chat(mensaje: MensajeChat):
    return StreamingResponse(generar_respuesta(mensaje.texto), media_type="text/event-stream")
```

Fíjate en que es un **generador** (`yield`), como los que viste en *Python profesional*: cada fragmento se envía en cuanto existe. En el
tema *Interfaces para apps con IA* verás cómo leerlo desde React.

Otros formatos que verás nombrados: **GraphQL** (el cliente pide exactamente los campos que quiere en una sola consulta) y **gRPC**
(comunicación rápida entre servicios con mensajes binarios). Para tus proyectos, REST + SSE cubre casi todo.

---

## 13. Errores típicos

| Síntoma | Causa | Solución |
|---|---|---|
| `422 Unprocessable Entity` inesperado | El JSON no coincide con el modelo (nombre o tipo de campo) | Lee el `detail` de la respuesta: dice qué campo falló |
| El frontend dice "blocked by CORS policy" | La API no permite ese origen | Configura `CORSMiddleware` con el dominio del frontend |
| `405 Method Not Allowed` | La ruta existe, pero no con ese método | Revisa `GET`/`POST` en cliente y servidor |
| Un error de negocio llega como 500 | Una excepción sin capturar | Conviértela en `HTTPException` con el código adecuado |
| Cobros o correos duplicados | Reintentos de operaciones no idempotentes | Clave de idempotencia |
| La API se vuelve lenta con el tiempo | Listados sin paginar | Pagina siempre y limita el tamaño |
| Datos internos en la respuesta | Devolver el objeto completo de la base de datos | `response_model` con solo los campos públicos |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| HTTP | Método + ruta + cabeceras + cuerpo; respuesta con código, cabeceras y cuerpo |
| REST | Sustantivos en plural; el método indica la acción; filtros en la query string |
| Códigos | 2xx bien, 4xx culpa del cliente, 5xx culpa tuya; 401 frente a 403; nunca 200 con error |
| FastAPI | Decoradores por ruta; los tipos validan; `/docs` automático |
| Pydantic | Modelos de entrada con `Field`; `response_model` para la salida |
| Validación | En el servidor, siempre; todos los errores por campo |
| Paginación | `(p - 1) * n`, páginas redondeando hacia arriba, máximo de tamaño; o cursor |
| Idempotencia | Clave única por operación; misma clave → mismo resultado sin repetir |
| Organización | Routers por dominio; rutas, servicios y repositorios; `Depends` |
| CORS | Lista solo tus dominios |
| Tiempo real | SSE para el streaming de un chatbot; WebSockets si ambos lados hablan |

## Autoevaluación final

1. ¿Qué diferencia hay entre parámetros de ruta y de consulta? Pon un ejemplo de cada uno.
2. ¿Qué significa que un método sea idempotente y por qué importa?
3. ¿Qué código devuelves si alguien intenta registrarse con un email que ya existe?
4. Envías un JSON con un campo de tipo incorrecto a un endpoint de FastAPI. ¿Qué pasa?
5. ¿Para qué sirve `response_model`?
6. Con 45 elementos y 10 por página, ¿cuántas páginas hay y en qué posición empieza la página 3?
7. Explica con tus palabras cómo funciona una clave de idempotencia.
8. ¿Por qué SSE es adecuado para el streaming de un chatbot?

**Respuestas:** 1) Los de ruta identifican un recurso (`/pedidos/42`); los de consulta filtran o paginan (`/pedidos?estado=pagado`).
2) Que repetirlo deja el sistema igual que hacerlo una vez; importa porque los clientes reintentan cuando la red falla. 3) `409
Conflict`. 4) FastAPI responde `422` automáticamente sin ejecutar tu función, indicando qué campo falló. 5) Para declarar y filtrar lo que
devuelve el endpoint, evitando enviar campos internos. 6) 5 páginas (la última con 5 elementos); la página 3 empieza en la posición 20.
7) El cliente envía un identificador único por operación; el servidor guarda el resultado asociado y, si la clave se repite, devuelve el
mismo resultado sin ejecutar otra vez; con datos distintos, rechaza la petición. 8) Porque el flujo es de un solo sentido (servidor →
cliente) mientras se genera la respuesta, y funciona sobre HTTP normal.
