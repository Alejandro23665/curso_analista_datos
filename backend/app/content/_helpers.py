"""Constructores de ejercicios para mantener el contenido corto y uniforme."""


def sql(id, title, skill, prompt, solution, starter="SELECT ", ordered=False, hint="", pg_only=False):
    return {"id": id, "kind": "sql", "title": title, "skill": skill, "prompt": prompt,
            "starter": starter, "solution": solution.strip(), "ordered": ordered, "hint": hint,
            "pg_only": pg_only}


def py(id, title, skill, prompt, starter, solution, tests, hint="", packages=None):
    return {"id": id, "kind": "python", "title": title, "skill": skill, "prompt": prompt,
            "starter": starter.strip("\n") + "\n", "solution": solution.strip("\n") + "\n",
            "tests": tests.strip("\n") + "\n", "hint": hint, "packages": packages or []}


def quiz(id, title, skill, prompt, options, answer, explanation):
    return {"id": id, "kind": "quiz", "title": title, "skill": skill, "prompt": prompt,
            "options": options, "answer": answer, "explanation": explanation}


def checklist(id, title, skill, prompt, items):
    return {"id": id, "kind": "checklist", "title": title, "skill": skill, "prompt": prompt,
            "items": items}


def parsons(id, title, skill, prompt, lines, explanation="", hint=""):
    """Ordenar líneas de código desordenadas. `lines` va en el orden correcto (con su sangría)."""
    return {"id": id, "kind": "parsons", "title": title, "skill": skill, "prompt": prompt,
            "lines": [line.rstrip() for line in lines], "explanation": explanation, "hint": hint}


def predict(id, title, skill, prompt, code, answer, explanation, hint=""):
    """Seguir el código a mano y escribir exactamente lo que imprime."""
    return {"id": id, "kind": "predict", "title": title, "skill": skill, "prompt": prompt,
            "code": code.strip("\n"), "answer": answer.strip("\n"), "explanation": explanation, "hint": hint}
