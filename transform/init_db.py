import os
from pathlib import Path

import duckdb
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

DUCKDB_PATH = os.getenv("DUCKDB_PATH", "data/motor_analytics.duckdb")
PROJECT_ROOT = Path(__file__).parent.parent


def init_db() -> None:
    """Initialize DuckDB and create bronze layer views."""
    logger.info(f"Connecting to DuckDB: {DUCKDB_PATH}")

    telemetry_path = PROJECT_ROOT / "data/bronze/telemetry/**/*.parquet"
    sessions_path = PROJECT_ROOT / "data/bronze/sessions/**/*.parquet"

    conn = duckdb.connect(DUCKDB_PATH)

    conn.execute("create schema if not exists bronze")

    conn.execute(f"""
        create or replace view bronze.telemetry_raw as
        select * exclude (filename)
        from read_parquet(
            '{telemetry_path}',
            hive_partitioning = true,
            filename = true
        )
    """)

    conn.execute(f"""
        create or replace view bronze.session_raw as
        select * exclude (filename)
        from read_parquet(
            '{sessions_path}',
            hive_partitioning = true,
            filename = true
        )
    """)

    conn.close()
    logger.info("Bronze layer initialized")


if __name__ == "__main__":
    init_db()
