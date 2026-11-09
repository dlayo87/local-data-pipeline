# Runbook

All commands run from the project folder with the virtual environment active
(.venv\Scripts\activate).

## Normal run
python orchestration/pipeline.py

## A dbt test fails
1. run_dbt test --select stg_companies --store-failures
2. Look at the failing rows in the table named in the output
3. Fix the data or the SQL, then run_dbt build

## Rebuild staging after changing cleaning logic
run_dbt build --full-refresh

## Start completely fresh
del /q data\warehouse.duckdb data\warehouse.duckdb.wal data\landing\*.parquet
Then run the pipeline.

## New monthly file from Companies House
Replace the CSV in data/raw, run convert_to_parquet.py and
split_into_batches.py, start fresh, then run the pipeline.

## "Could not set lock on file"
Close the dashboard (Ctrl+C in its terminal) and try again.
