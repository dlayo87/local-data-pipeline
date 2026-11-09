# Copies the next unloaded batch into data/landing and records it in load_log.
import os
import shutil
from datetime import datetime
import duckdb

BATCHES = "data/batches"
LANDING = "data/landing"
WAREHOUSE = "data/warehouse.duckdb"
os.makedirs(LANDING, exist_ok=True)

con = duckdb.connect(WAREHOUSE)
con.sql("""
    CREATE TABLE IF NOT EXISTS load_log (
        batch_name VARCHAR,
        row_count  BIGINT,
        loaded_at  TIMESTAMP
    )
""")

loaded = {r[0] for r in con.sql("SELECT batch_name FROM load_log").fetchall()}
pending = sorted(f for f in os.listdir(BATCHES) if f.endswith(".parquet") and f not in loaded)

if not pending:
    print("Nothing to land: every batch is already loaded.")
else:
    nxt = pending[0]
    shutil.copy(os.path.join(BATCHES, nxt), os.path.join(LANDING, nxt))
    # DuckDB 2.0: relations have no fetchone(), so read the single row with fetchall().
    rows = con.sql(f"SELECT COUNT(*) FROM read_parquet('{LANDING}/{nxt}')").fetchall()[0][0]
    con.execute("INSERT INTO load_log VALUES (?, ?, ?)", [nxt, rows, datetime.now()])
    print(f"Landed {nxt}: {rows:,} rows. {len(pending) - 1} batches left.")

con.close()
