from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TopicProgress(Base):
    """Estado de la parte teórica de cada tema."""

    __tablename__ = "topic_progress"

    topic_slug: Mapped[str] = mapped_column(String(80), primary_key=True)
    theory_done: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class Attempt(Base):
    """Cada intento de ejercicio (correcto o no). De aquí salen fortalezas y debilidades."""

    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[str] = mapped_column(String(80), index=True)
    topic_slug: Mapped[str] = mapped_column(String(80), index=True)
    skill: Mapped[str] = mapped_column(String(120), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    correct: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class Note(Base):
    """Apuntes personales por tema (Markdown)."""

    __tablename__ = "notes"

    topic_slug: Mapped[str] = mapped_column(String(80), primary_key=True)
    content: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class Activity(Base):
    """Eventos de estudio que no son intentos (p. ej. marcar teoría como leída)."""

    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kind: Mapped[str] = mapped_column(String(30))
    topic_slug: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class EnglishPlacement(Base):
    """Resultado de cada prueba de nivel de inglés (se usa la más reciente)."""

    __tablename__ = "english_placement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    level: Mapped[str] = mapped_column(String(4))
    scores: Mapped[str] = mapped_column(Text)  # JSON: {"A2": 0.83, "B1": 0.5, "B2": 0.17}
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class EnglishCard(Base):
    """Estado de repaso espaciado de cada tarjeta de vocabulario ya vista."""

    __tablename__ = "english_cards"

    card_id: Mapped[str] = mapped_column(String(40), primary_key=True)
    box: Mapped[int] = mapped_column(Integer, default=0)
    due: Mapped[date] = mapped_column(Date, index=True)
    introduced: Mapped[date] = mapped_column(Date, index=True)  # día en que se vio por primera vez
    reviews: Mapped[int] = mapped_column(Integer, default=0)
    lapses: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class StudyEvent(Base):
    """Eventos del estudio: bloques del temporizador, descansos (respetados o saltados), repasos y desafíos.

    `ref` identifica el evento en el cliente (p. ej. la hora de inicio del bloque) para no registrarlo dos veces
    cuando hay varias pestañas abiertas.
    """

    __tablename__ = "study_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kind: Mapped[str] = mapped_column(String(30), index=True)
    ref: Mapped[str] = mapped_column(String(80), default="")
    minutes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class ExerciseReview(Base):
    """Estado de repaso espaciado de cada ejercicio (del currículo o de los temas de interés)."""

    __tablename__ = "exercise_reviews"

    exercise_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    box: Mapped[int] = mapped_column(Integer, default=0)
    due: Mapped[date] = mapped_column(Date, index=True)
    lapses: Mapped[int] = mapped_column(Integer, default=0)
    reviews: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
