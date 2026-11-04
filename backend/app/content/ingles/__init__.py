"""Contenido de la vista de inglés: prueba de nivel, unidades por situación y vocabulario.

Está separado del currículo principal: no pertenece a ninguna ruta ni cuenta en el panel de avance.
"""
from pathlib import Path

from . import unidades_basico, unidades_entrevistas, unidades_equipo, unidades_freelance, unidades_tecnico
from .pronunciacion import PRON
from .prueba import PLACEMENT
from .vocabulario import VOCAB

LEVELS = [
    {"slug": "A1", "title": "A1 · Bases", "description": "El verbo to be, el presente y el pasado simple, preguntas, números y fechas: lo imprescindible, siempre en contexto de trabajo."},
    {"slug": "A2", "title": "A2 · Primeras situaciones", "description": "Frases cortas y claras para presentarte, pedir cosas y contar qué haces."},
    {"slug": "B1", "title": "B1 · Independiente", "description": "Explicar proyectos, hacer buenas preguntas y escribir mensajes de trabajo."},
    {"slug": "B2", "title": "B2 · Profesional", "description": "Negociar, dar y recibir críticas, justificar decisiones y contar incidentes."},
]

FOCUS = {
    "entrevistas": {"title": "Entrevistas", "icon": "🎤"},
    "freelance": {"title": "Clientes freelance", "icon": "🤝"},
    "equipo": {"title": "Trabajo en equipo", "icon": "💬"},
    "tecnico": {"title": "Inglés técnico", "icon": "⚙️"},
}

_LEVEL_INDEX = {level["slug"]: i for i, level in enumerate(LEVELS)}

# Orden por nivel. Dentro de cada nivel se respeta el orden de la lista (sorted es estable): el bloque A1 va en orden
# pedagógico (to be → presente → preguntas → pasado) y el resto, por enfoque.
UNITS = sorted(
    unidades_basico.UNITS + unidades_entrevistas.UNITS + unidades_freelance.UNITS + unidades_equipo.UNITS + unidades_tecnico.UNITS,
    key=lambda u: _LEVEL_INDEX[u["level"]],
)

# Las lecciones largas viven en lecciones/<slug>.md y sustituyen a la lección corta del diccionario de la unidad.
_LECCIONES = Path(__file__).parent / "lecciones"


def _leccion(unit):
    archivo = _LECCIONES / (unit["slug"] + ".md")
    return archivo.read_text(encoding="utf-8") if archivo.exists() else unit["lesson"]


UNITS = [dict(u, lesson=_leccion(u)) for u in UNITS]
VOCAB = [dict(c, pron=PRON.get(c["en"], "")) for c in VOCAB]

_UNIT_BY_SLUG = {u["slug"]: u for u in UNITS}
_EXERCISE_BY_ID = {ex["id"]: dict(ex, unit=u["slug"], focus=u["focus"]) for u in UNITS for ex in u["exercises"]}
_CARD_BY_ID = {c["id"]: c for c in VOCAB}

# Lo que nunca se envía al navegador antes de responder.
_HIDDEN = {"answer", "accepted", "explanation"}


def get_unit(slug):
    return _UNIT_BY_SLUG.get(slug)


def get_exercise(exercise_id):
    return _EXERCISE_BY_ID.get(exercise_id)


def get_card(card_id):
    return _CARD_BY_ID.get(card_id)


def skill_of(unit_or_exercise):
    return "Inglés: " + FOCUS[unit_or_exercise["focus"]]["title"]


def public_exercise(exercise):
    """Ejercicio listo para el navegador. El audio y el dictado sí viajan: los lee la voz del navegador."""
    data = {k: v for k, v in exercise.items() if k not in _HIDDEN | {"unit", "focus"}}
    if exercise["kind"] == "speak" and not exercise["show_target"]:
        data.pop("target")
    return data


def public_question(question):
    return {k: v for k, v in question.items() if k not in _HIDDEN}
