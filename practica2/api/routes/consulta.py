import unicodedata
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Pregunta

router = APIRouter(tags=["bot"])

MENSAJE_FALLBACK = "Lo siento, no encontré información sobre esa consulta. Por favor intenta con otras palabras o contacta directamente con nosotros."


def _normalizar(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode("ascii")


@router.get("/consulta")
def consultar(q: str, db: Session = Depends(get_db)):
    entrada = _normalizar(q.strip())
    if not entrada:
        return {"encontrado": False, "respuesta": MENSAJE_FALLBACK, "pregunta_id": None}

    todas = db.query(Pregunta).filter(Pregunta.activa == True).all()

    # Paso 1: buscar por keywords
    for p in todas:
        if p.keyw:
            keywords = [_normalizar(k.strip()) for k in p.keyw.split(",") if k.strip()]
            if any(kw in entrada for kw in keywords):
                return {"encontrado": True, "respuesta": p.respuesta, "pregunta_id": p.id}

    # Paso 2: buscar en el texto de la pregunta
    for p in todas:
        if _normalizar(p.pregunta) in entrada or entrada in _normalizar(p.pregunta):
            return {"encontrado": True, "respuesta": p.respuesta, "pregunta_id": p.id}

    return {"encontrado": False, "respuesta": MENSAJE_FALLBACK, "pregunta_id": None}
