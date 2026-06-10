import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import create_tables

app = FastAPI(title="SmartBot API")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "dev-secret"))

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/health")
def health():
    return {"status": "ok"}
