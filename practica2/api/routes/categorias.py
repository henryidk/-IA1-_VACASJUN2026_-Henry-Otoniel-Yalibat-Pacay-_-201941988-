from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Categoria
from dependencies import get_admin_session
from telegram_notify import notificar

router = APIRouter(prefix="/categorias", tags=["categorias"])


class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


@router.get("/")
def listar(db: Session = Depends(get_db)):
    return db.query(Categoria).all()


@router.get("/{id}")
def obtener(id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.post("/")
def crear(data: CategoriaCreate, db: Session = Depends(get_db), admin=Depends(get_admin_session)):
    if not admin:
        raise HTTPException(status_code=401, detail="No autenticado")
    if db.query(Categoria).filter(Categoria.nombre == data.nombre).first():
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
    categoria = Categoria(**data.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    notificar(db, f"Nueva categoria agregada: {categoria.nombre}")
    return categoria


@router.put("/{id}")
def actualizar(id: int, data: CategoriaUpdate, db: Session = Depends(get_db), admin=Depends(get_admin_session)):
    if not admin:
        raise HTTPException(status_code=401, detail="No autenticado")
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for campo, valor in data.model_dump(exclude_none=True).items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria


@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db), admin=Depends(get_admin_session)):
    if not admin:
        raise HTTPException(status_code=401, detail="No autenticado")
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria)
    db.commit()
    return {"mensaje": "Categoría eliminada"}
