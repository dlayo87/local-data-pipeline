-- Fails for any company number that is not exactly 8 characters long.
select company_number
from {{ ref('stg_companies') }}
where length(company_number) != 8
