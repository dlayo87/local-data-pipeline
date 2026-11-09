# UK Companies House Data Pipeline

An end-to-end batch data pipeline that turns the 5 million row Companies House
register into tested, analytics-ready tables and a dashboard, running entirely
on a laptop.

![Dashboard](docs/dashboard.png)

## Architecture
![Architecture](docs/architecture.png)

## Tech stack
Python, DuckDB, Parquet, dbt Core, Streamlit, Windows Task Scheduler

## Questions it answers
- How many companies are incorporated each month?
- Which industries have the most companies, and how old are they?
- Which postcode areas have the most new companies?
- How many active companies are overdue on their accounts?

## Results
| Metric | CSV | Parquet |
|---|---|---|
| File size | 2,810 MB | 290 MB |
| Count by status | 2.3 s | 0.04 s |

- 6 dbt models and 15 data tests, all passing
- 0 duplicate company numbers found
- Loads data incrementally: a backfill, then one month per run
- Failing tests stop the pipeline before bad data reaches the dashboard

![Lineage](docs/lineage.png)

## How to run it (Windows)
1. Download BasicCompanyData from Companies House, unzip it, and place the CSV in data/raw/
2. python -m venv .venv
3. .venv\Scripts\activate
4. pip install -r requirements.txt
5. python ingestion/convert_to_parquet.py
6. python ingestion/split_into_batches.py
7. python orchestration/pipeline.py
8. streamlit run dashboard/app.py

## Data source
Companies House Free Company Data Product, snapshot dated 1 October 2026.
Contains public sector information from Companies House.

## What I learned
- Converting the CSV to Parquet made the file about 10 times smaller and the same query about 50 times faster.
- Upgrading a library can quietly break working code: DuckDB 2.0 changed how query results are read, and a bare `except` hid the error until I printed it.
- An incremental model is fast, but a simple "newer than the latest date" filter would miss records that arrive late with an older date.

## What I would do next
- Track month-to-month changes with dbt snapshots
- Add automated tests on every change with GitHub Actions
