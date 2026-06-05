from backend.prolog_integration.prolog_engine import PrologEngine
import os

class RouteService:
    def __init__(self):
        self._engine = PrologEngine()
        self._nuevas_ciudades: list[str] = []
        self._nuevas_conexiones: list[tuple] = []

    def _normalizar(self, nombre: str) -> str:
        return nombre.strip().lower().replace(" ", "_")

    def obtener_ciudades(self) -> list[str]:
        return self._engine.listar_ciudades()

    def _validar(self, origen: str, destino: str) -> dict | None:
        origen_n = self._normalizar(origen)
        destino_n = self._normalizar(destino)

        if origen_n == destino_n:
            return {"error": "El origen y el destino no pueden ser la misma ciudad."}
        if not self._engine.ciudad_valida(origen_n):
            return {"error": f"La ciudad '{origen}' no existe en la base de conocimiento."}
        if not self._engine.ciudad_valida(destino_n):
            return {"error": f"La ciudad '{destino}' no existe en la base de conocimiento."}
        return None

    def buscar_rutas(self, origen: str, destino: str) -> dict:
        error = self._validar(origen, destino)
        if error:
            return error

        origen_n = self._normalizar(origen)
        destino_n = self._normalizar(destino)

        if not self._engine.hay_ruta(origen_n, destino_n):
            return {"error": f"No existe ninguna ruta entre '{origen}' y '{destino}'."}

        rutas = self._engine.obtener_todas_las_rutas(origen_n, destino_n)
        distancias = [r["distancia"] for r in rutas]

        return {
            "origen": origen_n,
            "destino": destino_n,
            "rutas": rutas,
            "estadisticas": {
                "total_rutas": len(rutas),
                "distancia_minima": min(distancias),
                "distancia_maxima": max(distancias),
                "distancia_promedio": round(sum(distancias) / len(distancias), 2)
            }
        }

    def buscar_ruta_mas_corta(self, origen: str, destino: str) -> dict:
        error = self._validar(origen, destino)
        if error:
            return error

        origen_n = self._normalizar(origen)
        destino_n = self._normalizar(destino)

        ruta = self._engine.obtener_ruta_mas_corta(origen_n, destino_n)
        if not ruta:
            return {"error": f"No existe ninguna ruta entre '{origen}' y '{destino}'."}

        return {"origen": origen_n, "destino": destino_n, "ruta_mas_corta": ruta}

    def agregar_ciudad_sesion(self, ciudad: str, conexiones: list[dict]) -> dict:
        ciudad_n = self._normalizar(ciudad)
        todas = self._engine.listar_ciudades() + self._nuevas_ciudades

        if ciudad_n in todas:
            return {"error": f"La ciudad '{ciudad_n}' ya existe."}

        for conn in conexiones:
            destino_conn = self._normalizar(conn["destino"])
            if destino_conn not in todas:
                return {"error": f"La ciudad de conexión '{conn['destino']}' no existe."}
            if not isinstance(conn.get("distancia"), (int, float)) or conn["distancia"] <= 0:
                return {"error": "La distancia debe ser un número positivo."}

        self._nuevas_ciudades.append(ciudad_n)
        for conn in conexiones:
            self._nuevas_conexiones.append(
                (ciudad_n, self._normalizar(conn["destino"]), int(conn["distancia"]))
            )

        return {"mensaje": f"Ciudad '{ciudad_n}' agregada a la sesión.", "ciudad": ciudad_n}

    def obtener_sesion(self) -> dict:
        return {
            "nuevas_ciudades": self._nuevas_ciudades,
            "nuevas_conexiones": [
                {"origen": o, "destino": d, "distancia": dist}
                for o, d, dist in self._nuevas_conexiones
            ]
        }

    def confirmar_cambios(self) -> dict:
        if not self._nuevas_ciudades:
            return {"error": "No hay ciudades nuevas en la sesión para confirmar."}

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        extended_path = os.path.join(base_dir, "prolog", "rutas_extended.pl")

        # assertz agrega hechos sin reemplazar los ya definidos en rutas.pl
        lineas = ["% Archivo generado automaticamente — extension de rutas.pl\n\n"]
        for ciudad in self._nuevas_ciudades:
            lineas.append(f":- assertz(ciudad({ciudad})).\n")
        lineas.append("\n")
        for origen, destino, distancia in self._nuevas_conexiones:
            lineas.append(f":- assertz(conexion({origen}, {destino}, {distancia})).\n")

        with open(extended_path, "w", encoding="utf-8") as f:
            f.writelines(lineas)

        self._engine.recargar()

        ciudades_agregadas = list(self._nuevas_ciudades)
        self._nuevas_ciudades.clear()
        self._nuevas_conexiones.clear()

        return {
            "mensaje": "Cambios confirmados y base de conocimiento actualizada.",
            "ciudades_agregadas": ciudades_agregadas,
            "archivo_generado": "prolog/rutas_extended.pl"
        }

    def limpiar_sesion(self) -> dict:
        self._nuevas_ciudades.clear()
        self._nuevas_conexiones.clear()
        return {"mensaje": "Sesión limpiada. No se aplicaron cambios."}


# Instancia única compartida por toda la aplicación
route_service = RouteService()
