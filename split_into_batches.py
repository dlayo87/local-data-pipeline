# Splits the Parquet file into a backfill (before 2025) plus one file per month.
import os
import shutil
import duckdb

SRC = "data/parquet/companies.parquet"
OUT = "data/batches"
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

con = duckdb.connect()
con.sql(f"""
    CREATE TEMP VIEW dated AS
    SELECT *,
        CASE
            WHEN try_strptime(incorporationdate, '%d/%m/%Y') IS NULL
              OR try_strptime(incorporationdate, '%d/%m/%Y') < DATE '2025-01-01'
            THEN '0000_backfill'
            ELSE strftime(try_strptime(incorporationdate, '%d/%m/%Y'), '%Y_%m')
        END AS batch
    FROM read_parquet('{SRC}')
""")

batches = [r[0] for r in con.sql("SELECT DISTINCT batch FROM dated ORDER BY 1").fetchall()]
for b in batches:
    con.sql(f"COPY (SELECT * EXCLUDE (batch) FROM dated WHERE batch = '{b}') "
            f"TO '{OUT}/{b}.parquet' (FORMAT PARQUET)")
    print("Wrote", b)
print(f"{len(batches)} batches created")