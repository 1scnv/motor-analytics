import os
from pathlib import Path

import duckdb
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

DUCKDB_PATH = os.getenv("DUCKDB_PATH", "data/motor_analytics.duckdb")
SETUP_SQL = Path("transform/setup_bronze.sql")


def init_db() -> None:
    """Initialize DuckDB and create bronze layer views."""
    logger.info(f"Connecting to DuckDB: {DUCKDB_PATH}")

    conn = duckdb.connect(DUCKDB_PATH)
    sql = SETUP_SQL.read_text()
    conn.execute(sql)
    conn.close()

    logger.info("Bronze layer initialized")


if __name__ == "__main__":
    init_db()
