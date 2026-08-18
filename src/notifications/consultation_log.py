import csv
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

CSV_FIELDS = [
    "id",
    "closed_at",
    "nombre",
    "telefono",
    "interes",
    "origen",
    "reason",
]

try:
    from zoneinfo import ZoneInfo

    _AR_TZ = ZoneInfo("America/Argentina/Buenos_Aires")
except Exception:
    _AR_TZ = timezone(timedelta(hours=-3))


def _lock_file(handle):
    if os.name == "nt":
        import msvcrt

        handle.seek(0)
        if handle.read(1) == "":
            handle.write("0")
            handle.flush()
        handle.seek(0)
        while True:
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                return
            except OSError:
                time.sleep(0.05)
    else:
        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)


def _unlock_file(handle):
    if os.name == "nt":
        import msvcrt

        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class _FileLock:
    def __init__(self, path: Path):
        self.path = path
        self._handle = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = open(self.path, "a+", encoding="utf-8")
        _lock_file(self._handle)
        return self._handle

    def __exit__(self, exc_type, exc, tb):
        try:
            _unlock_file(self._handle)
        finally:
            self._handle.close()
            self._handle = None


def _seq_lock_path() -> Path:
    seq_path = Path(config.CONSULTATION_SEQ_PATH)
    return seq_path.with_name(seq_path.name + ".lock")


def next_consulta_id() -> int:
    seq_path = Path(config.CONSULTATION_SEQ_PATH)
    seq_path.parent.mkdir(parents=True, exist_ok=True)
    with _FileLock(_seq_lock_path()):
        current = 0
        if seq_path.exists():
            text = seq_path.read_text(encoding="utf-8").strip()
            if text.isdigit():
                current = int(text)
        nxt = current + 1
        seq_path.write_text(str(nxt), encoding="utf-8")
        return nxt


def closed_at_local() -> str:
    return datetime.now(_AR_TZ).strftime("%Y-%m-%d %H:%M")


def append_consultation_row(
    consulta_id: int,
    nombre: str,
    telefono: str,
    interes: str,
    origen: str,
    reason: str,
) -> None:
    path = Path(config.CONSULTATION_LOG_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with _FileLock(_seq_lock_path()):
        new_file = not path.exists() or path.stat().st_size == 0
        with path.open("a", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            if new_file:
                writer.writeheader()
            writer.writerow(
                {
                    "id": consulta_id,
                    "closed_at": closed_at_local(),
                    "nombre": nombre,
                    "telefono": telefono,
                    "interes": interes,
                    "origen": origen,
                    "reason": reason,
                }
            )
    logger.info("Consulta #%s registrada (origen=%s, reason=%s)", consulta_id, origen, reason)
