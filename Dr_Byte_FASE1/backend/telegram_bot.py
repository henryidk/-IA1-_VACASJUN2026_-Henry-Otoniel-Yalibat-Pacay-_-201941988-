from telegram import Bot
from telegram.error import TelegramError
import asyncio
import config
import bot_config

_bot = None
_token_actual = None


def resetear_bot():
    global _bot, _token_actual
    _bot = None
    _token_actual = None


def get_bot(token):
    global _bot, _token_actual
    if _bot is None or token != _token_actual:
        _bot = Bot(token=token)
        _token_actual = token
    return _bot


def verificar_conexion():
    cfg = bot_config.leer_config()
    token = cfg['token'] or config.TELEGRAM_TOKEN

    async def _verificar():
        bot = get_bot(token)
        info = await bot.get_me()
        return {'nombre': info.first_name, 'username': info.username}

    return asyncio.run(_verificar())


def enviar_notificacion(id_diagnostico, fecha, sintomas, descripcion, recomendaciones):
    cfg = bot_config.leer_config()

    if not cfg['activo']:
        return

    token      = cfg['token']   or config.TELEGRAM_TOKEN
    chat_id    = cfg['chat_id'] or config.TELEGRAM_CHAT_ID
    encabezado = cfg['encabezado']

    recomendaciones_texto = '\n'.join([f'  • {r}' for r in recomendaciones])
    sintomas_texto = ', '.join(sintomas)

    mensaje = (
        f'{encabezado}\n\n'
        f'*ID:* {id_diagnostico}\n'
        f'*Fecha:* {fecha}\n\n'
        f'*Síntomas reportados:*\n  {sintomas_texto}\n\n'
        f'⚠️ *Falla detectada:*\n  {descripcion}\n\n'
        f'*Recomendaciones:*\n{recomendaciones_texto}'
    )

    async def _enviar():
        bot = get_bot(token)
        await bot.send_message(
            chat_id=chat_id,
            text=mensaje,
            parse_mode='Markdown'
        )

    try:
        asyncio.run(_enviar())
    except TelegramError as e:
        print(f'Error al enviar notificación de Telegram: {e}')
