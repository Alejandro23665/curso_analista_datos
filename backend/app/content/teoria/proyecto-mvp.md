# Proyecto: tu MVP en producción

Este capítulo es diferente: no introduce conceptos nuevos, sino que **los junta todos** en un proyecto real. Vas a construir y lanzar un
producto pequeño, con usuarios reales, aplicando lo que viste en la ruta: FastAPI, PostgreSQL, autenticación segura, arquitectura en capas,
pruebas, CI, despliegue, observabilidad, métricas y la mentalidad de MVP.

Es probablemente **la pieza más valiosa de tu portafolio**. Un reclutador ve cientos de proyectos de tutoriales; muy pocos candidatos
junior pueden decir "esto está en producción, lo usan 12 personas y esta es la mejora que hice a partir de sus comentarios". Y si el
problema es bueno, puede ser el inicio de tu startup.

La guía está organizada en fases, con lo que debes entregar en cada una. Cuenta con **4-6 semanas** a tiempo parcial.

---

## Fase 0: elegir el problema y recortar el alcance (días 1-3)

### Elegir

Aplica lo del capítulo de startup. Las mejores fuentes, por orden:

1. **Un problema que viste en tus clientes freelance** o en tu entorno (un negocio de un familiar, una comunidad a la que perteneces).
2. Una tarea manual y repetitiva que alguien concreto hace cada semana.
3. Un problema propio, si eres un usuario representativo.

Ejemplos de tamaño adecuado:

- Recordatorios automáticos de citas por correo o WhatsApp para un consultorio pequeño.
- Un asistente que responde las preguntas frecuentes de un negocio con sus documentos (RAG), con un panel de las preguntas sin respuesta.
- Un registro de pedidos por encargo para una pastelería, con avisos cuando un pedido está listo.
- Un extractor de datos de facturas en PDF a una hoja de cálculo para un contador.

Lo importante: que exista **al menos una persona concreta** que lo vaya a usar. Habla con ella antes de empezar (las preguntas del
capítulo de startup).

### Recortar

Escribe la **funcionalidad central** en una frase: *"El consultorio carga sus citas y los pacientes reciben un recordatorio el día
antes"*. Todo lo que no sea imprescindible para esa frase va a una lista de "después".

| Ahora (MVP) | Después (si los usuarios lo piden) |
|---|---|
| Registro e inicio de sesión | Inicio de sesión con Google |
| Crear, ver y cancelar citas | Calendario visual con arrastrar y soltar |
| Recordatorio por correo el día antes | WhatsApp, SMS |
| Un tipo de usuario (el consultorio) | Roles, varios profesionales |
| — | Pagos, modo oscuro, app móvil, estadísticas avanzadas |

**La trampa más común**: llevar tres semanas sin lanzar porque "falta" añadir pagos, modo oscuro, notificaciones y la app móvil. Lanza
**la funcionalidad central a unos pocos usuarios** y decide lo demás según lo que digan.

### Entregable

Un **ADR** (capítulo de arquitectura) con: el problema, el usuario, la funcionalidad central, lo que queda fuera y las decisiones técnicas
principales (stack, dónde se despliega, por qué).

---

## Fase 1: el esqueleto desplegado (semana 1)

Lo primero no es la funcionalidad: es un **esqueleto que funciona de punta a punta en producción**. Desplegar al final es la receta para
descubrir problemas de configuración el día del lanzamiento.

1. Repositorio en GitHub con la estructura en capas:

```
backend/
  app/
    main.py            # crea la app de FastAPI y registra las rutas
    config.py          # configuración desde variables de entorno (pydantic-settings)
    db.py              # motor y sesión de SQLAlchemy
    citas/             # un módulo por dominio
      rutas.py
      servicio.py
      repositorio.py
      modelos.py
    usuarios/
  migrations/          # Alembic
  tests/
frontend/              # React + Vite (o plantillas de servidor si prefieres algo más simple)
docker-compose.yml     # PostgreSQL local
.env.example           # nombres de las variables, sin valores secretos
AGENTS.md              # contexto para agentes de código
README.md
```

2. Un endpoint `/health` que comprueba la conexión con la base.
3. Una migración inicial con Alembic.
4. **Desplegado**: backend (Railway, Render, Fly.io o una función de Vercel), base de datos gestionada (Neon, Supabase) y frontend (Vercel,
   Netlify). La URL pública responde.
5. **CI** con GitHub Actions: linter y pruebas en cada push.

Entregable: una URL pública que devuelve `{"status": "ok"}` y una CI en verde.

---

## Fase 2: datos y autenticación (semana 2)

### Modelo de datos

Diseña las tablas normalizadas (capítulo de modelado) con sus restricciones (capítulo de bases de datos):

```sql
usuarios (id, email UNIQUE NOT NULL, hash_contrasena NOT NULL, creado_en)
citas    (id, usuario_id REFERENCES usuarios NOT NULL, paciente, email_paciente,
          fecha_hora TIMESTAMPTZ NOT NULL, estado CHECK (estado IN ('activa','cancelada')),
          recordatorio_enviado BOOLEAN DEFAULT false, creado_en)
```

Índices en las columnas por las que filtrarás (`usuario_id`, `fecha_hora`).

### Autenticación

Aplica el capítulo de seguridad:

- Contraseñas con un hash lento y con sal (Argon2 o bcrypt mediante una librería), **nunca** en texto plano.
- Sesión con una cookie `HttpOnly; Secure; SameSite=Lax`, o un proveedor de autenticación si prefieres no implementarla.
- Límite de intentos en el inicio de sesión.

### Autorización

**Cada endpoint comprueba que el recurso pertenece al usuario de la sesión.** Escribe la regla como una función pura y pruébala:
un usuario no puede ver, editar ni cancelar las citas de otro (si lo intenta, `404`).

Entregable: registro, inicio de sesión y CRUD de la entidad principal, con pruebas de autorización.

---

## Fase 3: la funcionalidad central (semanas 3-4)

### Lógica en servicios, con pruebas

Las reglas de negocio van en la capa de servicios, con las dependencias inyectadas (capítulo de arquitectura). Por ejemplo:

- No se puede crear una cita en el pasado.
- No se puede cancelar una cita que ya ocurrió.
- El recordatorio se envía una sola vez por cita.

Cada regla tiene sus pruebas unitarias, incluidos los casos borde (justo a la hora límite, fechas con zona horaria, cita cancelada).

### Tareas en segundo plano

Enviar los recordatorios no debe ocurrir dentro de una petición HTTP. Opciones, de más simple a más compleja:

- Un **cron** de la plataforma (Railway, Render y GitHub Actions permiten tareas programadas) que llama cada hora a un script.
- Una cola con un *worker* (lo verás en *Diseño de sistemas*), si el volumen lo justifica.

Hazlo **idempotente**: si el script se ejecuta dos veces, no debe enviar dos recordatorios (por eso la columna `recordatorio_enviado`, que
se marca en la misma operación). Y con **reintentos** si el proveedor de correo falla.

### Si tu MVP usa IA

Aplica la sección de IA de la ruta: la clave solo en el backend, límites de longitud y de peticiones, streaming si la respuesta es larga,
manejo de errores del proveedor, un conjunto de evaluación de 20-30 casos y control del costo por usuario.

Entregable: la funcionalidad central funcionando en producción, con pruebas de la lógica principal ejecutándose en la CI.

---

## Fase 4: listo para usuarios reales (semana 4-5)

Antes de invitar a nadie, la lista de producción (capítulo de calidad):

- [ ] **Logs estructurados** sin datos sensibles.
- [ ] **Seguimiento de errores** (Sentry tiene un plan gratuito) con una alerta por correo.
- [ ] **Copias de seguridad** de la base, y probaste restaurar una.
- [ ] Sabes cómo hacer **rollback** del último despliegue.
- [ ] Revisión de **seguridad**: claves en variables de entorno, CORS con tu dominio, autorización en cada endpoint, consultas
      parametrizadas, sin HTML sin escapar.
- [ ] La **interfaz** tiene estados de carga, vacío y error, y funciona en el móvil.
- [ ] Un texto breve de **privacidad**: qué datos guardas y para qué.

### Métricas

Define y registra (capítulo de métricas y de startup):

- **Activación**: el momento en que el usuario experimenta el valor ("creó su primera cita y se envió el primer recordatorio").
- **Retención**: qué fracción sigue usándolo cada semana.
- Una o dos métricas propias del producto (recordatorios enviados, ausencias evitadas según el usuario).

Basta con una tabla de eventos (`eventos(usuario_id, tipo, creado_en)`) y unas consultas SQL, o una herramienta de analítica de producto
con plan gratuito.

---

## Fase 5: usuarios reales e iteración (semana 5-6)

1. **Consigue al menos 5 usuarios reales**: la persona con la que hablaste al principio, sus conocidos, clientes freelance, comunidades.
   No hace falta que paguen todavía (aunque si alguno paga, mejor).
2. **Acompaña el primer uso**: míralos usarlo (en persona o por videollamada) sin ayudar. Anota dónde dudan, dónde se equivocan y qué
   preguntan. Aprenderás más en una hora que en una semana de suposiciones.
3. **Pregunta** después de una o dos semanas: ¿qué es lo más útil? ¿qué falta? ¿qué sobra? ¿cómo te sentirías si dejara de existir?
4. **Haz una iteración** basada en lo que viste y en los datos: el cambio que más usuarios necesitaron. Documenta qué cambiaste y por qué.

---

## Fase 6: contarlo (la última semana)

Un proyecto que nadie ve no te consigue entrevistas ni clientes.

### README

```markdown
# Recordatorio de Citas
Recordatorios automáticos para consultorios pequeños. Reduce las citas perdidas.
**Demo:** https://... (usuario de prueba en la página de inicio)

![captura o GIF del flujo principal]

## El problema
Los consultorios pequeños pierden ~15 % de las citas por olvidos de los pacientes...

## Qué hace
...

## Arquitectura
[diagrama simple: React → FastAPI → PostgreSQL; cron → servicio de correo]

## Decisiones técnicas
- Monolito modular en capas (ADR 001)...
- Recordatorios idempotentes con un cron horario (ADR 002)...

## Resultados
- 7 usuarios reales, 140 recordatorios enviados en 3 semanas.
- Activación: 5 de 7. Retención en la semana 2: 4 de 7.
- Iteración: añadí la confirmación de asistencia por enlace porque 3 usuarios la pidieron.

## Cómo ejecutarlo en local
...

## Qué mejoraría
...
```

Lo que más impresiona de este README no es la tecnología: son la **demo funcionando**, los **usuarios reales**, las **decisiones
explicadas** y la **iteración basada en datos**.

### Publicación en LinkedIn

Un post breve contando el problema, qué construiste, qué aprendiste y un resultado, con una captura y el enlace. Es una de las mejores
formas de que te encuentren reclutadores y clientes, y practica para explicarlo en entrevistas.

---

## Problemas típicos y cómo salir de ellos

| Problema | Salida |
|---|---|
| "Todavía no está listo para enseñarlo" | Si la funcionalidad central funciona, lánzalo. La vergüenza es normal |
| El alcance crece cada semana | Vuelve al ADR; todo lo nuevo va a la lista de "después" |
| Te atascas con una tecnología nueva | Vuelve a lo que conoces; el MVP no es para aprender un framework |
| Nadie lo usa | Habla con los que lo probaron: ¿el problema era real? ¿el producto lo resuelve? Ajusta o cambia de problema |
| Un agente de código escribió una parte que no entiendes | Pídele que te la explique o reescríbela; en la entrevista te preguntarán por ella |
| Te desanimas | Es normal: cada fase completada es un avance real. Comparte lo que llevas, aunque no esté terminado |

---

## Resumen del capítulo

| Fase | Entregable |
|---|---|
| 0. Problema y alcance | Una funcionalidad central y un ADR |
| 1. Esqueleto | URL pública con `/health`, CI en verde |
| 2. Datos y autenticación | CRUD con autenticación segura y pruebas de autorización |
| 3. Funcionalidad central | Lógica en servicios con pruebas; tareas en segundo plano idempotentes |
| 4. Producción | Logs, errores, copias probadas, rollback, seguridad, métricas |
| 5. Usuarios | Al menos 5 usuarios reales y una iteración basada en sus comentarios |
| 6. Contarlo | README con demo, decisiones y resultados; post en LinkedIn |

## Autoevaluación final

1. ¿Por qué se despliega el esqueleto en la primera semana y no al final?
2. Escribe en una frase la funcionalidad central de un MVP para una pastelería que recibe pedidos por encargo.
3. ¿Qué comprobación debe hacer cada endpoint que devuelve o modifica un recurso?
4. ¿Por qué el envío de recordatorios debe ser idempotente?
5. ¿Qué cinco cosas revisas antes de invitar a usuarios reales?
6. Define la activación de tu MVP.
7. ¿Qué aprendes mirando a un usuario usar el producto sin ayudarle?
8. ¿Qué cuatro elementos hacen que el README de un MVP impresione?

**Respuestas:** 1) Para descubrir pronto los problemas de configuración y despliegue y tener siempre una versión pública. 2) Por ejemplo:
"La pastelería registra los pedidos por encargo y el cliente recibe un aviso cuando su pedido está listo". 3) Que el recurso pertenece
al usuario de la sesión (o que tiene permiso). 4) Para que, si la tarea se ejecuta dos veces o se reintenta, no se envíen recordatorios
duplicados. 5) Logs sin datos sensibles, seguimiento de errores, copias de seguridad probadas, rollback conocido y revisión de seguridad
(además de los estados de la interfaz y el móvil). 6) El momento en que el usuario experimenta el valor por primera vez, por ejemplo
"se envió el primer recordatorio de una cita que creó". 7) Dónde duda, dónde se equivoca y qué no entiende, sin las suposiciones propias.
8) La demo funcionando, los usuarios reales con resultados, las decisiones técnicas explicadas y la iteración basada en datos.
