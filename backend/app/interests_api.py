"""API de los temas de interés: lista de áreas y detalle de cada una (bloques, temas y progreso)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import content
from .content import intereses
from .db import get_db
from .progress import topic_states

router = APIRouter(prefix="/api")


def _area_summary(area, states):
    blocks, next_topic = [], None
    total_hours = weighted = 0.0
    for index, block in enumerate(area["blocks"], start=1):
        topics = []
        for slug in block["topics"]:
            topic = content.get_topic(slug)
            st = states[slug]
            total_hours += topic["hours"]
            weighted += st["percent"] * topic["hours"]
            topics.append({"slug": slug, "title": topic["title"], "hours": topic["hours"], **st})
            if next_topic is None and st["status"] != "completado":
                next_topic = {"slug": slug, "title": topic["title"], "percent": st["percent"]}
        weight = sum(t["hours"] for t in topics) or 1
        blocks.append({
            "slug": "%s-%d" % (area["slug"], index),
            "title": "%s · %s" % (block.get("label", index), block["title"]),
            "description": block.get("description", ""),
            "percent": round(sum(t["percent"] * t["hours"] for t in topics) / weight),
            "topics": topics,
        })
    all_topics = [t for b in blocks for t in b["topics"]]
    return {
        "slug": area["slug"], "title": area["title"], "description": area["description"], "notice": area.get("notice", ""),
        "blocks": blocks,
        "total_hours": round(total_hours),
        "percent": round(weighted / total_hours) if total_hours else 0,
        "topics_total": len(all_topics),
        "topics_completed": sum(1 for t in all_topics if t["status"] == "completado"),
        "next_topic": next_topic,
    }


@router.get("/interests")
def list_interests(db: Session = Depends(get_db)):
    states = topic_states(db)
    areas = []
    for area in intereses.AREAS:
        summary = _area_summary(area, states)
        areas.append({k: summary[k] for k in ("slug", "title", "description", "percent", "topics_total", "topics_completed", "total_hours")}
                     | {"blocks": len(summary["blocks"])})
    return {"areas": areas}


@router.get("/interests/{slug}")
def get_interest(slug: str, db: Session = Depends(get_db)):
    area = intereses.get_area(slug)
    if not area:
        raise HTTPException(404, "Área no encontrada")
    return _area_summary(area, topic_states(db))
