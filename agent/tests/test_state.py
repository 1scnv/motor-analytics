from pathlib import Path

import pytest

from agent.state import is_processed, mark_processed


@pytest.fixture(autouse=True)
def clean_state(tmp_path, monkeypatch):
    """Redirect state file to tmp_path for each test."""
    monkeypatch.setattr("agent.state.STATE_FILE", tmp_path / ".agent_state.json")


def test_file_not_processed_initially():
    assert is_processed("some_session.ibt") is False


def test_mark_processed_sets_file_as_processed():
    filename = "ferrari296gt3_spa_2026-05-18.ibt"
    mark_processed(
        filename,
        Path("data/telemetry/file.parquet"),
        Path("data/sessions/file.parquet"),
    )
    assert is_processed(filename) is True


def test_different_files_are_independent():
    mark_processed(
        "file_a.ibt", Path("data/telemetry/a.parquet"), Path("data/sessions/a.parquet")
    )
    assert is_processed("file_a.ibt") is True
    assert is_processed("file_b.ibt") is False


def test_mark_processed_persists_paths():
    filename = "ferrari296gt3_spa_2026-05-18.ibt"
    telemetry_path = Path("data/bronze/telemetry/date=2026-05-18/ferrari.parquet")
    session_path = Path("data/bronze/sessions/date=2026-05-18/ferrari.parquet")

    mark_processed(filename, telemetry_path, session_path)

    import json

    import agent.state as state_module

    state = json.loads(state_module.STATE_FILE.read_text())
    assert state["processed"][filename]["telemetry_path"] == str(telemetry_path)
    assert state["processed"][filename]["session_path"] == str(session_path)


def test_mark_processed_records_timestamp():
    filename = "ferrari296gt3_spa_2026-05-18.ibt"
    mark_processed(
        filename, Path("data/telemetry/a.parquet"), Path("data/sessions/a.parquet")
    )

    import json

    import agent.state as state_module

    state = json.loads(state_module.STATE_FILE.read_text())
    assert "processed_at" in state["processed"][filename]
