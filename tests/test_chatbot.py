import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chatbot import AskResult, TiaChatbot


def test_ask_returns_string():
    bot = TiaChatbot()
    result = bot.ask("test-session", "Hola")
    assert isinstance(result, AskResult)
    assert isinstance(result.reply, str)
    assert len(result.reply) > 0
    assert result.consulta_id == 1
