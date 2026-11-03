# Agentes, tool calling y MCP

Hasta ahora, el modelo solo producía texto. Con **tool calling** (llamada a herramientas) puede además **pedir que se ejecute una
acción**: consultar el estado de un pedido en tu base de datos, buscar en un catálogo, crear una cita en un calendario. Cuando el modelo
encadena varias de esas acciones por su cuenta para cumplir un objetivo, tienes un **agente**.

Es la parte de la IA aplicada que más demanda tiene ahora mismo, y también la que más se usa mal: muchos problemas que se resuelven con
"un agente" funcionarían mejor, más barato y de forma más fiable con un flujo fijo. Este capítulo te enseña cómo funcionan por dentro,
cómo construir uno de forma segura, cuándo **no** usarlo y qué es MCP.

---

## 1. Tool calling: el modelo no ejecuta nada

La idea más importante del capítulo: **el modelo nunca ejecuta las herramientas**. Solo **pide** que se ejecuten, con un texto
estructurado (nombre y argumentos). **Tu código** decide si ejecutarla, la ejecuta y le devuelve el resultado.

```
1. Tu código envía: la pregunta del usuario + la lista de herramientas disponibles (nombre, descripción, esquema)
2. El modelo responde: "quiero llamar a estado_pedido con {"pedido_id": 4471}"
3. Tu código: valida los argumentos, ejecuta la función real, obtiene {"estado": "enviado", "llega": "2025-07-03"}
4. Tu código envía el resultado al modelo
5. El modelo responde al usuario: "Tu pedido 4471 ya fue enviado y llegará el 3 de julio."
```

Esto es lo que hace posible la seguridad: entre el paso 2 y el 3 está **tu código**, que puede validar, limitar, pedir confirmación o
negarse.

### Definir una herramienta

Cada herramienta se describe con un **nombre**, una **descripción** y un **esquema de entrada** en formato JSON Schema:

```python
herramientas = [
    {
        "name": "estado_pedido",
        "description": (
            "Devuelve el estado de envío de un pedido de la tienda. "
            "Úsala cuando el cliente pregunte dónde está su pedido o cuándo llega. "
            "Necesita el número de pedido; si el cliente no lo ha dado, pídeselo antes."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "pedido_id": {"type": "integer", "description": "Número del pedido, p. ej. 4471"},
            },
            "required": ["pedido_id"],
        },
    }
]
```

La **descripción es un prompt**: el modelo decide cuándo y cómo usar la herramienta leyéndola. Una buena descripción dice qué hace,
**cuándo usarla** (y cuándo no) y qué significa cada parámetro. Es lo que más influye en que el agente funcione bien.

### JSON Schema en lo básico

| Clave | Significado |
|---|---|
| `"type": "object"` | La entrada es un objeto (un diccionario) |
| `properties` | Los campos permitidos y el tipo de cada uno |
| `required` | La lista de campos obligatorios |
| `"type"` de cada campo | `"string"`, `"integer"`, `"number"` (entero o decimal), `"boolean"`, `"array"`, `"object"` |
| `enum` | Lista de valores permitidos: `{"type": "string", "enum": ["web", "app", "tienda"]}` |

---

## 2. Validar antes de ejecutar

Los argumentos los escribe el modelo, y el modelo **puede equivocarse**: omitir un campo obligatorio, inventar uno que no existe o poner
un texto donde iba un número. Y si el contenido que procesa el modelo viene de usuarios o documentos externos, alguien puede intentar
**manipularlo** para que llame a una herramienta con argumentos maliciosos. Por eso tu código **valida siempre** antes de ejecutar.

Las tres comprobaciones básicas contra el esquema:

1. **Faltan campos obligatorios**: cada nombre de `required` debe estar en los argumentos.
2. **Sobran campos**: un argumento que no está en `properties` es sospechoso (o un error del modelo).
3. **Tipos incorrectos**: el valor de cada campo debe ser del tipo declarado.

Lo útil es **recolectar todos los errores** en una lista (no detenerse en el primero), porque así puedes devolvérselos todos al modelo y
que corrija la llamada de una vez.

### La correspondencia de tipos en Python, y una trampa

| JSON Schema | Python |
|---|---|
| `string` | `str` |
| `integer` | `int` |
| `number` | `int` o `float` |
| `boolean` | `bool` |

La trampa: en Python, **`bool` es una subclase de `int`**. Mira:

```python
isinstance(True, int)     # True   ← ¡sorpresa!
isinstance(True, bool)    # True
isinstance(5, bool)       # False
True + True               # 2
type(True) is int         # False
```

Si validas un `integer` solo con `isinstance(valor, int)`, aceptarías `True` como número de pedido. Para un validador estricto, un
booleano **no** debe aceptarse como `integer` ni como `number`: hay que comprobar explícitamente que no sea un `bool`.

En proyectos reales, usa una librería de validación: **Pydantic** (que ya conoces de FastAPI) o `jsonschema`. Pero conviene entender qué
hacen.

---

## 3. Ejecutar sin romper el sistema

La ejecución de una herramienta puede fallar de muchas formas: el modelo pidió una herramienta que no existe, la base de datos no
responde, el pedido no existe, la función lanza una excepción. Si ese error **revienta tu programa**, el agente se cae a mitad de una
conversación.

El principio: **convertir los fallos en resultados**. La función que ejecuta las herramientas nunca deja escapar una excepción; devuelve
siempre un resultado estructurado que indica si fue bien o mal, y en el segundo caso, un mensaje de error **útil para el modelo**:

| Situación | Lo que se devuelve al modelo |
|---|---|
| Todo bien | El resultado |
| Herramienta desconocida | "La herramienta X no existe; las disponibles son: ..." |
| Argumentos inválidos | La lista de errores de validación |
| La función lanzó una excepción | Un mensaje con el tipo de error, sin detalles internos sensibles |

¿Por qué devolver el error al modelo en lugar de abortar? Porque **el modelo puede recuperarse**: si le dices "falta el campo pedido_id",
pedirá el número al usuario; si le dices "el pedido 4471 no existe", lo comunicará. Los agentes robustos son los que manejan bien los
errores.

Herramientas de Python que necesitas: un diccionario `{nombre: funcion}` para buscar la herramienta (`nombre in herramientas` o `.get`),
llamar a una función con un diccionario de argumentos usando `funcion(**argumentos)`, y `try/except Exception as e` para capturar el error
(con `str(e)` o `type(e).__name__` para describirlo).

```python
def sumar(a, b):
    return a + b

args = {"a": 2, "b": 3}
sumar(**args)          # 5: ** desempaqueta el diccionario como argumentos con nombre
```

---

## 4. El bucle del agente

Un agente es un **bucle**: el modelo pide herramientas, tú las ejecutas y le devuelves los resultados, hasta que el modelo da una
respuesta final.

```
mensajes = [pregunta del usuario]
repetir (como máximo N veces):
    respuesta = modelo(mensajes)
    si la respuesta es texto final  →  devolverla y terminar
    si pide una herramienta:
        añadir a mensajes lo que pidió el modelo
        ejecutar la herramienta (sin romper nada)
        añadir a mensajes el resultado
si se agotan los pasos  →  terminar con un mensaje de que no se pudo completar
```

Tres detalles esenciales:

1. **El historial crece en cada vuelta**: el modelo necesita ver lo que pidió y lo que obtuvo para decidir el siguiente paso. Si no
   añades la petición y el resultado a `mensajes`, el modelo volverá a pedir lo mismo una y otra vez.
2. **Un límite de pasos**: sin él, un agente confundido puede entrar en un bucle infinito de llamadas, gastando tokens (dinero) sin parar.
3. **Un final controlado** cuando se alcanza el límite: devolver algo útil en vez de colgarse.

### Con el SDK de Anthropic

Así se ve el bucle con la API de Claude (los nombres de los campos son los de esta API; cada proveedor tiene su formato, pero la idea es
la misma):

```python
import anthropic

client = anthropic.Anthropic()

def responder(pregunta, herramientas, funciones, max_pasos=8):
    mensajes = [{"role": "user", "content": pregunta}]

    for _ in range(max_pasos):
        respuesta = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=2048,
            system="Eres el asistente de la tienda. Usa las herramientas para consultar datos reales.",
            tools=herramientas,
            messages=mensajes,
        )

        if respuesta.stop_reason != "tool_use":
            return "".join(b.text for b in respuesta.content if b.type == "text")

        # 1) Guardar en el historial lo que pidió el modelo (texto y bloques tool_use)
        mensajes.append({"role": "assistant", "content": respuesta.content})

        # 2) Ejecutar cada herramienta pedida y devolver los resultados en un mensaje del usuario
        resultados = []
        for bloque in respuesta.content:
            if bloque.type == "tool_use":
                ok, contenido = ejecutar_herramienta(funciones, bloque.name, bloque.input)
                resultados.append({
                    "type": "tool_result",
                    "tool_use_id": bloque.id,      # enlaza el resultado con la petición
                    "content": str(contenido),
                    "is_error": not ok,
                })
        mensajes.append({"role": "user", "content": resultados})

    return "No pude completar la consulta. ¿Puedes darme más detalles?"
```

`ejecutar_herramienta` es la función de la sección 3: busca la función, valida los argumentos, la ejecuta dentro de un `try` y devuelve
si fue bien y el resultado o el error. El campo `is_error` le dice al modelo que la herramienta falló, para que se recupere.

El SDK también ofrece un *tool runner* que hace este bucle por ti; escribirlo a mano una vez es la mejor forma de entender qué hace.

---

## 5. ¿Agente o flujo fijo?

Esta es la decisión de diseño más importante, y la pregunta que más se hace en entrevistas.

| | Flujo fijo (*workflow*) | Agente |
|---|---|---|
| Quién decide los pasos | **Tu código** | **El modelo** |
| Previsibilidad | Alta: siempre los mismos pasos | Baja: puede tomar caminos distintos |
| Costo y latencia | Bajos y estables | Más llamadas, variables |
| Depuración | Fácil | Difícil |
| Cuándo usarlo | Los pasos se conocen de antemano | Los pasos dependen de lo que se va descubriendo |

Ejemplo: un cliente quiere que cada mensaje de WhatsApp se clasifique (consulta, reclamo o compra) y se responda con la información del
catálogo. Los pasos se conocen: **clasificar → buscar (RAG) → responder**. Es un flujo fijo con tres llamadas, no un agente con quince
herramientas que "decida". El flujo será más barato, más rápido, más fácil de probar y más fiable.

Patrones de flujo fijo muy útiles:

- **Encadenar** (*chaining*): la salida de un paso es la entrada del siguiente (extraer → validar → resumir).
- **Enrutar** (*routing*): un primer paso clasifica y, según la categoría, se sigue un camino distinto (cada uno con su prompt).
- **Paralelizar**: varias llamadas independientes a la vez (analizar 10 documentos) y combinar los resultados.

Un agente se justifica cuando **no puedes saber de antemano** los pasos: investigar un problema abriendo archivos según lo que encuentra,
una tarea con muchas ramas posibles. Y aun así, empieza con **pocas herramientas bien descritas**: con muchas, el modelo elige peor.

**La regla práctica: empieza por lo más simple que funcione** (una llamada; luego un flujo fijo; y solo si hace falta, un agente).

---

## 6. Herramientas peligrosas: permisos y confirmación

Una herramienta de **lectura** (consultar el estado de un pedido) tiene poco riesgo. Una herramienta que **actúa** (reembolsar, enviar un
correo, borrar, pagar) puede causar daños reales si el modelo se equivoca o si alguien lo manipula con una inyección de instrucciones.

Defensas en capas:

1. **Mínimo privilegio**: dale al agente solo las herramientas que necesita. Un asistente de soporte no necesita poder borrar clientes.
2. **Validación de argumentos** con límites de negocio: un reembolso nunca mayor que el importe del pedido ni que un máximo fijo, y solo
   sobre pedidos del cliente que está conversando (la identidad sale de la **sesión**, no de lo que dice el modelo).
3. **Confirmación humana** (*human in the loop*) para las acciones irreversibles o caras: el agente propone ("¿Confirmas el reembolso de
   25 USD del pedido 4471?") y la acción solo se ejecuta cuando una persona aprueba.
4. **Registro** de cada llamada (quién, qué, con qué argumentos, resultado) para poder auditar.
5. **Límites**: número máximo de pasos, de llamadas y de gasto por conversación.

Confiar en que "el modelo sabe cuándo usarla" o esconder la descripción de la herramienta no son defensas.

---

## 7. MCP: Model Context Protocol

Cada aplicación de IA definía sus herramientas a su manera, y conectar N aplicaciones con M servicios exigía N × M integraciones. **MCP**
(*Model Context Protocol*) es un **estándar abierto** para exponer **herramientas, datos y prompts** a aplicaciones de IA, de forma que
cualquier cliente compatible pueda usarlos. Se suele comparar con un "USB-C para la IA".

```
Clientes MCP (Claude, IDEs, agentes propios)  ◄── protocolo MCP ──►  Servidores MCP (tu base de datos, GitHub, tu API, un CRM)
```

Un **servidor MCP** expone tres tipos de cosas:

| Tipo | Qué es | Ejemplo |
|---|---|---|
| **Tools** (herramientas) | Acciones que el modelo puede pedir | `buscar_pedido`, `crear_ticket` |
| **Resources** (recursos) | Datos que se pueden leer | Un archivo, el esquema de una base de datos |
| **Prompts** | Plantillas de instrucciones reutilizables | "Resumir el ticket X" |

Un servidor MCP mínimo en Python con el SDK oficial:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tienda")

@mcp.tool()
def stock_producto(producto_id: int) -> dict:
    """Devuelve el stock disponible de un producto del catálogo."""
    # consultar la base de datos (con un usuario de solo lectura)
    return {"producto_id": producto_id, "stock": 12}

if __name__ == "__main__":
    mcp.run()
```

El SDK genera el esquema a partir de los **tipos** de los parámetros y la descripción a partir del **docstring**: por eso ambos importan.

### Por qué te interesa

- **Para clientes freelance**: construir un servidor MCP para el sistema de un negocio (su inventario, su CRM) permite que lo usen desde
  Claude u otros clientes compatibles sin una interfaz propia.
- **Para tu portafolio**: un servidor MCP pequeño y bien hecho sobre datos reales es un proyecto diferenciador.

### Seguridad en MCP

Instalar un servidor MCP es **dar acceso** a un modelo: a tus archivos, a tu base de datos, a tus cuentas.

- Instala solo servidores de fuentes **confiables** y revisa qué permisos piden.
- En los tuyos: **solo lectura** por defecto, credenciales con el mínimo privilegio, validación de argumentos y confirmación para lo que
  modifica datos.
- Las respuestas de un servidor MCP (contenido de páginas, issues, correos) pueden contener **inyecciones de instrucciones**.

---

## 8. Probar un agente

Un agente se prueba en dos niveles:

- **Las piezas, sin modelo**: la validación, la ejecución segura y el bucle se pueden probar con un **modelo falso** (una función que
  devuelve respuestas predefinidas: "primero pide esta herramienta, luego responde"). Así compruebas que el bucle añade el historial,
  respeta el límite de pasos y maneja los errores, sin gastar tokens y con resultados deterministas.
- **El comportamiento, con el modelo**: un conjunto de casos (preguntas y qué herramienta debería usar, con qué argumentos, y qué respuesta
  final se espera), medido como verás en *Evaluación y seguridad de sistemas de IA*.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Tool calling | El modelo **pide**; tu código valida, ejecuta y devuelve el resultado |
| Definición | Nombre, descripción (es un prompt) y esquema JSON |
| Validación | Faltan, sobran, tipos; recolectar todos los errores; `bool` es subclase de `int` |
| Ejecución segura | Nunca dejar escapar excepciones; devolver errores útiles al modelo |
| Bucle | Historial que crece, límite de pasos, final controlado |
| Agente vs flujo | Si conoces los pasos, flujo fijo; empieza por lo más simple |
| Acciones peligrosas | Mínimo privilegio, límites, confirmación humana, registro |
| MCP | Estándar para exponer tools, resources y prompts a cualquier cliente compatible |
| Pruebas | Modelo falso para las piezas; conjunto de casos para el comportamiento |

## Autoevaluación final

1. ¿Quién ejecuta una herramienta en el tool calling: el modelo o tu código? ¿Por qué importa?
2. ¿Qué debe contener una buena descripción de herramienta?
3. ¿Qué devuelve `isinstance(False, int)` y qué problema causa al validar?
4. ¿Por qué conviene recolectar todos los errores de validación en una lista?
5. Una herramienta lanza una excepción. ¿Qué debe hacer tu código?
6. ¿Qué pasa si en el bucle no añades al historial la petición del modelo y el resultado?
7. ¿Por qué un agente necesita un límite de pasos?
8. Un cliente quiere clasificar correos y responder con su catálogo. ¿Agente o flujo fijo? ¿Por qué?
9. ¿Cómo protegerías una herramienta `cancelar_suscripcion`?

**Respuestas:** 1) Tu código; entre la petición y la ejecución puedes validar, limitar o pedir confirmación. 2) Qué hace, cuándo usarla
(y cuándo no) y qué significa cada parámetro. 3) `True`; un validador ingenuo aceptaría un booleano como entero. 4) Para devolverlos
todos al modelo y que corrija la llamada de una vez. 5) Capturarla y devolver un resultado de error útil para el modelo, sin romper el
programa. 6) El modelo no sabe lo que ya pidió y obtuvo, y repetirá la misma petición. 7) Para evitar bucles infinitos que gastan tokens
sin parar. 8) Flujo fijo: los pasos se conocen (clasificar, buscar, responder); es más barato, rápido y fiable. 9) Solo sobre la cuenta
del usuario de la sesión, con confirmación humana explícita, registro de la acción y sin darla a agentes que no la necesitan.
