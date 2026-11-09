# Converts the Companies House CSV into one compressed Parquet file
# and measures the difference in size and speed.
import os
import time
import duckdb
from common import raw_view, csv_files

OUT = "data/parquet/companies.parquet"
os.makedirs("data/parquet", exist_ok=True)

con = duckdb.connect()
v = raw_view(con)

print("Converting... this takes a few minutes")
start = time.time()
con.sql(f"COPY (SELECT * FROM {v}) TO '{OUT}' (FORMAT PARQUET, COMPRESSION ZSTD)")
print(f"Converted in {time.time() - start:.0f} seconds")

csv_mb = sum(os.path.getsize(f) for f in csv_files()) / 1e6
parquet_mb = os.path.getsize(OUT) / 1e6
print(f"\nCSV size:     {csv_mb:,.0f} MB")
print(f"Parquet size: {parquet_mb:,.0f} MB")

query = "SELECT companystatus, COUNT(*) FROM {} GROUP BY 1"
for label, src in [("CSV", v), ("Parquet", f"read_parquet('{OUT}')")]:
    t = time.time()
    con.sql(query.format(src)).fetchall()
    print(f"{label} query time: {time.time() - t:.2f} seconds")
