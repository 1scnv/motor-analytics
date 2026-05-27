import time
from pathlib import Path

from loguru import logger
from watchdog.events import FileCreatedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from agent.parser import parse_ibt
from agent.state import is_processed, mark_processed
from agent.writer import write_parquet


class IBTHandler(FileSystemEventHandler):
    def __init__(self, data_path: str | Path, settle_time: int = 5):
        self.data_path = Path(data_path)
        self.settle_time = settle_time  # seconds to wait before processing

    def on_created(self, event: FileCreatedEvent) -> None:
        if not isinstance(event, FileCreatedEvent):
            return
        if not event.src_path.endswith(".ibt"):
            return

        filepath = Path(event.src_path)
        logger.info(f"New .ibt detected: {filepath.name}")

        # wait for iRacing to finish writing the file
        time.sleep(self.settle_time)

        _process_file(filepath, self.data_path)


def _process_file(filepath: Path, data_path: Path) -> None:
    """Parse, write and mark a single .ibt file as processed."""
    if is_processed(filepath.name):
        logger.warning(f"Already processed, skipping: {filepath.name}")
        return

    try:
        session_info, telemetry = parse_ibt(filepath)
        telemetry_path, session_path = write_parquet(session_info, telemetry, data_path)
        mark_processed(filepath.name, telemetry_path, session_path)
    except Exception as e:
        logger.error(f"Failed to process {filepath.name}: {e}")


def start_watcher(telemetry_path: str | Path, data_path: str | Path) -> None:
    """Start monitoring the telemetry folder for new .ibt files."""
    telemetry_path = Path(telemetry_path)

    if not telemetry_path.exists():
        raise FileNotFoundError(f"Telemetry path not found: {telemetry_path}")

    handler = IBTHandler(data_path=data_path)
    observer = Observer()
    observer.schedule(handler, str(telemetry_path), recursive=False)
    observer.start()

    logger.info(f"Watching: {telemetry_path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Watcher stopped")

    observer.join()
