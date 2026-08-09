import json
import re
from dataclasses import dataclass

from src.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

_PHONE_RE = re.compile(
    r"(?:\+?54[\s-]?)?(?:9[\s-]?)?(?:\d{2,4}[\s-]?)?\d{6,10}|\b\d{8,13}\b"
)
_NAME_RE = re.compile(
    r"(?:me llamo|mi nombre es|soy)\s+"
    r"([A-ZÁÉÍÓÚÑÜ][\wáéíóúñü]+(?:\s+[A-ZÁÉÍÓÚÑÜ][\wáéíóúñü]+){0,3})",
    re.IGNORECASE,
)
_ACTIVITY_KEYWORDS = (
    "yoga",
    "prenatal",
    "postparto",
    "post-parto",
    "esferokinesis",
    "hatha",
    "funcional",
    "movida vital",
    "masaje",
    "kinesiolog",
    "psicolog",
    "lactancia",
    "taller",
    "parto",
)

_SUMMARY_SYSTEM_PROMPT = """\
Sos un extractor de datos de una conversación entre un usuario y TIA (asistente de TRAMA).
A partir del diálogo, devolvé SOLO un JSON con estas claves:
- "nombre": nombre de la persona interesada, o null si no aparece
- "telefono": teléfono de contacto, o null si no aparece
- "intereses": actividad/servicio de interés (si eligió por número de menú, resolvé el nombre de la actividad), o null si no se puede determinar

Reglas:
- Usá únicamente información del diálogo; no inventes.
- Nombre y teléfono pueden venir en el mismo mensaje (ej. "Emiliano 1167462412").
- Si el usuario confirma inscripción a una clase mencionada, incluí esa clase en intereses.
"""


@dataclass
class SessionSummary:
    name: str
    phone: str
    interests: str
    log: str

    @property
    def subject_name(self) -> str:
        if self.name and self.name != "No provisto":
            return self.name
        return "Sin identificar"


def _dialog_messages(history: list) -> list[tuple[str, str]]:
    dialog = []
    for msg in history:
        role = msg.get("role")
        if role not in ("user", "assistant"):
            continue
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        label = "Usuario" if role == "user" else "TIA"
        dialog.append((label, content))
    return dialog


def _format_log(dialog: list[tuple[str, str]]) -> str:
    if not dialog:
        return "(sin mensajes)"
    return "\n\n".join(f"{label}: {text}" for label, text in dialog)


def _normalize_field(value, empty: str) -> str:
    if value is None:
        return empty
    text = str(value).strip()
    if not text or text.lower() in ("null", "none", "n/a"):
        return empty
    return text


def _build_session_summary_heuristic(history: list) -> SessionSummary:
    dialog = _dialog_messages(history)
    user_texts = [text for label, text in dialog if label == "Usuario"]
    joined_users = "\n".join(user_texts)

    name = "No provisto"
    for text in user_texts:
        match = _NAME_RE.search(text)
        if match:
            name = match.group(1).strip()
            break

    phone = "No provisto"
    phone_match = _PHONE_RE.search(joined_users.replace(" ", ""))
    if not phone_match:
        phone_match = _PHONE_RE.search(joined_users)
    if phone_match:
        phone = phone_match.group(0).strip()

    interests_found = []
    lower_joined = joined_users.lower()
    for keyword in _ACTIVITY_KEYWORDS:
        if keyword in lower_joined and keyword not in interests_found:
            interests_found.append(keyword)
    interests = ", ".join(interests_found) if interests_found else "Ver log / no detectado"

    return SessionSummary(
        name=name,
        phone=phone,
        interests=interests,
        log=_format_log(dialog),
    )


def _summarize_with_llm(history: list, client) -> dict | None:
    dialog = _dialog_messages(history)
    if not dialog:
        return None

    dialog_text = "\n".join(f"{label}: {text}" for label, text in dialog)
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {"role": "system", "content": _SUMMARY_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Diálogo:\n\n{dialog_text}\n\nRespondé solo JSON.",
            },
        ],
        temperature=0,
        max_tokens=200,
        response_format={"type": "json_object"},
    )
    raw = (response.choices[0].message.content or "").strip()
    if not raw:
        return None
    data = json.loads(raw)
    if not isinstance(data, dict):
        return None
    return data


def build_session_summary(history: list, client=None) -> SessionSummary:
    """Arma el resumen PING. Si hay client OpenAI, intenta LLM y cae a heurística."""
    dialog = _dialog_messages(history)
    log = _format_log(dialog)

    if client is not None:
        try:
            data = _summarize_with_llm(history, client)
            if data is not None:
                return SessionSummary(
                    name=_normalize_field(data.get("nombre"), "No provisto"),
                    phone=_normalize_field(data.get("telefono"), "No provisto"),
                    interests=_normalize_field(
                        data.get("intereses"), "Ver log / no detectado"
                    ),
                    log=log,
                )
        except Exception as exc:
            logger.error("Fallo resumen LLM de sesión; uso heurística: %s", exc)

    return _build_session_summary_heuristic(history)


def format_ping_email(summary: SessionSummary) -> tuple[str, str]:
    subject = f"Nueva consulta TIA — {summary.subject_name}"
    body = (
        f"Contacto: {summary.name} / {summary.phone}\n"
        f"Intereses: {summary.interests}\n"
        f"Log:\n{summary.log}\n"
    )
    return subject, body
