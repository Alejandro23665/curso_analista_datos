"""Pruebas de la lógica pura (no necesitan base de datos).

Ejecutar desde la carpeta backend:   python -m unittest discover -s tests -v
Si psycopg/sqlalchemy no están instalados, se simulan para poder probar igualmente.
"""
import sqlite3
import sys
import types
import unittest
from datetime import date, datetime
from decimal import Decimal

try:  # pragma: no cover
    import psycopg  # noqa: F401
    import sqlalchemy  # noqa: F401
except ImportError:  # pragma: no cover
    psycopg = types.ModuleType("psycopg")
    psycopg.Error = Exception
    psycopg.Connection = object
    psycopg_sql = types.ModuleType("psycopg.sql")
    psycopg_conninfo = types.ModuleType("psycopg.conninfo")
    psycopg_conninfo.make_conninfo = lambda *a, **k: ""
    psycopg.sql = psycopg_sql
    psycopg.conninfo = psycopg_conninfo
    sqlalchemy = types.ModuleType("sqlalchemy")
    sa_engine = types.ModuleType("sqlalchemy.engine")
    sa_engine.make_url = lambda url: None
    sys.modules.update({
        "psycopg": psycopg, "psycopg.sql": psycopg_sql, "psycopg.conninfo": psycopg_conninfo,
        "sqlalchemy": sqlalchemy, "sqlalchemy.engine": sa_engine,
    })

from app import content, sandbox  # noqa: E402
from app.sandbox_seed import build_sql  # noqa: E402


class PrepareTests(unittest.TestCase):
    def test_quita_comentarios_y_punto_y_coma(self):
        self.assertEqual(sandbox.prepare("-- hola\nSELECT 1; "), "SELECT 1")
        self.assertEqual(sandbox.prepare("/* x */ select 1"), "select 1")

    def test_acepta_with(self):
        self.assertTrue(sandbox.prepare("WITH a AS (SELECT 1) SELECT * FROM a").startswith("WITH"))

    def test_rechaza_escrituras(self):
        for query in ("DROP TABLE orders", "DELETE FROM orders", "INSERT INTO x VALUES (1)", "UPDATE x SET a = 1"):
            with self.assertRaises(sandbox.SandboxError):
                sandbox.prepare(query)

    def test_rechaza_varias_consultas(self):
        with self.assertRaises(sandbox.SandboxError):
            sandbox.prepare("SELECT 1; DROP TABLE orders")

    def test_rechaza_vacia(self):
        with self.assertRaises(sandbox.SandboxError):
            sandbox.prepare("   -- solo comentario")


class CompareTests(unittest.TestCase):
    def res(self, rows, columns=("a", "b")):
        return {"columns": list(columns), "rows": rows}

    def test_sin_orden_ignora_el_orden_de_filas(self):
        ok, _ = sandbox.compare(self.res([[1, "x"], [2, "y"]]), self.res([[2, "y"], [1, "x"]]), ordered=False)
        self.assertTrue(ok)

    def test_con_orden_detecta_orden_incorrecto(self):
        ok, msg = sandbox.compare(self.res([[1, "x"], [2, "y"]]), self.res([[2, "y"], [1, "x"]]), ordered=True)
        self.assertFalse(ok)
        self.assertIn("orden", msg)

    def test_numeros_enteros_y_decimales_equivalentes(self):
        ok, _ = sandbox.compare(self.res([[5, 1.001]]), self.res([[5.0, 1.0]]), ordered=True)
        self.assertTrue(ok)

    def test_columnas_y_filas_distintas(self):
        ok, msg = sandbox.compare(self.res([[1]], ("a",)), self.res([[1, 2]]), ordered=False)
        self.assertFalse(ok)
        self.assertIn("columna", msg)
        ok, msg = sandbox.compare(self.res([[1, 2]]), self.res([[1, 2], [3, 4]]), ordered=False)
        self.assertFalse(ok)
        self.assertIn("fila", msg)

    def test_nulos(self):
        ok, _ = sandbox.compare(self.res([[None, 1]]), self.res([[None, 1]]), ordered=True)
        self.assertTrue(ok)


class JsonValueTests(unittest.TestCase):
    def test_conversiones(self):
        self.assertEqual(sandbox._json_value(Decimal("3.00")), 3)
        self.assertEqual(sandbox._json_value(Decimal("3.25")), 3.25)
        self.assertEqual(sandbox._json_value(date(2024, 1, 5)), "2024-01-05")
        self.assertEqual(sandbox._json_value(datetime(2024, 1, 5)), "2024-01-05")
        self.assertEqual(sandbox._json_value(datetime(2024, 1, 5, 13, 30)), "2024-01-05 13:30:00")
        self.assertIsNone(sandbox._json_value(None))


class SeedTests(unittest.TestCase):
    def test_datos_esperados(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(build_sql())
        count = lambda t: conn.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
        self.assertEqual((count("customers"), count("products"), count("orders"), count("employees")), (40, 24, 220, 24))
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM customers WHERE id > 34 AND id NOT IN (SELECT customer_id FROM orders)").fetchone()[0], 6)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM order_items WHERE product_id = 24").fetchone()[0], 0)

    def test_es_determinista(self):
        self.assertEqual(build_sql(), build_sql())


class ContentTests(unittest.TestCase):
    def test_ids_unicos_y_tipos(self):
        ids = [ex["id"] for t in content.TOPICS for ex in t["exercises"]]
        self.assertEqual(len(ids), len(set(ids)))
        slugs = [t["slug"] for t in content.TOPICS]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_no_se_filtra_la_respuesta_del_quiz(self):
        quiz = next(ex for t in content.TOPICS for ex in t["exercises"] if ex["kind"] == "quiz")
        self.assertNotIn("answer", content.public_exercise(quiz))
        self.assertIn("explanation", content.public_exercise(quiz))

    def test_cada_tema_pertenece_a_una_fase(self):
        phases = {p["slug"] for p in content.PHASES}
        self.assertTrue(all(t["phase"] in phases for t in content.TOPICS))


if __name__ == "__main__":
    unittest.main()


class ConfigAndAuthTests(unittest.TestCase):
    def test_normaliza_url_de_neon_y_vercel(self):
        import importlib
        import os
        from app import config
        previous = {k: os.environ.get(k) for k in ("DATABASE_URL", "DATABASE_URL_UNPOOLED")}
        try:
            os.environ.pop("DATABASE_URL_UNPOOLED", None)
            os.environ["DATABASE_URL"] = "postgres://u:p@host.neon.tech/db?sslmode=require"
            self.assertEqual(importlib.reload(config).DATABASE_URL, "postgresql+psycopg://u:p@host.neon.tech/db?sslmode=require")
            os.environ["DATABASE_URL_UNPOOLED"] = "postgresql://u:p@direct.neon.tech/db"
            self.assertEqual(importlib.reload(config).DATABASE_URL, "postgresql+psycopg://u:p@direct.neon.tech/db")
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
            importlib.reload(config)

    def test_sesion_con_contrasena(self):
        from app import auth
        original = auth.APP_PASSWORD
        try:
            auth.APP_PASSWORD = ""
            self.assertTrue(auth.is_authenticated(None), "Sin contraseña configurada no se pide acceso")
            auth.APP_PASSWORD = "secreta"
            self.assertFalse(auth.is_authenticated(None))
            self.assertFalse(auth.is_authenticated("cookie-falsa"))
            self.assertTrue(auth.is_authenticated(auth.session_token()))
            self.assertTrue(auth.check_password("secreta"))
            self.assertFalse(auth.check_password("otra"))
            self.assertFalse(auth.check_password("ñandú"), "No debe fallar con caracteres no ASCII")
        finally:
            auth.APP_PASSWORD = original
