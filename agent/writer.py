from dataclasses import asdict
from pathlib import Path

import pandas as pd
from loguru import logger

from agent.parser import SessionInfo


def write_parquet(
    session_info: SessionInfo,
    telemetry: list[dict],
    data_path: str | Path,
) -> tuple[Path, Path]:
    """Write session info and telemetry records to Parquet files."""
    data_path = Path(data_path)
    session_date = _extract_date(session_info.ibt_filename)
    stem = _build_stem(session_info.ibt_filename)

    telemetry_path = _write_telemetry(telemetry, data_path, session_date, stem)
    session_path = _write_session(session_info, data_path, session_date, stem)

    return telemetry_path, session_path


def _extract_date(filename: str) -> str:
    """Extract date string from ibt filename (e.g. '2026-05-18')."""
    parts = Path(filename).stem.split(" ")
    for part in parts:
        if len(part) == 10 and part.count("-") == 2:  # matches YYYY-MM-DD
            return part
    return "unknown"


def _build_stem(filename: str) -> str:
    """Build a safe filename stem from ibt filename."""
    return Path(filename).stem.replace(" ", "_")


def _write_telemetry(
    telemetry: list[dict],
    data_path: Path,
    session_date: str,
    stem: str,
) -> Path:
    """Write telemetry records to Parquet."""
    output_path = data_path / "telemetry" / f"date={session_date}" / f"{stem}.parquet"

    if output_path.exists():
        logger.warning(f"Telemetry file already exists, skipping: {output_path}")
        return output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(telemetry)
    df.to_parquet(output_path, index=False)

    logger.info(f"Telemetry written: {output_path} ({len(df)} records)")
    return output_path


def _write_session(
    session_info: SessionInfo,
    data_path: Path,
    session_date: str,
    stem: str,
) -> Path:
    """Write session metadata to Parquet."""
    output_path = data_path / "sessions" / f"date={session_date}" / f"{stem}.parquet"

    if output_path.exists():
        logger.warning(f"Session file already exists, skipping: {output_path}")
        return output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([asdict(session_info)])
    df.to_parquet(output_path, index=False)

    logger.info(f"Session written: {output_path}")
    return output_path
