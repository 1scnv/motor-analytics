from dataclasses import dataclass
from pathlib import Path

import irsdk
import yaml
from loguru import logger


@dataclass
class SessionInfo:
    ibt_filename: str
    track: str
    car: str
    session_type: str
    total_laps: int
    best_lap_time: float


TELEMETRY_CHANNELS = [
    "SessionTime",
    "Lap",
    "LapDistPct",
    "Speed",
    "Throttle",
    "Brake",
    "Clutch",
    "Gear",
    "RPM",
    "SteeringWheelAngle",
    "LapCurrentLapTime",
    "LapDeltaToBestLap",
    "LongAccel",
    "LatAccel",
    "Lat",
    "Lon",
]


def parse_ibt(filepath: str | Path) -> tuple[SessionInfo, list[dict]]:
    """Parse an iRacing .ibt file and return session info and telemetry records."""
    filepath = Path(filepath)
    logger.info(f"Parsing {filepath.name}")

    ibt = irsdk.IBT()
    ibt.open(str(filepath))

    session_info = _extract_session_info(ibt, filepath.name)
    telemetry = _extract_telemetry(ibt)

    ibt.close()

    logger.info(f"Parsed {len(telemetry)} records from {filepath.name}")
    return session_info, telemetry


def _extract_session_info(ibt: irsdk.IBT, filename: str) -> SessionInfo:
    """Extract session metadata from ibt file."""
    session_yaml = _read_session_yaml(ibt)

    total_laps = max(ibt.get_all("LapCompleted") or [0])
    best_lap_time = max(ibt.get_all("LapBestLapTime") or [0.0])

    return SessionInfo(
        ibt_filename=filename,
        track=session_yaml["WeekendInfo"]["TrackName"],
        car=session_yaml["DriverInfo"]["Drivers"][0]["CarScreenName"],
        session_type=session_yaml["SessionInfo"]["Sessions"][0]["SessionType"],
        total_laps=int(total_laps),
        best_lap_time=float(best_lap_time),
    )


def _read_session_yaml(ibt: irsdk.IBT) -> dict:
    """Read and parse the session YAML embedded in the ibt file."""
    offset = ibt._header.session_info_offset
    length = ibt._header.session_info_len
    raw = ibt._shared_mem[offset : offset + length]
    return yaml.safe_load(raw.decode("utf-8", errors="replace"))


def _extract_telemetry(ibt: irsdk.IBT) -> list[dict]:
    """Extract all telemetry records from ibt file."""
    total = ibt._disk_header.session_record_count

    channels_data = {}
    for channel in TELEMETRY_CHANNELS:
        data = ibt.get_all(channel)
        if data is not None:
            channels_data[channel] = data

    return [
        {channel: values[i] for channel, values in channels_data.items()}
        for i in range(total)
    ]
