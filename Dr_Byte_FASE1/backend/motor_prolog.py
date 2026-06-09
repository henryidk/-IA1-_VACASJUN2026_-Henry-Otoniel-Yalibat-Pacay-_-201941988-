from pyswip import Prolog
import threading
import config

_lock = threading.Lock()
_prolog = None


def _get_prolog():
    global _prolog
    if _prolog is None:
        _prolog = Prolog()
        _prolog.consult(config.PROLOG_FILE)
    return _prolog


def obtener_diagnostico(sintomas):
    with _lock:
        prolog = _get_prolog()
        lista = '[' + ','.join(sintomas) + ']'
        query = f'diagnostico_completo({lista}, Falla, Recomendaciones)'

        resultados = list(prolog.query(query))
        if not resultados:
            return None

        falla = str(resultados[0]['Falla'])
        recomendaciones = [str(r) for r in resultados[0]['Recomendaciones']]

        desc_resultado = list(prolog.query(f'descripcion_falla({falla}, Descripcion)'))
        descripcion = str(desc_resultado[0]['Descripcion']) if desc_resultado else falla

        return {
            'falla': falla,
            'descripcion': descripcion,
            'recomendaciones': recomendaciones
        }


def obtener_sintomas():
    with _lock:
        prolog = _get_prolog()
        resultados = list(prolog.query('sintoma(S), descripcion_sintoma(S, D)'))
        return [{'id': str(r['S']), 'descripcion': str(r['D'])} for r in resultados]
