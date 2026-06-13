from telegram import Bot
from telegram.error import TelegramError
import asyncio
import config
import bot_config


def resetear_bot():
    pass


def verificar_conexion():
    cfg = bot_config.leer_config()
    token = cfg['token'] or config.TELEGRAM_TOKEN

    async def _verificar():
        async with Bot(token=token) as bot:
            info = await bot.get_me()
            return {'nombre': info.first_name, 'username': info.username}

    return asyncio.run(_verificar())


def enviar_notificacion(id_diagnostico, fecha, sintomas, descripcion, recomendaciones):
    cfg = bot_config.leer_config()

    token      = cfg['token']   or config.TELEGRAM_TOKEN
    chat_id    = cfg['chat_id'] or config.TELEGRAM_CHAT_ID
    encabezado = cfg['encabezado']

    if not cfg['activo']:
        async def _mantenimiento():
            async with Bot(token=token) as bot:
                await bot.send_message(
                    chat_id=chat_id,
                    text='Lo sentimos, el bot está en mantenimiento. Regresa más tarde.',
                )
        try:
            asyncio.run(_mantenimiento())
        except Exception as e:
            print(f'[Telegram] Error al enviar mensaje de mantenimiento: {type(e).__name__}: {e}')
        return

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
        async with Bot(token=token) as bot:
            await bot.send_message(
                chat_id=chat_id,
                text=mensaje,
                parse_mode='Markdown'
            )

    try:
        asyncio.run(_enviar())
    except Exception as e:
        print(f'[Telegram] Error al enviar notificación: {type(e).__name__}: {e}')
