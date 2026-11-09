-- Fails if staging loses companies: every distinct non-blank company number
-- in the source must appear exactly once in stg_companies.
with source_count as (
    select count(distinct trim(companynumber)) as n
    from {{ source('raw', 'companies') }}
    where nullif(trim(companynumber), '') is not null
),
staging_count as (
    select count(*) as n from {{ ref('stg_companies') }}
)
select s.n as source_companies, t.n as staging_companies
from source_count s, staging_count t
where s.n != t.n
