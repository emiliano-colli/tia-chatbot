import re
import unicodedata


_FAREWELL_PHRASES = frozenset(
    {
        "salir",
        "exit",
        "quit",
        "chau",
        "chau chau",
        "adios",
        "adiós",
        "bye",
        "bye bye",
        "fin",
        "termine",
        "terminé",
        "me fui",
        "me voy",
        "nos vemos",
        "cerramos",
        "cerramos aca",
        "cerramos acá",
        "cerramos aqui",
        "cerramos aquí",
        "listo",
        "basta",
        "hasta luego",
        "hasta pronto",
        "eso es todo",
        "nada mas",
        "nada más",
        "ok chau",
        "bueno chau",
        "gracias chau",
        "quedamos asi",
        "quedamos así",
    }
)


def _normalize_message(text: str) -> str:
    text = (text or "").strip().lower()
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[!?.…,;:]+$", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def is_session_end_message(text: str) -> bool:
    """True si el mensaje completo es una despedida / cierre de conversación."""
    normalized = _normalize_message(text)
    if not normalized:
        return False
    if normalized in _FAREWELL_PHRASES:
        return True
    # Variantes sin tilde ya cubiertas en varios casos; probar forma ASCII simple
    ascii_form = (
        unicodedata.normalize("NFD", normalized)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    return ascii_form in _FAREWELL_PHRASES or ascii_form in {
        "adios",
        "termine",
        "cerramos aca",
        "cerramos aqui",
        "nada mas",
    }
