"""Rutas de aprendizaje (perfiles profesionales).

Cada ruta ordena los temas en secciones propias. Un tema puede estar en varias rutas: como el progreso se guarda
por tema, al completarlo cuenta en todas las rutas que lo incluyen.
"""

import os

FUNDAMENTOS = ["python-fundamentos", "python-estructuras", "python-datos"]
SQL_COMPLETO = ["sql-select", "sql-agregaciones", "sql-joins", "sql-subconsultas-cte", "sql-ventanas", "sql-avanzado"]
EMPLEO = ["empleo-portafolio", "empleo-entrevistas"]

TRACKS = [
    {
        "slug": "ingeniero-datos",
        "title": "Ingeniero de datos",
        "icon": "🛠️",
        "description": "Construye los sistemas que mueven, limpian y sirven los datos: pipelines, bases de datos, calidad y cloud.",
        "sections": [
            {"title": "Fundamentos de Python", "topics": FUNDAMENTOS + ["sys-python-pro"]},
            {"title": "SQL a fondo", "topics": SQL_COMPLETO},
            {"title": "Python para datos", "topics": ["pandas-basico", "pandas-limpieza", "pandas-transformacion", "ia-asistida"]},
            {"title": "Bases de datos y sistemas", "topics": ["de-modelado", "sys-bd-apps", "de-herramientas", "sys-calidad"]},
            {"title": "Pipelines y plataforma de datos", "topics": ["de-python-etl", "de-orquestacion-dbt", "de-cloud", "proyecto-pipeline"]},
            {"title": "Analítica e IA", "topics": ["estadistica", "ml-sklearn", "ia-llm-fundamentos", "ia-llm-rag"]},
            {"title": "Camino al empleo", "topics": EMPLEO},
        ],
    },
    {
        "slug": "producto",
        "title": "Ingeniero de producto y startups",
        "icon": "🚀",
        "description": "Diseña y construye sistemas y productos completos (backend, seguridad, arquitectura, despliegue) y aprende a validarlos con clientes reales.",
        "sections": [
            {"title": "Fundamentos de Python y herramientas",
             "topics": FUNDAMENTOS + ["sys-python-pro", "leer-depurar-codigo", "de-herramientas"],
             "description": "Git desde el principio, y a leer y depurar código: lo que más harás en tu primer empleo y al revisar lo que genera la IA."},
            {"title": "SQL para el trabajo y las entrevistas",
             "topics": ["sql-select", "sql-agregaciones", "sql-joins", "sql-subconsultas-cte", "sql-ventanas"],
             "description": "Incluye CTE y funciones de ventana: son lo que más se pregunta en las pruebas técnicas."},
            {"title": "APIs e IA: tu primera demo",
             "topics": ["sys-apis", "ia-asistida", "ia-llm-fundamentos", "ia-llm-rag", "sys-seguridad", "frontend-ia"],
             "description": "Al terminar construye la demo del chatbot (backend + interfaz desplegada) para tu portafolio."},
            {"title": "Salir al mercado (en paralelo)",
             "topics": ["freelance-clientes", "empleo-ia", "algoritmos-entrevistas", "empleo-entrevistas", "ingles-tecnico"],
             "description": "Empieza en cuanto tengas la demo y combínala con las secciones siguientes: propuestas freelance, "
                            "postulaciones y práctica de entrevistas cada semana, no al final."},
            {"title": "IA a fondo: agentes, evaluación y desarrollo con agentes",
             "topics": ["ia-agentes-codigo", "ia-agentes", "ia-evals-seguridad"],
             "description": "Convierte tu demo en un sistema con herramientas, evaluado y seguro: es lo que más te diferencia como junior."},
            {"title": "Bases de datos y producción", "topics": ["de-modelado", "sys-bd-apps", "sys-calidad", "sys-arquitectura"]},
            {"title": "Producto y startup", "topics": ["bi-metricas", "est-ab-testing", "startup-mvp", "proyecto-mvp"]},
            {"title": "Más adelante: nivel semi-senior", "topics": ["sys-diseno", "sys-distribuida"],
             "description": "Rara vez se piden a un junior. Estúdialos cuando ya tengas ingresos o empleo."},
        ],
    },
    {
        "slug": "analista",
        "title": "Analista de datos",
        "icon": "📊",
        "description": "Convierte datos en decisiones: SQL, pandas, estadística, BI (Excel y Power BI) y comunicación.",
        "sections": [
            {"title": "Fundamentos de Python", "topics": FUNDAMENTOS},
            {"title": "SQL para análisis", "topics": SQL_COMPLETO},
            {"title": "Análisis con Python", "topics": ["pandas-basico", "pandas-limpieza", "pandas-transformacion", "visualizacion", "ia-asistida"]},
            {"title": "Estadística aplicada", "topics": ["estadistica", "est-probabilidad", "est-inferencia", "est-ab-testing", "est-regresion", "proyecto-eda"]},
            {"title": "BI y comunicación", "topics": ["bi-metricas", "bi-excel", "bi-powerbi", "data-storytelling", "proyecto-dashboard"]},
            {"title": "Machine learning", "topics": ["ml-sklearn"]},
            {"title": "Camino al empleo", "topics": EMPLEO},
        ],
    },
]

# Rutas que se muestran en la web. Las demás siguen definidas (y su progreso guardado), solo ocultas.
# Para reactivarlas: variable de entorno ACTIVE_TRACKS, por ejemplo "producto,ingeniero-datos,analista".
ACTIVE_TRACKS = [s.strip() for s in os.getenv("ACTIVE_TRACKS", "producto").split(",") if s.strip()]


def visible_tracks():
    visibles = [t for slug in ACTIVE_TRACKS for t in TRACKS if t["slug"] == slug]
    return visibles or TRACKS


def get_track(slug):
    """Devuelve la ruta visible pedida o, si no existe o está oculta, la primera ruta visible."""
    visibles = visible_tracks()
    return next((t for t in visibles if t["slug"] == slug), visibles[0])


def track_topic_slugs(track):
    return [slug for section in track["sections"] for slug in section["topics"]]


def visible_topic_slugs():
    return {slug for t in visible_tracks() for slug in track_topic_slugs(t)}


def tracks_with_topic(topic_slug):
    return [{"slug": t["slug"], "title": t["title"], "icon": t["icon"]}
            for t in visible_tracks() if topic_slug in track_topic_slugs(t)]
