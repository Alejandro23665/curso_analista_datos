# Interfaces para apps con IA: React, TypeScript y streaming

Un cliente o un reclutador no abre tu repositorio: **abre un enlace y prueba**. Si escribe una pregunta y durante 15 segundos no pasa
nada, cierra la pestaña. Si ve cómo la respuesta aparece palabra por palabra, con las fuentes citadas debajo y un botón para detenerla,
percibe un producto profesional, aunque el backend sea idéntico.

Ya conoces React por tu formación. Este capítulo se centra en lo **específico de una app con IA**: la arquitectura correcta, el streaming
de principio a fin (del modelo a la pantalla), los estados de la interfaz, TypeScript para no romper nada y el despliegue.

---

## 1. La arquitectura correcta

```
Navegador (React)  ──►  Tu backend (FastAPI)  ──►  API del modelo (Claude u otro)
                   ◄──  (streaming SSE)       ◄──  (streaming)
```

Tres reglas que no se negocian:

1. **La clave de la API vive solo en el backend**, como variable de entorno. Todo lo que está en el frontend (incluido cualquier
   `VITE_API_KEY`, que Vite incrusta en el JavaScript publicado) lo puede leer cualquiera con las herramientas del navegador. Una clave
   expuesta se usa para gastar tu saldo en horas.
2. **El backend decide qué se envía al modelo**: el prompt del sistema, los documentos del RAG, el modelo, el límite de tokens. Si el
   frontend enviara el prompt del sistema, cualquiera podría cambiarlo y usar tu backend como un acceso gratuito al modelo.
3. **El backend protege el gasto**: autenticación (o al menos un límite de peticiones por IP o por usuario), longitud máxima del mensaje
   y del historial, y un límite de `max_tokens`.

El frontend solo hace tres cosas: enviar el mensaje del usuario (y el historial), mostrar la respuesta a medida que llega y gestionar los
estados de la interfaz.

---

## 2. Por qué streaming

Un LLM genera la respuesta **token a token**. Una respuesta de 400 palabras puede tardar 10-20 segundos en completarse, pero el primer
token llega en uno o dos segundos.

- **Sin streaming**: el usuario mira una pantalla quieta hasta que la respuesta está completa.
- **Con streaming**: ve texto en uno o dos segundos y lee mientras se genera.

El tiempo total es el mismo y se gastan los mismos tokens; lo que cambia es el **tiempo hasta el primer contenido**, que es lo que el
usuario percibe como velocidad. Además, el streaming evita que las peticiones largas choquen con los límites de tiempo de los servidores
y proxies.

---

## 3. Server-Sent Events (SSE): el formato

**SSE** es un estándar sencillo para que el servidor envíe una secuencia de eventos por una respuesta HTTP que se mantiene abierta. Es
texto plano, línea a línea, con la cabecera `Content-Type: text/event-stream`. Las reglas básicas:

| Línea | Significado |
|---|---|
| `data: <contenido>` | Datos del evento. Ojo: el prefijo es `data:` **seguido de un espacio** |
| `event: <nombre>` | Nombre del tipo de evento (opcional) |
| `: <texto>` | Comentario: se ignora (se usa para mantener viva la conexión) |
| línea vacía | Separa un evento del siguiente |

Ejemplo de un stream:

```
: conectado

event: delta
data: {"texto": "La capital"}

event: delta
data: {"texto": " de Francia es París."}

event: fin
data: {"tokens_salida": 9}
```

Muchas APIs (y muchos backends) usan una convención para marcar el **final**: una línea de datos especial, un evento con nombre propio
como el `fin` de arriba, o simplemente cerrar la conexión. Quien lee el stream tiene que **reconocer el final y dejar de leer**.

### Un detalle que causa muchos errores: los espacios y los saltos de línea

El texto de un modelo empieza muchas veces con un espacio (`" de Francia"`): es parte de la respuesta. Al quitar el prefijo `data: `,
**quita exactamente ese prefijo** y nada más; si usas `.strip()` sobre el contenido, se pegarán las palabras ("La capitalde Francia").

Y si el contenido tiene un **salto de línea**, rompería el formato (cada línea SSE es un campo). Por eso es habitual enviar cada fragmento
como **JSON** (`json.dumps` convierte el salto de línea en `\n` escrito), como en el ejemplo de arriba.

Herramientas de Python útiles para procesar este tipo de líneas: `linea.startswith("data: ")`, el corte `linea[len("data: "):]` y
`"".join(partes)` para unir los fragmentos acumulados en una lista.

### Comprueba que entendiste

**Pregunta:** recibes las líneas `data: Hola`, `: ping` y `data:  mundo` (con dos espacios). ¿Qué texto debería mostrarse?

**Respuesta:** `"Hola mundo"`. El comentario se ignora; del tercer fragmento se quita el prefijo `data: ` (con un espacio) y queda
`" mundo"`, con su espacio inicial, que es parte del texto.

---

## 4. El backend: reenviar el stream del modelo

Con FastAPI y el SDK de Anthropic, el backend recibe el stream del modelo y lo reenvía al navegador como SSE:

```python
import json, os
import anthropic
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI()
client = anthropic.Anthropic()          # lee ANTHROPIC_API_KEY del entorno

class Mensaje(BaseModel):
    rol: str = Field(pattern="^(user|assistant)$")
    texto: str = Field(max_length=4000)

class Peticion(BaseModel):
    mensajes: list[Mensaje] = Field(max_length=20)

SYSTEM = "Eres el asistente de la tienda. Responde en español, de forma breve."

def sse(evento: str, datos: dict) -> str:
    return f"event: {evento}\ndata: {json.dumps(datos, ensure_ascii=False)}\n\n"

@app.post("/api/chat")
def chat(p: Peticion):
    def generar():
        try:
            with client.messages.stream(
                model="claude-opus-5-5",
                max_tokens=1024,
                system=SYSTEM,
                messages=[{"role": m.rol, "content": m.texto} for m in p.mensajes],
            ) as stream:
                for texto in stream.text_stream:
                    yield sse("delta", {"texto": texto})
                final = stream.get_final_message()
            yield sse("fin", {"tokens_salida": final.usage.output_tokens})
        except anthropic.APIError:
            yield sse("error", {"mensaje": "El asistente no está disponible. Inténtalo de nuevo."})

    return StreamingResponse(generar(), media_type="text/event-stream")
```

Qué hay que notar:

- **Validación con Pydantic**: el rol solo puede ser `user` o `assistant`, cada mensaje tiene una longitud máxima y el historial, un
  número máximo de mensajes. Protege tu gasto.
- `generar()` es un **generador**: cada `yield` envía un trozo al navegador en cuanto está listo.
- Los errores que ocurren **después** de empezar a enviar no pueden cambiar el código HTTP (ya se envió el 200), por eso se comunican como
  un **evento de error** dentro del stream.
- El mensaje de error para el usuario es genérico; el detalle va a los logs del servidor.
- Si el navegador cierra la conexión (el usuario pulsa "Detener"), el servidor deja de consumir el generador y la generación se corta, con
  lo que dejas de pagar tokens que nadie va a leer.

---

## 5. El frontend: leer el stream en React

`EventSource`, la API nativa de SSE en el navegador, solo permite peticiones `GET`, y un chat necesita enviar el historial con `POST`.
Por eso se usa `fetch` y se lee el cuerpo poco a poco:

```js
async function enviar(mensajes, alFragmento, signal) {
  const resp = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mensajes }),
    signal,                                   // permite cancelar con AbortController
  });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

  const lector = resp.body.getReader();
  const decoder = new TextDecoder();
  let pendiente = "";

  while (true) {
    const { done, value } = await lector.read();
    if (done) break;
    pendiente += decoder.decode(value, { stream: true });

    // Los eventos están separados por una línea en blanco
    const eventos = pendiente.split("\n\n");
    pendiente = eventos.pop();                // el último puede estar incompleto: se guarda para la próxima vuelta
    for (const bloque of eventos) {
      const evento = parsearEvento(bloque);   // { nombre, datos } a partir de las líneas event:/data:
      if (evento) alFragmento(evento);
    }
  }
}
```

La idea más importante de este código es **`pendiente`**: la red no entrega los datos alineados con los eventos. Un trozo puede traer
evento y medio, y el resto llega en el siguiente. Por eso se acumula el texto, se procesan solo los eventos **completos** y se guarda el
final incompleto para la siguiente lectura.

### Actualizar el estado sin perder fragmentos

```jsx
const [mensajes, setMensajes] = useState([]);

function alFragmento({ nombre, datos }) {
  if (nombre === "delta") {
    setMensajes((prev) => {
      const ultimo = prev[prev.length - 1];
      return [...prev.slice(0, -1), { ...ultimo, texto: ultimo.texto + datos.texto }];
    });
  }
}
```

Dos claves de React aquí:

- Se usa la **forma funcional** `setMensajes(prev => ...)`: los fragmentos llegan muy seguidos y, si usaras la variable `mensajes`
  directamente, podrías trabajar con una versión antigua del estado y perder texto.
- **No se modifica** el objeto existente (`ultimo.texto += ...`): se crea uno nuevo. React detecta los cambios comparando referencias.

### Detener la generación

```jsx
const controlador = useRef(null);

async function preguntar(texto) {
  controlador.current = new AbortController();
  try {
    await enviar(historial, alFragmento, controlador.current.signal);
  } catch (e) {
    if (e.name !== "AbortError") setError("No se pudo obtener respuesta.");
  }
}

function detener() {
  controlador.current?.abort();
}
```

Cancelar no es un error: por eso se ignora el `AbortError`.

### Renderizar la respuesta de forma segura

Los modelos responden en **Markdown** (listas, negritas, código). Para mostrarlo, usa una librería como `react-markdown` (la que usa esta
plataforma), que convierte el Markdown en componentes de React **sin** usar `dangerouslySetInnerHTML`. Trata la salida del modelo como
entrada no confiable: no permitas HTML crudo y ten cuidado con las imágenes externas, que pueden usarse para filtrar datos a otro
servidor.

---

## 6. Los estados de la interfaz

Una interfaz de chat profesional se diseña **estado por estado**:

| Estado | Qué ve el usuario | Detalle técnico |
|---|---|---|
| Vacío | Una frase de bienvenida y 3-4 preguntas de ejemplo que se pueden pulsar | Enseña qué sabe hacer el asistente |
| Enviando | El mensaje del usuario aparece al instante; indicador de "pensando" | Actualización optimista |
| Respondiendo | Texto que crece; botón **Detener** | `AbortController` |
| Bloqueado | Botón de enviar desactivado mientras responde | Evita peticiones duplicadas |
| Error | Mensaje claro y botón **Reintentar** | El modelo puede saturarse (429/529) o caer la red |
| Terminado | Las **fuentes** citadas (en un RAG) y, opcionalmente, botones de valoración | La valoración alimenta tu evaluación |

Otros detalles que marcan la diferencia:

- **Desplazamiento automático** hacia abajo mientras llega texto, pero **no** si el usuario subió a leer algo anterior.
- `Enter` envía y `Shift+Enter` añade una línea nueva.
- El campo de texto recupera el foco después de enviar.
- **Móvil**: la mayoría de la gente abrirá tu enlace desde el teléfono. Prueba que el teclado no tape el campo de texto.
- **Accesibilidad**: los botones con solo icono necesitan `aria-label`, y la zona de mensajes puede llevar `aria-live="polite"` para que
  los lectores de pantalla anuncien la respuesta.

---

## 7. TypeScript: tipar el contrato con el backend

Las ofertas actuales piden "React + TypeScript" casi siempre. Su mayor valor en una app con IA es **tipar el contrato** entre el frontend
y el backend, para que el editor te avise si accedes a un campo que no existe:

```ts
type Rol = "user" | "assistant";

interface Mensaje {
  rol: Rol;
  texto: string;
  fuentes?: Fuente[];          // opcional: solo en las respuestas del RAG
}

interface Fuente {
  documento: string;
  seccion: string;
}

type EventoChat =
  | { nombre: "delta"; datos: { texto: string } }
  | { nombre: "fin"; datos: { tokens_salida: number } }
  | { nombre: "error"; datos: { mensaje: string } };
```

`EventoChat` es una **unión discriminada**: según el valor de `nombre`, TypeScript sabe qué forma tienen los `datos`.

```ts
function alFragmento(e: EventoChat) {
  switch (e.nombre) {
    case "delta":  agregarTexto(e.datos.texto); break;        // aquí TypeScript sabe que existe .texto
    case "error":  setError(e.datos.mensaje); break;
    case "fin":    setTerminado(true); break;
  }
}
```

Conceptos de TypeScript que más vas a usar: tipos e interfaces, uniones de literales (`"user" | "assistant"`), campos opcionales (`?`),
uniones discriminadas, genéricos básicos (`useState<Mensaje[]>([])`) y `unknown` para datos que vienen de fuera hasta validarlos.

Recuerda que los tipos **desaparecen al compilar**: no validan nada en tiempo de ejecución. Si el backend envía algo distinto, TypeScript
no lo detecta. Para validar de verdad los datos externos se usa una librería como **Zod**, igual que Pydantic en el backend.

---

## 8. Desarrollo local y despliegue

### En local

Vite sirve el frontend en un puerto (5173) y FastAPI el backend en otro (8000). Para no pelear con CORS en desarrollo, configura el
**proxy** de Vite para que `/api` vaya al backend (esta plataforma lo hace así):

```js
// vite.config.js
export default {
  server: { proxy: { "/api": "http://localhost:8000" } },
};
```

### En producción

| Opción | Cuándo |
|---|---|
| Frontend y backend en el **mismo dominio** (Vercel con función de Python, o un nginx delante) | Lo más sencillo: sin CORS |
| Frontend en Vercel/Netlify y backend en Railway/Render/Fly.io | Backends con procesos largos, WebSockets o tareas en segundo plano |

Si están en dominios distintos, configura **CORS** en el backend con la lista exacta de dominios del frontend, nunca `*` en producción.

Problemas típicos del streaming en producción:

- Algunos **proxies acumulan la respuesta** (*buffering*) y la entregan de golpe al final, anulando el streaming. En nginx se desactiva con
  `proxy_buffering off` o con la cabecera `X-Accel-Buffering: no`.
- Las funciones *serverless* tienen un **tiempo máximo de ejecución**; revisa el límite de tu plataforma para respuestas largas.
- La **compresión** (gzip) puede retener fragmentos pequeños; desactívala para la ruta del stream si notas que el texto llega a trompicones.

---

## 9. Antes de enseñar la demo

Una prueba rápida desde el móvil, con datos móviles, en modo incógnito (como la verá un desconocido):

1. ¿Carga el enlace en menos de 3 segundos?
2. ¿Entiendo qué hace la app sin que nadie me lo explique?
3. ¿La respuesta empieza a aparecer en uno o dos segundos?
4. ¿Puedo detenerla?
5. Si apago la red a mitad de una respuesta, ¿veo un error claro con opción de reintentar?
6. ¿Se ven las fuentes de cada respuesta?
7. En las herramientas de desarrollo (pestaña *Network* y el código fuente), ¿aparece alguna clave? (No debe aparecer.)

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Arquitectura | Navegador → tu backend → modelo; la clave solo en el backend |
| Streaming | Mismo tiempo total, mucho menos tiempo hasta el primer texto |
| SSE | Líneas `data: ` (con espacio), `event:`, comentarios `:`, eventos separados por línea en blanco |
| Fragmentos | Quitar solo el prefijo; no usar `strip`; JSON para los saltos de línea |
| Backend | `client.messages.stream` + generador + `StreamingResponse`; errores como eventos |
| Frontend | `fetch` + `getReader` + búfer de lo pendiente; `setState` funcional; `AbortController` |
| Estados | Vacío, enviando, respondiendo, error con reintento, fuentes |
| TypeScript | Tipar el contrato; uniones discriminadas; los tipos no validan en ejecución |
| Despliegue | Proxy en local; mismo dominio o CORS exacto; cuidado con el *buffering* |

## Autoevaluación final

1. ¿Por qué una variable `VITE_API_KEY` no es un lugar seguro para la clave del modelo?
2. ¿El streaming reduce el costo o el tiempo total de la respuesta? ¿Qué mejora entonces?
3. ¿Por qué no se debe usar `.strip()` sobre el contenido de cada fragmento?
4. ¿Por qué se envían los fragmentos como JSON en el ejemplo del backend?
5. En el lector del frontend, ¿para qué sirve la variable `pendiente`?
6. ¿Por qué se usa `setMensajes(prev => ...)` en lugar de `setMensajes([...mensajes, ...])` al recibir fragmentos?
7. Un error del modelo ocurre después de haber enviado 20 fragmentos. ¿Por qué no puedes devolver un código 500?
8. ¿TypeScript te protege si el backend cambia el nombre de un campo? ¿Qué usarías para validarlo de verdad?

**Respuestas:** 1) Vite la incrusta en el JavaScript que se descarga el navegador: cualquiera puede leerla. 2) No: mismo costo y mismo
tiempo total; mejora el tiempo hasta el primer contenido, que es lo que el usuario percibe. 3) Porque los espacios iniciales y finales
son parte del texto; quitarlos pega las palabras. 4) Para que un salto de línea dentro del texto no rompa el formato de líneas de SSE.
5) Para guardar el evento incompleto que llegó al final de un trozo y completarlo con la siguiente lectura. 6) Porque los fragmentos llegan
muy seguidos y la variable del cierre podría tener un estado antiguo; la forma funcional siempre parte del último estado. 7) Porque el
código de estado y las cabeceras ya se enviaron con el primer fragmento; el error se comunica como un evento dentro del stream. 8) No, los
tipos desaparecen al compilar; se valida con una librería como Zod.
