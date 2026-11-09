-- Cleaning should not lose more than 0.1% of rows.
with src as (select count(*) as n from {{ source('raw', 'companies') }}),
     stg as (select count(*) as n from {{ ref('stg_companies') }})
select src.n as source_rows, stg.n as staging_rows
from src, stg
where stg.n < src.n * 0.999