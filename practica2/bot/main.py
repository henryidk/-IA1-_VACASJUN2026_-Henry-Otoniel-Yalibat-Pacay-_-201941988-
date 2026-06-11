import os
import logging
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "http://api:8000")


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Soy SmartBot, tu asistente de consultas automatizado.\n\n"
        "Escribe tu pregunta y te responderé con la información disponible.\n\n"
        "Usa /ayuda para ver cómo funciona o /categorias para ver los temas disponibles."
    )


async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Cómo usar SmartBot:\n\n"
        "1. Escribe tu pregunta directamente en el chat.\n"
        "2. Recibirás una respuesta automática basada en nuestra base de datos.\n"
        "3. Si no encuentro respuesta, te lo haré saber.\n\n"
        "Comandos disponibles:\n"
        "/start - Mensaje de bienvenida\n"
        "/ayuda - Muestra esta ayuda\n"
        "/categorias - Lista los temas disponibles"
    )


async def cmd_categorias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{API_URL}/categorias/")
            categorias = response.json()

        if not categorias:
            await update.message.reply_text("No hay categorías disponibles en este momento.")
            return

        texto = "Temas disponibles:\n\n"
        for cat in categorias:
            texto += f"• {cat['nombre']}"
            if cat.get("descripcion"):
                texto += f" — {cat['descripcion']}"
            texto += "\n"

        await update.message.reply_text(texto)
    except httpx.RequestError:
        await update.message.reply_text("No se pudo obtener las categorías. Intenta más tarde.")


async def handle_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    usuario = update.message.from_user.username or update.message.from_user.first_name

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{API_URL}/consulta", params={"q": texto})
            data = response.json()
        await update.message.reply_text(data["respuesta"])
    except httpx.RequestError:
        logging.error(f"No se pudo conectar a la API para consulta de: {usuario}")
        await update.message.reply_text("El servicio no está disponible en este momento. Intenta más tarde.")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        await update.message.reply_text("Ocurrió un error al procesar tu consulta. Intenta de nuevo.")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ayuda", cmd_ayuda))
    app.add_handler(CommandHandler("categorias", cmd_categorias))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mensaje))
    logging.info("Bot iniciado y escuchando mensajes...")
    app.run_polling()
