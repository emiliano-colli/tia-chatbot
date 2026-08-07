from datetime import datetime
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("America/Buenos_Aires")

_DIAS = (
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado",
    "domingo",
)
_MESES = (
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
)

GET_CURRENT_DATETIME_TOOL = {
    "type": "function",
    "function": {
        "name": "get_current_datetime",
        "description": (
            "Obtiene la fecha y hora actuales en America/Buenos_Aires "
            "(día de la semana, fecha y hora en español). Usala cuando "
            "necesites interpretar referencias temporales como hoy, "
            "mañana o esta semana."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
}

CHATBOT_TOOLS = [GET_CURRENT_DATETIME_TOOL]


def get_current_datetime() -> str:
    """Fecha/hora actual en Buenos Aires, en español."""
    now = datetime.now(TIMEZONE)
    dia = _DIAS[now.weekday()]
    mes = _MESES[now.month - 1]
    return f"{dia} {now.day} de {mes} de {now.year}, {now.hour:02d}:{now.minute:02d}"


def run_tool(name: str, arguments: str | None = None) -> str:
    """Ejecuta una tool conocida por nombre."""
    if name == "get_current_datetime":
        return get_current_datetime()
    raise ValueError(f"Tool desconocida: {name}")
