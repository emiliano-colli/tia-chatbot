import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chatbot import TiaChatbot


def test_ask_returns_string():
    bot = TiaChatbot()
    respuesta = bot.ask("test-session", "Hola")
    assert isinstance(respuesta, str)
    assert len(respuesta) > 0
