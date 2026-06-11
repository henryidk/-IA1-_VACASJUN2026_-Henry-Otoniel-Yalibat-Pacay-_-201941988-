import os
import logging
import httpx
from sqlalchemy.orm import Session
from models import Config

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def _get_chat_id(db: Session) -> str | None:
    config = db.query(Config).filter(Config.clave == "telegram_chat_id").first()
    if config and config.valor and config.valor.strip():
        return config.valor.strip()
    return None


def notificar(db: Session, mensaje: str):
    chat_id = _get_chat_id(db)
    if not chat_id:
        logging.warning("notificar: chat_id no configurado, omitiendo notificacion")
        return
    if not TELEGRAM_TOKEN:
        logging.warning("notificar: TELEGRAM_TOKEN no disponible, omitiendo notificacion")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        resp = httpx.post(url, json={"chat_id": chat_id, "text": mensaje}, timeout=5)
        logging.info(f"notificar: [{resp.status_code}] {mensaje}")
    except Exception as e:
        logging.error(f"notificar: error enviando mensaje — {e}")
