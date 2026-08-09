import re
from dataclasses import dataclass


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


def build_session_summary(history: list) -> SessionSummary:
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

    log_lines = [f"{label}: {text}" for label, text in dialog]
    log = "\n\n".join(log_lines) if log_lines else "(sin mensajes)"

    return SessionSummary(name=name, phone=phone, interests=interests, log=log)


def format_ping_email(summary: SessionSummary) -> tuple[str, str]:
    subject = f"Nueva consulta TIA — {summary.subject_name}"
    body = (
        f"Contacto: {summary.name} / {summary.phone}\n"
        f"Intereses: {summary.interests}\n"
        f"Log:\n{summary.log}\n"
    )
    return subject, body
