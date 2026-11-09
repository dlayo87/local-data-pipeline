-- A lookup list of every SIC code and its description.
select
    sic_code,
    any_value(sic_description) as sic_description
from {{ ref('int_company_sic_codes') }}
group by 1