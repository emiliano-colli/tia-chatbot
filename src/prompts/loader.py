from pathlib import Path

PROMPT_PATH = Path(__file__).parent / "system_prompt.md"

def load_system_prompt() -> str:
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"No se encontró el prompt en {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")
