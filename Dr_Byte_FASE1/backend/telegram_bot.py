from telegram import Bot
from telegram.error import TelegramError
import asyncio
import config

_bot = None


def get_bot():
    global _bot
    if _bot is None:
        _bot = Bot(token=config.TELEGRAM_TOKEN)
    return _bot


def verificar_conexion():
    async def _verificar():
        bot = get_bot()
        info = await bot.get_me()
        return {'nombre': info.first_name, 'username': info.username}

    return asyncio.run(_verificar())


def enviar_notificacion(id_diagnostico, fecha, sintomas, descripcion, recomendaciones):
    recomendaciones_texto = '\n'.join([f'  • {r}' for r in recomendaciones])
    sintomas_texto = ', '.join(sintomas)

    mensaje = (
        f'🩺 *Nuevo diagnóstico — Doctor Byte*\n\n'
        f'🔢 *ID:* {id_diagnostico}\n'
        f'📅 *Fecha:* {fecha}\n\n'
        f'🔍 *Síntomas reportados:*\n  {sintomas_texto}\n\n'
        f'⚠️ *Falla detectada:*\n  {descripcion}\n\n'
        f'💡 *Recomendaciones:*\n{recomendaciones_texto}'
    )

    async def _enviar():
        bot = get_bot()
        await bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=mensaje,
            parse_mode='Markdown'
        )

    try:
        asyncio.run(_enviar())
    except TelegramError as e:
        print(f'Error al enviar notificación de Telegram: {e}')
