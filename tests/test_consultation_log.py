import csv
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chatbot import TiaChatbot
from src.config import config
from src.notifications.consultation_log import next_consulta_id
from src.notifications.ping import SessionSummary, format_ping_email, has_contact


def _read_csv_rows():
    path = Path(config.CONSULTATION_LOG_PATH)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_consulta_ids_are_correlative():
    assert next_consulta_id() == 1
    assert next_consulta_id() == 2
    assert next_consulta_id() == 3


def test_has_contact_requires_name_or_phone():
    empty = SessionSummary(
        name="No provisto",
        phone="No provisto",
        interests="yoga",
        log="Hola",
    )
    named = SessionSummary(
        name="Ana", phone="No provisto", interests="yoga", log="x"
    )
    phoned = SessionSummary(
        name="No provisto", phone="1167462412", interests="", log="x"
    )
    assert has_contact(empty) is False
    assert has_contact(named) is True
    assert has_contact(phoned) is True


def test_hola_close_writes_csv_without_ping():
    bot = TiaChatbot(start_idle_watcher=False)
    bot.sessions["s-hola"] = [
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "¡Hola!"},
    ]
    bot.last_activity["s-hola"] = datetime.now(timezone.utc)
    bot.consulta_ids["s-hola"] = next_consulta_id()
    bot.origins["s-hola"] = "web"

    fake = SessionSummary(
        name="No provisto",
        phone="No provisto",
        interests="Ver log / no detectado",
        log="Hola",
    )
    with patch("src.chatbot.build_session_summary", return_value=fake):
        with patch("src.chatbot.send_admin_ping") as mock_send:
            assert bot.end_session("s-hola", reason="timeout") is True

    mock_send.assert_not_called()
    rows = _read_csv_rows()
    assert len(rows) == 1
    assert rows[0]["id"] == "1"
    assert rows[0]["origen"] == "web"
    assert rows[0]["reason"] == "timeout"
    assert rows[0]["nombre"] == "No provisto"


def test_contact_close_writes_csv_and_pings():
    bot = TiaChatbot(start_idle_watcher=False)
    bot.sessions["s-ana"] = [
        {"role": "user", "content": "me llamo Ana 1167462412"},
        {"role": "assistant", "content": "Hola Ana"},
    ]
    bot.last_activity["s-ana"] = datetime.now(timezone.utc)
    bot.consulta_ids["s-ana"] = next_consulta_id()
    bot.origins["s-ana"] = "cli"

    fake = SessionSummary(
        name="Ana",
        phone="1167462412",
        interests="yoga",
        log="me llamo Ana",
    )
    with patch("src.chatbot.build_session_summary", return_value=fake):
        with patch("src.chatbot.send_admin_ping") as mock_send:
            assert bot.end_session("s-ana", reason="formal") is True
            mock_send.assert_called_once()
            sent = mock_send.call_args[0][0]
            assert sent.consulta_id == 1
            assert sent.origin == "cli"

    rows = _read_csv_rows()
    assert rows[0]["nombre"] == "Ana"
    assert rows[0]["telefono"] == "1167462412"
    assert rows[0]["origen"] == "cli"


def test_format_ping_email_includes_id_and_origin():
    summary = SessionSummary(
        name="Ana",
        phone="1167462412",
        interests="Yoga Postparto",
        log="hola",
        consulta_id=42,
        origin="web",
    )
    subject, body = format_ping_email(summary)
    assert subject == "Nueva consulta TIA #42 — Ana / 1167462412 / Yoga Postparto"
    assert "ID: 42" in body
    assert "Origen: web" in body


def test_web_origin_default_on_injected_session():
    bot = TiaChatbot(start_idle_watcher=False)
    bot.sessions["s-web"] = [{"role": "user", "content": "Hola"}]
    bot.last_activity["s-web"] = datetime.now(timezone.utc)
    fake = SessionSummary(
        name="No provisto",
        phone="No provisto",
        interests="Ver log / no detectado",
        log="Hola",
    )
    with patch("src.chatbot.build_session_summary", return_value=fake):
        with patch("src.chatbot.send_admin_ping"):
            bot.end_session("s-web", reason="formal")
    assert _read_csv_rows()[0]["origen"] == "web"
