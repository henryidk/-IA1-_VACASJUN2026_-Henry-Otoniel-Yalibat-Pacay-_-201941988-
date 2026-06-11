from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Pregunta
from dependencies import get_admin_session
from telegram_notify import notificar

router = APIRouter(prefix="/preguntas", tags=["preguntas"])


class PreguntaCreate(BaseModel):
    pregunta: str
    respuesta: str
    categoria_id: Optional[int] = None
    activa: Optional[bool] = True


class PreguntaUpdate(BaseModel):
    pregunta: Optional[str] = None
    respuesta: Optional[str] = None
    categoria_id: Optional[int] = None
    activa: Optional[bool] = None


@router.get("/")
def listar(categoria_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Pregunta)
    if categoria_id:
        query = query.filter(Pregunta.categoria_id == categoria_id)
    return query.all()


@router.get("/{id}")
def obtener(id: int, db: Session = Depends(get_db)):
    pregunta = db.query(Pregunta).filter(Pregunta.id == id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return pregunta


@router.post("/")
def crear(data: PreguntaCreate, db: Session = Depends(get_db), admin=Depends(get_admin_session)):
    if not admin:
        raise HTTPException(status_code=401, detail="No autenticado")
    pregunta = Pregunta(**data.model_dump())
    db.add(pregunta)
    db.commit()
    db.refresh(pregunta)
    notificar(db, f"Nueva pregunta agregada: {pregunta.pregunta}")
    return pregunta


@router.put("/{id}")
def actualizar(id: int, data: PreguntaUpdate, db: Session = Depends(get_db), admin=Depends(get_admin_session)):
    if not admin:
        raise HTTPException(status_code=401, detail="No autenticado")
    pregunta = db.query(Pregunta).filter(Pregunta.id == id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    for campo, valor in data.model_dump(exclude_none=True).items():
        setattr(pregunta, campo, valor)
    db.commit()
    db.refresh(pregunta)
    return pregunta


@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db), admin=Depends(get_admin_session)):
    if not admin:
        raise HTTPException(status_code=401, detail="No autenticado")
    pregunta = db.query(Pregunta).filter(Pregunta.id == id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    db.delete(pregunta)
    db.commit()
    return {"mensaje": "Pregunta eliminada"}
