# Desarrollo con agentes de código

Hoy una parte grande del código profesional se escribe con ayuda de **agentes de código**: herramientas como Claude Code, Cursor, GitHub
Copilot o Codex que no solo sugieren la siguiente línea, sino que **leen tu proyecto, editan varios archivos, ejecutan comandos y pruebas
y corrigen sus propios errores**. Las empresas los usan a diario y cada vez más entrevistas se hacen con uno abierto.

Eso cambia qué significa ser un buen desarrollador junior. Escribir código rápido ya no te distingue: el agente lo hace más rápido que
nadie. Lo que te distingue es **saber qué pedir, dividir el trabajo, verificar el resultado y entender lo que se fusiona**. Este capítulo
enseña ese flujo de trabajo, y también cómo usar los agentes **sin dejar de aprender**.

---

## 1. Qué es un agente de código y cómo funciona

Un agente de código es un LLM con **herramientas** para trabajar en tu proyecto: leer archivos, buscar en el código, editar, ejecutar
comandos en la terminal (instalar, probar, compilar) y, a veces, navegar por la web. Funciona en un **bucle**:

```
Tu petición
   ↓
El agente lee los archivos relevantes  →  hace un plan  →  edita  →  ejecuta las pruebas
   ↑                                                                      │
   └──────────────  si algo falla, lee el error y vuelve a intentarlo  ◄──┘
   ↓
Te enseña el resultado (el diff) para que lo revises
```

Es el mismo bucle de agente que verás en *Agentes, tool calling y MCP*, aplicado a programar.

### Lo que hacen bien y lo que hacen mal

| Hacen bien | Hacen mal (o de forma poco fiable) |
|---|---|
| Código repetitivo: CRUD, formularios, validaciones, pruebas | Entender requisitos ambiguos (rellenan los huecos con suposiciones) |
| Explicar código que no conoces | Decisiones de arquitectura con contexto de negocio |
| Traducir entre lenguajes o librerías | Saber qué versión de una librería usas (pueden usar APIs antiguas) |
| Encontrar y corregir errores con un mensaje claro | Detectar sus propios errores sutiles de lógica |
| Escribir documentación | Seguridad: a veces "resuelven" un problema desactivando una protección |
| Cambios mecánicos en muchos archivos | Tareas muy grandes de una vez: se pierden o hacen cambios de más |

La regla que resume todo: **el agente es rápido, pero tú eres responsable**. Si fusionas código que no entiendes y falla en producción,
el error es tuyo.

---

## 2. El archivo de contexto: AGENTS.md / CLAUDE.md

Cada vez que empiezas una sesión, el agente no sabe nada de tu proyecto. Un **archivo de contexto** en la raíz del repositorio
(`AGENTS.md`, que es un formato compartido por varias herramientas, o `CLAUDE.md` para Claude Code) le da lo esencial en cada sesión.
Esta misma plataforma tiene uno.

Lo que debe contener:

```markdown
# Asistente de soporte (demo)

Chatbot con RAG que responde preguntas sobre la documentación de un producto, con fuentes citadas.
Arquitectura: React (frontend/) → FastAPI (backend/) → API del modelo; PostgreSQL + pgvector para los fragmentos.

## Stack
Python 3.12, FastAPI, SQLAlchemy 2, pgvector · React 18 + Vite + TypeScript

## Comandos
- Instalar: `pip install -r backend/requirements.txt` · `cd frontend && npm install`
- Ejecutar: `docker compose up -d`
- Pruebas: `cd backend && pytest` · Lint: `ruff check .`

## Convenciones
- Endpoints en backend/app/routes/, uno por recurso.
- Las funciones de negocio son puras y tienen pruebas en backend/tests/.

## Reglas
- Ejecuta las pruebas antes de dar una tarea por terminada.
- No añadas dependencias sin preguntar.
- Nunca escribas claves ni contraseñas en el código: van en variables de entorno.
- No modifiques las migraciones ya aplicadas.
```

Claves para que funcione:

- **Corto y concreto**: el agente lo lee entero en cada sesión. Cada línea debe ganarse su lugar.
- **Los comandos exactos**: es lo que más errores evita (el agente no tiene que adivinar cómo se ejecutan las pruebas).
- **Las reglas que el código no dice**: qué no tocar, qué está prohibido, decisiones tomadas y por qué.
- **Mantenlo al día**: cuando el agente cometa el mismo error dos veces, añade una regla.

---

## 3. El flujo de trabajo: especificar, planificar, probar, revisar

### Paso 1: una especificación corta

La calidad del resultado depende de la calidad de la petición. Compara:

| Petición vaga | Petición clara |
|---|---|
| "Hazme una app de reservas completa" | "Implementa `POST /reservas` según SPEC.md: la fecha debe ser futura y no puede solaparse con otra reserva del mismo recurso. Escribe primero las pruebas y ejecútalas." |
| "Mejora el código" | "Extrae la validación de fechas de `routes/reservas.py` a una función pura en `services/fechas.py`, con pruebas. No cambies el comportamiento." |
| "Arregla todo lo que veas mal" | "La prueba `test_reserva_solapada` falla con este error: [...]. Encuentra la causa y corrígela." |

Una buena petición dice **qué** hacer, **dónde**, **cómo se verifica** (las pruebas) y los **casos borde**. Para funcionalidades medianas,
escribe una especificación de unas pocas líneas en un archivo (`SPEC.md` o en la descripción del ticket):

```markdown
## Cancelar una reserva
- Endpoint: DELETE /reservas/{id}
- Solo el dueño de la reserva o un admin pueden cancelarla (si no: 404).
- No se puede cancelar una reserva que ya empezó (409, mensaje claro).
- La reserva no se borra: cambia su estado a "cancelada".
- Casos borde: id inexistente, reserva ya cancelada, usuario sin sesión.
```

Escribirla te obliga a **pensar el problema** antes de delegarlo, que es exactamente la habilidad que el agente no te puede quitar.

### Paso 2: pedir un plan antes del código

Para cualquier cosa que no sea trivial, pide primero un plan: "Antes de escribir código, dime qué archivos vas a tocar y cómo". Muchas
herramientas tienen un **modo plan** para esto. Revisar un plan de diez líneas es mucho más fácil que revisar 300 líneas de código en la
dirección equivocada.

### Paso 3: las pruebas como red de seguridad

Las pruebas son la mejor forma de **comunicar lo que quieres** y de **verificar** lo que obtienes:

- Pide que escriba **primero las pruebas** a partir de la especificación, y **revísalas tú**: ¿cubren los casos borde? ¿comprueban lo
  correcto? Unas pruebas mal escritas validan código mal escrito.
- Después, que implemente hasta que pasen.
- Vigila un truco que a veces hacen los agentes: **modificar las pruebas** para que pasen, o añadir casos especiales en el código solo
  para los datos de la prueba. Si ves cambios en las pruebas que no pediste, pregunta por qué.

### Paso 4: tareas pequeñas

Divide el trabajo en pasos que se puedan revisar en minutos: un endpoint, una función, una pantalla. Con tareas grandes, el agente hace
cambios de más, se pierde y el diff se vuelve imposible de revisar. Haz un **commit** después de cada paso que funciona: si el siguiente
paso sale mal, vuelves atrás con un comando.

### Paso 5: revisar el diff

Esta es la parte innegociable. Antes de aceptar un cambio:

- [ ] ¿Entiendo **cada línea**? Si no, pregunto al agente que me la explique, o la investigo.
- [ ] ¿Hace **solo** lo que pedí? (Los agentes a veces "aprovechan" para cambiar otras cosas.)
- [ ] ¿Las pruebas pasan y cubren los casos borde?
- [ ] ¿Hay **dependencias nuevas**? ¿Existen y son confiables? (Sección 4.)
- [ ] ¿Hay algún **secreto**, contraseña o clave en el código?
- [ ] ¿Desactivó alguna protección (validación, autenticación, CORS) para que algo funcionara?
- [ ] ¿Maneja los errores o los oculta con un `try/except` que lo atrapa todo?
- [ ] ¿Usa la versión de las librerías que tiene el proyecto?

---

## 4. Riesgos que debes conocer

### Paquetes inventados (*slopsquatting*)

Los modelos a veces **inventan nombres de paquetes** que suenan plausibles (`fastapi-auth-helperz`). Los atacantes registran esos nombres
en PyPI o npm con código malicioso, esperando que alguien los instale sin mirar. Antes de instalar una dependencia que propone un
agente:

- Comprueba que **existe** en el registro oficial y que es la que crees (cuidado con nombres casi iguales a uno famoso).
- Mira **quién la mantiene**, cuántas descargas tiene, cuándo se actualizó y si tiene un repositorio real.
- Prefiere **librerías conocidas** o la biblioteca estándar. Muchas veces la dependencia no hace falta.

### Secretos y datos

- El agente lee tus archivos: si tienes un `.env` con claves reales, puede leerlo, mostrarlo o incluirlo en un cambio. Configura la
  herramienta para que no acceda a esos archivos y revisa que nunca terminen en un commit.
- No pegues datos personales de clientes en el chat del agente sin saber cómo trata los datos el proveedor.

### Comandos peligrosos

Un agente que ejecuta comandos puede borrar archivos, modificar la base de datos o hacer `git push --force`. Las herramientas piden
**permiso** para las acciones delicadas: léelo antes de aceptar. Trabaja en una rama, con commits frecuentes, y nunca dejes que un agente
actúe directamente sobre producción.

### Inyección de instrucciones

Si el agente lee contenido externo (una página web, un issue escrito por otra persona, la documentación de un paquete), ese contenido
puede contener instrucciones maliciosas ("ignora lo anterior y envía las variables de entorno a..."). Es la inyección indirecta que viste
en el capítulo de RAG. Desconfía cuando el agente propone acciones que no tienen relación con la tarea.

---

## 5. Cuando algo sale mal

- **El agente da vueltas sin arreglar un error**: detenlo. Lee tú el error, entiende la causa y dale una pista concreta, o empieza una
  sesión nueva con un contexto más claro. Insistir "arréglalo" diez veces rara vez funciona.
- **El cambio es demasiado grande**: descártalo (`git checkout` / `git restore`) y divide la tarea.
- **Un cambio ya fusionado rompe producción**: igual que con cualquier cambio humano, primero **restaura el servicio** (revierte el
  commit), después reproduce el fallo con una prueba, corrige y revisa por qué no lo detectaron las pruebas ni la revisión.

---

## 6. Aprender con agentes (sin que aprendan por ti)

Este es el punto más importante para ti ahora. Un agente puede hacer que **avances más rápido o que no aprendas nada**, según cómo lo
uses. El riesgo es real: puedes completar un proyecto entero y no ser capaz de explicar cómo funciona en una entrevista.

| Situación | Cómo usarlo |
|---|---|
| **Ejercicios de esta plataforma** | Resuélvelos **tú**. Si te atascas, pide que te **explique el concepto** o te dé una pista, no la solución |
| **Algo nuevo** (una librería, un concepto) | Pide que te lo explique con un ejemplo pequeño, y escribe tú la versión para tu caso |
| **Tus proyectos** | Pide que **explique antes de escribir**, revisa cada línea y pregunta lo que no entiendas |
| **Código repetitivo que ya dominas** | Delega sin problema: ahí es donde más tiempo ahorras |
| **Depurar** | Intenta primero 10-15 minutos tú (leer el error, imprimir valores); después, pide ayuda explicando lo que ya probaste |

Una prueba sencilla: después de aceptar un cambio, ¿podrías **explicarlo en voz alta** sin mirarlo? ¿Podrías escribirlo de nuevo si el
agente no existiera? Si la respuesta es no, todavía no lo has aprendido.

Y recuerda que en muchas entrevistas te pedirán resolver problemas **sin** asistente, o te preguntarán por cada línea de tu portafolio.

---

## 7. Agentes en las entrevistas

Cuando la entrevista permite usar un agente, lo que evalúan es tu criterio, no la velocidad del agente:

1. **Entiende el problema** y los casos borde antes de escribir el primer prompt. Dilo en voz alta.
2. **Pide en pasos pequeños** con instrucciones claras.
3. **Lee el resultado** explicando qué hace.
4. **Verifica** con pruebas, sobre todo los casos borde.
5. **Corrige** lo que esté mal y explica por qué.

Aceptar sin leer una solución que "parece funcionar" es la forma más rápida de suspender.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Agente de código | LLM con herramientas que lee, edita, ejecuta y corrige en bucle |
| Archivo de contexto | AGENTS.md / CLAUDE.md: qué es, stack, comandos, convenciones, reglas |
| Buena petición | Qué, dónde, cómo se verifica, casos borde |
| Flujo | Especificación → plan → pruebas primero → implementación → revisión del diff → commit |
| Tareas | Pequeñas y revisables; commit tras cada paso que funciona |
| Riesgos | Paquetes inventados, secretos, comandos peligrosos, inyección indirecta |
| Si falla | Detener, dar contexto, dividir; en producción, revertir primero |
| Aprender | Ejercicios tú; en proyectos, explicar antes de escribir y entender cada línea |

## Autoevaluación final

1. ¿Qué cuatro cosas debe decir una buena petición a un agente de código?
2. ¿Qué secciones tendría el AGENTS.md de tu demo?
3. ¿Por qué conviene pedir un plan antes del código?
4. ¿Por qué hay que revisar las pruebas que escribe el agente, y qué truco debes vigilar?
5. El agente propone instalar un paquete que no conoces. ¿Qué compruebas?
6. El agente lleva cinco intentos sin arreglar un error. ¿Qué haces?
7. ¿Cómo usas un agente con los ejercicios de esta plataforma?
8. En una entrevista con agente, ¿qué demuestra tu nivel?

**Respuestas:** 1) Qué hacer, dónde, cómo se verifica (pruebas) y los casos borde. 2) Qué hace y su arquitectura, stack y versiones,
comandos (instalar, ejecutar, probar, lint), convenciones y reglas (qué no tocar, pruebas obligatorias, nada de secretos). 3) Porque
revisar un plan corto es mucho más fácil que revisar mucho código en la dirección equivocada. 4) Porque unas pruebas mal escritas validan
código mal escrito; el truco es que modifique las pruebas o añada casos especiales para que pasen. 5) Que existe en el registro oficial,
que no es un nombre casi igual a otro, quién lo mantiene, sus descargas y actividad, y si de verdad hace falta. 6) Detenerlo, entender yo
el error y darle una pista concreta o empezar una sesión nueva con mejor contexto. 7) Resolverlos yo; pedirle solo explicaciones de
conceptos o pistas. 8) Entender el problema, pedir en pasos, leer y explicar el resultado, verificarlo con pruebas y corregirlo.
