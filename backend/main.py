from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="Sistema de Rutas Interdepartamentales",
    description="API para consulta de rutas entre ciudades de Guatemala usando Prolog",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/")
def raiz():
    return {"mensaje": "Sistema de Rutas Interdepartamentales", "estado": "activo"}
