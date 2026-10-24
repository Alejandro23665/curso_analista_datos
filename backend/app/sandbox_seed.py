"""Datos de práctica para el esquema `sandbox`.

Es determinista: el mismo script produce siempre los mismos datos. Usa solo SQL portable
(INTEGER, TEXT, NUMERIC, DATE) para poder validarlo también con SQLite.
Los valores de texto no llevan tildes para evitar errores al escribir las consultas.
"""
import random
from datetime import date, timedelta

SCHEMA_SQL = """
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    segment TEXT NOT NULL,
    signup_date DATE NOT NULL
);
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date DATE NOT NULL,
    status TEXT NOT NULL,
    channel TEXT NOT NULL
);
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL
);
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    title TEXT NOT NULL,
    salary NUMERIC(10,2) NOT NULL,
    hire_date DATE NOT NULL,
    manager_id INTEGER REFERENCES employees(id)
);
"""

PRODUCTS = [
    ("Laptop 14", "Tecnologia", 899.00), ("Auriculares BT", "Tecnologia", 59.90),
    ("Teclado mecanico", "Tecnologia", 89.00), ("Monitor 24", "Tecnologia", 189.00),
    ("Webcam HD", "Tecnologia", 45.50), ("Cargador USB-C", "Tecnologia", 19.99),
    ("Lampara escritorio", "Hogar", 34.50), ("Silla ergonomica", "Hogar", 249.00),
    ("Cafetera", "Hogar", 79.00), ("Juego de sabanas", "Hogar", 42.00),
    ("Aspiradora", "Hogar", 159.00), ("Set de cuchillos", "Hogar", 64.00),
    ("Balon de futbol", "Deportes", 27.00), ("Mancuernas 10kg", "Deportes", 55.00),
    ("Bicicleta urbana", "Deportes", 420.00), ("Esterilla yoga", "Deportes", 22.00),
    ("Zapatillas running", "Deportes", 110.00), ("Botella termica", "Deportes", 18.00),
    ("Novela historica", "Libros", 15.50), ("Manual de SQL", "Libros", 39.90),
    ("Atlas del mundo", "Libros", 48.00), ("Libro de cocina", "Libros", 24.00),
    ("Guia de Python", "Libros", 44.00), ("Diccionario", "Libros", 12.00),
]

EMPLOYEES = [
    (1, "Elena Ortiz", "Direccion", "CEO", 9500, "2018-03-01", None),
    (2, "Marcos Lara", "Ventas", "Director", 6200, "2019-02-15", 1),
    (3, "Patricia Nunez", "Datos", "Director", 6400, "2019-05-20", 1),
    (4, "Hector Salas", "Ingenieria", "Director", 6600, "2018-09-10", 1),
    (5, "Rosa Medina", "Finanzas", "Director", 6100, "2019-07-01", 1),
    (6, "Tomas Rivas", "Ventas", "Ejecutivo", 3200, "2021-01-11", 2),
    (7, "Lucia Paredes", "Ventas", "Ejecutivo", 3200, "2021-06-07", 2),
    (8, "Gabriel Soto", "Ventas", "Ejecutivo", 3500, "2022-02-14", 2),
    (9, "Irene Campos", "Ventas", "Asistente", 2200, "2023-03-20", 2),
    (10, "Nicolas Pardo", "Datos", "Analista", 3800, "2021-08-02", 3),
    (11, "Sara Benitez", "Datos", "Analista", 3800, "2022-01-17", 3),
    (12, "Felipe Cruz", "Datos", "Ingeniero de datos", 4800, "2020-11-09", 3),
    (13, "Alicia Ferrer", "Datos", "Ingeniero de datos", 5100, "2020-04-27", 3),
    (14, "Bruno Aguilar", "Datos", "Analista", 3400, "2023-05-08", 3),
    (15, "Monica Reyes", "Ingenieria", "Desarrollador", 4500, "2021-03-15", 4),
    (16, "Oscar Delgado", "Ingenieria", "Desarrollador", 4500, "2022-07-04", 4),
    (17, "Julia Montes", "Ingenieria", "Desarrollador", 4100, "2023-01-23", 4),
    (18, "Ivan Herrera", "Ingenieria", "DevOps", 5200, "2020-10-12", 4),
    (19, "Natalia Pena", "Finanzas", "Contador", 3300, "2021-09-06", 5),
    (20, "Raul Bravo", "Finanzas", "Contador", 3300, "2022-04-18", 5),
    (21, "Clara Ibarra", "Finanzas", "Analista", 3600, "2023-02-13", 5),
    (22, "Hugo Valdez", "Operaciones", "Coordinador", 3000, "2020-06-22", 2),
    (23, "Eva Navarro", "Operaciones", "Asistente", 2200, "2023-08-28", 22),
    (24, "Dario Fuentes", "Operaciones", "Asistente", 2400, "2024-01-15", 22),
]


def _q(value):
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return repr(value)
    return "'" + str(value).replace("'", "''") + "'"


def _insert(table, rows):
    statements = []
    for i in range(0, len(rows), 100):
        chunk = rows[i:i + 100]
        values = ",\n".join("(" + ", ".join(_q(v) for v in row) + ")" for row in chunk)
        statements.append("INSERT INTO %s VALUES\n%s;" % (table, values))
    return "\n".join(statements)


def _rand_date(rng, start, end):
    return (start + timedelta(days=rng.randint(0, (end - start).days))).isoformat()


def build_sql():
    """Devuelve el script completo (esquema + datos). Se ejecuta con search_path = sandbox."""
    rng = random.Random(2024)
    first = ["Ana", "Luis", "Carla", "Mateo", "Sofia", "Diego", "Valentina", "Andres", "Camila", "Jose",
             "Daniela", "Pedro", "Laura", "Miguel", "Isabella", "Carlos", "Mariana", "Jorge", "Paula", "Ricardo"]
    last = ["Rojas", "Perez", "Gomez", "Diaz", "Torres", "Ramos", "Silva", "Castro", "Mora", "Vega"]
    countries = ["Venezuela", "Colombia", "Mexico", "Argentina", "Chile", "Espana"]
    segments = ["Consumidor", "Pyme", "Corporativo"]

    customers = []
    for i in range(1, 41):
        last_name = last[(i - 1) % 10] if i <= 20 else last[(i + 2) % 10]
        customers.append((
            i, "%s %s" % (first[(i - 1) % 20], last_name), rng.choice(countries), rng.choice(segments),
            _rand_date(rng, date(2023, 1, 1), date(2024, 6, 30)),
        ))

    products = [(i + 1, n, c, p) for i, (n, c, p) in enumerate(PRODUCTS)]

    statuses = ["completado"] * 7 + ["cancelado"] * 2 + ["pendiente"]
    channels = ["web", "app", "tienda"]
    orders, items = [], []
    item_id = 1
    for oid in range(1, 221):
        # Los clientes 35..40 nunca compran; el producto 24 nunca se vende (útil para LEFT JOIN).
        orders.append((oid, rng.randint(1, 34), _rand_date(rng, date(2024, 1, 1), date(2025, 6, 30)),
                       rng.choice(statuses), rng.choice(channels)))
        for pid in rng.sample(range(1, 24), rng.randint(1, 4)):
            items.append((item_id, oid, pid, rng.randint(1, 5), PRODUCTS[pid - 1][2]))
            item_id += 1

    parts = [
        SCHEMA_SQL,
        _insert("customers", customers),
        _insert("products", products),
        _insert("orders", orders),
        _insert("order_items", items),
        _insert("employees", EMPLOYEES),
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    print(build_sql())
