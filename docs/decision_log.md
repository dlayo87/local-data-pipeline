# Decision log

| Decision | Options considered | Why I chose it | Trade-off |
|---|---|---|---|
| DuckDB as the database | Postgres, pandas, Spark | No server, very fast on one laptop | Only one program can write at a time |
| Read everything as text, set types in dbt | Let DuckDB guess types | Guessing can fail on messy columns; dbt casts are tested | More SQL to write |
| Clean column names once in Python | Quote messy names everywhere | Leading spaces and dots break SQL | One extra helper file |
| Backfill, then monthly batches | Daily batches, one big load | Mirrors a real first load followed by a feed | Late records with old dates would be missed |
| Windows Task Scheduler | Prefect, Airflow | Built into Windows, nothing to install | No web dashboard of runs |
