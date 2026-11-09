-- Companies per postcode area: total, new in the last year, overdue on accounts.
select
    postcode_area,
    count(*)                                                                     as companies,
    count(*) filter (where incorporation_date >= current_date - interval 12 month) as new_last_12_months,
    count(*) filter (where company_status = 'Active'
                       and accounts_next_due_date < current_date)                as accounts_overdue
from {{ ref('stg_companies') }}
where postcode_area is not null
group by 1