"""Lógica pura de la motivación y del repaso: XP, niveles, racha con protectores, logros, desafío del día y repaso
espaciado de ejercicios. No depende de la base de datos, así se puede probar sin PostgreSQL.

La XP no se guarda: se recalcula siempre a partir del historial (intentos, actividad y eventos de estudio). Así no
hay que mantener contadores sincronizados y cualquier cambio de reglas se aplica también al pasado.
"""
import hashlib
from collections import defaultdict
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# XP
# ---------------------------------------------------------------------------

XP_SOLVED = 10            # resolver un ejercicio por primera vez
XP_FIRST_TRY = 5          # extra si se resolvió sin haber fallado antes
XP_THEORY = 15            # teoría de un tema o lección de inglés (una vez por tema)
XP_PLACEMENT = 20         # prueba de nivel de inglés (una vez)
XP_VOCAB = 2              # cada tarjeta de vocabulario repasada
XP_EVENTS = {
    "break_done": 20,     # bloque de estudio terminado con su descanso respetado
    "review_ok": 8,       # ejercicio del repaso del día acertado
    "review_fail": 2,     # ejercicio del repaso fallado: el esfuerzo también cuenta
    "challenge": 25,      # desafío del día superado
}
DAILY_GOAL_XP = 60

# Actividades que suman XP una sola vez por tema
_ONCE_PER_TOPIC = {"theory", "english_lesson"}


def xp_entries(attempts, activities, events):
    """Lista de (fecha, xp, origen) a partir del historial.

    attempts: [(fecha, exercise_id, correct)], activities: [(fecha, kind, topic_slug)], events: [(fecha, kind)].
    Las fechas ya vienen en la zona horaria del usuario. Los intentos deben ir en orden cronológico.
    """
    entries = []
    solved, failed = set(), set()
    for day, exercise_id, correct in attempts:
        if correct and exercise_id not in solved:
            entries.append((day, XP_SOLVED + (0 if exercise_id in failed else XP_FIRST_TRY), "ejercicio"))
            solved.add(exercise_id)
        elif not correct:
            failed.add(exercise_id)

    seen = set()
    for day, kind, slug in activities:
        if kind in _ONCE_PER_TOPIC:
            if (kind, slug) not in seen:
                seen.add((kind, slug))
                entries.append((day, XP_THEORY, "teoria"))
        elif kind == "english_placement" and kind not in seen:
            seen.add(kind)
            entries.append((day, XP_PLACEMENT, "ingles"))
        elif kind == "english_vocab":
            entries.append((day, XP_VOCAB, "vocabulario"))

    for day, kind in events:
        if kind in XP_EVENTS:
            entries.append((day, XP_EVENTS[kind], kind))
    return entries


def xp_by_day(entries):
    totals = defaultdict(int)
    for day, xp, _ in entries:
        totals[day] += xp
    return dict(totals)


# ---------------------------------------------------------------------------
# Niveles
# ---------------------------------------------------------------------------

TITLES = [(1, "Aprendiz"), (3, "Explorador"), (5, "Practicante"), (8, "Constructor"), (12, "Ingeniero"),
          (17, "Arquitecto"), (23, "Maestro")]


def level_threshold(level: int) -> int:
    """XP total necesaria para alcanzar un nivel: 0, 100, 300, 600, 1000, 1500... (cada nivel pide 100 más)."""
    return 50 * level * (level - 1)


def level_info(xp: int) -> dict:
    level = 1
    while xp >= level_threshold(level + 1):
        level += 1
    title = [t for lv, t in TITLES if lv <= level][-1]
    start, end = level_threshold(level), level_threshold(level + 1)
    return {"level": level, "title": title, "xp": xp, "into_level": xp - start, "for_next": end - start}


# ---------------------------------------------------------------------------
# Racha con protectores
# ---------------------------------------------------------------------------

FREEZE_EVERY = 7   # cada 7 días seguidos se gana un protector
MAX_FREEZES = 2


def streak_info(active_days, today: date) -> dict:
    """Racha actual, mejor racha y protectores.

    Un día sin estudiar gasta un protector (si hay) en lugar de romper la racha. Hoy todavía no cuenta como perdido.
    """
    active = set(active_days)
    result = {"current": 0, "best": 0, "freezes": 0, "frozen_days": [], "today_done": today in active}
    if not active:
        return result
    streak = best = freezes = 0
    frozen = []
    day = min(active)
    while day <= today:
        if day in active:
            streak += 1
            if streak % FREEZE_EVERY == 0:
                freezes = min(MAX_FREEZES, freezes + 1)
        elif day != today:
            if freezes and streak:
                freezes -= 1
                frozen.append(day)
            else:
                streak = 0
        best = max(best, streak)
        day += timedelta(days=1)
    result.update(current=streak, best=best, freezes=freezes, frozen_days=[d.isoformat() for d in frozen])
    return result


# ---------------------------------------------------------------------------
# Logros
# ---------------------------------------------------------------------------

# (clave, título, descripción, icono de lucide, métrica, objetivo)
ACHIEVEMENTS = [
    ("primer-ejercicio", "Primer paso", "Resuelve tu primer ejercicio.", "Footprints", "solved", 1),
    ("ejercicios-25", "Calentando motores", "Resuelve 25 ejercicios.", "Flame", "solved", 25),
    ("ejercicios-100", "Centenario", "Resuelve 100 ejercicios.", "Medal", "solved", 100),
    ("ejercicios-250", "Imparable", "Resuelve 250 ejercicios.", "Rocket", "solved", 250),
    ("primer-tema", "Tema cerrado", "Completa un tema entero: teoría y ejercicios.", "BookCheck", "topics", 1),
    ("temas-5", "Cinco de cinco", "Completa 5 temas.", "Library", "topics", 5),
    ("temas-15", "Media ruta", "Completa 15 temas.", "Map", "topics", 15),
    ("racha-3", "Constancia", "Estudia 3 días seguidos.", "CalendarCheck", "best_streak", 3),
    ("racha-7", "Una semana entera", "Estudia 7 días seguidos.", "CalendarRange", "best_streak", 7),
    ("racha-30", "Hábito de hierro", "Estudia 30 días seguidos.", "Trophy", "best_streak", 30),
    ("primer-bloque", "En la zona", "Completa un bloque de estudio con su descanso.", "Timer", "pomodoros", 1),
    ("bloques-25", "Ritmo sostenido", "Completa 25 bloques de estudio con su descanso.", "Hourglass", "pomodoros", 25),
    ("disciplina", "Disciplina", "Un día con 4 bloques o más y ningún descanso saltado.", "ShieldCheck", "disciplined_days", 1),
    ("repaso-10", "Memoria que dura", "Acierta 10 ejercicios en el repaso del día.", "BrainCircuit", "reviews_ok", 10),
    ("repaso-50", "Memoria de elefante", "Acierta 50 ejercicios en el repaso del día.", "Brain", "reviews_ok", 50),
    ("desafio-1", "Retador", "Supera tu primer desafío del día.", "Swords", "challenges", 1),
    ("desafio-10", "Cazador de desafíos", "Supera 10 desafíos del día.", "Crown", "challenges", 10),
    ("primera-curiosidad", "Curiosidad", "Resuelve un ejercicio de un tema de interés.", "Sparkles", "interest_solved", 1),
    ("nivel-5", "Practicante", "Llega al nivel 5.", "Star", "level", 5),
    ("nivel-10", "Doble dígito", "Llega al nivel 10.", "Gem", "level", 10),
]


def achievements(metrics: dict) -> list:
    return [
        {"key": key, "title": title, "description": description, "icon": icon, "target": target,
         "value": min(metrics.get(metric, 0), target), "unlocked": metrics.get(metric, 0) >= target}
        for key, title, description, icon, metric, target in ACHIEVEMENTS
    ]


def disciplined_days(events) -> int:
    """Días con al menos 4 bloques completados y ningún descanso saltado. events: [(fecha, kind)]."""
    blocks, skipped = defaultdict(int), set()
    for day, kind in events:
        if kind == "break_done":
            blocks[day] += 1
        elif kind == "break_skipped":
            skipped.add(day)
    return sum(1 for day, n in blocks.items() if n >= 4 and day not in skipped)


# ---------------------------------------------------------------------------
# Repaso espaciado de ejercicios
# ---------------------------------------------------------------------------

REVIEW_INTERVALS = [1, 3, 7, 21, 60]   # días hasta el siguiente repaso según la caja
REVIEW_SESSION = 10                     # ejercicios como máximo en el repaso del día
REVIEWABLE = {"python", "sql", "quiz", "predict", "parsons"}


def review_update(state, correct: bool, today: date) -> dict:
    """Nuevo estado de repaso de un ejercicio tras un intento.

    state: None (nunca repasado) o {"box", "due", "lapses", "reviews"}.
    - Un fallo lo devuelve a la caja 0: vuelve mañana.
    - Un acierto en su día de repaso (o después) lo sube de caja: vuelve más tarde.
    - Un acierto antes de tiempo (por ejemplo, al reintentar en la página del tema) no cambia nada.
    """
    if state is None:
        box = 0
        return {"box": box, "due": today + timedelta(days=REVIEW_INTERVALS[box]), "lapses": 0 if correct else 1,
                "reviews": 0}
    state = dict(state)
    if not correct:
        state.update(box=0, due=today + timedelta(days=REVIEW_INTERVALS[0]), lapses=state["lapses"] + 1)
    elif state["due"] <= today:
        box = min(state["box"] + 1, len(REVIEW_INTERVALS) - 1)
        state.update(box=box, due=today + timedelta(days=REVIEW_INTERVALS[box]), reviews=state["reviews"] + 1)
    return state


def pick_daily(candidates, today: date, salt: str = ""):
    """Elige un elemento de forma determinista para el día: el mismo durante todo el día, distinto al siguiente."""
    if not candidates:
        return None
    ordered = sorted(candidates)
    seed = int(hashlib.sha256((today.isoformat() + salt).encode()).hexdigest(), 16)
    return ordered[seed % len(ordered)]


def interleave(items, key, today: date):
    """Mezcla los ejercicios del repaso para que no salgan agrupados por tema (mezclar ayuda a recordar)."""
    return sorted(items, key=lambda item: hashlib.sha256((today.isoformat() + key(item)).encode()).hexdigest())
