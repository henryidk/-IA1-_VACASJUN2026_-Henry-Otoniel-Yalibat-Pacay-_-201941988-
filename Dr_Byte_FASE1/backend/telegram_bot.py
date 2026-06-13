import httpx
import config
import bot_config

_API = 'https://api.telegram.org/bot{token}/{method}'


def _post(token, method, **kwargs):
    url = _API.format(token=token, method=method)
    try:
        r = httpx.post(url, json=kwargs, timeout=10)
        return r.json()
    except Exception as e:
        print(f'[Telegram] Error HTTP: {type(e).__name__}: {e}')
        return {}


def resetear_bot():
    pass


def verificar_conexion():
    cfg = bot_config.leer_config()
    token = cfg['token'] or config.TELEGRAM_TOKEN
    resp = _post(token, 'getMe')
    if resp.get('ok'):
        bot = resp['result']
        return {'nombre': bot['first_name'], 'username': bot['username']}
    return {}


def _enviar_mensaje(token, chat_id, texto, parse_mode=None):
    params = {'chat_id': chat_id, 'text': texto}
    if parse_mode:
        params['parse_mode'] = parse_mode
    resp = _post(token, 'sendMessage', **params)
    if not resp.get('ok'):
        print(f'[Telegram] Respuesta no OK: {resp.get("description", resp)}')


def enviar_notificacion(id_diagnostico, fecha, sintomas, descripcion, recomendaciones):
    cfg = bot_config.leer_config()

    token   = cfg['token']   or config.TELEGRAM_TOKEN
    chat_id = cfg['chat_id'] or config.TELEGRAM_CHAT_ID

    if not cfg['activo']:
        _enviar_mensaje(token, chat_id,
                        'Lo sentimos, el bot está en mantenimiento. Regresa más tarde.')
        return

    encabezado            = cfg['encabezado']
    sintomas_texto        = ', '.join(sintomas)
    recomendaciones_texto = '\n'.join([f'  • {r}' for r in recomendaciones])

    mensaje = (
        f'<b>{encabezado}</b>\n\n'
        f'<b>ID:</b> {id_diagnostico}\n'
        f'<b>Fecha:</b> {fecha}\n\n'
        f'<b>Síntomas reportados:</b>\n  {sintomas_texto}\n\n'
        f'⚠️ <b>Falla detectada:</b>\n  {descripcion}\n\n'
        f'<b>Recomendaciones:</b>\n{recomendaciones_texto}'
    )

    _enviar_mensaje(token, chat_id, mensaje, parse_mode='HTML')
