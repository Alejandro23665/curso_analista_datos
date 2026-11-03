# Diseño de sistemas: escalar, caché, colas y fiabilidad

Tu MVP funciona con 10 usuarios en un servidor. ¿Qué pasa con 10 000? ¿Y cuando el proveedor de correo tarda 5 segundos, la API del
modelo devuelve errores de saturación o alguien envía mil peticiones por minuto? El **diseño de sistemas** trata de cómo construir
aplicaciones que siguen funcionando cuando crece la carga y cuando las cosas fallan, porque siempre fallan.

En las entrevistas de backend aparece a menudo una pregunta abierta de diseño ("¿cómo diseñarías un acortador de URLs?", "¿y el backend
de un chatbot para miles de negocios?"). Para un puesto junior no esperan una arquitectura de Google: esperan que conozcas las piezas
básicas, que razones con números y que expliques los compromisos. Este capítulo te da esas piezas.

---

## 1. Estimar con números aproximados

Antes de diseñar, **estima la escala**. No hace falta precisión: basta con el orden de magnitud.

Un día tiene 86 400 segundos (≈ 10⁵ para cuentas rápidas). Ejemplo: 200 000 usuarios activos al día, con unas 30 peticiones cada uno:

```
200 000 × 30 = 6 000 000 peticiones al día
6 000 000 / 86 400 ≈ 69 peticiones por segundo de media
pico ≈ 3-5 veces la media ≈ 200-350 por segundo
```

Un solo servidor modesto con FastAPI atiende cientos de peticiones simples por segundo, así que esta app **no necesita** una arquitectura
compleja. Esa conclusión, sacada en un minuto, es exactamente lo que buscan en una entrevista.

Números de referencia (órdenes de magnitud):

| Operación | Tiempo aproximado |
|---|---|
| Leer de memoria | Nanosegundos |
| Leer de Redis (en la misma red) | ~0,5-1 ms |
| Consulta simple con índice en PostgreSQL | ~1-5 ms |
| Petición entre servicios en el mismo centro de datos | ~1-10 ms |
| Petición a otro continente | ~100-200 ms |
| Respuesta completa de un LLM | Segundos |

La conclusión práctica: **la red y las llamadas externas dominan**. Por eso una caché o evitar una consulta N+1 marca más diferencia que
optimizar un bucle de Python.

---

## 2. Escalar: vertical y horizontal

- **Vertical**: un servidor más grande (más CPU, más memoria). Simple, sin cambiar el código, pero con un límite y un único punto de fallo.
- **Horizontal**: **más servidores** iguales detrás de un **balanceador de carga** que reparte las peticiones.

```
                ┌──► servidor 1 ──┐
usuarios ──► balanceador ──► servidor 2 ──┼──► base de datos
                └──► servidor 3 ──┘
```

### Servidores sin estado

Para escalar horizontalmente, los servidores deben ser **sin estado** (*stateless*): cualquier servidor puede atender cualquier petición.
Un error típico: guardar las sesiones **en la memoria** de cada servidor. Con un servidor funciona; con tres detrás de un balanceador, el
usuario inicia sesión en el servidor 1, su siguiente petición va al 2, que no lo conoce, y **pierde la sesión al azar**.

Soluciones: guardar el estado compartido fuera de los servidores (sesiones en la base de datos o en **Redis**) o usar **cookies
firmadas** que contienen la información (como hace esta plataforma). Lo mismo para archivos subidos: van a un almacenamiento de objetos
(S3 o similar), no al disco del servidor.

### La base de datos suele ser el cuello de botella

Los servidores de aplicación se multiplican fácilmente; la base de datos no. Estrategias, en orden de complejidad:

1. **Índices y consultas eficientes** (capítulo de bases de datos). Resuelven la mayoría de los problemas.
2. **Caché** (sección 3).
3. **Réplicas de lectura**: copias de la base que reciben los cambios de la principal y atienden las lecturas.
4. **Particionado** (*sharding*): dividir los datos entre varias bases (sección 7).

### Retraso de replicación

Las réplicas reciben los cambios con un pequeño **retraso** (milisegundos o segundos). Consecuencia: un usuario cambia su foto de perfil
(escritura en la principal), recarga la página (lectura en una réplica) y **sigue viendo la foto vieja**. No es un error del navegador.
Solución habitual: **leer de la principal** lo que el usuario acaba de escribir (por ejemplo, sus propios datos durante unos segundos tras
una escritura).

---

## 3. Caché

Una **caché** guarda el resultado de una operación costosa para reutilizarlo. Si la página de un producto se consulta 1 000 veces por
minuto y cambia una vez al día, no tiene sentido ir a la base 1 000 veces.

```
petición ──► ¿está en la caché? ──sí──► devolverla (rápido)
                    │
                    no
                    ▼
            consultar la base ──► guardar en la caché ──► devolverla
```

Este patrón se llama ***cache-aside***. Dónde puede vivir la caché: en la memoria del proceso (lo más rápido, pero no se comparte entre
servidores), en **Redis** (compartida), en una **CDN** (archivos estáticos y páginas, cerca del usuario) o en el navegador (cabeceras
HTTP `Cache-Control`).

### El problema difícil: la invalidación

Si los datos cambian, la caché queda **desactualizada**. Estrategias:

- **Tiempo de vida (TTL)**: cada entrada caduca tras N segundos. Simple y robusto; aceptas datos de hasta N segundos de antigüedad.
- **Invalidar al escribir**: al actualizar el producto, borrar su entrada de la caché.
- Normalmente se combinan las dos.

### Probar código que depende del tiempo

Un TTL depende del reloj. Para probarlo sin esperar de verdad, se **inyecta el reloj** (inyección de dependencias, capítulo de
arquitectura): en producción se usa `time.monotonic` (un reloj que solo avanza, adecuado para medir intervalos, a diferencia de la hora
del sistema, que puede cambiar), y en las pruebas una función falsa que devuelve el valor que quieras:

```python
class RelojFalso:
    def __init__(self):
        self.t = 0.0
    def __call__(self):          # permite usar el objeto como función: reloj()
        return self.t
    def avanzar(self, segundos):
        self.t += segundos

reloj = RelojFalso()
reloj()            # 0.0
reloj.avanzar(30)
reloj()            # 30.0
```

Fíjate en los límites al comparar: "caduca cuando han pasado `ttl` segundos **o más**" se traduce en `>=`, no en `>`. Las pruebas deben
cubrir justo el instante límite.

### Política de expulsión: LRU

Una caché en memoria tiene **capacidad limitada**. Cuando se llena, hay que expulsar algo. La política más usada es **LRU** (*Least
Recently Used*): se expulsa la entrada **usada hace más tiempo**, suponiendo que lo usado recientemente se volverá a usar.

```
capacidad 3
guardar A, B, C       → orden de uso: A, B, C    (A es la menos reciente)
obtener A             → orden: B, C, A           (leer también cuenta como uso)
guardar D             → caché llena: se expulsa B → C, A, D
```

Los dos detalles que más se olvidan: **leer** una entrada también la marca como reciente, y **actualizar** una clave existente no debe
expulsar nada. En Python, `collections.OrderedDict` mantiene el orden de inserción y tiene operaciones para mover una clave al final
(`move_to_end`) y sacar la primera (`popitem(last=False)`); con ellas, la entrada menos reciente está siempre al principio. Para cachear
funciones puras, la librería estándar ya trae `functools.lru_cache`.

---

## 4. Colas y tareas en segundo plano

Al registrarse un usuario, envías un correo de bienvenida con un proveedor que a veces tarda 5 segundos. Si lo envías **dentro** de la
petición de registro, el usuario espera 5 segundos, y si el proveedor falla, el registro parece fallar.

La solución: una **cola**. La petición deja una tarea ("enviar bienvenida a usuario 42") y responde de inmediato; un proceso aparte (un
***worker***) toma las tareas de la cola y las ejecuta, con reintentos si fallan.

```
API ──► cola (Redis, RabbitMQ, SQS) ──► worker(s) ──► proveedor de correo
 │
 └──► responde al usuario en milisegundos
```

Úsala para todo lo que es **lento, falible o no necesita respuesta inmediata**: correos, procesar documentos para un RAG, generar
informes, llamadas largas a un LLM, webhooks a terceros. Herramientas en Python: **Celery**, **RQ**, **Dramatiq**, o las tareas de fondo
de FastAPI para casos muy simples (que se pierden si el servidor se reinicia).

Propiedades importantes:

- Las colas suelen garantizar entrega **al menos una vez**: una tarea puede ejecutarse **dos veces** (si el worker cae después de hacerla
  pero antes de confirmarla). Por eso las tareas deben ser **idempotentes** (capítulo de arquitectura distribuida).
- Una **cola de mensajes muertos** (*dead letter queue*) recoge las tareas que fallan todos los reintentos, para revisarlas a mano.
- Las colas **absorben picos**: si llegan 10 000 tareas de golpe, se procesan a su ritmo sin tumbar el sistema.

---

## 5. Fiabilidad: reintentos, tiempos de espera y límites

### Tiempos de espera (*timeouts*)

Toda llamada externa necesita un **tiempo máximo**. Sin él, si el servicio externo se cuelga, tus peticiones se acumulan esperando para
siempre y tu aplicación se cae con él.

### Reintentos con espera exponencial

Muchos fallos son **transitorios** (un error de red, un `429` o `503` de una API saturada): vuelven a funcionar si esperas un poco. Pero
reintentar **inmediatamente** y muchas veces empeora las cosas (si mil clientes reintentan a la vez, el servicio saturado recibe aún más
carga). La práctica estándar: **espera exponencial** con un máximo.

```
espera = min(base × 2^n, máximo)        n = 0, 1, 2, ...

con base = 1 s y máximo = 10 s:
intento fallido 0 → espera 1 s
intento fallido 1 → espera 2 s
intento fallido 2 → espera 4 s
intento fallido 3 → espera 8 s
intento fallido 4 → espera 10 s   (16 s superaría el máximo)
```

Detalles de diseño:

- Un **número máximo de intentos**; si se agotan, se propaga el error (no se oculta).
- **No se espera después del último intento**: no tiene sentido dormir si ya no vas a reintentar.
- Se suele añadir **aleatoriedad** (*jitter*) a la espera, para que los clientes no reintenten todos a la vez.
- Solo se reintenta lo que **puede** tener éxito al repetirse: un `400` (petición mal formada) fallará siempre.
- Solo se reintentan operaciones **idempotentes** o protegidas con una clave de idempotencia (no quieres cobrar dos veces).
- Para probarlo sin esperar de verdad, la función de dormir se **inyecta** (como el reloj): en las pruebas, una función que solo registra
  cuánto le pidieron esperar.

Los SDK de los proveedores de LLM (como el de Anthropic) ya reintentan automáticamente los errores transitorios con espera exponencial.

### Limitar peticiones (*rate limiting*)

Protege tu API (y tu factura del LLM) de abusos y picos: "como máximo N peticiones por usuario y periodo". El algoritmo más usado es el
**cubo de fichas** (*token bucket*):

- El cubo tiene una **capacidad** máxima de fichas y empieza **lleno**.
- Cada petición **gasta una ficha**; si no hay ninguna, se rechaza (respuesta `429 Too Many Requests`).
- Las fichas se **recargan** a un ritmo constante (por ejemplo, 2 por segundo), sin superar la capacidad.

Ejemplo con capacidad 5 y recarga de 1 ficha por segundo:

```
t = 0 s     cubo: 5    llegan 5 peticiones → todas permitidas, cubo: 0
t = 0 s     llega otra → rechazada (0 fichas)
t = 2,5 s   recarga: 0 + 2,5 × 1 = 2,5 fichas
            llegan 3 peticiones → 2 permitidas (quedan 0,5), 1 rechazada
t = 100 s   recarga: 0,5 + 97,5 = 98 → se limita a la capacidad: 5
```

Las ventajas: permite **ráfagas** cortas (hasta la capacidad) y limita el ritmo medio. La recarga no necesita un temporizador: se calcula
en cada petición a partir del **tiempo transcurrido** desde la última (con el reloj inyectado). En producción, con varios servidores, el
estado del cubo se guarda en Redis para que todos compartan el límite.

---

## 6. Observabilidad

Cuantas más piezas tiene un sistema, más difícil es saber qué falló. Lo viste en el capítulo de calidad: **logs estructurados**,
**métricas** (latencia, tráfico, errores, saturación) y **seguimiento de errores**. En sistemas con colas y varios servicios se añade la
**trazabilidad distribuida**: un identificador de petición (*request id* o *trace id*) que se propaga por todas las piezas, para seguir
una petición de principio a fin en los logs.

---

## 7. Particionado

Cuando una sola base de datos no puede con todos los datos o escrituras, se **particiona**: cada base guarda una parte. La pregunta es
**qué partición le toca a cada dato**. Lo habitual es calcular un **hash** de una clave (el id del cliente) y tomar el resto entre el
número de particiones:

```
partición = hash(clave) mod n
```

Requisitos:

- **Determinista**: la misma clave siempre debe ir a la misma partición, en cualquier servidor y en cualquier ejecución. Ojo: la función
  `hash()` de Python **cambia entre ejecuciones** para los textos (por seguridad), así que no sirve; se usa un hash estable como los de
  `hashlib` (MD5, SHA-256), convirtiendo su resultado hexadecimal en un entero (`int(texto_hex, 16)`).
- **Bien repartido**: que ninguna partición reciba mucho más que las demás.
- **Cuidado al cambiar n**: con `mod n`, al pasar de 4 a 5 particiones casi todas las claves cambian de partición. El **hashing
  consistente** reduce ese movimiento; es un tema de entrevistas más avanzadas.

Para casi cualquier proyecto que construyas en los próximos años, **no necesitarás particionar**: PostgreSQL bien indexado aguanta
muchísimo. Conviene conocer el concepto.

---

## 8. Cómo abordar una pregunta de diseño en una entrevista

1. **Aclarar requisitos** (5 minutos): ¿qué funcionalidades? ¿cuántos usuarios? ¿más lecturas o escrituras? ¿qué latencia es aceptable?
   ¿qué pasa si se pierde un dato?
2. **Estimar** la escala con números aproximados.
3. **Diseño básico**: cliente → API → base de datos. Define las entidades y los endpoints principales.
4. **Profundizar** en el cuello de botella: caché para lecturas frecuentes, cola para tareas lentas, réplicas, límites.
5. **Fallos**: ¿qué pasa si cae la base, el proveedor externo o un servidor?
6. **Compromisos**: explica qué ganas y qué pierdes con cada decisión ("la caché con TTL de 60 s significa que un cambio de precio puede
   tardar un minuto en verse").

Ejemplo resumido: **el backend de un chatbot RAG para muchos negocios**. API sin estado detrás de un balanceador; PostgreSQL con pgvector
y un `negocio_id` en cada tabla (filtrado en cada consulta); la indexación de documentos en una cola con workers; streaming de las
respuestas; límite de peticiones por negocio con cubo de fichas en Redis; reintentos con espera exponencial ante la API del modelo; caché
de respuestas a preguntas frecuentes; métricas de costo por negocio. Empieza simple y explica qué añadirías cuando crezca.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Estimar | Peticiones/día ÷ 86 400; pico = 3-5 × media |
| Escalar | Horizontal con servidores sin estado; estado en la base, Redis o cookies firmadas |
| Réplicas | Escalan lecturas; cuidado con el retraso de replicación |
| Caché | Cache-aside; invalidación con TTL o al escribir; LRU para limitar memoria |
| Tiempo en pruebas | Inyectar el reloj y la función de dormir |
| Colas | Tareas lentas o falibles fuera de la petición; al menos una vez → idempotencia |
| Reintentos | Espera exponencial con máximo y jitter; solo errores transitorios |
| Rate limiting | Cubo de fichas: capacidad, recarga por tiempo transcurrido, 429 |
| Particionado | Hash estable mod n; no `hash()` de Python |
| Entrevista | Requisitos, estimación, diseño básico, cuellos de botella, fallos, compromisos |

## Autoevaluación final

1. 1 000 000 de usuarios diarios hacen 20 peticiones cada uno. ¿Cuántas peticiones por segundo de media?
2. Pasas a tres servidores y los usuarios pierden la sesión al azar. ¿Por qué?
3. Un usuario edita su nombre, recarga y ve el nombre antiguo. Las lecturas van a réplicas. ¿Qué pasa?
4. Caché LRU de capacidad 2: guardar A, guardar B, obtener A, guardar C. ¿Qué clave se expulsa?
5. ¿Por qué se inyecta el reloj en una caché con TTL?
6. ¿Por qué el correo de bienvenida no debe enviarse dentro de la petición de registro?
7. Con base 0,5 s y máximo 4 s, ¿cuánto se espera tras los fallos 0, 1, 2, 3 y 4?
8. Cubo de fichas: capacidad 10, recarga 2/s, vacío en t = 0. ¿Cuántas fichas hay en t = 3 s? ¿Y en t = 30 s?
9. ¿Por qué no se usa `hash()` de Python para elegir la partición?

**Respuestas:** 1) 20 000 000 / 86 400 ≈ 231 por segundo. 2) Las sesiones estaban en la memoria de cada servidor; hay que guardarlas en
un almacén compartido o usar cookies firmadas. 3) Retraso de replicación: leer de la principal tras una escritura del propio usuario.
4) B (A se usó más recientemente al leerla). 5) Para probar la caducidad sin esperar de verdad y con resultados deterministas. 6) Porque
el usuario esperaría y un fallo del proveedor parecería un fallo del registro; va a una cola con reintentos. 7) 0,5; 1; 2; 4; 4 segundos.
8) 6 fichas; 10 (la capacidad máxima). 9) Porque cambia entre ejecuciones para los textos; la misma clave podría ir a otra partición.
