from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Categoria, Pregunta, Config
from telegram_notify import notificar

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def check_auth(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse(url="/login", status_code=302)
    return None


# --- DASHBOARD ---

@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    redir = check_auth(request)
    if redir:
        return redir
    config = db.query(Config).filter(Config.clave == "telegram_chat_id").first()
    return templates.TemplateResponse(request=request, name="dashboard.html", context={
        "admin": request.session.get("admin"),
        "total_preguntas": db.query(Pregunta).count(),
        "total_categorias": db.query(Categoria).count(),
        "chat_id": config.valor if config else "",
    })


# --- PREGUNTAS ---

@router.get("/panel/preguntas")
def listar_preguntas(request: Request, db: Session = Depends(get_db)):
    redir = check_auth(request)
    if redir:
        return redir
    return templates.TemplateResponse(request=request, name="preguntas.html", context={
        "admin": request.session.get("admin"),
        "preguntas": db.query(Pregunta).all(),
        "categorias": db.query(Categoria).all(),
    })


@router.get("/panel/preguntas/nueva")
def nueva_pregunta_form(request: Request, db: Session = Depends(get_db)):
    redir = check_auth(request)
    if redir:
        return redir
    return templates.TemplateResponse(request=request, name="pregunta_form.html", context={
        "admin": request.session.get("admin"),
        "pregunta": None,
        "categorias": db.query(Categoria).all(),
    })


@router.post("/panel/preguntas/nueva")
def crear_pregunta(
    request: Request,
    pregunta: str = Form(...),
    respuesta: str = Form(...),
    categoria_id: Optional[str] = Form(None),
    keyw: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    redir = check_auth(request)
    if redir:
        return redir
    cat_id = int(categoria_id) if categoria_id and categoria_id.strip() else None
    nueva = Pregunta(pregunta=pregunta, respuesta=respuesta, categoria_id=cat_id, activa=True, keyw=keyw)
    db.add(nueva)
    db.commit()
    notificar(db, f"Nueva pregunta agregada: {pregunta}")
    return RedirectResponse(url="/panel/preguntas", status_code=302)


@router.get("/panel/preguntas/{id}/editar")
def editar_pregunta_form(id: int, request: Request, db: Session = Depends(get_db)):
    redir = check_auth(request)
    if redir:
        return redir
    pregunta = db.query(Pregunta).filter(Pregunta.id == id).first()
    if not pregunta:
        return RedirectResponse(url="/panel/preguntas", status_code=302)
    return templates.TemplateResponse(request=request, name="pregunta_form.html", context={
        "admin": request.session.get("admin"),
        "pregunta": pregunta,
        "categorias": db.query(Categoria).all(),
    })


@router.post("/panel/preguntas/{id}/editar")
def actualizar_pregunta(
    id: int,
    request: Request,
    pregunta: str = Form(...),
    respuesta: str = Form(...),
    categoria_id: Optional[str] = Form(None),
    activa: Optional[str] = Form(None),
    keyw: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    redir = check_auth(request)
    if redir:
        return redir
    obj = db.query(Pregunta).filter(Pregunta.id == id).first()
    if obj:
        obj.pregunta = pregunta
        obj.respuesta = respuesta
        obj.categoria_id = int(categoria_id) if categoria_id and categoria_id.strip() else None
        obj.activa = activa == "on"
        obj.keyw = keyw
        db.commit()
        notificar(db, f"Pregunta actualizada: {pregunta}")
    return RedirectResponse(url="/panel/preguntas", status_code=302)


@router.post("/panel/preguntas/{id}/eliminar")
def eliminar_pregunta(id: int, request: Request, db: Session = Depends(get_db)):
    redir = check_auth(request)
    if redir:
        return redir
    obj = db.query(Pregunta).filter(Pregunta.id == id).first()
    if obj:
        notificar(db, f"Pregunta eliminada: {obj.pregunta}")
        db.delete(obj)
        db.commit()
    return RedirectResponse(url="/panel/preguntas", status_code=302)


# --- CATEGORIAS ---

@router.get("/panel/categorias")
def listar_categorias(request: Request, db: Session = Depends(get_db)):
    redir = check_auth(request)
    if redir:
        return redir
    return templates.TemplateResponse(request=request, name="categorias.html", context={
        "admin": request.session.get("admin"),
        "categorias": db.query(Categoria).all(),
    })


@router.get("/panel/categorias/nueva")
def nueva_categoria_form(request: Request):
    redir = check_auth(request)
    if redir:
        return redir
    return templates.TemplateResponse(request=request, name="categoria_form.html", context={
        "admin": request.session.get("admin"),
        "categoria": None,
    })


@router.post("/panel/categorias/nueva")
def crear_categoria(
    request: Request,
    nombre: str = Form(...),
    descripcion: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    redir = check_auth(request)
    if redir:
        return redir
    db.add(Categoria(nombre=nombre, descripcion=descripcion))
    db.commit()
    notificar(db, f"Nueva categoria agregada: {nombre}")
    return RedirectResponse(url="/panel/categorias", status_code=302)


@router.get("/panel/categorias/{id}/editar")
def editar_categoria_form(id: int, request: Request, db: Session = Depends(get_db)):
    redir = check_auth(request)
    if redir:
        return redir
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        return RedirectResponse(url="/panel/categorias", status_code=302)
    return templates.TemplateResponse(request=request, name="categoria_form.html", context={
        "admin": request.session.get("admin"),
        "categoria": categoria,
    })


@router.post("/panel/categorias/{id}/editar")
def actualizar_categoria(
    id: int,
    request: Request,
    nombre: str = Form(...),
    descripcion: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    redir = check_auth(request)
    if redir:
        return redir
    obj = db.query(Categoria).filter(Categoria.id == id).first()
    if obj:
        obj.nombre = nombre
        obj.descripcion = descripcion
        db.commit()
        notificar(db, f"Categoria actualizada: {nombre}")
    return RedirectResponse(url="/panel/categorias", status_code=302)


@router.post("/panel/categorias/{id}/eliminar")
def eliminar_categoria(id: int, request: Request, db: Session = Depends(get_db)):
    redir = check_auth(request)
    if redir:
        return redir
    obj = db.query(Categoria).filter(Categoria.id == id).first()
    if obj:
        notificar(db, f"Categoria eliminada: {obj.nombre}")
        db.delete(obj)
        db.commit()
    return RedirectResponse(url="/panel/categorias", status_code=302)


# --- CONFIG ---

@router.get("/panel/config")
def config_page(request: Request, db: Session = Depends(get_db)):
    redir = check_auth(request)
    if redir:
        return redir
    config = db.query(Config).filter(Config.clave == "telegram_chat_id").first()
    return templates.TemplateResponse(request=request, name="config.html", context={
        "admin": request.session.get("admin"),
        "chat_id": config.valor if config else "",
    })


@router.post("/panel/config")
def actualizar_config(
    request: Request,
    chat_id: str = Form(...),
    db: Session = Depends(get_db),
):
    redir = check_auth(request)
    if redir:
        return redir
    config = db.query(Config).filter(Config.clave == "telegram_chat_id").first()
    if config:
        config.valor = chat_id
        db.commit()
    return RedirectResponse(url="/panel/config?ok=1", status_code=302)
