
# Prints every company status as a ready-to-paste line for _stg_models.yml
import duckdb

rows = duckdb.sql("""
    select distinct trim(companystatus) as status
    from read_parquet('data/parquet/companies.parquet')
    where trim(companystatus) != ''
    order by 1
""").fetchall()

print("values: " + str([r[0] for r in rows]))
