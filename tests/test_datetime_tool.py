import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tools.datetime_tool import get_current_datetime, run_tool


def test_get_current_datetime_spanish_format_and_timezone():
    result = get_current_datetime()
    now = datetime.now(ZoneInfo("America/Buenos_Aires"))

    dias = (
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo",
    )
    meses = (
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

    assert dias[now.weekday()] in result
    assert meses[now.month - 1] in result
    assert str(now.year) in result
    assert f"{now.day}" in result
    assert ":" in result


def test_run_tool_dispatches_get_current_datetime():
    result = run_tool("get_current_datetime")
    assert isinstance(result, str)
    assert len(result) > 0
