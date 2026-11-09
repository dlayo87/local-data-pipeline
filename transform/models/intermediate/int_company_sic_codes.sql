-- One row per company per SIC code, with the code and description split apart.
with companies as (
    select company_number, sic_text_1, sic_text_2, sic_text_3, sic_text_4
    from {{ ref('stg_companies') }}
),

unpivoted as (
    select company_number, 1 as sic_position, sic_text_1 as sic_text from companies
    union all
    select company_number, 2, sic_text_2 from companies
    union all
    select company_number, 3, sic_text_3 from companies
    union all
    select company_number, 4, sic_text_4 from companies
)

select
    company_number,
    sic_position,
    trim(split_part(sic_text, ' - ', 1))                 as sic_code,
    trim(substr(sic_text, strpos(sic_text, ' - ') + 3))  as sic_description
from unpivoted
where sic_text like '% - %'