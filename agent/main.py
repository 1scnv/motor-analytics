import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from agent.watcher import start_watcher

load_dotenv()


def main() -> None:
    telemetry_path = os.getenv("IRACING_TELEMETRY_PATH")
    data_path = os.getenv("DATA_PATH", "data/bronze")

    if not telemetry_path:
        raise ValueError("IRACING_TELEMETRY_PATH is not set in .env")

    logger.info("Starting Motor Analytics agent")
    logger.info(f"Telemetry path: {telemetry_path}")
    logger.info(f"Data path: {data_path}")

    start_watcher(
        telemetry_path=Path(telemetry_path),
        data_path=Path(data_path),
    )


if __name__ == "__main__":
    main()
