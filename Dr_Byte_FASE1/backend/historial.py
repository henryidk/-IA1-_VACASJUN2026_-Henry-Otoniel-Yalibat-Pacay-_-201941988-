import json
import os
import threading
from datetime import datetime
import config

_lock = threading.Lock()


def _leer_historial():
    if not os.path.exists(config.HISTORY_PATH):
        return []
    with open(config.HISTORY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _escribir_historial(datos):
    os.makedirs(os.path.dirname(config.HISTORY_PATH), exist_ok=True)
    with open(config.HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def guardar_diagnostico(sintomas, falla, descripcion, recomendaciones):
    with _lock:
        historial = _leer_historial()

        entrada = {
            'id': len(historial) + 1,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sintomas': sintomas,
            'falla': falla,
            'descripcion': descripcion,
            'recomendaciones': recomendaciones
        }

        historial.append(entrada)
        _escribir_historial(historial)
        return entrada


def obtener_historial():
    with _lock:
        return _leer_historial()


def obtener_por_id(id_diagnostico):
    with _lock:
        historial = _leer_historial()
        for entrada in historial:
            if entrada['id'] == id_diagnostico:
                return entrada
        return None
