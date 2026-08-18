import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from app.api import app
from src.chatbot import TiaChatbot
from src.notifications.ping import SessionSummary
from src.utils.session_end import SESSION_END_REPLY


def test_ask_farewell_ends_session_without_llm():
    bot = TiaChatbot(start_idle_watcher=False)
    bot.sessions["farewell-session"] = [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "¡Hola!"},
    ]
    bot.last_activity["farewell-session"] = datetime.now(timezone.utc)

    fake = SessionSummary(
        name="No provisto",
        phone="No provisto",
        interests="Ver log / no detectado",
        log="Hola",
    )
    with patch.object(bot.client.chat.completions, "create") as mock_create:
        with patch("src.chatbot.build_session_summary", return_value=fake):
            with patch("src.chatbot.send_admin_ping") as mock_send:
                result = bot.ask("farewell-session", "chau")

    assert result.reply == SESSION_END_REPLY
    mock_create.assert_not_called()
    mock_send.assert_not_called()
    assert "farewell-session" not in bot.sessions


def test_ask_farewell_without_session_skips_ping():
    bot = TiaChatbot(start_idle_watcher=False)

    with patch.object(bot.client.chat.completions, "create") as mock_create:
        with patch("src.chatbot.send_admin_ping") as mock_send:
            result = bot.ask("new-session", "chau")

    assert result.reply == SESSION_END_REPLY
    mock_create.assert_not_called()
    mock_send.assert_not_called()
    assert "new-session" not in bot.sessions


def test_get_root_returns_html():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "TIA" in response.text
    assert "/static/logo-trama.jpg" in response.text
    assert 'id="consulta-id"' in response.text
    assert (
        "Preguntame sobre clases de yoga, entrenamiento funcional, "
        "talleres, servicios de salud, bienestar y más 🌿"
    ) in response.text


def test_chat_farewell_via_api():
    client = TestClient(app)
    bot = TiaChatbot(start_idle_watcher=False)
    bot.sessions["api-farewell"] = [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "info de yoga"},
    ]
    bot.last_activity["api-farewell"] = datetime.now(timezone.utc)

    fake = SessionSummary(
        name="No provisto",
        phone="No provisto",
        interests="yoga",
        log="info de yoga",
    )
    with patch("app.api.bot", bot):
        with patch("src.chatbot.build_session_summary", return_value=fake):
            with patch("src.chatbot.send_admin_ping") as mock_send:
                with patch.object(bot.client.chat.completions, "create") as mock_create:
                    response = client.post(
                        "/chat",
                        json={"session_id": "api-farewell", "message": "chau"},
                    )

    assert response.status_code == 200
    assert response.json()["reply"] == SESSION_END_REPLY
    mock_create.assert_not_called()
    mock_send.assert_not_called()
    assert "api-farewell" not in bot.sessions
