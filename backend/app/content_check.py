"""Valida el currículo: estructura, soluciones de Python y consultas SQL (con SQLite).

Uso (desde la carpeta backend):   python -m app.content_check
Las consultas marcadas pg_only=True usan funciones propias de PostgreSQL y se validan aparte.
"""
import importlib.util
import io
import sqlite3
import sys
import traceback
from contextlib import redirect_stdout

from . import content
from .sandbox_seed import build_sql

KINDS = {"sql", "python", "quiz", "checklist"}
errors, warnings = [], []


def run_python(code, tests):
    ns = {"__name__": "__main__"}
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            exec(compile(code, "<codigo>", "exec"), ns)
            exec(compile(tests, "<pruebas>", "exec"), ns)
        return True, ""
    except AssertionError as exc:
        return False, "AssertionError: %s" % exc
    except BaseException:
        return False, traceback.format_exc(limit=-2)


def main():
    slugs, ids = set(), set()
    conn = sqlite3.connect(":memory:")
    conn.executescript(build_sql())
    phases = {p["slug"] for p in content.PHASES}
    checked = {"python": 0, "sql": 0, "quiz": 0, "checklist": 0}
    skipped = []

    for topic in content.TOPICS:
        slug = topic["slug"]
        if slug in slugs:
            errors.append("slug duplicado: " + slug)
        slugs.add(slug)
        if topic["phase"] not in phases:
            errors.append("%s: fase desconocida %s" % (slug, topic["phase"]))
        if len(topic["theory"].split()) < 150:
            errors.append("%s: teoría demasiado corta" % slug)
        if not topic["exercises"]:
            errors.append("%s: sin ejercicios" % slug)

        for ex in topic["exercises"]:
            eid = ex["id"]
            if eid in ids:
                errors.append("id duplicado: " + eid)
            ids.add(eid)
            if ex["kind"] not in KINDS:
                errors.append("%s: tipo inválido" % eid)
                continue
            checked[ex["kind"]] += 1

            if ex["kind"] == "quiz":
                if not (0 <= ex["answer"] < len(ex["options"])) or len(ex["options"]) < 2:
                    errors.append("%s: quiz mal formado" % eid)
            elif ex["kind"] == "checklist":
                if len(ex["items"]) < 2:
                    errors.append("%s: checklist muy corta" % eid)
            elif ex["kind"] == "sql":
                if ex["pg_only"]:
                    skipped.append(eid)
                    continue
                try:
                    cur = conn.execute(ex["solution"])
                    rows = cur.fetchall()
                    if not rows:
                        errors.append("%s: la solución no devuelve filas" % eid)
                except Exception as exc:
                    errors.append("%s: la solución SQL falla en SQLite: %s" % (eid, exc))
            else:  # python
                missing = [p for p in ex["packages"] if importlib.util.find_spec(p) is None]
                if missing:
                    skipped.append("%s (falta %s)" % (eid, ",".join(missing)))
                    continue
                ok, msg = run_python(ex["solution"], ex["tests"])
                if not ok:
                    errors.append("%s: la solución NO pasa sus pruebas -> %s" % (eid, msg))
                ok, _ = run_python(ex["starter"], ex["tests"])
                if ok:
                    errors.append("%s: el código inicial ya pasa las pruebas (debería fallar)" % eid)

    print("Temas: %d | ejercicios: %s" % (len(content.TOPICS), checked))
    if skipped:
        print("No verificados aquí (%d): %s" % (len(skipped), ", ".join(skipped)))
    if errors:
        print("\nERRORES (%d):" % len(errors))
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("Currículo OK")


if __name__ == "__main__":
    main()
