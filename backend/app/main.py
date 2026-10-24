import csv
import io
import logging
import math
import threading
import time
from collections import Counter, defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from . import auth, content, sandbox
from .config import APP_TZ, CORS_ORIGINS, DATABASE_URL_SOURCE, HOURS_PER_DAY, ON_VERCEL
from .db import Base, engine, get_db
from .models import Activity, Attempt, Note, TopicProgress

log = logging.getLogger("datapath")
TZ = ZoneInfo(APP_TZ)

MIN_ATTEMPTS = 3  # intentos mínimos para clasificar una habilidad


_ready = False
_ready_lock = threading.Lock()


def ensure_ready() -> None:
    """Crea las tablas y el sandbox una sola vez por proceso (en Vercel, por instancia)."""
    global _ready
    if _ready:
        return
    with _ready_lock:
        if _ready:
            return
        Base.metadata.create_all(engine)
        sandbox.init_sandbox()
        _ready = True


@asynccontextmanager
async def lifespan(_: FastAPI):
    # En Docker la base puede tardar en arrancar; en Vercel no conviene esperar al arrancar la función.
    retries = 1 if ON_VERCEL else 30
    for attempt in range(1, retries + 1):
        try:
            await run_in_threadpool(ensure_ready)
            break
        except Exception as exc:
            log.warning("Esperando a PostgreSQL (intento %d/%d): %s", attempt, retries, exc)
            if attempt < retries:
                time.sleep(2)
    yield


app = FastAPI(title="DataPath API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

def _db_error_message(exc: Exception) -> str:
    """Explica por qué falló la base, sin mostrar contraseñas (los errores de psycopg no las incluyen)."""
    if DATABASE_URL_SOURCE is None and ON_VERCEL:
        return ("No hay ninguna base de datos configurada: falta la variable DATABASE_URL. "
                "En Vercel: Storage → Create Database → Neon → Connect, y luego Redeploy.")
    first_line = (str(exc).strip().splitlines() or [""])[0][:300]
    return "La base de datos no está disponible (%s: %s). Variable usada: %s." % (
        type(exc).__name__, first_line, DATABASE_URL_SOURCE or "ninguna (valor por defecto local)")


PUBLIC_PATHS = {"/api/health", "/api/session", "/api/login", "/api/logout"}


@app.middleware("http")
async def guard(request: Request, call_next):
    """Pide la contraseña (si está configurada) e inicializa la base en la primera petición."""
    path = request.url.path
    if path.startswith("/api/") and path not in PUBLIC_PATHS:
        if not auth.is_authenticated(request.cookies.get(auth.COOKIE_NAME)):
            return JSONResponse({"detail": "Necesitas iniciar sesión"}, status_code=401)
        if not _ready:
            try:
                await run_in_threadpool(ensure_ready)
            except Exception as exc:
                log.exception("No se pudo inicializar la base de datos")
                return JSONResponse({"detail": _db_error_message(exc)}, status_code=503)
    return await call_next(request)


# ---------------------------------------------------------------------------
# Cálculo de progreso
# ---------------------------------------------------------------------------

def _topic_states(db: Session) -> dict:
    theory = {row.topic_slug: row.theory_done for row in db.scalars(select(TopicProgress))}

    solved = defaultdict(set)
    for slug, exercise_id in db.execute(
        select(Attempt.topic_slug, Attempt.exercise_id).where(Attempt.correct.is_(True)).distinct()
    ):
        solved[slug].add(exercise_id)

    attempts = {
        slug: (int(n or 0), int(ok or 0))
        for slug, n, ok in db.execute(
            select(Attempt.topic_slug, func.count(), func.sum(case((Attempt.correct.is_(True), 1), else_=0)))
            .group_by(Attempt.topic_slug)
        )
    }

    states = {}
    for topic in content.TOPICS:
        slug = topic["slug"]
        valid_ids = {ex["id"] for ex in topic["exercises"]}
        total = len(valid_ids)
        n_solved = len(solved[slug] & valid_ids)
        done = bool(theory.get(slug))
        n_attempts, n_correct = attempts.get(slug, (0, 0))
        if total:
            fraction = 0.25 * (1 if done else 0) + 0.75 * (n_solved / total)
        else:
            fraction = 1.0 if done else 0.0
        if done and n_solved == total:
            status = "completado"
        elif done or n_solved:
            status = "en_curso"
        else:
            status = "pendiente"
        states[slug] = {
            "theory_done": done, "solved": n_solved, "total": total, "percent": round(fraction * 100),
            "status": status, "attempts": n_attempts,
            "accuracy": round(n_correct / n_attempts, 2) if n_attempts else None,
        }
    return states


def _activity_counts(db: Session) -> Counter:
    counts = Counter()
    for (ts,) in db.execute(select(Attempt.created_at)):
        counts[ts.astimezone(TZ).date()] += 1
    for (ts,) in db.execute(select(Activity.created_at)):
        counts[ts.astimezone(TZ).date()] += 1
    return counts


def _streak(counts: Counter, today) -> int:
    day = today if counts.get(today) else today - timedelta(days=1)
    streak = 0
    while counts.get(day):
        streak += 1
        day -= timedelta(days=1)
    return streak


def _skill_level(attempts: int, accuracy: float | None) -> str:
    if attempts == 0:
        return "sin_datos"
    if attempts < MIN_ATTEMPTS:
        return "en_progreso"
    if accuracy >= 0.75:
        return "fuerte"
    if accuracy < 0.5:
        return "debil"
    return "regular"


# ---------------------------------------------------------------------------
# Esquemas de entrada
# ---------------------------------------------------------------------------

class TheoryBody(BaseModel):
    done: bool


class NoteBody(BaseModel):
    content: str


class QueryBody(BaseModel):
    query: str


class SubmitBody(BaseModel):
    answer: int | None = None   # quiz
    query: str | None = None    # sql
    passed: bool | None = None  # python / checklist (se evalúan en el navegador)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

class LoginBody(BaseModel):
    password: str


@app.get("/api/health")
def health():
    return {"status": "ok", "database_configured": DATABASE_URL_SOURCE is not None, "database_ready": _ready}


@app.get("/api/session")
def session_status(request: Request):
    return {
        "auth_required": auth.enabled(),
        "authenticated": auth.is_authenticated(request.cookies.get(auth.COOKIE_NAME)),
    }


@app.post("/api/login")
def login(body: LoginBody, request: Request, response: Response):
    if not auth.enabled():
        return {"authenticated": True}
    if not auth.check_password(body.password):
        time.sleep(1)  # frena los intentos por fuerza bruta
        raise HTTPException(401, "Contraseña incorrecta")
    secure = request.headers.get("x-forwarded-proto", request.url.scheme) == "https"
    response.set_cookie(
        auth.COOKIE_NAME, auth.session_token(), max_age=auth.COOKIE_MAX_AGE,
        httponly=True, samesite="lax", secure=secure, path="/",
    )
    return {"authenticated": True}


@app.post("/api/logout")
def logout(response: Response):
    response.delete_cookie(auth.COOKIE_NAME, path="/")
    return {"authenticated": False}


@app.get("/api/curriculum")
def curriculum():
    return {
        "phases": [
            dict(phase, topics=[content.topic_meta(t) for t in content.TOPICS if t["phase"] == phase["slug"]])
            for phase in content.PHASES
        ]
    }


@app.get("/api/topics/{slug}")
def get_topic(slug: str, db: Session = Depends(get_db)):
    topic = content.get_topic(slug)
    if not topic:
        raise HTTPException(404, "Tema no encontrado")
    note = db.get(Note, slug)
    solved = {
        row for (row,) in db.execute(
            select(Attempt.exercise_id).where(Attempt.topic_slug == slug, Attempt.correct.is_(True)).distinct()
        )
    }
    order = [t["slug"] for t in content.TOPICS]
    i = order.index(slug)
    return {
        **content.topic_meta(topic),
        "theory": topic["theory"],
        "exercises": [content.public_exercise(ex) for ex in topic["exercises"]],
        "solved_ids": sorted(solved),
        "note": note.content if note else "",
        "progress": _topic_states(db)[slug],
        "prev": order[i - 1] if i > 0 else None,
        "next": order[i + 1] if i + 1 < len(order) else None,
    }


@app.post("/api/topics/{slug}/theory")
def set_theory(slug: str, body: TheoryBody, db: Session = Depends(get_db)):
    if not content.get_topic(slug):
        raise HTTPException(404, "Tema no encontrado")
    row = db.get(TopicProgress, slug) or TopicProgress(topic_slug=slug)
    row.theory_done = body.done
    db.add(row)
    if body.done:
        db.add(Activity(kind="theory", topic_slug=slug))
    db.commit()
    return _topic_states(db)[slug]


@app.put("/api/topics/{slug}/note")
def save_note(slug: str, body: NoteBody, db: Session = Depends(get_db)):
    if not content.get_topic(slug):
        raise HTTPException(404, "Tema no encontrado")
    note = db.get(Note, slug) or Note(topic_slug=slug)
    note.content = body.content
    db.add(note)
    db.commit()
    return {"saved": True, "updated_at": datetime.now(TZ).isoformat()}


@app.get("/api/sandbox/schema")
def sandbox_schema():
    try:
        return {"tables": sandbox.schema()}
    except sandbox.SandboxError as exc:
        raise HTTPException(503, str(exc))


CSV_EXPORTS = {
    "customers": "SELECT * FROM customers ORDER BY id",
    "products": "SELECT * FROM products ORDER BY id",
    "orders": "SELECT * FROM orders ORDER BY id",
    "order_items": "SELECT * FROM order_items ORDER BY id",
    "employees": "SELECT * FROM employees ORDER BY id",
    "ventas": (
        "SELECT oi.id AS linea_id, o.id AS pedido_id, o.order_date AS fecha, o.status AS estado, "
        "o.channel AS canal, c.id AS cliente_id, c.name AS cliente, c.country AS pais, c.segment AS segmento, "
        "p.name AS producto, p.category AS categoria, oi.quantity AS cantidad, oi.unit_price AS precio_unitario, "
        "oi.quantity * oi.unit_price AS importe "
        "FROM order_items oi JOIN orders o ON o.id = oi.order_id "
        "JOIN customers c ON c.id = o.customer_id JOIN products p ON p.id = oi.product_id ORDER BY oi.id"
    ),
}


@app.get("/api/sandbox/csv/{name}")
def sandbox_csv(name: str):
    """Descarga los datos de práctica en CSV (para Excel y Power BI)."""
    query = CSV_EXPORTS.get(name)
    if query is None:
        raise HTTPException(404, "Tabla no disponible para descarga")
    try:
        result = sandbox.run_query(query, max_rows=sandbox.CHECK_ROWS)
    except sandbox.SandboxError as exc:
        raise HTTPException(503, str(exc))
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")
    writer.writerow(result["columns"])
    writer.writerows(result["rows"])
    return Response(
        content="\ufeff" + buffer.getvalue(),  # BOM para que Excel detecte UTF-8
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="%s.csv"' % name},
    )


@app.post("/api/sql/run")
def sql_run(body: QueryBody):
    try:
        return sandbox.run_query(body.query, max_rows=sandbox.DISPLAY_ROWS)
    except sandbox.SandboxError as exc:
        return {"error": str(exc)}


_expected_cache: dict = {}


def _expected(exercise: dict) -> dict:
    if exercise["id"] not in _expected_cache:
        _expected_cache[exercise["id"]] = sandbox.run_query(exercise["solution"], max_rows=sandbox.CHECK_ROWS)
    return _expected_cache[exercise["id"]]


@app.post("/api/exercises/{exercise_id}/submit")
def submit(exercise_id: str, body: SubmitBody, db: Session = Depends(get_db)):
    exercise = content.get_exercise(exercise_id)
    if not exercise:
        raise HTTPException(404, "Ejercicio no encontrado")
    kind = exercise["kind"]
    result: dict = {}

    if kind == "quiz":
        if body.answer is None:
            raise HTTPException(422, "Falta la respuesta")
        correct = body.answer == exercise["answer"]
        result = {"explanation": exercise["explanation"]}
    elif kind == "sql":
        try:
            got = sandbox.run_query(body.query or "", max_rows=sandbox.CHECK_ROWS)
            correct, feedback = sandbox.compare(got, _expected(exercise), exercise.get("ordered", False))
            result = {
                "feedback": feedback, "columns": got["columns"], "rows": got["rows"][:sandbox.DISPLAY_ROWS],
                "truncated": len(got["rows"]) > sandbox.DISPLAY_ROWS,
            }
        except sandbox.SandboxError as exc:
            correct = False
            result = {"feedback": "Tu consulta tiene un error.", "error": str(exc)}
    else:  # python, checklist
        correct = bool(body.passed)

    db.add(Attempt(
        exercise_id=exercise_id, topic_slug=exercise["topic"], skill=exercise["skill"],
        kind=kind, correct=correct,
    ))
    db.commit()
    return {"correct": correct, **result, "progress": _topic_states(db)[exercise["topic"]]}


@app.get("/api/progress")
def progress(db: Session = Depends(get_db)):
    states = _topic_states(db)
    today = datetime.now(TZ).date()

    phases, total_hours, remaining, next_topic = [], 0.0, 0.0, None
    overall_acc = []
    for phase in content.PHASES:
        topics = []
        for topic in (t for t in content.TOPICS if t["phase"] == phase["slug"]):
            st = states[topic["slug"]]
            total_hours += topic["hours"]
            remaining += topic["hours"] * (1 - st["percent"] / 100)
            overall_acc.append(st["percent"] * topic["hours"])
            entry = {"slug": topic["slug"], "title": topic["title"], "hours": topic["hours"], **st}
            topics.append(entry)
            if next_topic is None and st["status"] != "completado":
                next_topic = {"slug": topic["slug"], "title": topic["title"], "summary": topic["summary"],
                              "phase": phase["title"], **st}
        weight = sum(t["hours"] for t in topics) or 1
        phases.append({
            "slug": phase["slug"], "title": phase["title"], "description": phase["description"],
            "percent": round(sum(t["percent"] * t["hours"] for t in topics) / weight), "topics": topics,
        })

    counts = _activity_counts(db)
    days_left = math.ceil(remaining / HOURS_PER_DAY) if HOURS_PER_DAY > 0 else None
    return {
        "hours_per_day": HOURS_PER_DAY,
        "overall_percent": round(sum(overall_acc) / total_hours) if total_hours else 0,
        "total_hours": round(total_hours),
        "remaining_hours": round(remaining),
        "days_left": days_left,
        "eta_date": (today + timedelta(days=days_left)).isoformat() if days_left is not None else None,
        "streak": _streak(counts, today),
        "topics_completed": sum(1 for s in states.values() if s["status"] == "completado"),
        "topics_total": len(states),
        "phases": phases,
        "next_topic": next_topic,
    }


@app.get("/api/stats")
def stats(db: Session = Depends(get_db)):
    states = _topic_states(db)
    today = datetime.now(TZ).date()

    topics_by_skill = defaultdict(list)
    for topic in content.TOPICS:
        for skill in content.skills_of(topic):
            topics_by_skill[skill].append({"slug": topic["slug"], "title": topic["title"]})

    raw = {
        skill: (int(n or 0), int(ok or 0))
        for skill, n, ok in db.execute(
            select(Attempt.skill, func.count(), func.sum(case((Attempt.correct.is_(True), 1), else_=0)))
            .group_by(Attempt.skill)
        )
    }

    skills = []
    for skill, topics in topics_by_skill.items():
        n, ok = raw.get(skill, (0, 0))
        accuracy = round(ok / n, 2) if n else None
        skills.append({
            "skill": skill, "attempts": n, "correct": ok, "accuracy": accuracy,
            "level": _skill_level(n, accuracy), "topics": topics,
        })

    strengths = sorted((s for s in skills if s["level"] == "fuerte"), key=lambda s: -s["accuracy"])
    weaknesses = sorted((s for s in skills if s["level"] == "debil"), key=lambda s: s["accuracy"])
    review = []
    for s in weaknesses:
        for t in s["topics"]:
            if t not in review:
                review.append(t)

    counts = _activity_counts(db)
    activity = [
        {"date": (today - timedelta(days=i)).isoformat(), "count": counts.get(today - timedelta(days=i), 0)}
        for i in range(27, -1, -1)
    ]
    total_attempts = sum(n for n, _ in raw.values())
    total_correct = sum(ok for _, ok in raw.values())
    return {
        "skills": sorted(skills, key=lambda s: (s["level"] == "sin_datos", s["accuracy"] is None, s["accuracy"] or 0)),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "review_topics": review,
        "activity": activity,
        "totals": {
            "attempts": total_attempts,
            "correct": total_correct,
            "accuracy": round(total_correct / total_attempts, 2) if total_attempts else None,
            "exercises_solved": sum(s["solved"] for s in states.values()),
            "exercises_total": sum(s["total"] for s in states.values()),
        },
    }
