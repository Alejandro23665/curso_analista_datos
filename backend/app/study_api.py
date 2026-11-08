"""API de estudio: temporizador (bloques y descansos), motivación (XP, nivel, racha, logros) y repaso del día."""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import content, game
from .db import get_db
from .models import Activity, Attempt, ExerciseReview, StudyEvent
from .progress import TZ, activity_counts, topic_states

router = APIRouter(prefix="/api")

TIMER_EVENTS = {"pomodoro", "break_done", "break_skipped"}


def _today():
    return datetime.now(TZ).date()


def _local(ts):
    return ts.astimezone(TZ).date()


class EventBody(BaseModel):
    kind: str
    ref: str = Field(default="", max_length=80)
    minutes: int = Field(default=0, ge=0, le=600)


@router.post("/study/events")
def add_event(body: EventBody, db: Session = Depends(get_db)):
    """Registra un bloque terminado o un descanso (respetado o saltado). Ignora duplicados de otras pestañas."""
    if body.kind not in TIMER_EVENTS:
        raise HTTPException(422, "Tipo de evento desconocido")
    if body.ref and db.scalar(select(StudyEvent.id).where(StudyEvent.kind == body.kind, StudyEvent.ref == body.ref)):
        return {"saved": False, "duplicate": True}
    db.add(StudyEvent(kind=body.kind, ref=body.ref, minutes=body.minutes))
    db.commit()
    return {"saved": True}


# ---------------------------------------------------------------------------
# Historial y XP
# ---------------------------------------------------------------------------

def _history(db: Session):
    attempts = [(_local(ts), ex, ok) for ts, ex, ok in db.execute(
        select(Attempt.created_at, Attempt.exercise_id, Attempt.correct).order_by(Attempt.created_at, Attempt.id))]
    activities = [(_local(ts), kind, slug) for ts, kind, slug in db.execute(
        select(Activity.created_at, Activity.kind, Activity.topic_slug).order_by(Activity.created_at, Activity.id))]
    events = [(_local(ts), kind, minutes) for ts, kind, minutes in db.execute(
        select(StudyEvent.created_at, StudyEvent.kind, StudyEvent.minutes).order_by(StudyEvent.created_at, StudyEvent.id))]
    return attempts, activities, events


def xp_for_attempt(db: Session, exercise_id: str, correct: bool) -> tuple[int, bool]:
    """XP que gana un intento antes de guardarlo y si fue un golpe de suerte (misma regla que game.xp_entries)."""
    if not correct:
        return 0, False
    previous = {ok for (ok,) in db.execute(select(Attempt.correct).where(Attempt.exercise_id == exercise_id))}
    if True in previous:
        return 0, False
    xp = game.XP_SOLVED + (0 if False in previous else game.XP_FIRST_TRY)
    lucky = game.es_golpe_de_suerte(exercise_id, _today())
    return (xp * 2 if lucky else xp), lucky


def _weekly(entries, attempts, events, today):
    """Últimos 7 días frente a los 7 anteriores."""
    def window(start, end):
        days = {start + timedelta(days=i) for i in range((end - start).days + 1)}
        tried = [ok for day, _, ok in attempts if day in days]
        first_solves = sum(1 for day, xp, source in entries if day in days and source == "ejercicio")
        return {
            "xp": sum(xp for day, xp, _ in entries if day in days),
            "solved": first_solves,
            "attempts": len(tried),
            "accuracy": round(sum(tried) / len(tried), 2) if tried else None,
            "blocks": sum(1 for day, kind, _ in events if day in days and kind == "break_done"),
            "minutes": sum(m for day, kind, m in events if day in days and kind == "pomodoro"),
            "skipped": sum(1 for day, kind, _ in events if day in days and kind == "break_skipped"),
        }
    return {"this": window(today - timedelta(days=6), today), "previous": window(today - timedelta(days=13), today - timedelta(days=7))}


@router.get("/game")
def game_summary(db: Session = Depends(get_db)):
    today = _today()
    attempts, activities, events = _history(db)
    simple_events = [(day, kind) for day, kind, _ in events]
    entries = game.xp_entries(attempts, activities, simple_events)
    by_day = game.xp_by_day(entries)
    total = sum(by_day.values())
    level = game.level_info(total)

    counts = activity_counts(db)
    streak = game.streak_info({day for day, n in counts.items() if n}, today)

    states = topic_states(db)
    solved_ids = {ex for _, ex, ok in attempts if ok and content.get_exercise(ex)}
    interest_solved = sum(1 for ex in solved_ids if content.get_topic(content.get_exercise(ex)["topic"]).get("interest"))
    metrics = {
        "solved": len(solved_ids),
        "topics": sum(1 for s in states.values() if s["status"] == "completado"),
        "best_streak": streak["best"],
        "pomodoros": sum(1 for _, kind in simple_events if kind == "break_done"),
        "disciplined_days": game.disciplined_days(simple_events),
        "reviews_ok": sum(1 for _, kind in simple_events if kind == "review_ok"),
        "challenges": sum(1 for _, kind in simple_events if kind == "challenge"),
        "interest_solved": interest_solved,
        "level": level["level"],
    }

    # Calendario: 26 semanas completas que terminan en la semana actual (empiezan en lunes)
    start = today - timedelta(days=today.weekday() + 7 * 25)
    calendar = [{"date": (start + timedelta(days=i)).isoformat(), "xp": by_day.get(start + timedelta(days=i), 0),
                 "frozen": (start + timedelta(days=i)).isoformat() in streak["frozen_days"]}
                for i in range((today - start).days + 1)]

    return {
        "level": level,
        "today_xp": by_day.get(today, 0),
        "daily_goal": game.DAILY_GOAL_XP,
        "streak": streak,
        "achievements": game.achievements(metrics),
        "weekly": _weekly(entries, attempts, events, today),
        "calendar": calendar,
        "blocks_today": sum(1 for day, kind in simple_events if day == today and kind == "break_done"),
    }


# ---------------------------------------------------------------------------
# Repaso del día
# ---------------------------------------------------------------------------

def _reviewable(exercise_id):
    exercise = content.get_exercise(exercise_id)
    return exercise if exercise and exercise["kind"] in game.REVIEWABLE else None


def _backfill(db: Session, today):
    """Da estado de repaso a los ejercicios intentados antes de que existiera el repaso del día."""
    known = set(db.scalars(select(ExerciseReview.exercise_id)))
    last, failed, solved = {}, set(), set()
    for ts, ex, ok in db.execute(select(Attempt.created_at, Attempt.exercise_id, Attempt.correct)):
        if ex in known or not _reviewable(ex):
            continue
        last[ex] = max(last.get(ex, _local(ts)), _local(ts))
        (solved if ok else failed).add(ex)
    for ex, day in last.items():
        box = 0 if ex in failed or ex not in solved else 1
        db.add(ExerciseReview(exercise_id=ex, box=box, due=min(today, day + timedelta(days=game.REVIEW_INTERVALS[box])),
                              lapses=1 if ex in failed else 0, reviews=0))
    if last:
        db.commit()


def update_review(db: Session, exercise_id: str, correct: bool):
    """Actualiza el repaso espaciado de un ejercicio tras un intento (desde el tema, el repaso o el desafío)."""
    if not _reviewable(exercise_id):
        return
    today = _today()
    row = db.get(ExerciseReview, exercise_id)
    state = None if row is None else {"box": row.box, "due": row.due, "lapses": row.lapses, "reviews": row.reviews}
    new = game.review_update(state, correct, today)
    row = row or ExerciseReview(exercise_id=exercise_id)
    row.box, row.due, row.lapses, row.reviews = new["box"], new["due"], new["lapses"], new["reviews"]
    db.add(row)


def record_mode(db: Session, exercise_id: str, correct: bool, mode: str) -> int:
    """Registra el resultado de un ejercicio hecho desde el repaso o el desafío. Devuelve la XP extra."""
    today = _today()
    if mode == "review":
        kind = "review_ok" if correct else "review_fail"
        ref = "%s:%s" % (exercise_id, today.isoformat())
        if not db.scalar(select(StudyEvent.id).where(StudyEvent.ref == ref, StudyEvent.kind.in_(["review_ok", "review_fail"]))):
            db.add(StudyEvent(kind=kind, ref=ref))
            return game.XP_EVENTS[kind]
    elif mode == "challenge" and correct:
        ref = "challenge:" + today.isoformat()
        if not db.scalar(select(StudyEvent.id).where(StudyEvent.kind == "challenge", StudyEvent.ref == ref)):
            db.add(StudyEvent(kind="challenge", ref=ref))
            return game.XP_EVENTS["challenge"]
    return 0


def _card(exercise_id, extra=None):
    exercise = content.get_exercise(exercise_id)
    topic = content.get_topic(exercise["topic"])
    return {"exercise": content.public_exercise(exercise), "topic": {"slug": topic["slug"], "title": topic["title"]},
            **(extra or {})}


@router.get("/review")
def review(db: Session = Depends(get_db)):
    today = _today()
    _backfill(db, today)
    rows = [r for r in db.scalars(select(ExerciseReview).where(ExerciseReview.due <= today)) if _reviewable(r.exercise_id)]
    rows.sort(key=lambda r: (r.due, r.box))
    due_total = len(rows)
    chosen = game.interleave(rows[:game.REVIEW_SESSION], key=lambda r: r.exercise_id, today=today)

    done_today = 0
    challenge_done = False
    for (ref,) in db.execute(select(StudyEvent.ref).where(StudyEvent.kind.in_(["review_ok", "review_fail", "challenge"]))):
        if ref.endswith(today.isoformat()):
            if ref.startswith("challenge:"):
                challenge_done = True
            else:
                done_today += 1

    states = topic_states(db)
    pending = [
        {"slug": slug, "title": content.get_topic(slug)["title"], "solved": st["solved"], "total": st["total"]}
        for slug, st in states.items()
        if st["theory_done"] and st["solved"] < st["total"]
    ][:6]

    due_ids = {r.exercise_id for r in rows}
    candidates = [ex["id"] for t in content.TOPICS if states[t["slug"]]["status"] != "pendiente"
                  for ex in t["exercises"] if ex["kind"] in game.REVIEWABLE and ex["id"] not in due_ids]
    challenge_id = game.pick_daily(candidates, today, salt="challenge")

    return {
        "items": [_card(r.exercise_id, {"box": r.box, "lapses": r.lapses}) for r in chosen],
        "due_total": due_total,
        "done_today": done_today,
        "session_size": game.REVIEW_SESSION,
        "pending_practice": pending,
        "challenge": _card(challenge_id, {"done": challenge_done, "xp": game.XP_EVENTS["challenge"]}) if challenge_id else None,
    }

