"""Ejecución segura de las consultas SQL de práctica.

Las consultas del alumno se ejecutan con un rol de solo lectura (`sandbox_ro`) que únicamente ve
el esquema `sandbox`, con transacciones de solo lectura y un límite de tiempo. Así, aunque la app
se despliegue en un servidor, el alumno no puede tocar sus propias tablas de progreso.
"""
import logging
import re
from datetime import date, datetime
from decimal import Decimal

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo
from sqlalchemy.engine import make_url

from .config import DATABASE_URL, SANDBOX_DB_PASSWORD
from .sandbox_seed import build_sql

log = logging.getLogger("datapath.sandbox")

SANDBOX_ROLE = "sandbox_ro"
DISPLAY_ROWS = 200
CHECK_ROWS = 5000
STATEMENT_TIMEOUT = "5s"
_use_role = False


class SandboxError(Exception):
    """Error mostrado al alumno (sintaxis, permisos, etc.)."""


def _conninfo(user=None, password=None) -> str:
    """Cadena de conexión de libpq, conservando parámetros como sslmode (necesario en Neon/Supabase)."""
    u = make_url(DATABASE_URL)
    params = {key: (value[-1] if isinstance(value, tuple) else value) for key, value in u.query.items()}
    params.update(host=u.host, port=u.port, dbname=u.database,
                  user=user or u.username, password=password if user else u.password)
    return make_conninfo(**{key: value for key, value in params.items() if value is not None})


def _admin_conninfo() -> str:
    return _conninfo()


def init_sandbox() -> None:
    """Crea el esquema `sandbox` con datos (solo la primera vez) y el rol de solo lectura."""
    global _use_role
    with psycopg.connect(_admin_conninfo(), autocommit=True, prepare_threshold=None) as conn:
        exists = conn.execute("SELECT to_regclass('sandbox.employees')").fetchone()[0]
        if exists is None:
            log.info("Creando esquema sandbox con datos de práctica...")
            # Todo en una transacción: es atómico y SET LOCAL funciona también tras un PgBouncer.
            with conn.transaction():
                conn.execute("DROP SCHEMA IF EXISTS sandbox CASCADE")
                conn.execute("CREATE SCHEMA sandbox")
                conn.execute("SET LOCAL search_path TO sandbox")
                for statement in build_sql().split(";\n"):
                    if statement.strip():
                        conn.execute(statement)
        try:
            role_exists = conn.execute(
                "SELECT 1 FROM pg_roles WHERE rolname = %s", (SANDBOX_ROLE,)
            ).fetchone()
            action = "ALTER ROLE {} WITH LOGIN PASSWORD {}" if role_exists else "CREATE ROLE {} LOGIN PASSWORD {}"
            conn.execute(sql.SQL(action).format(sql.Identifier(SANDBOX_ROLE), sql.Literal(SANDBOX_DB_PASSWORD)))
            conn.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
                sql.Identifier(conn.info.dbname), sql.Identifier(SANDBOX_ROLE)))
            conn.execute(sql.SQL("GRANT USAGE ON SCHEMA sandbox TO {}").format(sql.Identifier(SANDBOX_ROLE)))
            conn.execute(sql.SQL("GRANT SELECT ON ALL TABLES IN SCHEMA sandbox TO {}").format(
                sql.Identifier(SANDBOX_ROLE)))
            _use_role = True
        except psycopg.Error as exc:
            _use_role = False
            log.warning("No se pudo crear el rol %s (%s). Se usará una conexión de solo lectura "
                        "con el usuario principal.", SANDBOX_ROLE, exc)


def _connect() -> psycopg.Connection:
    info = _conninfo(SANDBOX_ROLE, SANDBOX_DB_PASSWORD) if _use_role else _admin_conninfo()
    return psycopg.connect(info, autocommit=True, prepare_threshold=None)


_FIRST_WORD = re.compile(r"^(select|with)\b", re.IGNORECASE)


def prepare(query: str) -> str:
    """Quita comentarios y valida que sea una única consulta de lectura."""
    text = re.sub(r"/\*.*?\*/", " ", query or "", flags=re.DOTALL)
    text = re.sub(r"--[^\n]*", " ", text).strip().rstrip(";").strip()
    if not text:
        raise SandboxError("Escribe una consulta primero.")
    if not _FIRST_WORD.match(text):
        raise SandboxError("Aquí solo se permiten consultas de lectura: empieza con SELECT (o WITH ... SELECT).")
    if ";" in text:
        raise SandboxError("Ejecuta una sola consulta a la vez (quita los ';' intermedios).")
    return text


def _json_value(value):
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return value if value == value else None
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, datetime):
        if (value.hour, value.minute, value.second, value.microsecond) == (0, 0, 0, 0):
            return value.date().isoformat()
        return value.replace(tzinfo=None).isoformat(sep=" ")
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _error_message(exc: psycopg.Error) -> str:
    diag = getattr(exc, "diag", None)
    return (getattr(diag, "message_primary", None) or str(exc)).strip()


def run_query(query: str, max_rows: int = DISPLAY_ROWS) -> dict:
    text = prepare(query)
    try:
        with _connect() as conn, conn.transaction():
            # Transacción de solo lectura, limitada al esquema sandbox y con tiempo máximo.
            conn.execute("SET TRANSACTION READ ONLY")
            conn.execute("SET LOCAL search_path TO sandbox")
            conn.execute("SET LOCAL statement_timeout = '%s'" % STATEMENT_TIMEOUT)
            cur = conn.execute(text)
            if cur.description is None:
                raise SandboxError("La consulta no devolvió columnas.")
            columns = [c.name for c in cur.description]
            fetched = cur.fetchmany(max_rows + 1)
    except psycopg.Error as exc:
        raise SandboxError(_error_message(exc)) from None
    return {
        "columns": columns,
        "rows": [[_json_value(v) for v in row] for row in fetched[:max_rows]],
        "truncated": len(fetched) > max_rows,
    }


def _norm(value):
    if value is None or isinstance(value, (bool, str)):
        return value
    if isinstance(value, (int, float)):
        return round(float(value), 2)
    return str(value)


def compare(got: dict, expected: dict, ordered: bool = False):
    """Compara dos resultados (columnas por posición, números a 2 decimales)."""
    if len(got["columns"]) != len(expected["columns"]):
        return False, "Tu resultado tiene %d columna(s); se esperaban %d." % (
            len(got["columns"]), len(expected["columns"]))
    got_rows = [tuple(_norm(v) for v in row) for row in got["rows"]]
    exp_rows = [tuple(_norm(v) for v in row) for row in expected["rows"]]
    if len(got_rows) != len(exp_rows):
        return False, "Tu consulta devolvió %d fila(s); se esperaban %d." % (len(got_rows), len(exp_rows))
    same_set = sorted(got_rows, key=repr) == sorted(exp_rows, key=repr)
    if ordered:
        if got_rows == exp_rows:
            return True, "¡Correcto!"
        if same_set:
            return False, "Los datos son correctos, pero el orden no es el que pide el enunciado."
    elif same_set:
        return True, "¡Correcto!"
    return False, "El número de filas coincide, pero los valores no. Revisa filtros, agrupaciones y columnas."


def schema() -> list:
    result = run_query(
        "SELECT table_name, column_name, data_type FROM information_schema.columns "
        "WHERE table_schema = 'sandbox' ORDER BY table_name, ordinal_position",
        max_rows=500,
    )
    tables = {}
    for table, column, data_type in result["rows"]:
        tables.setdefault(table, []).append({"name": column, "type": data_type})
    return [{"name": name, "columns": cols} for name, cols in tables.items()]
