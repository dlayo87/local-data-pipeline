# Data dictionary

## Source: BasicCompanyData (Companies House)
- One row per company currently on the register
- Snapshot date: 1 October 2026
- Rows: 5,704,711
- Incorporation dates from 1 January 1327 to 1 October 2026

## Main table: stg_companies
| Column | Type | Description | Example | Notes |
|---|---|---|---|---|
| company_number | text | Companies House number | 08209948 | Unique, 8 characters, kept as text to keep leading zeros |
| company_name | text | Registered name | ! LTD | |
| company_status | text | Status on the register | Active | Values: Active, Active - Proposal to Strike off, Liquidation, In Administration, Live but Receiver Manager on at least one charge, Voluntary Arrangement, In Administration/Administrative Receiver, RECEIVERSHIP, ADMINISTRATION ORDER, ADMINISTRATIVE RECEIVER, In Administration/Receiver Manager, RECEIVER MANAGER / ADMINISTRATIVE RECEIVER, VOLUNTARY ARRANGEMENT / RECEIVER MANAGER, VOLUNTARY ARRANGEMENT / ADMINISTRATIVE RECEIVER |
| company_category | text | Type of company | Private Limited Company | |
| incorporation_date | date | Date incorporated | 2012-09-11 | Source format was DD/MM/YYYY |
| postcode_area | text | Letters at the start of the postcode | HG | Created in staging |
| sic_text_1 | text | Primary industry code and description | 62020 - Information technology consultancy activities | Up to 4 per company |

## Known issues
- The file only lists companies still on the register, so dissolved companies are rare (no row has a dissolution date)
- Overdue accounts are compared with today's date, not the snapshot date
- 38 companies have incorporation dates before 1850. These are real, not errors: Royal Charter bodies (numbers starting RC) such as the Goldsmiths' Company, chartered in 1327
- 91,475 companies have no registered postcode, so they are left out of the postcode area summary
- Status values mix capitalisation (for example "Active" and "RECEIVERSHIP"), exactly as Companies House publishes them
- "New in the last 12 months" stays at 0 until batches from the last 12 months have been loaded
