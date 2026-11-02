"""Constructores de ejercicios de inglés (mismo estilo que content/_helpers.py)."""


def choice(id, prompt, options, answer, explanation):
    """Elegir la opción correcta."""
    return {"id": id, "kind": "choice", "prompt": prompt, "options": options, "answer": answer, "explanation": explanation}


def listen(id, audio, question, options, answer, explanation=""):
    """Escuchar un audio (leído por el navegador) y responder una pregunta. El texto se muestra al terminar."""
    return {"id": id, "kind": "listen", "audio": audio, "prompt": question, "options": options, "answer": answer,
            "explanation": explanation}


def fill(id, sentence, accepted, es="", explanation=""):
    """Completar el hueco (___) de una frase. `accepted` son las respuestas válidas."""
    return {"id": id, "kind": "fill", "sentence": sentence, "accepted": list(accepted), "es": es, "explanation": explanation}


def translate(id, es, accepted, explanation=""):
    """Traducir una frase del español al inglés. La primera respuesta aceptada es la de referencia."""
    return {"id": id, "kind": "translate", "es": es, "accepted": list(accepted), "explanation": explanation}


def dictation(id, text, es=""):
    """Escuchar y escribir exactamente lo que se oye."""
    return {"id": id, "kind": "dictation", "text": text, "es": es}


def speak(id, prompt, target, accepted=None, show_target=True):
    """Decir una frase en voz alta. Con show_target=False se responde sin ver la frase (traducción oral)."""
    return {"id": id, "kind": "speak", "prompt": prompt, "target": target, "accepted": [target] + list(accepted or []),
            "show_target": show_target}
