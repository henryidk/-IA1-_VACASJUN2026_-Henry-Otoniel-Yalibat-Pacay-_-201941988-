from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Pregunta

router = APIRouter(tags=["bot"])

MENSAJE_FALLBACK = "Lo siento, no encontré información sobre esa consulta. Por favor intenta con otras palabras o contacta directamente con nosotros."


@router.get("/consulta")
def consultar(q: str, db: Session = Depends(get_db)):
    termino = f"%{q.strip()}%"
    pregunta = (
        db.query(Pregunta)
        .filter(Pregunta.activa == True)
        .filter(
            func.unaccent(Pregunta.pregunta).ilike(func.unaccent(termino)) |
            func.unaccent(Pregunta.keyw).ilike(func.unaccent(termino))
        )
        .first()
    )
    if pregunta:
        return {"encontrado": True, "respuesta": pregunta.respuesta, "pregunta_id": pregunta.id}
    return {"encontrado": False, "respuesta": MENSAJE_FALLBACK, "pregunta_id": None}
