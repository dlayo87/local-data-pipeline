# Profiles the Companies House data: row counts, columns, values.
import duckdb
from common import raw_view

con = duckdb.connect()
v = raw_view(con)

print("\n1. TOTAL ROWS")
print(con.sql(f"SELECT COUNT(*) AS total_rows FROM {v}"))

print("\n2. IS COMPANY NUMBER UNIQUE? (the two numbers should match)")
print(con.sql(f"SELECT COUNT(*) AS total_rows, COUNT(DISTINCT companynumber) AS unique_numbers FROM {v}"))

print("\n3. FIVE SAMPLE COMPANIES")
print(con.sql(f"""
    SELECT companynumber, companyname, companystatus, incorporationdate, siccode_sictext_1
    FROM {v} LIMIT 5
"""))

print("\n4. COMPANY STATUS VALUES (write these down for Part 9)")
print(con.sql(f"SELECT companystatus, COUNT(*) AS companies FROM {v} GROUP BY 1 ORDER BY 2 DESC"))

print("\n5. COMPANY CATEGORY VALUES")
print(con.sql(f"SELECT companycategory, COUNT(*) AS companies FROM {v} GROUP BY 1 ORDER BY 2 DESC LIMIT 15"))

print("\n6. SAVING FULL PROFILE OF EVERY COLUMN...")
con.sql(f"SUMMARIZE {v}").df().to_csv("docs/profile_output.csv", index=False)
print("Saved to docs/profile_output.csv")