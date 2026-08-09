import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.session_end import is_session_end_message


def test_session_end_phrases():
    assert is_session_end_message("salir")
    assert is_session_end_message("Chau!")
    assert is_session_end_message("me fui")
    assert is_session_end_message("terminé")
    assert is_session_end_message("fin")
    assert is_session_end_message("listo")
    assert is_session_end_message("cerramos acá")
    assert is_session_end_message("hasta luego")
    assert is_session_end_message("quedamos así")
    assert is_session_end_message("quedamos asi")


def test_non_end_messages():
    assert not is_session_end_message("Hola")
    assert not is_session_end_message("quiero saber qué clases dan")
    assert not is_session_end_message("si lo tengo")
    assert not is_session_end_message("Emiliano 1167462412")
    assert not is_session_end_message("")
