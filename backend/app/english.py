"""Lógica pura de la vista de inglés: corrección de respuestas, nivel de la prueba y repaso espaciado.

No depende de la base de datos, así se puede probar sin PostgreSQL.
"""
import re
import unicodedata
from datetime import date, timedelta
from difflib import SequenceMatcher

# Contracciones que se expanden antes de comparar: "I'm" y "I am" cuentan igual.
CONTRACTIONS = {
    "i'm": "i am", "you're": "you are", "we're": "we are", "they're": "they are", "he's": "he is", "she's": "she is",
    "it's": "it is", "that's": "that is", "there's": "there is", "what's": "what is", "let's": "let us",
    "i've": "i have", "we've": "we have", "you've": "you have", "they've": "they have",
    "i'll": "i will", "we'll": "we will", "you'll": "you will", "it'll": "it will", "they'll": "they will",
    "i'd": "i would", "we'd": "we would", "you'd": "you would",
    "don't": "do not", "doesn't": "does not", "didn't": "did not", "isn't": "is not", "aren't": "are not",
    "wasn't": "was not", "weren't": "were not", "haven't": "have not", "hasn't": "has not", "can't": "cannot",
    "won't": "will not", "shouldn't": "should not", "couldn't": "could not", "wouldn't": "would not",
    # Las mismas sin apóstrofo (así llegan a veces del dictado por voz o del teclado). Se omiten las ambiguas: its, well, were, id.
    "im": "i am", "youre": "you are", "theyre": "they are", "thats": "that is", "theres": "there is", "whats": "what is",
    "ive": "i have", "dont": "do not", "doesnt": "does not", "didnt": "did not", "isnt": "is not", "arent": "are not",
    "wasnt": "was not", "werent": "were not", "havent": "have not", "hasnt": "has not", "cant": "cannot",
    "shouldnt": "should not", "couldnt": "could not", "wouldnt": "would not",
}

# Umbral de parecido (0-1) para dar por buena una respuesta libre.
THRESHOLDS = {"translate": 0.9, "dictation": 0.9, "speak": 0.8}


def normalize(text: str) -> str:
    """Minúsculas, sin acentos ni puntuación (salvo apóstrofos dentro de palabras) y contracciones expandidas."""
    text = (text or "").replace("’", "'").replace("‘", "'").replace("`", "'")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    text = re.sub(r"(^| )'+|'+( |$)", " ", text)  # apóstrofos sueltos
    words = []
    for word in text.split():
        words.extend(CONTRACTIONS.get(word, word).split())
    return " ".join(words)


def similarity(expected: str, got: str) -> float:
    """Parecido por palabras entre 0 y 1 (1 = idénticas tras normalizar)."""
    a, b = normalize(expected).split(), normalize(got).split()
    if not a and not b:
        return 1.0
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def word_diff(expected: str, got: str) -> dict:
    """Palabras que faltan y que sobran respecto a la respuesta esperada."""
    a, b = normalize(expected).split(), normalize(got).split()
    missing, extra = [], []
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag in ("replace", "delete"):
            missing.extend(a[i1:i2])
        if tag in ("replace", "insert"):
            extra.extend(b[j1:j2])
    return {"missing": missing, "extra": extra}


def check(exercise: dict, answer: int | None = None, text: str | None = None) -> dict:
    """Corrige un ejercicio de inglés. Devuelve {"correct": bool, ...detalles para mostrar}."""
    kind = exercise["kind"]
    if kind in ("choice", "listen"):
        result = {"correct": answer == exercise["answer"], "explanation": exercise.get("explanation", "")}
        if kind == "listen":
            result["transcript"] = exercise["audio"]
        return result

    text = text or ""
    if kind == "fill":
        accepted = exercise["accepted"]
        correct = normalize(text) in {normalize(a) for a in accepted}
        return {"correct": correct, "expected": accepted[0], "explanation": exercise.get("explanation", "")}

    if kind == "dictation":
        options = [exercise["text"]]
    elif kind in ("translate", "speak"):
        options = exercise["accepted"]
    else:
        raise ValueError("Tipo de ejercicio desconocido: %s" % kind)

    best = max(options, key=lambda option: similarity(option, text))
    score = similarity(best, text)
    return {
        "correct": score >= THRESHOLDS[kind],
        "score": round(score, 2),
        "threshold": THRESHOLDS[kind],
        "expected": best,
        "heard": text,
        **word_diff(best, text),
        "explanation": exercise.get("explanation", ""),
    }


# ---------------------------------------------------------------------------
# Prueba de nivel
# ---------------------------------------------------------------------------

LEVEL_ORDER = ["A1", "A2", "B1", "B2"]
PASS_MARK = 0.6


def placement_level(scores: dict) -> str:
    """Nivel a partir del porcentaje de aciertos por bloque: {"A2": 0.8, "B1": 0.5, "B2": 0.2} -> "A2"."""
    level = "A1"
    for band in ("A2", "B1", "B2"):
        if scores.get(band, 0) < PASS_MARK:
            break
        level = band
    return level


def placement_scores(questions: list, answers: dict) -> dict:
    """Porcentaje de aciertos por nivel. `answers` es {id_pregunta: índice elegido}."""
    totals, hits = {}, {}
    for q in questions:
        totals[q["level"]] = totals.get(q["level"], 0) + 1
        if answers.get(q["id"]) == q["answer"]:
            hits[q["level"]] = hits.get(q["level"], 0) + 1
    return {band: round(hits.get(band, 0) / n, 2) for band, n in totals.items()}


# ---------------------------------------------------------------------------
# Repaso espaciado (cajas de Leitner)
# ---------------------------------------------------------------------------

INTERVALS = [0, 1, 3, 7, 14, 30, 60]  # días hasta el siguiente repaso según la caja
LEARNED_BOX = 4
GRADES = ("otra", "dificil", "bien", "facil")


def schedule(box: int, grade: str, today: date) -> tuple[int, date]:
    """Nueva caja y fecha de repaso tras calificar una tarjeta."""
    if grade not in GRADES:
        raise ValueError("Calificación desconocida: %s" % grade)
    top = len(INTERVALS) - 1
    if grade == "otra":
        box = 0
    elif grade == "dificil":
        box = max(1, box)
    elif grade == "bien":
        box = min(box + 1, top)
    else:
        box = min(box + 2, top)
    return box, today + timedelta(days=INTERVALS[box])
