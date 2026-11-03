# Arquitectura distribuida: eventos, sagas, CQRS y outbox

En un monolito con una sola base de datos, una transacción garantiza que todo ocurre o nada ocurre. Cuando el sistema se reparte entre
varios servicios, colas y bases de datos (o simplemente cuando tu aplicación tiene que avisar a un sistema externo), esa garantía
desaparece: **la red falla, los mensajes se duplican, los servicios se reinician a mitad de una operación**.

Este capítulo explica los patrones que se usan para construir sistemas fiables en ese mundo: comunicación síncrona y asíncrona,
arquitectura orientada a eventos, consumidores idempotentes, el patrón outbox, sagas y CQRS. Son temas habituales en entrevistas de
backend de nivel medio, y algunos (la idempotencia y el outbox) los necesitarás mucho antes de lo que crees, en cuanto integres pagos,
webhooks o colas.

Una advertencia antes de empezar: **estos patrones resuelven problemas de sistemas grandes y añaden complejidad**. Un MVP con 50 usuarios y
un desarrollador no necesita Kafka, sagas ni CQRS: un monolito modular con una cola para tareas en segundo plano basta. Se adoptan cuando
un problema real los justifica.

---

## 1. Síncrono y asíncrono

| | Síncrono (petición-respuesta) | Asíncrono (mensajes/eventos) |
|---|---|---|
| Cómo | El servicio A llama a B por HTTP y **espera** la respuesta | A publica un mensaje en una cola o bus y **sigue**; B lo procesa cuando puede |
| Acoplamiento | Alto: si B está caído o lento, A también falla o se ralentiza | Bajo: A no depende de que B esté disponible en ese momento |
| Respuesta inmediata | Sí | No: el resultado llega después |
| Complejidad | Baja | Mayor: duplicados, orden, consistencia eventual |
| Ejemplo | Consultar el precio de un producto | Enviar el correo de confirmación de un pedido |

Una cadena de llamadas síncronas es tan fiable como su eslabón más débil: si A llama a B, que llama a C, y cada uno está disponible el 99 %
del tiempo, la cadena lo está el 0,99³ ≈ 97 %. La comunicación asíncrona rompe esa dependencia.

---

## 2. Arquitectura orientada a eventos

Un **evento** es un hecho que **ya ocurrió**, nombrado en pasado: `PedidoCreado`, `PagoConfirmado`, `UsuarioRegistrado`. El servicio que
lo produce lo **publica**, sin saber quién lo escuchará; los servicios interesados se **suscriben** y reaccionan.

```
Servicio de pedidos ──publica──► PedidoCreado ──► Servicio de correo   (envía la confirmación)
                                              ├──► Servicio de stock    (reserva las unidades)
                                              └──► Analítica            (registra la venta)
```

Ventaja: añadir un nuevo consumidor (por ejemplo, un programa de puntos) **no exige tocar** el servicio de pedidos. Inconvenientes: el
flujo completo ya no se ve en un solo lugar del código, y depurar requiere buena observabilidad (identificadores de correlación).

Un evento bien diseñado lleva un **identificador único**, el tipo, la fecha y los datos necesarios:

```json
{"id": "evt_7f3a", "tipo": "PedidoCreado", "ocurrido_en": "2026-11-02T14:03:11Z",
 "datos": {"pedido_id": 1001, "cliente_id": 42, "total": 59.90}}
```

Herramientas: colas como RabbitMQ o SQS, *streams* como Kafka o Redis Streams.

---

## 3. Entrega "al menos una vez" y consumidores idempotentes

Los sistemas de mensajería casi nunca garantizan "exactamente una vez". Lo normal es **al menos una vez**: el consumidor procesa el
mensaje y luego lo **confirma**; si se cae **entre** procesar y confirmar, la cola entrega el mensaje otra vez. Resultado: **mensajes
duplicados**. Lo mismo pasa con los webhooks de las pasarelas de pago, que reenvían el aviso si tu servidor no respondió a tiempo.

Si el consumidor que procesa `PagoConfirmado` no está preparado, un duplicado puede **enviar dos productos o acreditar dos veces un saldo**.

La solución es que el consumidor sea **idempotente**: procesar el mismo mensaje dos veces tiene el mismo efecto que procesarlo una vez.

### Cómo se consigue

- **Registrar los ids procesados**: antes de procesar, mirar si el id del evento ya se procesó; si es así, ignorarlo. En producción, ese
  registro vive en la base de datos (una tabla con el id como clave única), idealmente en la **misma transacción** que el efecto.
- **Operaciones naturalmente idempotentes**: "poner el estado del pedido en *pagado*" es idempotente; "sumar 10 al saldo" no lo es.

### El detalle crucial: cuándo marcar como procesado

¿Qué pasa si el procesamiento **falla** a mitad (una excepción)? Si ya habías marcado el id como procesado **antes** de procesar, el
reintento lo ignorará y el evento **se perderá para siempre**. El id solo debe quedar registrado **cuando el procesamiento terminó con
éxito**; si falla, el error se propaga (para que la cola reintente) y el id queda libre. En Python, eso significa marcar después de la
llamada que puede fallar, no antes; y recordar que un `set` es la estructura natural para "¿ya vi este id?" en O(1).

---

## 4. El problema de la doble escritura y el patrón outbox

Guardas un pedido en la base y luego publicas `PedidoCreado` en la cola:

```python
guardar_pedido(pedido)          # 1) base de datos
publicar("PedidoCreado", ...)   # 2) cola
```

Si el servidor se reinicia **justo entre** los dos pasos, el pedido existe pero el evento **nunca se publica**: el cliente no recibe la
confirmación y el stock no se reserva. Si inviertes el orden, puedes publicar el evento de un pedido que luego no se guardó. Son **dos
sistemas distintos** y no hay una transacción que los abarque a los dos. Es el problema de la **doble escritura**.

### La solución: outbox

1. En la **misma transacción** en que guardas el pedido, insertas el evento en una tabla de la misma base, la **outbox** (bandeja de
   salida), marcado como **no publicado**. Ahora las dos escrituras son atómicas: o se guardan ambas o ninguna.
2. Un proceso aparte (el **publicador**) lee periódicamente las entradas no publicadas, las envía a la cola y las marca como publicadas.

```sql
BEGIN;
INSERT INTO pedidos (...) VALUES (...);
INSERT INTO outbox (evento, publicado) VALUES ('{"tipo": "PedidoCreado", ...}', false);
COMMIT;
```

### Cómo se comporta el publicador

- Recorre las entradas pendientes **en orden** (para que los eventos salgan en el orden en que ocurrieron).
- Marca cada entrada como publicada **solo después** de publicarla con éxito.
- Si una publicación **falla**, se **detiene**: esa entrada y las siguientes quedan pendientes para el próximo intento. Si siguiera con
  las siguientes, se perdería el orden.
- Si el publicador se cae después de publicar pero antes de marcar, el evento se publicará **otra vez** en el siguiente intento: de nuevo,
  entrega al menos una vez. Por eso los consumidores deben ser idempotentes. Los dos patrones van juntos.

---

## 5. Sagas: transacciones que abarcan varios servicios

Un pedido requiere: reservar el stock (servicio de inventario), cobrar (servicio de pagos) y programar el envío (servicio de logística).
Cada servicio tiene su base de datos; no hay una transacción común. ¿Qué pasa si el cobro falla después de haber reservado el stock?

Una **saga** es una secuencia de pasos locales donde cada paso tiene una **acción de compensación** que deshace su efecto:

| Paso | Acción | Compensación |
|---|---|---|
| 1 | Reservar stock | Liberar el stock |
| 2 | Cobrar | Reembolsar |
| 3 | Programar el envío | Cancelar el envío |

Si un paso falla, se ejecutan las compensaciones de los pasos **ya completados**, en **orden inverso**:

```
reservar stock ✔ → cobrar ✔ → programar envío ✘
                                    │
          reembolsar ◄──────────────┘   (compensación del paso 2)
          liberar stock                 (compensación del paso 1)
```

Detalles importantes:

- Se compensan **solo los pasos que terminaron**; el paso que falló no hizo nada que deshacer (o se diseña para que así sea).
- **Orden inverso**: se deshace primero lo último que se hizo, como al desapilar una pila. Guardar las compensaciones de los pasos
  completados en una lista y recorrerla al revés (`reversed(...)`) es la forma natural de hacerlo.
- Tras compensar, el error original **se sigue comunicando** (se vuelve a lanzar), para que quien llamó sepa que la operación falló.
- Las compensaciones también pueden fallar: deben ser idempotentes y reintentables, y se registran para revisión manual si no hay forma.
- Una compensación no siempre "borra": un correo enviado no se puede desenviar; la compensación es enviar otro que lo corrija.

Hay dos estilos: **orquestación** (un coordinador central llama a cada servicio en orden) y **coreografía** (cada servicio reacciona a los
eventos del anterior). La orquestación es más fácil de seguir y depurar.

---

## 6. CQRS

**CQRS** (*Command Query Responsibility Segregation*) significa **separar el modelo que escribe del modelo que lee**:

- El lado de **escritura** (comandos: `CrearPedido`, `CancelarPedido`) aplica las reglas de negocio sobre un modelo normalizado.
- El lado de **lectura** (consultas) usa **vistas optimizadas** para cada pantalla: tablas desnormalizadas, un índice de búsqueda o una
  caché, actualizadas a partir de los eventos del lado de escritura.

```
comandos ──► modelo de escritura (reglas, base normalizada) ──eventos──► proyecciones ──► vistas de lectura ◄── consultas
```

Cuándo tiene sentido: cuando las lecturas y las escrituras tienen necesidades muy distintas (un panel que combina datos de muchas tablas y
se consulta miles de veces por minuto). El costo: las vistas de lectura se actualizan con un pequeño retraso (**consistencia eventual**)
y hay más piezas que mantener. Una versión ligera que ya conoces: las tablas agregadas o vistas materializadas para un dashboard
(capítulo de modelado).

**Event sourcing** va más lejos: en lugar de guardar el estado actual, se guarda la **secuencia de eventos** y el estado se reconstruye a
partir de ellos. Da un historial completo y auditable, pero es complejo; se usa en dominios concretos (contabilidad, sistemas financieros).

---

## 7. Consistencia eventual

En un sistema distribuido, distintas partes pueden ver **temporalmente** datos distintos: el pedido ya está creado, pero el panel aún no
lo muestra; el pago se confirmó, pero el correo llega 10 segundos después. Si el sistema deja de recibir cambios, todas las partes acaban
**convergiendo** al mismo estado: eso es la **consistencia eventual**.

Lo importante es **diseñar para ella**:

- En la interfaz: estados intermedios honestos ("pago en proceso"), en lugar de prometer algo que aún no ha ocurrido.
- En el negocio: decidir qué **debe** ser inmediato y consistente (no vender stock que no existe, no cobrar dos veces) y qué puede esperar
  unos segundos (el correo, la analítica).

---

## 8. Cuándo usar cada cosa

| Situación | Patrón |
|---|---|
| Una tarea lenta que no necesita respuesta inmediata | Cola + worker (capítulo de diseño de sistemas) |
| Recibes webhooks o mensajes de una cola | **Consumidor idempotente** (siempre) |
| Guardas datos y debes avisar a otro sistema de forma fiable | **Outbox** |
| Una operación de negocio abarca varios servicios con sus propias bases | **Saga** con compensaciones |
| Lecturas muy distintas de las escrituras y con mucha carga | CQRS (o, más simple, vistas materializadas) |
| Necesitas el historial completo de cambios como fuente de verdad | Event sourcing |
| MVP, un equipo pequeño | **Monolito modular** + una cola; nada de lo demás hasta que haga falta |

La idempotencia es la que más pronto vas a necesitar: en cuanto integres una pasarela de pagos o cualquier webhook, recibirás duplicados.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Síncrono vs asíncrono | Esperar la respuesta vs publicar y seguir; acoplamiento alto vs bajo |
| Eventos | Hechos en pasado, con id único; el productor no conoce a los consumidores |
| Al menos una vez | Los mensajes se duplican; los consumidores deben ser idempotentes |
| Consumidor idempotente | Registrar los ids procesados **solo tras el éxito** |
| Doble escritura | Base y cola no comparten transacción |
| Outbox | Evento en una tabla en la misma transacción; publicador en orden, se detiene al primer fallo |
| Saga | Pasos con compensación; si falla uno, compensar los completados en orden inverso y relanzar el error |
| CQRS | Separar el modelo de escritura de las vistas de lectura |
| Consistencia eventual | Las partes convergen; diseñar la interfaz y el negocio para ello |

## Autoevaluación final

1. ¿Qué ventaja tiene publicar un evento frente a llamar por HTTP a cada servicio interesado?
2. ¿Por qué una cola con entrega "al menos una vez" produce duplicados?
3. Un consumidor marca el id del evento como procesado y luego procesa; el procesamiento lanza una excepción. ¿Qué problema hay?
4. ¿Por qué "poner el estado en pagado" es idempotente y "sumar 10 al saldo" no?
5. Explica el problema de la doble escritura con un ejemplo.
6. En el outbox, ¿por qué el publicador se detiene al primer fallo en lugar de seguir con las siguientes entradas?
7. Una saga tiene los pasos A, B, C y D; C falla. ¿Qué compensaciones se ejecutan y en qué orden?
8. ¿Qué describe mejor CQRS?
9. Tienes un MVP con 50 usuarios. ¿Implementas sagas y CQRS?

**Respuestas:** 1) Menor acoplamiento: el productor no depende de que los consumidores estén disponibles y se pueden añadir consumidores
sin tocarlo. 2) Porque si el consumidor se cae después de procesar y antes de confirmar, la cola vuelve a entregar el mensaje. 3) El
reintento ignorará el evento porque ya está marcado, y se perderá; hay que marcarlo solo tras el éxito. 4) Repetir "poner en pagado" deja
el mismo estado; repetir "sumar 10" suma dos veces. 5) Se guarda un pedido en la base y el servidor se reinicia antes de publicar el
evento en la cola: el pedido existe pero nadie se entera. 6) Para conservar el orden de los eventos; los pendientes se publicarán en el
siguiente intento. 7) Las de B y A, en ese orden (inverso); D nunca se ejecutó y C falló. 8) Separar el modelo que escribe (con las reglas)
del modelo que lee (vistas optimizadas). 9) No: un monolito modular con una cola basta; se adoptan cuando un problema real los justifica.
