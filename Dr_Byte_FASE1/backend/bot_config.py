import json
import os
import threading
import config

_lock = threading.Lock()

_CONFIG_PATH = os.path.join(os.path.dirname(config.HISTORY_PATH), 'bot_config.json')

_DEFAULTS = {
    'token':      '',
    'chat_id':    '',
    'activo':     True,
    'encabezado': 'Nuevo diagnóstico — Doctor Byte',
}


def _leer_archivo():
    if not os.path.exists(_CONFIG_PATH):
        return {}
    with open(_CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _escribir_archivo(datos):
    os.makedirs(os.path.dirname(_CONFIG_PATH), exist_ok=True)
    with open(_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def leer_config():
    with _lock:
        guardado = _leer_archivo()
        return {
            'token':      guardado.get('token')      or config.TELEGRAM_TOKEN,
            'chat_id':    guardado.get('chat_id')    or config.TELEGRAM_CHAT_ID,
            'activo':     guardado.get('activo',     _DEFAULTS['activo']),
            'encabezado': guardado.get('encabezado') or _DEFAULTS['encabezado'],
        }


def guardar_config(datos):
    with _lock:
        actual = _leer_archivo()
        actual.update({
            'token':      datos.get('token',      actual.get('token',      '')),
            'chat_id':    datos.get('chat_id',    actual.get('chat_id',    '')),
            'activo':     datos.get('activo',     actual.get('activo',     True)),
            'encabezado': datos.get('encabezado', actual.get('encabezado', _DEFAULTS['encabezado'])),
        })
        _escribir_archivo(actual)

    # Si el token cambió, forzar recreación del objeto Bot
    import telegram_bot
    telegram_bot.resetear_bot()
