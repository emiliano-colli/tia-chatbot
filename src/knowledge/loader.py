import os

KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "cronograma.md")

def load_knowledge() -> str:
    if not os.path.exists(KNOWLEDGE_PATH):
        raise FileNotFoundError(
            f"No se encontró la base de conocimientos en {KNOWLEDGE_PATH}"
        )
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        return f.read()
