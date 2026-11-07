"""Temas de interés: áreas para el tiempo libre, fuera de las rutas y del avance del panel.

Cada área es un paquete dentro de esta carpeta (por ejemplo, `ml/`) con:
- `AREA`: slug, título, descripción, orden, aviso opcional y bloques (cada bloque lista los slugs de sus temas).
- `TOPICS`: los temas, con el mismo formato que los del currículo (mismos ejercicios y mismos helpers).
- `teoria/<slug>.md` (opcional): el capítulo largo de cada tema.

Para añadir un área nueva basta con crear su carpeta: se descubre sola al arrancar.
"""
import importlib
import pkgutil
from pathlib import Path

AREAS = []
TOPICS = []

for _info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    if not _info.ispkg:
        continue
    _module = importlib.import_module(__name__ + "." + _info.name)
    _area = _module.AREA
    _teoria = Path(_module.__file__).parent / "teoria"
    for _topic in _module.TOPICS:
        _md = _teoria / (_topic["slug"] + ".md")
        TOPICS.append(dict(_topic, interest=_area["slug"], phase="interes-" + _area["slug"],
                           theory=_md.read_text(encoding="utf-8") if _md.exists() else _topic["theory"]))
    AREAS.append(_area)

AREAS.sort(key=lambda a: (a.get("order", 100), a["title"]))
_AREA_BY_SLUG = {a["slug"]: a for a in AREAS}


def get_area(slug):
    return _AREA_BY_SLUG.get(slug)


def area_topic_slugs(area):
    return [slug for block in area["blocks"] for slug in block["topics"]]
