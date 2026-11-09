# Streamlit dashboard reading the dbt marts.
import duckdb
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="UK Companies Pipeline", layout="wide")


@st.cache_data(ttl=60)
def load(sql):
    # Open, read, close, so the dashboard never blocks the pipeline.
    con = duckdb.connect("data/warehouse.duckdb", read_only=True)
    df = con.sql(sql).df()
    con.close()
    return df


monthly = load("""
    select incorporation_month, sum(companies_incorporated) as companies
    from fct_incorporations_monthly
    where incorporation_month >= date '2015-01-01'
    group by 1 order by 1
""")
sectors = load("select * from mart_sector_summary order by companies desc limit 15")
areas = load("select * from mart_area_summary order by companies desc")
log = load("select * from load_log order by loaded_at desc limit 10")

st.title("UK Companies House pipeline")

c1, c2, c3 = st.columns(3)
c1.metric("Companies with a UK postcode", f"{int(areas.companies.sum()):,}")
c2.metric("New in the last 12 months", f"{int(areas.new_last_12_months.sum()):,}")
c3.metric("Active, accounts overdue", f"{int(areas.accounts_overdue.sum()):,}")

st.subheader("Incorporations per month since 2015")
st.plotly_chart(px.line(monthly, x="incorporation_month", y="companies"),
                width="stretch")

left, right = st.columns(2)
with left:
    st.subheader("Top 15 industries by primary SIC code")
    fig = px.bar(sectors, x="companies", y="sic_description", orientation="h")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, width="stretch")
with right:
    st.subheader("Top 20 postcode areas")
    st.dataframe(areas.head(20), hide_index=True)

st.subheader("Pipeline health: last 10 loads")
st.dataframe(log, hide_index=True)
