import os
from pathlib import Path

import pandas as pd
import pytest
from dotenv import load_dotenv

from agent.parser import parse_ibt
from agent.writer import write_parquet

load_dotenv()

IBT_FILE = (
    Path(os.getenv("IRACING_TELEMETRY_PATH", ""))
    / "ferrari296gt3_mexicocity gp 2026-05-18 22-16-59.ibt"
)


@pytest.fixture
def parsed_ibt():
    if not IBT_FILE.exists():
        pytest.skip("IBT file not available — set IRACING_TELEMETRY_PATH in .env")
    return parse_ibt(IBT_FILE)


@pytest.fixture
def written_parquet(parsed_ibt, tmp_path):
    session, telemetry = parsed_ibt
    telemetry_path, session_path = write_parquet(session, telemetry, tmp_path)
    return telemetry_path, session_path, session, telemetry


def test_write_parquet_returns_paths(written_parquet):
    telemetry_path, session_path, _, _ = written_parquet
    assert isinstance(telemetry_path, Path)
    assert isinstance(session_path, Path)


def test_telemetry_file_exists(written_parquet):
    telemetry_path, _, _, _ = written_parquet
    assert telemetry_path.exists()


def test_session_file_exists(written_parquet):
    _, session_path, _, _ = written_parquet
    assert session_path.exists()


def test_telemetry_parquet_content(written_parquet):
    telemetry_path, _, _, telemetry = written_parquet
    df = pd.read_parquet(telemetry_path)
    assert len(df) == len(telemetry)
    assert "Speed" in df.columns
    assert "Throttle" in df.columns
    assert "Lap" in df.columns


def test_session_parquet_content(written_parquet):
    _, session_path, session, _ = written_parquet
    df = pd.read_parquet(session_path)
    assert len(df) == 1
    assert df.iloc[0]["track"] == session.track
    assert df.iloc[0]["car"] == session.car


def test_parquet_partitioned_by_date(written_parquet):
    telemetry_path, session_path, _, _ = written_parquet
    assert "date=" in str(telemetry_path)


def test_skip_existing_file_does_not_overwrite(written_parquet, tmp_path, parsed_ibt):
    telemetry_path, _, _, _ = written_parquet
    mtime_before = telemetry_path.stat().st_mtime

    session, telemetry = parsed_ibt
    write_parquet(session, telemetry, tmp_path)

    mtime_after = telemetry_path.stat().st_mtime
    assert mtime_before == mtime_after  # file was not modified
