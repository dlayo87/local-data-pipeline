# Shared helper: reads the Companies House CSV and tidies the column names.
import glob
import re
import duckdb

CSV_GLOB = "data/raw/*.csv"


def csv_files():
    files = sorted(glob.glob(CSV_GLOB))
    if not files:
        raise SystemExit("No CSV found in data/raw. Go back to Part 3.")
    return files


def clean_name(name):
    """' RegAddress.PostTown' becomes 'regaddress_posttown'."""
    name = name.strip().lower()
    return re.sub(r"[^a-z0-9]+", "_", name).strip("_")


def raw_view(con):
    """Create a view called companies_raw with tidy column names."""
    csv_files()
    src = f"read_csv('{CSV_GLOB}', header=true, all_varchar=true, sample_size=-1)"
    cols = [row[0] for row in con.sql(f"DESCRIBE SELECT * FROM {src}").fetchall()]
    select_list = ",\n    ".join(f'"{c}" AS {clean_name(c)}' for c in cols)
    con.sql(f"CREATE OR REPLACE VIEW companies_raw AS SELECT\n    {select_list}\nFROM {src}")
    return "companies_raw"