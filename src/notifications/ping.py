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
- "intereses": actividad, servicio o familia de interés, o null solo si el diálogo no nombra ninguna

Reglas:
- Usá únicamente información del diálogo; no inventes.
- Nombre y teléfono pueden venir en el mismo mensaje (ej. "Emiliano 1167462412").
- Preguntar si hay una actividad (ej. "tienen clases de yoga") cuenta como interés. No hace falta menú numérico ni pedido de inscripción.
- Pedir precios, horarios o requisitos de lo ya hablado cuenta como interés, aunque el mensaje sea una sola palabra (ej. "precios").
- Si TIA listó varias variantes de una familia (ej. Yoga Prenatal, Postparto y Hatha) y el usuario no eligió una, en "intereses" poné la familia (ej. "yoga" o "clases de yoga"), no null.
- Si el usuario pidió inscribirse a una actividad, en "intereses" incluí la actividad y la marca "solicitó inscripción" (ej. "Yoga Postparto — solicitó inscripción").
- Si el usuario pidió turno/reserva de un servicio, en "intereses" incluí el servicio y la marca "solicitó turno" (ej. "Masaje — solicitó turno").
- No asumas que la inscripción o el turno ya fueron confirmados por TIA; solo registrá la solicitud si el diálogo la muestra. En una consulta solo informativa no marques inscripción ni turno.
"""


@dataclass
class SessionSummary:
    name: str
    phone: str
    interests: str
    log: str
    consulta_id: int | None = None
    origin: str = ""

    @property
    def subject_name(self) -> str:
        if self.name and self.name != "No provisto":
            return self.name
        return "Sin identificar"


_MISSING_CONTACT = frozenset(
    {
        "",
        "no provisto",
        "sin identificar",
        "null",
        "none",
        "n/a",
        "no se puede determinar",
    }
)
_MISSING_INTEREST = frozenset(
    {
        "",
        "no provisto",
        "sin identificar",
        "ver log / no detectado",
        "null",
        "none",
        "n/a",
        "no se puede determinar",
        "no detectado",
    }
)


def _is_blank(value: str | None, empty: frozenset[str]) -> bool:
    return (value or "").strip().lower().rstrip(".") in empty


def _coalesce_field(llm_value: str, heuristic_value: str, empty: frozenset[str]) -> str:
    if not _is_blank(llm_value, empty):
        return llm_value
    if not _is_blank(heuristic_value, empty):
        return heuristic_value
    return llm_value


def has_contact(summary: SessionSummary) -> bool:
    """True si hay nombre o teléfono reales (placeholders no cuentan)."""
    return (not _is_blank(summary.name, _MISSING_CONTACT)) or (
        not _is_blank(summary.phone, _MISSING_CONTACT)
    )


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
    """Arma el resumen PING. LLM primero; campos vacíos se completan con heurística."""
    heuristic = _build_session_summary_heuristic(history)

    if client is not None:
        try:
            data = _summarize_with_llm(history, client)
            if data is not None:
                return SessionSummary(
                    name=_coalesce_field(
                        _normalize_field(data.get("nombre"), "No provisto"),
                        heuristic.name,
                        _MISSING_CONTACT,
                    ),
                    phone=_coalesce_field(
                        _normalize_field(data.get("telefono"), "No provisto"),
                        heuristic.phone,
                        _MISSING_CONTACT,
                    ),
                    interests=_coalesce_field(
                        _normalize_field(
                            data.get("intereses"), "Ver log / no detectado"
                        ),
                        heuristic.interests,
                        _MISSING_INTEREST,
                    ),
                    log=heuristic.log,
                )
        except Exception as exc:
            logger.error("Fallo resumen LLM de sesión; uso heurística: %s", exc)

    return heuristic


def format_ping_email(summary: SessionSummary) -> tuple[str, str]:
    segments = []
    if not _is_blank(summary.name, _MISSING_CONTACT):
        segments.append(summary.name.strip())
    if not _is_blank(summary.phone, _MISSING_CONTACT):
        segments.append(summary.phone.strip())
    if not _is_blank(summary.interests, _MISSING_INTEREST):
        segments.append(summary.interests.strip())

    id_part = f"#{summary.consulta_id}" if summary.consulta_id is not None else ""
    rest = " / ".join(segments)
    if id_part and rest:
        subject = f"Nueva consulta TIA {id_part} — {rest}"
    elif id_part:
        subject = f"Nueva consulta TIA {id_part}"
    elif rest:
        subject = f"Nueva consulta TIA — {rest}"
    else:
        subject = "Nueva consulta TIA"

    consulta_line = (
        f"ID: {summary.consulta_id}\n" if summary.consulta_id is not None else ""
    )
    origen_line = f"Origen: {summary.origin or '—'}\n"
    body = (
        f"{consulta_line}"
        f"Contacto: {summary.name} / {summary.phone}\n"
        f"Intereses: {summary.interests}\n"
        f"{origen_line}"
        f"Log:\n{summary.log}\n"
    )
    return subject, body
