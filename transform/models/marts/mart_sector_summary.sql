-- Companies per industry (primary SIC code), how many are active, average age.
select
    s.sic_code,
    d.sic_description,
    count(*)                                               as companies,
    count(*) filter (where c.company_status = 'Active')    as active_companies,
    round(avg(date_diff('year', c.incorporation_date, current_date)), 1) as avg_age_years
from {{ ref('int_company_sic_codes') }} s
join {{ ref('stg_companies') }} c using (company_number)
join {{ ref('dim_sic_codes') }} d using (sic_code)
where s.sic_position = 1
group by 1, 2