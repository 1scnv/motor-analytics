import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from agent.parser import SessionInfo, parse_ibt

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


def test_parse_ibt_returns_session_info(parsed_ibt):
    session, _ = parsed_ibt
    assert isinstance(session, SessionInfo)


def test_session_info_fields(parsed_ibt):
    session, _ = parsed_ibt
    assert session.track == "mexicocity gp"
    assert session.car == "Ferrari 296 GT3"
    assert session.session_type == "Offline Testing"
    assert session.total_laps > 0
    assert session.best_lap_time > 0
    assert session.ibt_filename.endswith(".ibt")


def test_parse_ibt_returns_telemetry_records(parsed_ibt):
    _, telemetry = parsed_ibt
    assert isinstance(telemetry, list)
    assert len(telemetry) > 0


def test_telemetry_record_has_expected_channels(parsed_ibt):
    _, telemetry = parsed_ibt
    expected_channels = {
        "SessionTime",
        "Lap",
        "LapDistPct",
        "Speed",
        "Throttle",
        "Brake",
        "Gear",
        "RPM",
    }
    assert expected_channels.issubset(telemetry[0].keys())


def test_telemetry_values_are_numeric(parsed_ibt):
    _, telemetry = parsed_ibt
    record = telemetry[0]
    assert isinstance(record["Speed"], float)
    assert isinstance(record["Lap"], int)
    assert isinstance(record["Throttle"], float)


def test_throttle_range(parsed_ibt):
    _, telemetry = parsed_ibt
    throttle_values = [r["Throttle"] for r in telemetry]
    assert all(-0.001 <= v <= 1.001 for v in throttle_values)


def test_brake_range(parsed_ibt):
    _, telemetry = parsed_ibt
    brake_values = [r["Brake"] for r in telemetry]
    assert all(-0.001 <= v <= 1.001 for v in brake_values)


def test_invalid_file_raises_error():
    with pytest.raises(FileNotFoundError):
        parse_ibt("/nonexistent/file.ibt")
