from ._helpers import checklist, py, quiz, sql

TOPICS = [
    {
        "slug": "ia-asistida",
        "phase": "pandas",
        "title": "Trabajar con asistentes de IA (y verificar lo que generan)",
        "summary": "Cómo pedir SQL y Python a un asistente de IA, cómo comprobar que es correcto y qué datos nunca compartir.",
        "hours": 8,
        "theory": r"""
# Trabajar con asistentes de IA (y verificar lo que generan)

Las empresas ya no buscan juniors que escriban código más rápido que una IA; buscan juniors que **usen la IA para rendir más y detecten cuándo se equivoca**.
Ese es el perfil de "junior aumentado". Este tema te enseña a trabajar así desde ahora, en el resto de la ruta y en tu primer empleo.

## 1. Para qué usarla (y para qué no)

**Úsala para:**
- Generar un primer borrador de una consulta SQL o una transformación de pandas.
- Explicar código o un error que no entiendes ("explícame este traceback línea por línea").
- Proponer casos de prueba y casos borde en los que no habías pensado.
- Documentar: docstrings, README, comentarios.
- Aprender: pídele ejercicios, que te corrija o que te haga preguntas de entrevista.

**No la uses para:**
- Decidir qué significa un número de negocio sin comprobarlo.
- Sustituir tu comprensión: si no puedes explicar el código que entregas, no lo entregues.
- Procesar datos confidenciales en herramientas que tu empresa no ha aprobado.

## 2. Cómo pedir bien (prompting para datos)

Un buen pedido da **contexto, esquema, granularidad y formato esperado**:

> *Mala:* "Dame las ventas por cliente."
>
> *Buena:* "Tengo PostgreSQL con `orders(id, customer_id, order_date, status)` y `order_items(order_id, quantity, unit_price)`.
> Quiero una fila por cliente con el total gastado en pedidos `completado` de 2024, ordenado de mayor a menor. Usa CTE y explica cada paso."

Pide también: "indica los supuestos que hiciste" y "¿qué casos borde podrían romper esta consulta?".

## 3. Los errores típicos del código generado

La IA produce código **que parece correcto**. Estos fallos aparecen una y otra vez:

| Fallo | Cómo detectarlo |
|---|---|
| **JOIN que multiplica filas** (sumas y conteos inflados) | Compara `COUNT(*)` antes y después del JOIN; usa `COUNT(DISTINCT id)` |
| **LEFT JOIN anulado por un WHERE** sobre la tabla derecha | Si esperabas incluir filas sin pareja, la condición va en el `ON` |
| **Nulos ignorados o mal tratados** | Prueba con datos que tengan `None`/`NULL` |
| **Divisiones entre el total equivocado** | Calcula a mano un caso pequeño |
| **Funciones o parámetros inventados** ("alucinaciones") | Busca la función en la documentación oficial |
| **Formatos de fecha intercambiados** (día/mes) | Prueba con una fecha como `2024-01-31` |
| **Orden o empates no definidos** | Revisa el `ORDER BY` y qué pasa con valores iguales |

## 4. Un método para verificar

1. **Lee** el código entero antes de ejecutarlo. Si no entiendes una línea, pregunta qué hace.
2. **Prueba con un caso pequeño** cuyo resultado conoces de antemano (3-5 filas que puedas calcular a mano).
3. **Comprueba totales:** la suma por categorías debe coincidir con el total general; el número de filas debe tener sentido.
4. **Prueba casos borde:** listas vacías, nulos, duplicados, empates, fechas límite.
5. **Compara con otra vía:** resuelve lo mismo en SQL y en pandas, o con otra consulta más simple.
6. **Escribe la prueba** (`assert`) para que el error no vuelva.

## 5. Seguridad y privacidad

- **Nunca** pegues contraseñas, claves de API, datos personales de clientes ni información confidencial en un asistente que tu empresa no haya autorizado.
- Usa **datos de ejemplo o anonimizados** para pedir ayuda: el esquema y 3 filas inventadas bastan.
- Revisa que el código generado no incluya dependencias desconocidas ni comandos peligrosos (borrar tablas, desactivar verificaciones).
- Si conectas un modelo a tus datos (como en un RAG), trata el contenido como **datos, no como instrucciones**.

## 6. Cómo contarlo en una entrevista

"Uso asistentes de IA para acelerar borradores y documentación, pero valido todo con casos de prueba y comprobaciones de totales.
Por ejemplo, una vez detecté que una consulta generada duplicaba pedidos por un JOIN con las líneas de pedido..." Una historia concreta como esa vale mucho.

## Cómo sabes que dominas este tema

- Escribes pedidos con esquema, granularidad y formato esperado.
- Detectas en minutos un JOIN que infla resultados o un LEFT JOIN anulado.
- Tienes un método fijo para verificar cualquier código antes de usarlo.

> En los ejercicios de abajo, el código inicial **lo "generó una IA" y tiene un error**. Tu trabajo es encontrarlo y corregirlo.
""",
        "exercises": [
            sql("ia-sql-1", "Pedidos inflados por un JOIN", "IA asistida: verificar código",
                "Un asistente generó esta consulta para obtener, por canal, el **número de pedidos completados** (`pedidos`) y sus **ingresos** (`ingresos`, 2 decimales). "
                "Los ingresos están bien, pero el número de pedidos sale inflado. Corrígela. Ordena por canal.",
                "SELECT o.channel, COUNT(DISTINCT o.id) AS pedidos, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS ingresos "
                "FROM orders o JOIN order_items oi ON oi.order_id = o.id WHERE o.status = 'completado' "
                "GROUP BY o.channel ORDER BY o.channel",
                starter="-- Consulta generada por IA: tiene un error\nSELECT o.channel,\n       COUNT(*) AS pedidos,\n       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS ingresos\nFROM orders o\nJOIN order_items oi ON oi.order_id = o.id\nWHERE o.status = 'completado'\nGROUP BY o.channel\nORDER BY o.channel",
                ordered=True,
                hint="Tras unir con order_items hay una fila por LÍNEA de pedido, no por pedido. ¿Cómo cuentas pedidos distintos?"),
            sql("ia-sql-2", "El LEFT JOIN que dejó de serlo", "IA asistida: verificar código",
                "Se pidió: **todos los clientes** (`id`, `name`) con cuántos pedidos **completados** tienen (`completados`), mostrando 0 si no tienen ninguno, ordenados por id. "
                "La consulta generada pierde clientes. Corrígela.",
                "SELECT c.id, c.name, COUNT(o.id) AS completados FROM customers c "
                "LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'completado' "
                "GROUP BY c.id, c.name ORDER BY c.id",
                starter="-- Consulta generada por IA: tiene un error\nSELECT c.id, c.name, COUNT(*) AS completados\nFROM customers c\nLEFT JOIN orders o ON o.customer_id = c.id\nWHERE o.status = 'completado'\nGROUP BY c.id, c.name\nORDER BY c.id",
                ordered=True,
                hint="La condición sobre orders en el WHERE descarta los clientes sin pedidos. Muévela al ON y cuenta o.id en lugar de *."),
            py("ia-py-nulos", "Promedio que ignora mal los nulos", "IA asistida: verificar código",
               "Se pidió `promedio_sin_nulos(valores)`: el promedio **ignorando** los `None`; si no queda ningún valor válido, debe devolver `None`. "
               "El código generado da resultados incorrectos. Corrígelo.",
               starter="""
def promedio_sin_nulos(valores):
    # Código generado por IA: tiene un error
    total = sum(v for v in valores if v is not None)
    return total / len(valores)
""",
               solution="""
def promedio_sin_nulos(valores):
    validos = [v for v in valores if v is not None]
    if not validos:
        return None
    return sum(validos) / len(validos)
""",
               tests="""
assert promedio_sin_nulos([10, None, 20]) == 15, "Ignorando el None, el promedio de 10 y 20 es 15"
assert promedio_sin_nulos([None, None]) is None, "Sin valores validos debe devolver None"
assert promedio_sin_nulos([]) is None, "Una lista vacia debe devolver None"
assert promedio_sin_nulos([0, 0]) == 0, "Los ceros si son valores validos"
""",
               hint="Divide entre la cantidad de valores válidos, no entre el total. Y cuida la lista sin valores válidos."),
            py("ia-py-top", "Top productos al revés", "IA asistida: verificar código",
               "Se pidió `top_n(ventas, n)`: `ventas` es un diccionario `{producto: monto}`; devuelve la lista de los `n` productos con **mayor** monto, de mayor a menor, "
               "y en caso de empate por orden alfabético. Corrige el código generado.",
               starter="""
def top_n(ventas, n):
    # Código generado por IA: tiene un error
    return sorted(ventas, key=lambda producto: ventas[producto])[:n]
""",
               solution="""
def top_n(ventas, n):
    return sorted(ventas, key=lambda producto: (-ventas[producto], producto))[:n]
""",
               tests="""
ventas = {"pan": 30, "leche": 50, "cafe": 50, "te": 10}
assert top_n(ventas, 2) == ["cafe", "leche"], "Los dos mayores son cafe y leche (50), empatados -> orden alfabetico"
assert top_n(ventas, 3) == ["cafe", "leche", "pan"]
assert top_n({}, 3) == []
""",
               hint="Ordena por monto descendente y luego por nombre: key=lambda p: (-ventas[p], p)."),
            py("ia-py-fechas", "Formato de fecha intercambiado", "IA asistida: verificar código",
               "Se pidió `dias_entre(inicio, fin)` para fechas en formato `'AAAA-MM-DD'`: devuelve cuántos días hay de `inicio` a `fin`. "
               "El código generado funciona con algunas fechas y falla con otras. Encuentra el error.",
               starter="""
from datetime import datetime

def dias_entre(inicio, fin):
    # Código generado por IA: tiene un error
    a = datetime.strptime(inicio, "%Y-%d-%m")
    b = datetime.strptime(fin, "%Y-%d-%m")
    return (b - a).days
""",
               solution="""
from datetime import datetime

def dias_entre(inicio, fin):
    a = datetime.strptime(inicio, "%Y-%m-%d")
    b = datetime.strptime(fin, "%Y-%m-%d")
    return (b - a).days
""",
               tests="""
assert dias_entre("2024-01-31", "2024-02-01") == 1, "Del 31 de enero al 1 de febrero hay 1 dia"
assert dias_entre("2024-03-01", "2024-03-11") == 10
assert dias_entre("2024-02-28", "2024-03-01") == 2, "2024 es bisiesto: hay 29 de febrero"
""",
               hint="Revisa el formato: %m es el mes y %d el día. Fechas como 2024-03-01 no delatan el error; 2024-01-31 sí."),
            quiz("ia-quiz-alucinacion", "Una función que no existe", "IA asistida: verificar código",
                 "El asistente te propone `df.drop_nulls()` para quitar nulos en pandas y al ejecutarlo obtienes `AttributeError`. ¿Qué haces?",
                 ["Reinstalar pandas", "Comprobar en la documentación oficial: en pandas el método es dropna(); drop_nulls() pertenece a otra librería (Polars)",
                  "Pedirle a la IA que lo arregle sin leer el error", "Abandonar pandas"], 1,
                 "Los asistentes a veces mezclan APIs de librerías parecidas. La documentación oficial es la fuente de verdad."),
            quiz("ia-quiz-privacidad", "Qué no compartir", "IA asistida: verificar código",
                 "Necesitas ayuda con una consulta sobre la tabla de clientes de tu empresa. ¿Qué es lo más adecuado compartir con un asistente público?",
                 ["Un export completo de la tabla con nombres y correos", "El esquema de la tabla y unas pocas filas inventadas",
                  "La cadena de conexión con usuario y contraseña", "Una captura de pantalla del CRM"], 1,
                 "El esquema y datos de ejemplo bastan para obtener ayuda sin exponer información personal ni credenciales."),
            quiz("ia-quiz-verificar", "Verificar una consulta", "IA asistida: verificar código",
                 "Una consulta generada devuelve los ingresos por categoría. ¿Cuál es la comprobación más rápida y útil?",
                 ["Ver que no dé error", "Comprobar que la suma de todas las categorías coincide con el ingreso total calculado por separado",
                  "Ver que los números sean redondos", "Ejecutarla dos veces"], 1,
                 "Que la consulta no falle no significa que sea correcta. Reconciliar totales detecta duplicados y filtros mal aplicados."),
            checklist("ia-check", "Mi flujo de trabajo con IA", "IA asistida: verificar código",
                      "Aplica este flujo en tus próximos 3 ejercicios difíciles (pide ayuda a un asistente y verifica).",
                      ["Escribí un pedido con esquema, granularidad y formato esperado", "Leí y entendí cada línea antes de ejecutarla",
                       "Probé con un caso pequeño calculado a mano", "Probé al menos un caso borde (nulos, vacío, empates)",
                       "Reconcilié totales o comparé con otra solución", "Anoté en Apuntes un error que la IA cometió y cómo lo detecté"]),
        ],
    },
]
