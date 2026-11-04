"""Endpoints de la vista de inglés (/api/english/...). Separados del currículo principal."""
import json
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from . import english
from .config import APP_TZ
from .content import ingles
from .db import get_db
from .models import Activity, Attempt, EnglishCard, EnglishPlacement, TopicProgress

router = APIRouter(prefix="/api/english")
TZ = ZoneInfo(APP_TZ)

NEW_CARDS_PER_DAY = 10
SESSION_SIZE = 20
UNIT_SLUGS = [u["slug"] for u in ingles.UNITS]
LEVEL_SLUGS = [lv["slug"] for lv in ingles.LEVELS]


def _today():
    return datetime.now(TZ).date()


# ---------------------------------------------------------------------------
# Progreso
# ---------------------------------------------------------------------------

def _unit_states(db: Session) -> dict:
    lessons = {row.topic_slug: row.theory_done for row in db.scalars(select(TopicProgress).where(TopicProgress.topic_slug.in_(UNIT_SLUGS)))}
    solved = defaultdict(set)
    for slug, exercise_id in db.execute(
        select(Attempt.topic_slug, Attempt.exercise_id)
        .where(Attempt.topic_slug.in_(UNIT_SLUGS), Attempt.correct.is_(True)).distinct()
    ):
        solved[slug].add(exercise_id)

    states = {}
    for unit in ingles.UNITS:
        slug = unit["slug"]
        valid = {ex["id"] for ex in unit["exercises"]}
        n_solved, total = len(solved[slug] & valid), len(valid)
        done = bool(lessons.get(slug))
        percent = round(100 * (0.2 * done + 0.8 * n_solved / total))
        status = "completado" if done and n_solved == total else "en_curso" if done or n_solved else "pendiente"
        states[slug] = {"lesson_done": done, "solved": n_solved, "total": total, "percent": percent, "status": status}
    return states


def _latest_placement(db: Session):
    row = db.scalars(select(EnglishPlacement).order_by(EnglishPlacement.created_at.desc()).limit(1)).first()
    if not row:
        return None
    return {"level": row.level, "scores": json.loads(row.scores), "date": row.created_at.astimezone(TZ).date().isoformat()}


def _start_level(placement) -> str:
    """Nivel por el que conviene empezar (A1 empieza por A2, el primero disponible)."""
    level = placement["level"] if placement else "A2"
    return level if level in LEVEL_SLUGS else LEVEL_SLUGS[0]


def _unit_meta(unit, state):
    focus = ingles.FOCUS[unit["focus"]]
    return {"slug": unit["slug"], "title": unit["title"], "summary": unit["summary"], "level": unit["level"],
            "focus": unit["focus"], "focus_title": focus["title"], "icon": focus["icon"], "minutes": unit["minutes"], **state}


def _vocab_counts(db: Session) -> dict:
    today = _today()
    rows = list(db.scalars(select(EnglishCard)))
    known = {c["id"] for c in ingles.VOCAB}
    rows = [r for r in rows if r.card_id in known]
    new_today = sum(1 for r in rows if r.introduced == today)
    return {
        "total": len(ingles.VOCAB),
        "seen": len(rows),
        "learned": sum(1 for r in rows if r.box >= english.LEARNED_BOX),
        "due": sum(1 for r in rows if r.due <= today),
        "new_available": max(0, min(NEW_CARDS_PER_DAY - new_today, len(ingles.VOCAB) - len(rows))),
    }


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    states = _unit_states(db)
    placement = _latest_placement(db)
    start = _start_level(placement)

    accuracy = {
        slug: (int(n or 0), int(ok or 0))
        for slug, n, ok in db.execute(
            select(Attempt.topic_slug, func.count(), func.sum(case((Attempt.correct.is_(True), 1), else_=0)))
            .where(Attempt.topic_slug.in_(UNIT_SLUGS)).group_by(Attempt.topic_slug)
        )
    }
    focus = []
    for slug, info in ingles.FOCUS.items():
        units = [u for u in ingles.UNITS if u["focus"] == slug]
        n = sum(accuracy.get(u["slug"], (0, 0))[0] for u in units)
        ok = sum(accuracy.get(u["slug"], (0, 0))[1] for u in units)
        focus.append({
            "slug": slug, **info,
            "percent": round(sum(states[u["slug"]]["percent"] for u in units) / len(units)),
            "attempts": n, "accuracy": round(ok / n, 2) if n else None,
        })

    levels = [dict(level, units=[_unit_meta(u, states[u["slug"]]) for u in ingles.UNITS if u["level"] == level["slug"]])
              for level in ingles.LEVELS]
    ordered = [u for u in ingles.UNITS if LEVEL_SLUGS.index(u["level"]) >= LEVEL_SLUGS.index(start)] + ingles.UNITS
    next_unit = next((u for u in ordered if states[u["slug"]]["status"] != "completado"), None)

    return {
        "placement": placement,
        "start_level": start,
        "percent": round(sum(s["percent"] for s in states.values()) / len(states)),
        "units_completed": sum(1 for s in states.values() if s["status"] == "completado"),
        "units_total": len(states),
        "next_unit": _unit_meta(next_unit, states[next_unit["slug"]]) if next_unit else None,
        "levels": levels,
        "focus": focus,
        "vocab": _vocab_counts(db),
    }


# ---------------------------------------------------------------------------
# Unidades y ejercicios
# ---------------------------------------------------------------------------

class LessonBody(BaseModel):
    done: bool


class EnglishSubmitBody(BaseModel):
    answer: int | None = None  # choice / listen
    text: str | None = None    # fill, translate, dictation, speak (texto escrito o transcrito)


@router.get("/units/{slug}")
def get_unit(slug: str, db: Session = Depends(get_db)):
    unit = ingles.get_unit(slug)
    if not unit:
        raise HTTPException(404, "Unidad no encontrada")
    solved = {
        row for (row,) in db.execute(
            select(Attempt.exercise_id).where(Attempt.topic_slug == slug, Attempt.correct.is_(True)).distinct()
        )
    }
    i = UNIT_SLUGS.index(slug)
    focus = ingles.FOCUS[unit["focus"]]
    return {
        "slug": slug, "title": unit["title"], "summary": unit["summary"], "level": unit["level"], "minutes": unit["minutes"],
        "focus": unit["focus"], "focus_title": focus["title"], "icon": focus["icon"],
        "lesson": unit["lesson"],
        "phrases": [{"en": en, "es": es, "pron": ingles.PRON.get(en, "")} for en, es in unit["phrases"]],
        "exercises": [ingles.public_exercise(ex) for ex in unit["exercises"]],
        "solved_ids": sorted(solved & {ex["id"] for ex in unit["exercises"]}),
        "progress": _unit_states(db)[slug],
        "prev": UNIT_SLUGS[i - 1] if i > 0 else None,
        "next": UNIT_SLUGS[i + 1] if i + 1 < len(UNIT_SLUGS) else None,
    }


@router.post("/units/{slug}/lesson")
def set_lesson(slug: str, body: LessonBody, db: Session = Depends(get_db)):
    if not ingles.get_unit(slug):
        raise HTTPException(404, "Unidad no encontrada")
    row = db.get(TopicProgress, slug) or TopicProgress(topic_slug=slug)
    row.theory_done = body.done
    db.add(row)
    if body.done:
        db.add(Activity(kind="english_lesson", topic_slug=slug))
    db.commit()
    return _unit_states(db)[slug]


@router.post("/exercises/{exercise_id}/submit")
def submit(exercise_id: str, body: EnglishSubmitBody, db: Session = Depends(get_db)):
    exercise = ingles.get_exercise(exercise_id)
    if not exercise:
        raise HTTPException(404, "Ejercicio no encontrado")
    if exercise["kind"] in ("choice", "listen") and body.answer is None:
        raise HTTPException(422, "Falta la respuesta")
    result = english.check(exercise, answer=body.answer, text=body.text)
    db.add(Attempt(
        exercise_id=exercise_id, topic_slug=exercise["unit"], skill=ingles.skill_of(exercise),
        kind=exercise["kind"], correct=result["correct"],
    ))
    db.commit()
    return {**result, "progress": _unit_states(db)[exercise["unit"]]}


# ---------------------------------------------------------------------------
# Prueba de nivel
# ---------------------------------------------------------------------------

class PlacementBody(BaseModel):
    answers: dict[str, int]


@router.get("/placement")
def placement_questions():
    return {"questions": [ingles.public_question(q) for q in ingles.PLACEMENT]}


@router.post("/placement")
def placement_submit(body: PlacementBody, db: Session = Depends(get_db)):
    scores = english.placement_scores(ingles.PLACEMENT, body.answers)
    level = english.placement_level(scores)
    db.add(EnglishPlacement(level=level, scores=json.dumps(scores)))
    db.add(Activity(kind="english_placement", topic_slug="english"))
    db.commit()
    def chosen(q):
        index = body.answers.get(q["id"])
        return q["options"][index] if index is not None and 0 <= index < len(q["options"]) else None

    review = [
        {"id": q["id"], "level": q["level"], "prompt": q["prompt"], "correct": body.answers.get(q["id"]) == q["answer"],
         "answer": q["options"][q["answer"]], "chosen": chosen(q)}
        for q in ingles.PLACEMENT
    ]
    return {"level": level, "scores": scores, "start_level": _start_level({"level": level}), "review": review}


# ---------------------------------------------------------------------------
# Vocabulario (repaso espaciado)
# ---------------------------------------------------------------------------

class GradeBody(BaseModel):
    grade: str


@router.get("/vocab")
def vocab_session(db: Session = Depends(get_db)):
    """Tarjetas para repasar hoy: primero las pendientes y luego algunas nuevas de tu nivel."""
    today = _today()
    seen = {row.card_id: row for row in db.scalars(select(EnglishCard))}
    due = sorted((r for r in seen.values() if r.due <= today and ingles.get_card(r.card_id)), key=lambda r: (r.due, r.box))
    counts = _vocab_counts(db)

    start = LEVEL_SLUGS.index(_start_level(_latest_placement(db)))
    unseen = [c for c in ingles.VOCAB if c["id"] not in seen]
    # Primero las de tu nivel y las anteriores; las de niveles superiores al final.
    unseen.sort(key=lambda c: (LEVEL_SLUGS.index(c["level"]) > start, LEVEL_SLUGS.index(c["level"])))

    cards = [dict(ingles.get_card(r.card_id), box=r.box, is_new=False) for r in due[:SESSION_SIZE]]
    room = max(0, min(SESSION_SIZE - len(cards), counts["new_available"]))
    cards += [dict(c, box=0, is_new=True) for c in unseen[:room]]
    return {"cards": cards, "counts": counts, "intervals": english.INTERVALS}


@router.post("/vocab/{card_id}")
def vocab_grade(card_id: str, body: GradeBody, db: Session = Depends(get_db)):
    if not ingles.get_card(card_id):
        raise HTTPException(404, "Tarjeta no encontrada")
    if body.grade not in english.GRADES:
        raise HTTPException(422, "Calificación no válida")
    today = _today()
    row = db.get(EnglishCard, card_id) or EnglishCard(card_id=card_id, box=0, due=today, introduced=today, reviews=0, lapses=0)
    if body.grade == "otra" and row.box > 0:
        row.lapses += 1
    row.box, row.due = english.schedule(row.box, body.grade, today)
    row.reviews += 1
    db.add(row)
    db.add(Activity(kind="english_vocab", topic_slug="english"))
    db.commit()
    return {"card_id": card_id, "box": row.box, "due": row.due.isoformat(), "counts": _vocab_counts(db)}
