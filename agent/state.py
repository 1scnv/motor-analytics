import json
from datetime import datetime
from pathlib import Path

from loguru import logger

STATE_FILE = Path("data/.agent_state.json")


def is_processed(filename: str) -> bool:
    """Check if an .ibt file has already been processed."""
    state = _load_state()
    return filename in state.get("processed", {})


def mark_processed(filename: str, telemetry_path: Path, session_path: Path) -> None:
    """Mark an .ibt file as successfully processed."""
    state = _load_state()

    state.setdefault("processed", {})[filename] = {
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "telemetry_path": str(telemetry_path),
        "session_path": str(session_path),
    }

    _save_state(state)
    logger.info(f"Marked as processed: {filename}")


def _load_state() -> dict:
    """Load state from JSON file, returning empty state if file doesn't exist."""
    if not STATE_FILE.exists():
        return {"processed": {}}

    with STATE_FILE.open("r") as f:
        return json.load(f)


def _save_state(state: dict) -> None:
    """Persist state to JSON file."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with STATE_FILE.open("w") as f:
        json.dump(state, f, indent=2)
