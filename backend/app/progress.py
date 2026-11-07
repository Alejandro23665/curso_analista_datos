"""Cálculos de progreso que comparten la API principal y la de estudio (repaso, motivación)."""
from collections import Counter, defaultdict
from zoneinfo import ZoneInfo

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from . import content, game
from .config import APP_TZ
from .models import Activity, Attempt, StudyEvent, TopicProgress

TZ = ZoneInfo(APP_TZ)

# Eventos que no cuentan como "día de estudio" (saltarse un descanso no es estudiar)
_NOT_STUDY = {"break_skipped"}


def topic_states(db: Session) -> dict:
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


def activity_counts(db: Session) -> Counter:
    """Acciones de estudio por día (intentos, actividad y eventos del temporizador o del repaso)."""
    counts = Counter()
    for (ts,) in db.execute(select(Attempt.created_at)):
        counts[ts.astimezone(TZ).date()] += 1
    for (ts,) in db.execute(select(Activity.created_at)):
        counts[ts.astimezone(TZ).date()] += 1
    for ts, kind in db.execute(select(StudyEvent.created_at, StudyEvent.kind)):
        if kind not in _NOT_STUDY:
            counts[ts.astimezone(TZ).date()] += 1
    return counts


def streak(counts: Counter, today) -> int:
    """Racha actual, contando los protectores (un día perdido no la rompe si hay protector)."""
    return game.streak_info({day for day, n in counts.items() if n}, today)["current"]
