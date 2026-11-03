# Trabajar con asistentes de IA (y verificar lo que generan)

Los asistentes de IA (Claude, ChatGPT, Copilot, Cursor...) escriben código, explican errores y redactan documentación en segundos. Las
empresas ya no buscan juniors que escriban código más rápido que una IA: buscan juniors que **usen la IA para rendir más y detecten cuándo
se equivoca**. Ese perfil se suele llamar "junior aumentado", y es el que vas a construir en este capítulo.

Aquí aprenderás:

- Para qué sirve (y para qué no) un asistente de IA.
- Cómo **pedir** bien: el contexto que necesita para acertar.
- Los **errores típicos** del código generado, para reconocerlos a primera vista.
- Un **método de verificación** que puedes aplicar a cualquier respuesta.
- Qué información **nunca** compartir.
- Cómo usar la IA para **aprender** sin que piense por ti.

En el tema *Desarrollo con agentes de código* verás cómo trabajar con agentes que editan proyectos completos. Este capítulo es la base:
saber pedir y saber verificar.

---

## 1. Qué es (y qué no es) un asistente de IA

Un asistente de IA está construido sobre un **modelo de lenguaje** (LLM): un sistema entrenado con enormes cantidades de texto y código
que genera la continuación más probable de lo que le escribes. En el tema *Cómo funcionan los LLMs por dentro* verás los detalles; para
usarlo bien, basta con entender tres consecuencias:

1. **Escribe con la misma seguridad cuando acierta que cuando se equivoca.** No tiene una alarma interna que diga "esto me lo estoy
   inventando". Por eso puede proponer una función que no existe con el mismo tono que una que sí.
2. **Solo sabe lo que le das y lo que aprendió en su entrenamiento.** No conoce tu base de datos, tus tablas ni tus reglas de negocio,
   salvo que se las cuentes. Si no le das el esquema, lo **inventa**.
3. **Es excelente en lo común y frágil en lo particular.** Una consulta típica le sale bien; los casos borde de tus datos (nulos,
   empates, duplicados, formatos raros) son justo donde falla.

Conclusión: es un colaborador muy rápido y muy culto, pero **sin acceso a tu contexto y sin responsabilidad**. La responsabilidad del
resultado es tuya.

---

## 2. Para qué usarlo (y para qué no)

**Úsalo para:**

- Generar un **primer borrador** de una consulta SQL, una función o una transformación de datos.
- **Explicar** código o un error que no entiendes: "explícame este traceback línea por línea".
- Proponer **casos de prueba** y casos borde en los que no habías pensado.
- **Documentar**: docstrings, README, comentarios, mensajes de commit.
- **Revisar** tu código: "¿qué errores o casos borde ves en esta función?".
- **Aprender**: pedirle ejercicios, que te corrija, que te haga preguntas de entrevista o que te explique un concepto de varias formas.

**No lo uses para:**

- **Decidir** qué significa un número de negocio sin comprobarlo.
- **Sustituir tu comprensión**: si no puedes explicar el código que entregas, no lo entregues.
- Procesar **datos confidenciales** en herramientas que tu empresa o tu cliente no han aprobado.
- Hacer los ejercicios de aprendizaje por ti (sección 8).

---

## 3. Cómo pedir bien

La calidad de la respuesta depende muchísimo de la calidad de la petición (el *prompt*). Un asistente sin contexto rellena los huecos con
suposiciones, y tus datos casi nunca coinciden con esas suposiciones.

### Los cinco ingredientes de una buena petición

1. **Contexto técnico**: motor de base de datos, lenguaje, versión, librerías. ("PostgreSQL 16", "Python 3.12 con pandas 2").
2. **El esquema o los datos**: tablas con sus columnas, o un ejemplo de los datos (inventado o anonimizado).
3. **La granularidad**: qué es una fila del resultado. ("Una fila por cliente", "una fila por mes y canal".)
4. **El formato esperado**: nombres de columnas, orden, cómo tratar los empates y los nulos.
5. **Las restricciones y lo que quieres además**: "usa CTE", "sin librerías externas", "explica cada paso", "indica los supuestos que
   hiciste".

### Ejemplo

> **Mala:** "Dame las ventas por cliente."

> **Buena:** "Tengo PostgreSQL con `orders(id, customer_id, order_date, status)` y `order_items(order_id, quantity, unit_price)`. Quiero
> **una fila por cliente** con el total gastado (`SUM(quantity * unit_price)`) en pedidos con `status = 'completado'` de 2024, ordenado de
> mayor a menor y, en empate, por `customer_id`. Usa una CTE y explica cada paso. Dime qué supuestos hiciste y qué casos podrían romper la
> consulta."

La segunda petición elimina casi todas las suposiciones: el asistente ya no tiene que adivinar nombres de columnas, qué cuenta como
"venta", el periodo ni el orden.

### Pide que razone y que dude

Frases que mejoran mucho las respuestas:

- "Antes de escribir código, explica cómo lo vas a resolver."
- "Indica los supuestos que estás haciendo."
- "¿Qué casos borde podrían hacer que esto falle?"
- "Revisa tu respuesta y busca errores."
- "Si no estás seguro de que una función exista, dilo."

### Itera

La primera respuesta es un borrador. Lo normal es iterar: "el resultado tiene clientes duplicados; ¿por qué?", "funciona, pero ahora
quiero incluir los clientes sin pedidos con 0". Cada corrección concreta mejora el resultado más que volver a empezar.

---

## 4. Los errores típicos del código generado

El código generado **parece correcto**: está bien formateado, tiene nombres razonables y suele funcionar con el ejemplo típico. Estos
fallos aparecen una y otra vez. Apréndelos de memoria, porque los verás en tus proyectos y en las entrevistas.

### En SQL

**El JOIN que multiplica filas.** El asistente une `orders` con `order_items` para sumar ingresos y en la misma consulta cuenta pedidos con
`COUNT(*)`. Pero tras el JOIN cada fila es una **línea de pedido**: el conteo sale inflado (un pedido con 3 líneas cuenta 3). Los ingresos
están bien, porque sumar líneas es correcto; el conteo no.

- **Cómo detectarlo:** compara `COUNT(*)` con `COUNT(DISTINCT o.id)`; si difieren, cada fila no es un pedido.
- **Corrección:** `COUNT(DISTINCT clave)`, o agregar en una CTE antes de unir.

**El LEFT JOIN anulado por un WHERE.** Pides "todos los clientes con sus pedidos completados, 0 si no tienen" y el asistente escribe un
`LEFT JOIN` con `WHERE o.status = 'completado'`. Ese `WHERE` elimina a los clientes sin pedidos (su `status` es `NULL`), y el `LEFT JOIN`
se comporta como un `INNER JOIN`.

- **Cómo detectarlo:** cuenta las filas del resultado: ¿están todos los clientes?
- **Corrección:** la condición sobre la tabla derecha va en el `ON`; y para contar, `COUNT(o.id)` en lugar de `COUNT(*)`.

**Divisiones entre el total equivocado o división entera.** Un porcentaje que divide entre el total general cuando debía dividir entre el
total del grupo, o que sale 0 por dividir dos enteros.

**Orden y empates sin definir.** Un `ORDER BY` sin desempate o un "top 1" con `ROW_NUMBER` sin desempate: el resultado puede cambiar entre
ejecuciones.

### En Python

**Nulos mal tratados.** Le pides un promedio "ignorando los `None`" y el asistente filtra los `None` para la suma pero divide entre la
longitud de la lista **original**, o filtra con `if v` y descarta también los ceros (recuerda: `0` es "falso" en Python). Dos errores
sutiles en una línea.

- **Cómo detectarlo:** prueba con `[10, None, 20]` (el promedio debe ser 15), con `[0, 10]` (debe ser 5) y con `[None, None]`.
- **Regla:** para excluir `None`, compara explícitamente: `v is not None`.

**Orden al revés o empates mal resueltos.** "Los N mayores, en empate por orden alfabético": ordenar por monto descendente **y** por nombre
ascendente a la vez requiere una clave de ordenación que combine ambos criterios (Python compara las tuplas elemento a elemento) y que tenga en cuenta que
uno va de mayor a menor y el otro de menor a mayor. Un asistente que olvida invertir el orden, o que lo invierte para los dos criterios,
devuelve el resultado al revés o desempata mal.

- **Cómo detectarlo:** prueba con un caso con empate y con el caso más simple (dos elementos de distinto valor).

**Formatos de fecha intercambiados.** Interpretar `'2024-03-05'` con un formato día-mes (`'%Y-%d-%m'`) en lugar de año-mes-día
(`'%Y-%m-%d'`). Lo traicionero: con fechas como `'2024-03-05'` "funciona" (da un resultado, aunque sea otra fecha), y solo explota con
días mayores que 12, como `'2024-01-31'` (no existe el mes 31).

- **Cómo detectarlo:** prueba siempre con un día mayor que 12 y compara con un cálculo que conoces (del 1 al 31 de enero hay 30 días).

En Python, las fechas se convierten con el módulo `datetime`:

```python
from datetime import datetime, date

d = datetime.strptime("2024-01-31", "%Y-%m-%d").date()   # texto -> fecha
print(d.year, d.month, d.day)                            # 2024 1 31
print((date(2024, 3, 1) - date(2024, 2, 1)).days)        # 29 (2024 es bisiesto)
print(date.fromisoformat("2024-01-31"))                  # otra forma para el formato ISO
```

`%Y` es el año con 4 cifras, `%m` el mes y `%d` el día. Restar dos fechas da un intervalo (`timedelta`) cuyo atributo `.days` son los días
de diferencia.

### En cualquier lenguaje

**Funciones, parámetros o librerías inventadas ("alucinaciones").** El asistente propone `df.drop_nulls()` en pandas. Ese método no existe
en pandas (es `dropna()`); existe en otra librería, Polars, y el modelo los mezcló. Al ejecutarlo obtienes `AttributeError`.

- **Qué hacer:** lee el error, busca la función en la **documentación oficial** y corrígela. No le pidas a la IA "arréglalo" sin leer el
  error: puede inventar otra cosa.
- **Peligro extra:** si el asistente inventa el **nombre de un paquete** e intentas instalarlo, podrías instalar un paquete malicioso que
  alguien publicó con ese nombre precisamente para aprovechar estos errores. Comprueba que el paquete existe y es el oficial antes de
  instalarlo.

| Fallo | Cómo detectarlo |
|---|---|
| JOIN que multiplica filas | Compara `COUNT(*)` con `COUNT(DISTINCT id)` |
| LEFT JOIN anulado por WHERE | ¿Aparecen los elementos sin pareja? |
| Nulos mal tratados | Prueba con `None`, `NULL`, ceros y todo nulo |
| División equivocada | Calcula a mano un caso pequeño |
| Funciones inventadas | Búscalas en la documentación oficial |
| Fechas intercambiadas | Prueba con un día mayor que 12 |
| Orden o empates indefinidos | Prueba con valores repetidos |

---

## 5. Un método para verificar cualquier respuesta

Aplica estos pasos **siempre**, con código tuyo o ajeno, generado o no:

1. **Lee** el código entero antes de ejecutarlo. Si no entiendes una línea, pregunta qué hace (al asistente o a la documentación).
2. **Prueba con un caso pequeño cuyo resultado conoces de antemano**: 3-5 filas o elementos que puedas calcular a mano.
3. **Reconcilia totales**: la suma por categorías debe coincidir con el total general calculado por separado; el número de filas debe
   tener sentido ("¿40 clientes? ¿por qué salen 38?").
4. **Prueba los casos borde**: vacío, nulos, duplicados, empates, fechas límite, el primer y el último elemento.
5. **Compara con otra vía**: resuelve lo mismo de otra forma (SQL y pandas, o una consulta más simple) y compara.
6. **Escribe la prueba** (`assert` o pytest) para que el error no vuelva.

La comprobación más rentable en datos es la **reconciliación de totales** (paso 3): toma segundos y detecta la mayoría de los JOIN mal
hechos y de los filtros perdidos.

```sql
-- Si esta suma no coincide con la suma de tu desglose por categoría, algo está mal
SELECT SUM(oi.quantity * oi.unit_price)
FROM order_items AS oi
JOIN orders AS o ON o.id = oi.order_id
WHERE o.status = 'completado';
```

---

## 6. Seguridad y privacidad

Todo lo que escribes en un asistente público sale de tu ordenador y llega a los servidores de una empresa. Según el servicio y su
configuración, puede guardarse o usarse para mejorar el modelo. Reglas:

- **Nunca** pegues contraseñas, claves de API, tokens ni cadenas de conexión.
- **Nunca** pegues datos personales de clientes (nombres, correos, teléfonos, documentos de identidad) ni información confidencial de una
  empresa en un asistente que no esté aprobado para ello.
- Para pedir ayuda basta con **el esquema y unas pocas filas inventadas**. Al asistente le sirve igual y no expones nada.
- En el trabajo, usa las herramientas que la empresa haya aprobado (muchas tienen versiones empresariales que no guardan los datos) y
  pregunta antes de usar otras.
- Revisa que el código generado no incluya **comandos peligrosos** (borrar tablas, `rm -rf`, desactivar verificaciones de seguridad) ni
  dependencias desconocidas.
- Si conectas un modelo a tus datos (como en un RAG), trata el contenido como **datos, no como instrucciones**: un documento puede contener
  texto que intente manipular al modelo (lo verás en *Evaluación y seguridad de sistemas de IA*).

---

## 7. Integrar la IA en tu flujo de trabajo

Un flujo de trabajo profesional con un asistente se parece a esto:

1. **Entiendes el problema tú primero**: qué entra, qué sale, qué casos borde hay.
2. **Pides un borrador** con contexto completo.
3. **Lo lees y lo verificas** con el método de la sección 5.
4. **Lo integras** en tu código, adaptándolo a tus convenciones.
5. **Escribes o pides las pruebas**, y compruebas que fallarían si el código estuviera mal.
6. **Haces commit** con un mensaje que explica el cambio (tú eres el autor responsable).

Y tres hábitos que marcan la diferencia:

- Lleva una lista (en *Apuntes*, por ejemplo) de **los errores que el asistente comete contigo**. Verás que se repiten, y aprenderás a
  pedir de forma que no ocurran.
- Cuando el asistente se equivoca, **entiende por qué** antes de corregir. Cada error suyo que detectas es algo que tú ya sabes.
- No aceptes cambios grandes de golpe: pide cambios pequeños que puedas revisar.

---

## 8. Usar la IA para aprender (sin que piense por ti)

Mientras **aprendes**, el riesgo de la IA es que te dé la sensación de saber sin saber: lees una solución, te parece lógica y crees que la
habrías escrito. Pero reconocer una solución no es lo mismo que producirla. En una entrevista, en una prueba técnica o cuando el
asistente se equivoque, solo tendrás lo que de verdad aprendiste.

Reglas para esta ruta:

- **Los ejercicios de la plataforma, resuélvelos tú.** Si te atascas, pide al asistente **una pista**, no la solución: "no me des el
  código; dame una pista sobre qué concepto necesito".
- Pídele que te **explique** conceptos de varias formas, que te ponga **ejemplos distintos** a los del ejercicio y que te haga
  **preguntas** para comprobar que entendiste.
- Cuando resuelvas algo, pídele que **revise tu solución** y te diga qué casos borde no cubriste.
- En tus proyectos, usa el asistente para lo que **ya sabrías hacer** (acelerar) y, para lo nuevo, pídele que te explique antes de que
  escriba.

Una prueba sencilla: si cierras la conversación y no podrías volver a escribir el código ni explicarlo, todavía no lo aprendiste.

---

## 9. Cómo contarlo en una entrevista

Te preguntarán cómo usas la IA. Una buena respuesta muestra **método y criterio**, con un ejemplo concreto:

> "Uso asistentes de IA para acelerar borradores, documentación y casos de prueba, pero valido todo antes de usarlo: pruebo con un caso
> pequeño calculado a mano, reconcilio totales y pruebo los casos borde. Por ejemplo, una vez una consulta generada contaba pedidos
> después de unir con las líneas de pedido y los inflaba; lo detecté porque el total no cuadraba con un conteo directo, y lo corregí con
> `COUNT(DISTINCT)`."

Una historia concreta como esa vale mucho más que "uso mucho ChatGPT". Ve guardando las tuyas.

---

## Resumen del capítulo

| Idea | Lo esencial |
|---|---|
| Qué es | Un generador de texto probable: seguro aunque se equivoque, sin tu contexto, frágil en los bordes |
| Pedir bien | Contexto técnico, esquema, granularidad, formato, restricciones; pide supuestos y casos borde |
| Errores típicos | JOIN que infla, LEFT JOIN anulado, nulos, divisiones, empates, fechas, funciones inventadas |
| Verificar | Leer, caso pequeño a mano, reconciliar totales, casos borde, otra vía, prueba |
| Privacidad | Nada de secretos ni datos personales; esquema y filas inventadas |
| Aprender | Pistas, no soluciones; si no puedes explicarlo, no lo aprendiste |
| Entrevistas | Método y criterio, con una historia concreta |

## Autoevaluación final

1. ¿Por qué un asistente puede inventar una función con total seguridad?
2. ¿Qué cinco ingredientes tiene una buena petición?
3. Una consulta une `orders` con `order_items` y cuenta pedidos con `COUNT(*)`. ¿Qué problema tiene?
4. ¿Por qué `if v` no sirve para quitar los `None` de una lista de números?
5. ¿Con qué fecha compruebas si un código confunde el día y el mes?
6. ¿Cuál es la comprobación más rápida para validar un desglose de ingresos por categoría?
7. Necesitas ayuda con una consulta sobre la tabla de clientes de tu empresa. ¿Qué compartes?
8. ¿Cómo pides ayuda con un ejercicio de aprendizaje sin que te lo resuelvan?

**Respuestas:** 1) Porque genera el texto más probable y no tiene un mecanismo que distinga lo que sabe de lo que inventa. 2) Contexto
técnico, esquema o datos, granularidad, formato esperado y restricciones. 3) Tras el JOIN cada fila es una línea de pedido, así que
`COUNT(*)` infla el número de pedidos; hay que usar `COUNT(DISTINCT o.id)`. 4) Porque también descarta los ceros, que son "falsos" en
Python; hay que comparar con `is not None`. 5) Con un día mayor que 12, como `2024-01-31`. 6) Comprobar que la suma de todas las categorías
coincide con el total calculado por separado. 7) El esquema de la tabla y unas pocas filas inventadas. 8) Pidiendo una pista sobre el
concepto, no el código.
