-- How many companies were incorporated each month, by company type.
select
    date_trunc('month', incorporation_date)::date  as incorporation_month,
    company_category,
    count(*)                                       as companies_incorporated
from {{ ref('stg_companies') }}
where incorporation_date is not null
group by 1, 2