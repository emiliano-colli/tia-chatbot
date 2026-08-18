import pytest

from src.config import config


@pytest.fixture(autouse=True)
def _consultation_files_in_tmp(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONSULTATION_LOG_PATH", str(tmp_path / "consultas.csv"))
    monkeypatch.setattr(config, "CONSULTATION_SEQ_PATH", str(tmp_path / "consulta_seq.txt"))
