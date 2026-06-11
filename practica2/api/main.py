import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import create_tables
from routes.auth import router as auth_router
from routes.categorias import router as categorias_router
from routes.preguntas import router as preguntas_router
from routes.consulta import router as consulta_router
from routes.config import router as config_router
from routes.panel import router as panel_router
import models  # noqa: F401 — necesario para que SQLAlchemy registre las tablas

app = FastAPI(title="SmartBot API")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "dev-secret"))

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    create_tables()


app.include_router(auth_router)
app.include_router(categorias_router)
app.include_router(preguntas_router)
app.include_router(consulta_router)
app.include_router(config_router)
app.include_router(panel_router)


@app.get("/health")
def health():
    return {"status": "ok"}
