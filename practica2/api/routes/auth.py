from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db
from models import UsuarioAdmin
from dependencies import get_admin_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/login")
def login_page(request: Request, admin=Depends(get_admin_session)):
    if admin:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(UsuarioAdmin).filter(UsuarioAdmin.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": "Usuario o contraseña incorrectos"}
        )
    request.session["admin"] = user.username
    return RedirectResponse(url="/", status_code=302)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)
