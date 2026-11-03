# Arquitectura de software

Al principio, todo cabe en un archivo: la ruta de FastAPI valida la petición, consulta la base, aplica las reglas, llama al modelo de IA y
devuelve la respuesta. Funciona. Pero cuando el proyecto crece, ese archivo se convierte en algo que nadie se atreve a tocar: cada cambio
rompe otra cosa, no se puede probar sin levantar la base de datos y cambiar de proveedor de correo exige revisar veinte funciones.

La **arquitectura** es el conjunto de decisiones sobre **cómo se organiza el código** para que siga siendo fácil de cambiar, de probar y
de entender. Este capítulo te da las ideas que más rinden en proyectos del tamaño de los tuyos (el MVP, la demo, los proyectos de
clientes): separación en capas, inyección de dependencias, el patrón repositorio, cómo elegir entre un monolito y microservicios, la
configuración y cómo documentar decisiones.

---

## 1. El problema: todo mezclado

```python
@app.post("/reservas")
def crear_reserva(datos: dict):
    conn = psycopg.connect("postgresql://admin:clave123@db/reservas")      # configuración y secreto en el código
    fila = conn.execute("SELECT ... FROM reservas WHERE sala = %s ...", (datos["sala"],)).fetchone()
    if fila:                                                               # regla de negocio mezclada con SQL
        return {"error": "ocupada"}
    conn.execute("INSERT INTO reservas ...", (...))
    conn.commit()
    smtplib.SMTP("smtp.gmail.com").sendmail(...)                           # efecto externo dentro de la ruta
    return {"ok": True}
```

Problemas:

- **No se puede probar** la regla "no se puede reservar una sala ocupada" sin una base de datos y un servidor de correo reales.
- **La regla está atrapada** en una ruta HTTP: si mañana las reservas también llegan por WhatsApp o por un agente de IA, hay que
  duplicarla.
- **Cambiar de proveedor** (de Gmail a otro servicio, de PostgreSQL a otra base) obliga a tocar la lógica de negocio.
- **Secretos en el código** (capítulo de seguridad).

## 2. Separación en capas

La solución clásica es dividir el código en **capas** con responsabilidades distintas:

```
┌─────────────────────────────────────────┐
│  Rutas / API (HTTP)                     │  recibir la petición, validar el formato, devolver la respuesta
├─────────────────────────────────────────┤
│  Servicios (lógica de negocio)          │  las reglas: qué se puede hacer y qué pasa cuando se hace
├─────────────────────────────────────────┤
│  Repositorios / adaptadores             │  hablar con la base de datos, el correo, el LLM, los pagos
└─────────────────────────────────────────┘
```

| Capa | Sabe de | No sabe de |
|---|---|---|
| **Rutas** | HTTP, códigos de estado, formatos de entrada y salida | Reglas de negocio, SQL |
| **Servicios** | Las reglas del negocio | HTTP, SQL, qué proveedor de correo se usa |
| **Repositorios / adaptadores** | SQL, APIs externas | Las reglas de negocio |

La regla de oro: las dependencias apuntan **hacia dentro**. Las rutas usan servicios; los servicios usan repositorios **a través de una
interfaz**; la lógica de negocio no importa nada de FastAPI ni de SQL.

### ¿Dónde va cada regla?

La regla "un pedido enviado no se puede cancelar" va en la **capa de servicios**:

- **No** en el componente de React del botón: ocultar el botón no impide que alguien llame a la API directamente.
- **No** en la ruta, mezclada con el parseo de la petición: no se podría reutilizar desde otros canales.
- **No solo** en un *trigger* de la base de datos: la lógica quedaría escondida y difícil de probar. (Las **restricciones** de la base, como
  un `CHECK`, sí son una buena defensa **adicional**.)

## 3. Inyección de dependencias

Un servicio necesita guardar datos y enviar notificaciones. Si **crea** esas dependencias dentro (`conn = psycopg.connect(...)`), queda
atado a ellas. Con **inyección de dependencias**, el servicio las **recibe** desde fuera:

```python
class ServicioReservas:
    def __init__(self, repositorio, notificador):
        self.repositorio = repositorio
        self.notificador = notificador

    def reservar(self, usuario_id, sala, hora):
        if not 8 <= hora <= 20:
            raise ValueError("Las salas solo se reservan de 8 a 20 h")
        if self.repositorio.existe(sala=sala, hora=hora):
            raise ValueError("La sala ya está reservada a esa hora")
        reserva_id = self.repositorio.guardar({"usuario_id": usuario_id, "sala": sala, "hora": hora})
        self.notificador.enviar(usuario_id, f"Reserva {reserva_id} confirmada: sala {sala} a las {hora} h")
        return reserva_id
```

El servicio no sabe si el repositorio es PostgreSQL, un archivo o una lista en memoria; solo sabe que tiene los métodos `existe` y
`guardar`. Tampoco sabe si el notificador envía un correo, un WhatsApp o nada.

Fíjate también en el **orden** dentro del método: primero las validaciones (que pueden lanzar errores), después el guardado, después la
notificación (que usa el id que devolvió el guardado), y al final se devuelve el resultado. Si validaras después de guardar, quedarían
datos inválidos en la base.

### La gran ventaja: probar sin infraestructura

En las pruebas, se inyectan **dobles falsos** que guardan en memoria y registran lo que reciben:

```python
class RepoFalso:
    def __init__(self):
        self.guardados = []
    def existe(self, **filtros):
        return any(all(r[k] == v for k, v in filtros.items()) for r in self.guardados)
    def guardar(self, datos):
        self.guardados.append(datos)
        return len(self.guardados)

class NotificadorFalso:
    def __init__(self):
        self.enviados = []
    def enviar(self, destinatario, mensaje):
        self.enviados.append((destinatario, mensaje))

def test_reserva_notifica_al_usuario():
    repo, notif = RepoFalso(), NotificadorFalso()
    servicio = ServicioReservas(repo, notif)

    rid = servicio.reservar(usuario_id=7, sala="A", hora=10)

    assert rid == 1
    assert notif.enviados == [(7, "Reserva 1 confirmada: sala A a las 10 h")]

def test_no_se_puede_reservar_dos_veces():
    servicio = ServicioReservas(RepoFalso(), NotificadorFalso())
    servicio.reservar(7, "A", 10)
    with pytest.raises(ValueError):
        servicio.reservar(8, "A", 10)
```

Las pruebas se ejecutan en milisegundos, sin base de datos ni correo, y prueban **exactamente** la regla de negocio.

### En FastAPI

FastAPI tiene un sistema de inyección con `Depends`:

```python
def obtener_servicio() -> ServicioReservas:
    return ServicioReservas(RepositorioPostgres(engine), NotificadorEmail(config.smtp_url))

@app.post("/reservas", status_code=201)
def crear_reserva(datos: ReservaIn, servicio: ServicioReservas = Depends(obtener_servicio),
                  usuario=Depends(usuario_actual)):
    try:
        rid = servicio.reservar(usuario.id, datos.sala, datos.hora)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {"id": rid}
```

La ruta queda fina: traduce HTTP a una llamada al servicio y el resultado (o el error) a HTTP. En las pruebas de la API puedes sustituir
la dependencia con `app.dependency_overrides`.

### Interfaces explícitas con Protocol

Para dejar claro qué métodos debe tener una dependencia, Python ofrece `typing.Protocol`:

```python
from typing import Protocol

class Notificador(Protocol):
    def enviar(self, destinatario: int, mensaje: str) -> None: ...
```

Cualquier clase con un método `enviar` compatible cumple el protocolo, sin heredar de nada. El editor y herramientas como `mypy` te avisan
si falta algo.

## 4. El patrón repositorio

Un **repositorio** encapsula el acceso a los datos de una entidad detrás de métodos con significado de negocio (`guardar`, `obtener`,
`listar`, `existe`), de modo que el resto del código no escribe SQL.

```python
class RepositorioReservasPostgres:
    def __init__(self, engine):
        self.engine = engine

    def guardar(self, datos):
        with self.engine.begin() as conn:
            return conn.execute(
                text("INSERT INTO reservas (usuario_id, sala, hora) VALUES (:usuario_id, :sala, :hora) RETURNING id"),
                datos,
            ).scalar_one()
```

Y para pruebas o prototipos, un repositorio **en memoria** con los mismos métodos. Detalles de diseño que hacen que un repositorio en
memoria se comporte como uno real:

- **El repositorio asigna los ids**, normalmente incrementales, igual que una base de datos con `SERIAL`.
- **Guarda y devuelve copias**, no el mismo objeto. Si devolvieras el diccionario interno, el código que lo recibe podría modificarlo y
  estaría cambiando los datos "guardados" sin pasar por el repositorio. Una base de datos real nunca permite eso.

```python
original = {"sala": "A"}
alias = original           # el MISMO objeto: cambiar alias cambia original
copia = dict(original)     # un objeto NUEVO con el mismo contenido (copia superficial)
alias["sala"] = "B"
original                   # {'sala': 'B'}
copia                      # {'sala': 'A'}
```

- **Filtrar con criterios flexibles**: un método `listar(**filtros)` que acepta cualquier combinación de campos (`listar(sala="A")`,
  `listar(sala="A", hora=10)`) y devuelve las entidades que cumplen **todos**. `all(...)` sobre `filtros.items()` expresa muy bien esa
  condición, como en el `RepoFalso` de arriba.

## 5. Monolito modular o microservicios

| | Monolito modular | Microservicios |
|---|---|---|
| Qué es | Una aplicación, un despliegue, dividida internamente en módulos por dominio | Varias aplicaciones independientes que se comunican por red |
| Complejidad | Baja | Alta: red, despliegues, observabilidad distribuida, datos repartidos |
| Equipo ideal | 1-20 personas | Muchos equipos que necesitan desplegar por separado |
| Transacciones | Normales (una base de datos) | Distribuidas, difíciles |
| Cambiar los límites | Fácil (mover código) | Difícil (cambiar APIs entre servicios) |

Para un desarrollador solo o una startup en fase de MVP, la respuesta es casi siempre un **monolito modular**: una aplicación con una
estructura por dominios, con límites claros entre módulos.

```
app/
  reservas/          ← un módulo por dominio
    rutas.py
    servicio.py
    repositorio.py
    modelos.py
  usuarios/
    ...
  pagos/
    ...
  config.py
  main.py
```

Cada módulo expone su servicio y los demás lo usan a través de él (no consultan sus tablas directamente). Si algún día un módulo necesita
escalar o desplegarse aparte, extraerlo como servicio es mucho más fácil si los límites ya estaban claros. Empezar con diez microservicios
y Kubernetes es resolver problemas que no tienes, a un costo enorme.

## 6. Configuración

Todo lo que **cambia entre entornos** (desarrollo, staging, producción) va fuera del código, en **variables de entorno**: la URL de la base
de datos, las claves de API, el nivel de log, los orígenes de CORS. En producción, los secretos van en el gestor de secretos de la
plataforma.

Con Pydantic se valida al arrancar:

```python
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    database_url: str
    anthropic_api_key: str
    log_level: str = "info"
    cors_origins: list[str] = []

config = Config()   # lee las variables de entorno; si falta una obligatoria, falla AL ARRANCAR
```

Fallar al arrancar con un mensaje claro ("falta DATABASE_URL") es mucho mejor que fallar en mitad de una petición de un cliente.

## 7. Documentar decisiones: ADR

Dentro de seis meses (o cuando llegue otro desarrollador) alguien preguntará: "¿por qué usamos pgvector y no una base vectorial aparte?".
Un **ADR** (*Architecture Decision Record*) es un documento corto que responde a eso:

```markdown
# ADR 003: pgvector para los embeddings

## Contexto
El asistente necesita búsqueda semántica sobre ~5 000 fragmentos. Ya usamos PostgreSQL.

## Decisión
Usar la extensión pgvector en la misma base de datos.

## Alternativas consideradas
Qdrant y Pinecone: más funciones, pero otro servicio que desplegar, pagar y mantener.

## Consecuencias
+ Una sola base, transacciones y copias de seguridad comunes, SQL conocido.
− Si pasamos de varios millones de vectores, habrá que revisar el rendimiento.
```

Se guardan en el repositorio (`docs/adr/`). Para tu portafolio, dos o tres ADR de tu demo demuestran algo que buscan mucho las empresas:
**criterio técnico explicado**.

## 8. Principios que guían las decisiones

- **KISS** (*keep it simple*): la solución más simple que resuelve el problema real.
- **YAGNI** (*you aren't gonna need it*): no construyas para necesidades hipotéticas.
- **Responsabilidad única**: cada módulo, clase o función tiene una razón para cambiar.
- **Bajo acoplamiento, alta cohesión**: lo que cambia junto, vive junto; lo que no tiene relación, no se conoce.
- **Hacer fácil probar**: si algo es difícil de probar, suele estar mal separado.

La arquitectura no es dibujar diagramas: es tomar decisiones que hagan **barato el cambio** que más probablemente vas a necesitar.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Capas | Rutas (HTTP) → servicios (reglas) → repositorios/adaptadores (infraestructura) |
| Reglas de negocio | En los servicios, independientes de HTTP y SQL; restricciones de la base como defensa extra |
| Inyección de dependencias | El servicio recibe sus dependencias; en pruebas, dobles falsos |
| Orden en un servicio | Validar → guardar → efectos (notificar) → devolver |
| Repositorio | Métodos con significado; asigna ids; guarda y devuelve copias; filtros flexibles |
| Monolito modular | La opción por defecto para equipos pequeños y MVP |
| Configuración | Variables de entorno validadas al arrancar; secretos en un gestor |
| ADR | Contexto, decisión, alternativas, consecuencias |

## Autoevaluación final

1. ¿Qué problemas tiene una ruta que valida, consulta SQL, aplica reglas y envía correos?
2. ¿Dónde debe vivir la regla "no se puede reservar fuera del horario" y por qué no en el frontend?
3. ¿Qué significa inyección de dependencias y qué ventaja da en las pruebas?
4. En un método de servicio que valida, guarda y notifica, ¿por qué se valida primero?
5. ¿Por qué un repositorio en memoria debe devolver copias y no los objetos internos?
6. Tras `b = a` con `a` un diccionario, modificas `b`. ¿Qué pasa con `a`? ¿Y si hubieras hecho `b = dict(a)`?
7. Eres el único desarrollador de un MVP. ¿Monolito modular o microservicios? ¿Por qué?
8. ¿Dónde pones la URL de la base de datos y por qué conviene validarla al arrancar?
9. ¿Qué secciones tiene un ADR?

**Respuestas:** 1) No se puede probar sin infraestructura, la regla no se puede reutilizar, cambiar de proveedor obliga a tocar la
lógica y suele haber secretos en el código. 2) En la capa de servicios; en el frontend no protege nada porque se puede llamar a la API
directamente. 3) Que el componente recibe sus dependencias desde fuera; en las pruebas se sustituyen por dobles falsos, rápidos y sin
infraestructura. 4) Para no guardar datos inválidos ni enviar notificaciones de operaciones que no deberían ocurrir. 5) Para que nadie
pueda modificar los datos guardados sin pasar por el repositorio, igual que con una base real. 6) `a` también cambia (son el mismo
objeto); con `dict(a)`, `a` no cambia. 7) Monolito modular: mucho menos complejo, y los límites claros permiten extraer servicios después
si hace falta. 8) En variables de entorno (gestor de secretos en producción); validarla al arrancar da un error claro en vez de fallar en
mitad de una petición. 9) Contexto, decisión, alternativas consideradas y consecuencias.
