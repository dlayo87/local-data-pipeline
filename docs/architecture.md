# Architecture

![Architecture](architecture.png)

## Flow
CSV -> Parquet -> monthly batches -> landing -> dbt staging
-> dbt intermediate -> dbt marts -> Streamlit dashboard

## Layers
| Layer | Where | Type | Purpose |
|---|---|---|---|
| Raw | data/parquet | file | Untouched copy, all text |
| Landing | data/landing | files | Batches that have arrived |
| Staging | warehouse.duckdb | incremental table | Typed, cleaned, deduplicated |
| Intermediate | warehouse.duckdb | view | One row per company per SIC code |
| Marts | warehouse.duckdb | tables | Answers to the business questions |

## Orchestration
orchestration/pipeline.py runs: land next batch, dbt build (with tests), dbt docs.
Windows Task Scheduler can run it daily via run_pipeline.bat.
