# Bases de datos para aplicaciones: transacciones, concurrencia e índices

Escribir un `SELECT` que funciona es el primer paso. Construir una aplicación que **no pierde dinero, no vende más stock del que hay y no
se vuelve lenta** cuando llegan los usuarios es otro nivel, y es justo lo que diferencia a un backend junior que "sabe SQL" de uno en el
que se puede confiar.

Este capítulo cubre lo que pasa cuando una base de datos la usa una aplicación real: transacciones y ACID, qué ocurre cuando dos usuarios
hacen lo mismo a la vez, cómo evitar las condiciones de carrera, restricciones que protegen los datos, el famoso problema N+1, los índices
y cómo cambiar el esquema sin romper producción.

---

## 1. Transacciones: todo o nada

Una **transacción** agrupa varias operaciones para que se ejecuten **todas o ninguna**. El ejemplo clásico es una transferencia:

```sql
BEGIN;
UPDATE cuentas SET saldo = saldo - 100 WHERE id = 1;   -- restar al origen
UPDATE cuentas SET saldo = saldo + 100 WHERE id = 2;   -- sumar al destino
COMMIT;
```

Si el servidor se cae entre las dos sentencias **sin** transacción, desaparecen 100 del sistema. Con la transacción, si algo falla antes
del `COMMIT`, se hace `ROLLBACK` y la base queda **exactamente como estaba**.

### ACID

Las cuatro garantías de una transacción:

| Letra | Propiedad | Significado |
|---|---|---|
| **A** | Atomicidad | Todo o nada |
| **C** | Consistencia | Al terminar se cumplen todas las reglas (restricciones, claves foráneas) |
| **I** | Aislamiento | Las transacciones simultáneas no se ven a medias unas a otras |
| **D** | Durabilidad | Lo confirmado sobrevive a un corte de luz |

### Atomicidad en tu propio código

La misma idea se aplica fuera de la base de datos, en cualquier función que modifica varias cosas. El principio: **valida todo primero y
modifica después**. Si validas a mitad de las modificaciones, un error deja el estado a medias.

Ejemplo con la reserva de varios asientos de un evento:

```python
def reservar(asientos_libres, pedidos):
    """asientos_libres: set de asientos; pedidos: lista de asientos a reservar."""
    # 1) Validar TODO antes de tocar nada
    if not pedidos:
        raise ValueError("No hay asientos que reservar")
    if len(set(pedidos)) != len(pedidos):
        raise ValueError("Asientos repetidos en la petición")
    no_disponibles = [a for a in pedidos if a not in asientos_libres]
    if no_disponibles:
        raise ValueError(f"No disponibles: {no_disponibles}")

    # 2) Solo ahora, modificar
    for a in pedidos:
        asientos_libres.remove(a)
```

Si el asiento 3 de 4 no estuviera libre y hubieras ido quitando asientos dentro del bucle, los dos primeros quedarían reservados sin que
la operación se completara. Piensa también en los casos "raros" que el negocio no permite: cantidades cero o negativas, el mismo elemento
dos veces, referencias que no existen.

### Transacciones con SQLAlchemy

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    with session.begin():              # COMMIT al salir del bloque; ROLLBACK si hay una excepción
        origen = session.get(Cuenta, 1)
        destino = session.get(Cuenta, 2)
        origen.saldo -= 100
        destino.saldo += 100
```

---

## 2. Concurrencia: cuando dos usuarios hacen lo mismo a la vez

En una aplicación web, cientos de peticiones se ejecutan **al mismo tiempo**. Queda una unidad de un producto y dos clientes pulsan
"Comprar" a la vez:

```
Cliente A: SELECT stock FROM productos WHERE id = 7;   → 1
Cliente B: SELECT stock FROM productos WHERE id = 7;   → 1
Cliente A: (1 > 0, puede comprar) UPDATE productos SET stock = 0 WHERE id = 7;
Cliente B: (1 > 0, puede comprar) UPDATE productos SET stock = 0 WHERE id = 7;
→ Se vendieron 2 unidades con 1 en stock.
```

Esto es una **condición de carrera** (*race condition*): el resultado depende del orden en que se intercalan las operaciones. El patrón
peligroso es **leer, decidir en el código y escribir** en pasos separados: entre la lectura y la escritura, otro puede cambiar el dato.

### Solución 1: actualización condicional y atómica

Hacer la comprobación **dentro** de la misma sentencia de escritura:

```sql
UPDATE productos
SET stock = stock - 1
WHERE id = 7 AND stock >= 1;
```

La base de datos garantiza que cada `UPDATE` sobre una fila se aplica de forma atómica. Si dos llegan a la vez, el segundo ve el stock ya
en 0, la condición `stock >= 1` no se cumple y **no modifica ninguna fila**. Tu código comprueba cuántas filas cambiaron (`rowcount`): si
es 0, no había stock. No bloquea la tabla y es la solución más simple para contadores (stock, cupos, saldos).

### Solución 2: bloqueo pesimista

Bloquear la fila al leerla, para que nadie más pueda modificarla hasta que termines:

```sql
BEGIN;
SELECT stock FROM productos WHERE id = 7 FOR UPDATE;   -- los demás esperan aquí
-- lógica de negocio compleja...
UPDATE productos SET stock = stock - 1 WHERE id = 7;
COMMIT;
```

Útil cuando la lógica entre la lectura y la escritura es compleja. Inconveniente: los demás **esperan**, y si las transacciones se
bloquean en orden distinto pueden producirse **interbloqueos** (*deadlocks*).

### Solución 3: bloqueo optimista con versiones

Para ediciones donde los conflictos son raros (dos administradores editando la misma ficha de producto), en lugar de bloquear se
**detecta** el conflicto. Cada fila tiene una columna `version`:

1. Al leer, guardas la versión que viste (por ejemplo, 5).
2. Al guardar, actualizas **solo si la versión sigue siendo la que viste**, y la incrementas:

```sql
UPDATE productos
SET precio = 89.90, version = version + 1
WHERE id = 7 AND version = 5;
```

3. Si cambió 0 filas, alguien guardó antes que tú: hay un **conflicto**. Se avisa al usuario ("otra persona modificó este producto;
   recarga para ver los cambios") en vez de pisar su trabajo en silencio.

Detalles de diseño importantes:

- El número de versión lo gestiona **el sistema**, nunca el usuario: si se aceptara un cambio de `version` dentro de los datos editados,
  alguien podría saltarse la comprobación.
- El conflicto se señala con un error **específico** (en Python, una clase de excepción propia, como las que viste en el capítulo de
  Python profesional), para que el código que llama pueda distinguirlo de otros errores y responder un `409 Conflict`.
- En el código, conviene que la función que aplica los cambios **no modifique el objeto original**, sino que devuelva uno nuevo: así, si
  algo falla, el original sigue intacto. En Python, `{**original, **cambios}` crea un diccionario nuevo combinando los dos.

| Técnica | Cuándo |
|---|---|
| `UPDATE ... WHERE condición` | Contadores: stock, cupos, saldos |
| `SELECT ... FOR UPDATE` | Lógica compleja con conflictos frecuentes |
| Versión (optimista) | Ediciones de usuarios con conflictos raros |

---

## 3. Restricciones: que la base proteja los datos

El código de la aplicación tiene errores; la base de datos es la **última línea de defensa**. Las restricciones (*constraints*) impiden
que entren datos inválidos, venga de donde venga el error:

```sql
CREATE TABLE productos (
    id        SERIAL PRIMARY KEY,
    sku       TEXT NOT NULL UNIQUE,                       -- no puede repetirse
    nombre    TEXT NOT NULL,
    precio    NUMERIC(12, 2) NOT NULL CHECK (precio >= 0),
    stock     INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),  -- nunca negativo
    categoria_id INTEGER NOT NULL REFERENCES categorias(id)
);
```

| Restricción | Garantiza |
|---|---|
| `PRIMARY KEY` | Identificador único y no nulo |
| `NOT NULL` | El campo siempre tiene valor |
| `UNIQUE` | No hay dos filas con el mismo valor (correos, SKU) |
| `CHECK` | Una condición de negocio (precio no negativo, fechas coherentes) |
| `REFERENCES` (clave foránea) | La fila referenciada existe |

Con `CHECK (stock >= 0)`, aunque tu código tenga una condición de carrera, la base **rechaza** la venta que dejaría el stock negativo.

Un uso muy práctico de `UNIQUE`: la **idempotencia**. Si un cliente pulsa "Pagar" dos veces o la red reintenta la petición, una clave
única sobre un identificador de la operación (`idempotency_key`) impide que se registre dos veces.

### Tipos de datos: el dinero

**Nunca uses `FLOAT` para dinero.** Los números de coma flotante no representan exactamente valores como 0.1:

```python
0.1 + 0.2          # 0.30000000000000004
```

Usa `NUMERIC(12, 2)` (decimal exacto) en la base y `Decimal` en Python, o guarda **enteros en centavos** (`1999` = 19,99). Otros tipos
bien elegidos: `TIMESTAMPTZ` para fechas con hora (con zona horaria), `BOOLEAN`, `UUID` para identificadores públicos, `JSONB` para datos
semiestructurados.

---

## 4. El problema N+1

Es el problema de rendimiento más común en aplicaciones con ORM. Quieres mostrar una lista de clientes con su número de pedidos:

```python
clientes = session.query(Cliente).all()              # 1 consulta
for c in clientes:
    n = session.query(Pedido).filter_by(cliente_id=c.id).count()   # 1 consulta POR CLIENTE
```

Con 500 clientes, son **501 consultas**. Cada una tarda poco, pero cada viaje de ida y vuelta a la base cuesta (más aún si la base está
en otro servidor): la página tarda segundos. Se llama N+1 porque haces 1 consulta para la lista y N más, una por elemento.

Se detecta activando el registro de las consultas SQL (en SQLAlchemy, `echo=True`) y viendo la misma consulta repetida con distintos ids.

### La solución: que la base haga el trabajo en una consulta

Ejemplo con productos: cuántas veces se vendió cada libro.

```sql
SELECT p.id, p.name,
       COUNT(oi.id)                AS lineas,
       COALESCE(SUM(oi.quantity), 0) AS unidades
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.id
WHERE p.category = 'Libros'
GROUP BY p.id, p.name
ORDER BY p.id;
```

| id | name | lineas | unidades |
|---|---|---|---|
| 19 | Novela historica | 22 | 78 |
| 20 | Manual de SQL | 24 | 73 |
| 21 | Atlas del mundo | 27 | 81 |
| 22 | Libro de cocina | 20 | 59 |
| 23 | Guia de Python | 26 | 70 |
| 24 | Diccionario | 0 | 0 |

Tres detalles que hacen correcta esta consulta:

1. **`LEFT JOIN`**, no `JOIN`: el Diccionario no se ha vendido nunca. Con un `JOIN` normal desaparecería de la lista; con `LEFT JOIN`
   aparece con los campos de `order_items` a `NULL`.
2. **`COUNT(oi.id)`**, no `COUNT(*)`: `COUNT(*)` cuenta filas, y la fila del Diccionario existe (con nulos), así que daría **1**.
   `COUNT(columna)` ignora los nulos y da **0**. Es un error muy frecuente.
3. **`COALESCE(SUM(...), 0)`**: la suma de ningún valor es `NULL`; `COALESCE` la convierte en 0.

El filtro de la tabla principal (`p.category = 'Libros'`) va en el `WHERE`. Ojo: un filtro sobre la tabla del lado derecho de un
`LEFT JOIN` puesto en el `WHERE` eliminaría las filas sin pareja; si hace falta, va en la condición del `ON`.

### En el ORM

Los ORM ofrecen **carga anticipada** (*eager loading*) para traer las relaciones en una o dos consultas:

```python
from sqlalchemy.orm import selectinload

clientes = session.scalars(
    select(Cliente).options(selectinload(Cliente.pedidos))   # 2 consultas en total, no N+1
).all()
```

Y para conteos o sumas, mejor una consulta agregada como la de arriba que cargar todos los objetos.

---

## 5. Índices

Sin índice, para encontrar los pedidos de un cliente la base **lee toda la tabla** (*sequential scan*). Con millones de filas, eso son
segundos. Un **índice** es una estructura ordenada (normalmente un árbol B) que permite saltar directamente a las filas buscadas, como el
índice alfabético de un libro.

```sql
CREATE INDEX idx_pedidos_cliente ON pedidos (cliente_id);
```

### Cuándo crear un índice

- Columnas de las **claves foráneas** (PostgreSQL no las indexa automáticamente) y columnas que aparecen a menudo en `WHERE`, `JOIN` y
  `ORDER BY`.
- Las claves primarias y las columnas `UNIQUE` ya tienen índice.
- **No indexes todo**: cada índice ocupa espacio y **hace más lentas las escrituras** (cada `INSERT` y `UPDATE` debe actualizarlo).

### Índices compuestos y el orden de las columnas

Un índice sobre `(cliente_id, created_at)` está ordenado **primero por cliente y, dentro de cada cliente, por fecha**, como una guía
telefónica ordenada por apellido y luego por nombre.

| Consulta | ¿Aprovecha el índice? |
|---|---|
| `WHERE cliente_id = 5` | Sí (usa la primera columna) |
| `WHERE cliente_id = 5 AND created_at > '2026-01-01'` | Sí, perfectamente |
| `WHERE cliente_id = 5 ORDER BY created_at DESC` | Sí: los datos ya están en ese orden |
| `WHERE created_at > '2026-01-01'` (sin cliente) | **No bien**: es como buscar por nombre de pila en una guía ordenada por apellido |

La regla: un índice compuesto sirve para consultas que usan sus columnas **empezando por la izquierda**.

### Comprobar con EXPLAIN

```sql
EXPLAIN ANALYZE
SELECT * FROM pedidos WHERE cliente_id = 5;
```

Muestra el plan que usa la base y el tiempo real. Busca `Seq Scan` (lee toda la tabla) frente a `Index Scan` (usa un índice). Mide
**antes y después** de crear un índice: con tablas pequeñas, la base puede preferir leer todo, y está bien.

Cosas que impiden usar un índice: aplicar una función a la columna (`WHERE LOWER(email) = ...` no usa un índice sobre `email`; harías un
índice sobre `LOWER(email)`), y `LIKE '%texto'` con el comodín al principio.

---

## 6. Migraciones: cambiar el esquema sin romper nada

El esquema de la base evoluciona con la aplicación: nuevas columnas, nuevas tablas, cambios de tipo. Las **migraciones** son scripts
versionados que aplican esos cambios en orden, en todos los entornos. En Python, la herramienta estándar con SQLAlchemy es **Alembic**:

```
alembic revision --autogenerate -m "añadir columna telefono a clientes"
alembic upgrade head
```

Reglas:

- Las migraciones van en **Git** con el código y **nunca se editan** una vez aplicadas en producción: se crea una nueva.
- **Revisa** lo que genera `--autogenerate`: no detecta todo (por ejemplo, los renombrados los ve como borrar y crear, perdiendo datos).
- **Cambios compatibles** en producción: para renombrar una columna sin cortar el servicio, se hace en pasos (añadir la nueva, copiar los
  datos, cambiar el código para usar la nueva, y borrar la antigua más tarde). Añadir una columna `NOT NULL` a una tabla grande exige un
  valor por defecto.
- **Copia de seguridad** antes de migraciones arriesgadas, y prueba la migración con una copia de los datos reales.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Transacción | Todo o nada; ACID |
| Atomicidad en código | Validar todo primero, modificar después |
| Condición de carrera | Leer, decidir y escribir por separado es peligroso |
| `UPDATE ... WHERE` | Comprobación y escritura en una sentencia; mirar las filas afectadas |
| Bloqueo pesimista | `SELECT ... FOR UPDATE`; cuidado con los interbloqueos |
| Bloqueo optimista | Columna `version`; 0 filas = conflicto; la versión la gestiona el sistema |
| Restricciones | `NOT NULL`, `UNIQUE`, `CHECK`, claves foráneas: la última defensa |
| Dinero | `NUMERIC` o centavos enteros; nunca `FLOAT` |
| N+1 | Una consulta por elemento; solución: `JOIN` + agregación o carga anticipada |
| `LEFT JOIN` + conteo | `COUNT(columna)` y `COALESCE` para que los sin pareja den 0 |
| Índices | En claves foráneas y filtros frecuentes; compuestos de izquierda a derecha; `EXPLAIN` |
| Migraciones | Versionadas, nunca editadas, compatibles hacia atrás |

## Autoevaluación final

1. ¿Qué garantiza la atomicidad de una transacción?
2. ¿Por qué hay que validar todas las condiciones antes de empezar a modificar el estado?
3. Explica la condición de carrera de "leer el stock y luego actualizarlo".
4. ¿Cómo sabes, tras un `UPDATE ... WHERE id = 7 AND stock >= 1`, si la venta se realizó?
5. En el bloqueo optimista, ¿qué significa que el `UPDATE ... WHERE version = 5` cambie 0 filas?
6. ¿Por qué no se debe permitir que el usuario envíe un nuevo valor de `version`?
7. ¿Qué restricción impediría el stock negativo aunque el código tenga un error?
8. Tu página de clientes hace 301 consultas. ¿Cómo se llama el problema y cómo se arregla?
9. Con `LEFT JOIN`, un cliente sin pedidos aparece con `COUNT(*) = 1`. ¿Por qué y cómo se corrige?
10. Tienes un índice en `(cliente_id, created_at)`. ¿Sirve para `WHERE created_at > '2026-01-01'`?

**Respuestas:** 1) Que se aplican todas las operaciones o ninguna. 2) Para no dejar el estado a medias si una condición falla después
de haber cambiado algo. 3) Dos peticiones leen el mismo stock antes de que ninguna escriba; las dos deciden que pueden vender y se vende de
más. 4) Por el número de filas afectadas: 1 si se vendió, 0 si no había stock. 5) Que otra persona guardó antes (la versión ya no es 5):
es un conflicto. 6) Porque podría saltarse la comprobación de conflictos; la versión la incrementa el sistema. 7) `CHECK (stock >= 0)`.
8) N+1; con una consulta con `JOIN` y agregación, o con carga anticipada en el ORM. 9) Porque `COUNT(*)` cuenta la fila con nulos que
genera el `LEFT JOIN`; se usa `COUNT(columna_de_la_tabla_derecha)`. 10) No bien: el índice está ordenado primero por cliente.
