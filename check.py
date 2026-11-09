# Shows row counts for every table, and the load log once it exists.
import duckdb

con = duckdb.connect("data/warehouse.duckdb", read_only=True)
tables = ["stg_companies", "int_company_sic_codes", "fct_incorporations_monthly",
          "dim_sic_codes", "mart_sector_summary", "mart_area_summary"]
for t in tables:
    try:
        n = con.sql(f"select count(*) from {t}").fetchone()[0]
        print(f"{t:30} {n:>12,} rows")
    except Exception:
        print(f"{t:30} not built yet")

print("\nTop 5 postcode areas:")
try:
    print(con.sql("select * from mart_area_summary order by companies desc limit 5"))
except Exception:
    print("not built yet")

try:
    print("\nLoad log:")
    print(con.sql("select * from load_log order by loaded_at"))
except Exception:
    print("no batches loaded yet (that is normal until Part 10)")
con.close()