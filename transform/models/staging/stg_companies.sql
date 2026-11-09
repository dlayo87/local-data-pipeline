-- One row per company. Incremental: each run only adds companies newer than
-- the latest incorporation date already in the table.
{{ config(materialized='incremental', unique_key='company_number') }}

with source as (
    select * from {{ source('raw', 'companies') }}
),

cleaned as (
    select
        trim(companynumber)                                    as company_number,
        trim(companyname)                                      as company_name,
        nullif(trim(companystatus), '')                        as company_status,
        nullif(trim(companycategory), '')                      as company_category,
        nullif(trim(countryoforigin), '')                      as country_of_origin,
        try_strptime(nullif(trim(incorporationdate), ''), '%d/%m/%Y')::date    as incorporation_date,
        try_strptime(nullif(trim(dissolutiondate), ''), '%d/%m/%Y')::date      as dissolution_date,
        nullif(upper(trim(regaddress_posttown)), '')           as post_town,
        nullif(upper(trim(regaddress_postcode)), '')           as postcode,
        nullif(regexp_extract(upper(trim(regaddress_postcode)), '^[A-Z]{1,2}'), '') as postcode_area,
        nullif(trim(accounts_accountcategory), '')             as accounts_category,
        try_strptime(nullif(trim(accounts_nextduedate), ''), '%d/%m/%Y')::date as accounts_next_due_date,
        try_cast(mortgages_nummortoutstanding as integer)      as mortgages_outstanding,
        nullif(trim(siccode_sictext_1), '')                    as sic_text_1,
        nullif(trim(siccode_sictext_2), '')                    as sic_text_2,
        nullif(trim(siccode_sictext_3), '')                    as sic_text_3,
        nullif(trim(siccode_sictext_4), '')                    as sic_text_4
    from source
    where nullif(trim(companynumber), '') is not null
    {% if is_incremental() %}
      and try_strptime(incorporationdate, '%d/%m/%Y')::date
          > (select max(incorporation_date) from {{ this }})
    {% endif %}
)

select * from cleaned
qualify row_number() over (
    partition by company_number order by incorporation_date desc nulls last
) = 1
