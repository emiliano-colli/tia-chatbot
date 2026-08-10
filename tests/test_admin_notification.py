import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.notifications.ping import (
    SessionSummary,
    build_session_summary,
    format_ping_email,
)
from src.chatbot import TiaChatbot


def _emilio_menu_history():
    return [
        {"role": "assistant", "content": "¡Hola! 😊 ¿En qué puedo ayudarte hoy?"},
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "¡Hola! 😊 ¿Cómo estás?"},
        {"role": "user", "content": "quiero saber qué clases dan ?"},
        {
            "role": "assistant",
            "content": (
                "¿me pasás tu nombre completo y un teléfono de contacto por favor?"
            ),
        },
        {"role": "user", "content": "Emiliano 1167462412"},
        {
            "role": "assistant",
            "content": (
                "Gracias, Emiliano. Clases:\n"
                "1. Yoga Prenatal\n"
                "8. Yoga Postparto\n"
                "10. Hatha Yoga"
            ),
        },
        {"role": "user", "content": "8"},
        {
            "role": "assistant",
            "content": "Perfecto, Emiliano. Información sobre Yoga Postparto...",
        },
        {"role": "user", "content": "si me quiero inscribir"},
        {"role": "assistant", "content": "¡Genial! Confirmá teléfono..."},
        {"role": "user", "content": "1167462412"},
        {"role": "assistant", "content": "Gracias. ¿Tenés apto médico?"},
        {"role": "user", "content": "si lo tengo"},
        {"role": "assistant", "content": "Listo para inscripción Yoga Postparto."},
    ]


def _mock_llm_client(payload: dict) -> MagicMock:
    client = MagicMock()
    client.chat.completions.create.return_value = MagicMock(
        choices=[
            MagicMock(
                message=MagicMock(content=__import__("json").dumps(payload, ensure_ascii=False))
            )
        ]
    )
    return client


def test_format_ping_email_with_contact_heuristic():
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


def test_llm_summary_name_phone_together_and_menu_interest():
    history = _emilio_menu_history()
    client = _mock_llm_client(
        {
            "nombre": "Emiliano",
            "telefono": "1167462412",
            "intereses": "Yoga Postparto — solicitó inscripción",
        }
    )
    summary = build_session_summary(history, client=client)
    subject, body = format_ping_email(summary)

    assert client.chat.completions.create.called
    assert "Emiliano" in subject
    assert "Emiliano" in body
    assert "1167462412" in body
    assert "Yoga Postparto" in body
    assert "solicitó inscripción" in body
    assert "Usuario: Emiliano 1167462412" in body
    assert "Usuario: 8" in body


def test_llm_summary_marks_appointment_request():
    history = [
        {"role": "user", "content": "Hola, me llamo Laura 1144445555"},
        {"role": "assistant", "content": "Hola Laura"},
        {"role": "user", "content": "quiero sacar turno para masaje"},
        {"role": "assistant", "content": "Te cuento sobre masajes..."},
    ]
    client = _mock_llm_client(
        {
            "nombre": "Laura",
            "telefono": "1144445555",
            "intereses": "Masaje — solicitó turno",
        }
    )
    summary = build_session_summary(history, client=client)
    _, body = format_ping_email(summary)
    assert "Masaje" in body
    assert "solicitó turno" in body


def test_system_prompt_forbids_fake_enrollment():
    from src.prompts.loader import load_system_prompt

    prompt = load_system_prompt()
    assert "LÍMITES: INFORMACIÓN VS. FORMALIZACIÓN" in prompt
    assert "No podés" in prompt or "no lo simules" in prompt
    assert "procedo a registrar tu inscripción" in prompt
    assert "confirmación de inscripción" not in prompt
    assert "horario asignado" not in prompt


def test_llm_failure_falls_back_to_heuristic():
    history = [
        {"role": "user", "content": "me llamo Ana, tel 1199998888"},
        {"role": "assistant", "content": "Hola Ana"},
    ]
    client = MagicMock()
    client.chat.completions.create.side_effect = RuntimeError("api down")
    summary = build_session_summary(history, client=client)
    assert summary.name == "Ana"
    assert "1199998888" in summary.phone


def test_end_session_sends_ping_once():
    bot = TiaChatbot(start_idle_watcher=False)
    bot.sessions["s1"] = [
        {"role": "user", "content": "Hola, me llamo Ana"},
        {"role": "assistant", "content": "Hola Ana"},
    ]
    bot.last_activity["s1"] = datetime.now(timezone.utc)

    fake = SessionSummary(
        name="Ana", phone="No provisto", interests="Ver log / no detectado", log="x"
    )
    with patch("src.chatbot.build_session_summary", return_value=fake):
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

    fake = SessionSummary(
        name="No provisto",
        phone="No provisto",
        interests="Ver log / no detectado",
        log="hola",
    )
    with patch("src.chatbot.build_session_summary", return_value=fake):
        with patch("src.chatbot.send_admin_ping") as mock_send:
            with patch("src.chatbot.config") as mock_config:
                mock_config.SESSION_TIMEOUT_MINUTES = 30
                closed = bot.expire_idle_sessions()

    assert closed == ["old"]
    assert mock_send.call_count == 1
    assert "old" not in bot.sessions
