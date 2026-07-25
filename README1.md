# Motor Analytics — iRacing Edition

A personal end-to-end data pipeline that collects iRacing telemetry from `.ibt` files and delivers a driving analysis dashboard — built with a modern Analytics Engineering stack.

---

## Why this project

Most sim racing telemetry tools are black boxes: they collect your data, store it in their cloud, and give you limited control. Motor Analytics takes a different approach — a custom collection agent that feeds your own data warehouse, transformed with dbt, and visualized in Power BI.

Built for two audiences: sim racers who want deeper insight into their driving, and data engineers who want to see a real end-to-end pipeline in action.

---

## Architecture

```
 iRacing Simulator
       │
       │  generates .ibt files (~60Hz telemetry)
       ▼
 Python Agent  ──────────────────────────────────────
 │  watchdog   monitors Documents/iRacing/telemetry/
 │  pyirsdk    parses channels: speed, throttle,
 │             brake, RPM, gear, lap, track position
 │  writer     serializes to Parquet
 └──────────────────────────────────────────────────
       │
       │  Parquet files (partitioned by date)
       ▼
 DuckDB  ──────────────────────────────────────────
 │  reads Parquet natively (no load step required)
 │  dbt bronze  →  staging  →  marts
 │  fct_laps · dim_track · dim_car · fct_telemetry_summary
 └─────────────────────────────────────────────────
       │
       │  orchestrated by Airflow (Docker)
       ▼
 Power BI Dashboard
 │  lap time evolution · sector analysis
 │  throttle & brake traces · consistency metrics
 └─────────────────────────────────────────────────
```

---

## Stack

| Layer | Tool | Purpose |
|---|---|---|
| Collection | Python · pyirsdk · watchdog | Parse `.ibt` files and write Parquet |
| Storage | Parquet (local) | Portable, compressed, natively read by DuckDB |
| Warehouse | DuckDB | Serverless analytical database |
| Transformation | dbt Core + dbt-duckdb | Staging and marts with tests and docs |
| Orchestration | Airflow (Docker) | Pipeline scheduling and monitoring |
| CI/CD | GitHub Actions + dbt Slim CI | Quality gates on every PR |
| BI | Power BI Desktop | Driving analysis dashboard |

---

## Project structure

```
motor-analytics/
├── agent/          # collection agent (watcher, parser, writer, state)
├── data/           # local Parquet storage — not versioned
├── transform/      # dbt project (staging, marts, tests, macros)
├── orchestration/  # Airflow DAGs and Docker Compose
├── dashboard/      # Power BI file
├── docs/           # architecture decisions and data dictionary
├── CLAUDE.md       # AI-friendly development log and context
└── README.md
```

---

## Getting started

### Prerequisites

- WSL2 (Ubuntu 24.04+)
- Python 3.12+
- Git
- iRacing with telemetry enabled (`Options → Interface → Enable telemetry`)

### Setup

```bash
git clone git@github.com:1scnv/motor-analytics.git
cd motor-analytics

python3 -m venv .venv
source .venv/bin/activate

make install-dev

cp .env.example .env
# edit .env with your local paths

pre-commit install
```

### Commands

```bash
make lint         # check code style
make format       # auto-format code
make test         # run tests with coverage
make agent        # start the collection agent
make dbt-run      # run dbt models
make dbt-test     # run dbt tests
make dbt-docs     # generate and serve dbt documentation
make clean        # remove temporary files
```

---

## Roadmap

| Phase | Description | Status |
|---|---|---|
| 1 | Collection Agent | 🔄 In progress |
| 2 | Bronze Layer (DuckDB) | ⏳ Pending |
| 3 | Transformation (dbt) | ⏳ Pending |
| 4 | Orchestration (Airflow) | ⏳ Pending |
| 5 | CI/CD | ⏳ Pending |
| 6 | Dashboard (Power BI) | ⏳ Pending |

---

## License

MIT
