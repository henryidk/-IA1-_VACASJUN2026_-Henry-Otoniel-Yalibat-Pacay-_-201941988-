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


def recargar_prolog():
    global _prolog
    with _lock:
        _prolog = None
        _get_prolog()


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


def obtener_fallas():
    with _lock:
        prolog = _get_prolog()
        resultados = list(prolog.query('falla(F), descripcion_falla(F, D)'))
        return [{'id': str(r['F']), 'descripcion': str(r['D'])} for r in resultados]


def obtener_reglas():
    with _lock:
        prolog = _get_prolog()
        resultados = list(prolog.query('sintoma_falla(S, F)'))
        return [{'sintoma': str(r['S']), 'falla': str(r['F'])} for r in resultados]


def obtener_recomendaciones(id_falla=None):
    with _lock:
        prolog = _get_prolog()
        query = f'recomendacion({id_falla}, R)' if id_falla else 'recomendacion(F, R)'
        resultados = list(prolog.query(query))
        if id_falla:
            return [str(r['R']) for r in resultados]
        return [{'falla': str(r['F']), 'texto': str(r['R'])} for r in resultados]
