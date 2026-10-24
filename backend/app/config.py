"""Configuración leída de variables de entorno."""
import os

_DEFAULT_DB = "postgresql+psycopg://datapath:datapath@localhost:5432/datapath"


_URL_VARIABLES = ("DATABASE_URL_UNPOOLED", "DATABASE_URL", "POSTGRES_URL_NON_POOLING", "POSTGRES_URL")


def _database_url():
    """Acepta los nombres que usan Docker, Neon y Vercel, y fuerza el driver psycopg 3.

    Devuelve (url, nombre_de_la_variable_usada o None si se usa el valor por defecto)."""
    source = next((name for name in _URL_VARIABLES if os.getenv(name)), None)
    url = os.getenv(source) if source else _DEFAULT_DB
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            url = "postgresql+psycopg://" + url[len(prefix):]
            break
    return url, source


DATABASE_URL, DATABASE_URL_SOURCE = _database_url()
SANDBOX_DB_PASSWORD = os.getenv("SANDBOX_DB_PASSWORD", "sandbox_ro_change_me")
HOURS_PER_DAY = float(os.getenv("STUDY_HOURS_PER_DAY", "3"))
APP_TZ = os.getenv("APP_TZ", "America/Caracas")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()]

# Si se define, la app pide esta contraseña antes de mostrar nada (obligatorio al publicarla en internet).
APP_PASSWORD = os.getenv("APP_PASSWORD", "")
# Vercel define VERCEL=1 en sus funciones.
ON_VERCEL = bool(os.getenv("VERCEL"))
