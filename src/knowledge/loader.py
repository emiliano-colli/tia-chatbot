import re
from pathlib import Path

KNOWLEDGE_PATH = Path(__file__).resolve().parent / "cronograma.md"
STATIC_ROOT = Path(__file__).resolve().parents[2] / "app" / "static"
_STATIC_HREF_RE = re.compile(r"/static/([^\s<)\]\"']+)")


def _line_keeps_existing_static_files(line: str) -> bool:
    """Drop a knowledge line if it cites /static/... files that are not on disk."""
    missing = False
    found = False
    for match in _STATIC_HREF_RE.finditer(line):
        found = True
        rel = match.group(1).rstrip(".,;:!?")
        if not (STATIC_ROOT / rel).is_file():
            missing = True
            break
    if not found:
        return True
    return not missing


def load_knowledge() -> str:
    if not KNOWLEDGE_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró la base de conocimientos en {KNOWLEDGE_PATH}"
        )
    raw = KNOWLEDGE_PATH.read_text(encoding="utf-8")
    kept = [
        line
        for line in raw.splitlines(keepends=True)
        if _line_keeps_existing_static_files(line)
    ]
    return "".join(kept)
