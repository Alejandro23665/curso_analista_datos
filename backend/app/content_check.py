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

    # Rutas: cada tema debe existir y pertenecer al menos a una ruta
    en_alguna_ruta = set()
    for track in content.TRACKS:
        vistos = content.track_topic_slugs(track)
        if len(vistos) != len(set(vistos)):
            errors.append("ruta %s: tema repetido" % track["slug"])
        for slug in vistos:
            if content.get_topic(slug) is None:
                errors.append("ruta %s: el tema %s no existe" % (track["slug"], slug))
        en_alguna_ruta.update(vistos)
    for slug in slugs - en_alguna_ruta:
        errors.append("el tema %s no esta en ninguna ruta" % slug)
    for track in content.TRACKS:
        horas = sum(content.get_topic(s)["hours"] for s in content.track_topic_slugs(track) if content.get_topic(s))
        print("Ruta %-18s %2d temas  %3d h" % (track["slug"], len(content.track_topic_slugs(track)), horas))

    print("Temas: %d | ejercicios: %s" % (len(content.TOPICS), checked))
    check_english()
    if skipped:
        print("No verificados aquí (%d): %s" % (len(skipped), ", ".join(skipped)))
    if errors:
        print("\nERRORES (%d):" % len(errors))
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("Currículo OK")


EN_KINDS = {"choice", "listen", "fill", "translate", "dictation", "speak"}


def check_english():
    """Valida la vista de inglés: estructura y que cada respuesta de referencia se corrija como buena."""
    from . import english
    from .content import ingles

    ids, counts = set(), {}
    levels = {lv["slug"] for lv in ingles.LEVELS}
    for q in ingles.PLACEMENT:
        if q["id"] in ids:
            errors.append("id duplicado: " + q["id"])
        ids.add(q["id"])
        if q["level"] not in levels or q["kind"] not in ("choice", "listen") or not 0 <= q["answer"] < len(q["options"]):
            errors.append("%s: pregunta de nivel mal formada" % q["id"])
    for band in ("A2", "B1", "B2"):  # A1 es el resultado de no superar A2: no lleva preguntas propias
        if sum(1 for q in ingles.PLACEMENT if q["level"] == band) < 4:
            errors.append("prueba de nivel: menos de 4 preguntas de %s" % band)

    slugs = set()
    for unit in ingles.UNITS:
        slug = unit["slug"]
        if slug in slugs or content.get_topic(slug):
            errors.append("unidad de inglés con slug repetido: " + slug)
        slugs.add(slug)
        if unit["level"] not in levels or unit["focus"] not in ingles.FOCUS:
            errors.append("%s: nivel o enfoque desconocido" % slug)
        if len(unit["lesson"].split()) < 120:
            errors.append("%s: lección demasiado corta" % slug)
        if len(unit["phrases"]) < 4:
            errors.append("%s: pocas frases clave" % slug)
        for ex in unit["exercises"]:
            eid, kind = ex["id"], ex["kind"]
            counts[kind] = counts.get(kind, 0) + 1
            if eid in ids:
                errors.append("id duplicado: " + eid)
            ids.add(eid)
            if kind not in EN_KINDS:
                errors.append("%s: tipo inválido" % eid)
                continue
            if kind in ("choice", "listen"):
                if not 0 <= ex["answer"] < len(ex["options"]):
                    errors.append("%s: respuesta fuera de rango" % eid)
                continue
            if kind == "fill" and ex["sentence"].count("___") != 1:
                errors.append("%s: la frase debe tener exactamente un hueco ___" % eid)
            references = [ex["text"]] if kind == "dictation" else ex["accepted"]
            for reference in references:
                if not english.check(ex, text=reference)["correct"]:
                    errors.append("%s: la respuesta de referencia no se acepta: %r" % (eid, reference))
            if english.check(ex, text="")["correct"]:
                errors.append("%s: una respuesta vacía se da por buena" % eid)

    cards = set()
    for card in ingles.VOCAB:
        if card["id"] in cards:
            errors.append("tarjeta duplicada: " + card["id"])
        cards.add(card["id"])
        if card["level"] not in levels or card["focus"] not in ingles.FOCUS:
            errors.append("%s: nivel o enfoque desconocido" % card["id"])
    if len({c["en"].lower() for c in ingles.VOCAB}) != len(ingles.VOCAB):
        errors.append("vocabulario: hay expresiones en inglés repetidas")

    print("Inglés: %d unidades | ejercicios: %s | prueba: %d preguntas | vocabulario: %d tarjetas"
          % (len(ingles.UNITS), counts, len(ingles.PLACEMENT), len(ingles.VOCAB)))


if __name__ == "__main__":
    main()
