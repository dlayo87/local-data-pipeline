-- Every Companies House number should be exactly 8 characters.
select company_number
from {{ ref('stg_companies') }}
where length(company_number) <> 8