import smtplib
from email.message import EmailMessage

from src.config import config
from src.notifications.ping import SessionSummary, format_ping_email
from src.utils.logger import get_logger

logger = get_logger(__name__)


def send_admin_ping(summary: SessionSummary) -> bool:
    """Envía el PING al admin. Devuelve True si salió OK."""
    if not config.smtp_ready():
        logger.error(
            "No se pudo enviar PING: falta configuración SMTP "
            "(SMTP_USER, SMTP_PASSWORD, MAIL_FROM, ADMIN_EMAIL)."
        )
        return False

    subject, body = format_ping_email(summary)
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = config.MAIL_FROM
    message["To"] = config.ADMIN_EMAIL
    message.set_content(body)

    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=30) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.send_message(message)
        logger.info("PING enviado a admin para contacto=%s", summary.subject_name)
        return True
    except Exception as exc:
        logger.error("Error al enviar PING al admin: %s", exc)
        return False
