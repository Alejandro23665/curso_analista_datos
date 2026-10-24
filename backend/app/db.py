from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool

from .config import DATABASE_URL, ON_VERCEL

# prepare_threshold=None desactiva las sentencias preparadas: así funciona también con
# conexiones agrupadas (PgBouncer) como las de Neon o Supabase.
_engine_options = {"pool_pre_ping": True, "connect_args": {"prepare_threshold": None}}
if ON_VERCEL:
    # En funciones serverless no conviene mantener un pool de conexiones abiertas.
    _engine_options["poolclass"] = NullPool

engine = create_engine(DATABASE_URL, **_engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
