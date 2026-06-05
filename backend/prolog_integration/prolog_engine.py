from pyswip import Prolog
import os

class PrologEngine:
    def __init__(self):
        self._prolog = Prolog()
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self._base_pl = os.path.join(base_dir, "prolog", "rutas.pl")
        self._extended_pl = os.path.join(base_dir, "prolog", "rutas_extended.pl")
        self._cargar()

    def _cargar(self):
        self._prolog.consult(self._base_pl)
        if os.path.exists(self._extended_pl):
            self._prolog.consult(self._extended_pl)

    def recargar(self):
        self._cargar()

    def listar_ciudades(self) -> list[str]:
        resultado = list(self._prolog.query("listar_ciudades(Ciudades)"))
        if resultado:
            return [str(c) for c in resultado[0]["Ciudades"]]
        return []

    def ciudad_valida(self, ciudad: str) -> bool:
        return bool(list(self._prolog.query(f"ciudad_valida({ciudad})")))

    def hay_ruta(self, origen: str, destino: str) -> bool:
        return bool(list(self._prolog.query(f"hay_ruta({origen}, {destino})")))

    def obtener_todas_las_rutas(self, origen: str, destino: str) -> list[dict]:
        resultados = list(self._prolog.query(
            f"ruta({origen}, {destino}, Camino, Distancia)"
        ))
        rutas = [
            {"camino": [str(c) for c in r["Camino"]], "distancia": int(r["Distancia"])}
            for r in resultados
        ]
        return sorted(rutas, key=lambda r: r["distancia"])

    def obtener_ruta_mas_corta(self, origen: str, destino: str) -> dict | None:
        resultado = list(self._prolog.query(
            f"ruta_mas_corta({origen}, {destino}, Camino, Distancia)"
        ))
        if resultado:
            return {
                "camino": [str(c) for c in resultado[0]["Camino"]],
                "distancia": int(resultado[0]["Distancia"])
            }
        return None
