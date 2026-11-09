-- Fails for any company incorporated after today.
select company_number, incorporation_date
from {{ ref('stg_companies') }}
where incorporation_date > current_date
