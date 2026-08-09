import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.notifications.ping import build_session_summary, format_ping_email
from src.chatbot import TiaChatbot


def test_format_ping_email_with_contact():
    history = [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "Hola, me llamo María Pérez, mi tel es 11-5555-1234"},
        {"role": "assistant", "content": "¡Hola María!"},
        {"role": "user", "content": "Quiero info de yoga prenatal"},
        {"role": "assistant", "content": "Claro, te cuento..."},
    ]
    summary = build_session_summary(history)
    subject, body = format_ping_email(summary)

    assert subject.startswith("Nueva consulta TIA —")
    assert "María Pérez" in subject
    assert "Contacto:" in body
    assert "María Pérez" in body
    assert "Intereses:" in body
    assert "yoga" in body.lower() or "prenatal" in body.lower()
    assert "Log:" in body
    assert "Usuario:" in body
    assert "TIA:" in body


def test_format_ping_email_without_contact():
    history = [
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "¡Hola!"},
    ]
    summary = build_session_summary(history)
    subject, body = format_ping_email(summary)

    assert "Sin identificar" in subject
    assert "No provisto" in body
    assert "Log:" in body


def test_end_session_sends_ping_once():
    bot = TiaChatbot(start_idle_watcher=False)
    bot.sessions["s1"] = [
        {"role": "user", "content": "Hola, me llamo Ana"},
        {"role": "assistant", "content": "Hola Ana"},
    ]
    bot.last_activity["s1"] = datetime.now(timezone.utc)

    with patch("src.chatbot.send_admin_ping") as mock_send:
        assert bot.end_session("s1", reason="formal") is True
        assert mock_send.call_count == 1
        assert "s1" not in bot.sessions
        assert bot.end_session("s1", reason="formal") is False
        assert mock_send.call_count == 1


def test_expire_idle_sessions_uses_timeout():
    bot = TiaChatbot(start_idle_watcher=False)
    bot.sessions["old"] = [{"role": "user", "content": "hola"}]
    bot.last_activity["old"] = datetime.now(timezone.utc) - timedelta(minutes=60)

    with patch("src.chatbot.send_admin_ping") as mock_send:
        with patch("src.chatbot.config") as mock_config:
            mock_config.SESSION_TIMEOUT_MINUTES = 30
            closed = bot.expire_idle_sessions()

    assert closed == ["old"]
    assert mock_send.call_count == 1
    assert "old" not in bot.sessions
