"""Currículo: fases, temas, teoría y ejercicios. Todo el contenido vive en archivos Python/Markdown,
así puedes editarlo o ampliarlo sin tocar la base de datos."""
from . import fase_bi, fase_de, fase_empleo, fase_estadistica, fase_fundamentos, fase_ia_asistida, fase_ml, fase_pandas, fase_python, fase_sql

PHASES = [
    {"slug": "python", "title": "Fase 1 · Python para datos",
     "description": "Repaso dirigido de lo que más usarás: estructuras, funciones, archivos y errores."},
    {"slug": "sql", "title": "Fase 2 · SQL para análisis",
     "description": "De SELECT a funciones de ventana. SQL es la habilidad más pedida en roles de datos."},
    {"slug": "pandas", "title": "Fase 3 · Análisis con Python",
     "description": "pandas, limpieza, visualización y cómo trabajar con asistentes de IA verificando lo que generan."},
    {"slug": "estadistica", "title": "Fase 4 · Estadística aplicada",
     "description": "Descriptiva, probabilidad, inferencia, A/B testing y regresión. Cierra con tu Proyecto 1: un análisis exploratorio completo."},
    {"slug": "bi", "title": "Fase 5 · BI y comunicación",
     "description": "Métricas, Excel, Power BI y storytelling, y tu Proyecto 3: un dashboard publicado."},
    {"slug": "de", "title": "Fase 6 · Ingeniería de datos",
     "description": "Modelado, ETL, Docker, orquestación, calidad de datos y cloud."},
    {"slug": "ml", "title": "Fase 7 · ML e IA aplicada",
     "description": "Fundamentos de machine learning y de LLMs/RAG para tu perfil de datos."},
    {"slug": "empleo", "title": "Fase 8 · Camino al primer empleo",
     "description": "Portafolio, CV, LinkedIn y preparación de entrevistas técnicas."},
]

TOPICS = [t for module in (fase_fundamentos, fase_python, fase_sql, fase_pandas, fase_ia_asistida, fase_estadistica, fase_bi, fase_de, fase_ml, fase_empleo)
          for t in module.TOPICS]

_TOPIC_BY_SLUG = {t["slug"]: t for t in TOPICS}
_EXERCISE_BY_ID = {}
for _topic in TOPICS:
    for _ex in _topic["exercises"]:
        _EXERCISE_BY_ID[_ex["id"]] = dict(_ex, topic=_topic["slug"])


def get_topic(slug):
    return _TOPIC_BY_SLUG.get(slug)


def get_exercise(exercise_id):
    return _EXERCISE_BY_ID.get(exercise_id)


def skills_of(topic):
    return sorted({ex["skill"] for ex in topic["exercises"]})


def topic_meta(topic):
    return {
        "slug": topic["slug"], "title": topic["title"], "phase": topic["phase"],
        "summary": topic["summary"], "hours": topic["hours"],
        "skills": skills_of(topic), "exercise_count": len(topic["exercises"]),
    }


def public_exercise(exercise):
    """Ejercicio listo para enviar al navegador (sin la respuesta de los quizzes)."""
    data = {k: v for k, v in exercise.items() if k not in ("answer", "topic")}
    return data
