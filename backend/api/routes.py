from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.route_service import route_service

router = APIRouter()

# --- MODELOS DE SOLICITUD ---

class RutaRequest(BaseModel):
    origen: str
    destino: str

class ConexionRequest(BaseModel):
    destino: str
    distancia: float

class NuevaCiudadRequest(BaseModel):
    ciudad: str
    conexiones: list[ConexionRequest]


# --- ENDPOINTS ---

@router.get("/ciudades", summary="Listar todas las ciudades disponibles")
def listar_ciudades():
    ciudades = route_service.obtener_ciudades()
    return {"ciudades": ciudades, "total": len(ciudades)}


@router.post("/rutas", summary="Obtener todas las rutas entre dos ciudades")
def obtener_rutas(request: RutaRequest):
    resultado = route_service.buscar_rutas(request.origen, request.destino)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado


@router.post("/ruta-corta", summary="Obtener la ruta más corta entre dos ciudades")
def obtener_ruta_corta(request: RutaRequest):
    resultado = route_service.buscar_ruta_mas_corta(request.origen, request.destino)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado


@router.get("/sesion", summary="Ver ciudades pendientes de confirmar en la sesión")
def ver_sesion():
    return route_service.obtener_sesion()


@router.post("/ciudades/nueva", summary="Agregar una ciudad nueva a la sesión")
def agregar_ciudad(request: NuevaCiudadRequest):
    conexiones = [{"destino": c.destino, "distancia": c.distancia} for c in request.conexiones]
    resultado = route_service.agregar_ciudad_sesion(request.ciudad, conexiones)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado


@router.post("/ciudades/confirmar", summary="Confirmar cambios y generar rutas_extended.pl")
def confirmar_cambios():
    resultado = route_service.confirmar_cambios()
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado


@router.delete("/ciudades/sesion", summary="Limpiar la sesión sin aplicar cambios")
def limpiar_sesion():
    return route_service.limpiar_sesion()


@router.delete("/ciudades/restablecer", summary="Eliminar ciudades agregadas y volver a la base original")
def restablecer():
    return route_service.restablecer()
