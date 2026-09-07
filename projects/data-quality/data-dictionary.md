# Source contract

Everything in this folder is synthetic. One row represents one request's planned handling workload. Repeated `request_id` values require reconciliation; rows are not separate line items of the same request.

Import `data/requests.csv` into a sheet named `Requests`, with headers in row 1 and records in rows 2–9. Columns are fixed for this example:

| Column | Field | Rule |
| --- | --- | --- |
| A | request_id | Required, case-sensitive unique text identifier. Preserve the original value. |
| B | queue | Required; exactly `standard` or `priority`. |
| C | units | Required integer ≥ 0. Blank is unknown, not zero. |
| D | minutes_per_unit | Required integer > 0. |
| E | reported_minutes | Required integer ≥ 0; should equal C × D when inputs are available. |

All values are whole minutes or whole units. Exact integer comparison is appropriate; no currency, financial modeling, date arithmetic, or rounding tolerance is involved.

`formula-snapshot.json` records the captured formulas for E2:E9 and a synthetic summary at E10. The CSV contains reported values, not live formulas. A formula and a captured value can disagree; E7 deliberately illustrates that condition. The fixture does not establish whether the cause was stale calculation, manual export, or transcription.

The reported summary is 115 minutes from `=SUM(E2:E8)`. Full imported detail extends through row 9. This summary describes the raw row population; it is not a deduplicated operational total.

The script accepts the fixed five-column schema, canonical nonnegative integer text, and the row/summary formula patterns defined here. Unexpected patterns are flagged rather than evaluated. Whitespace normalization, fuzzy duplicates, arbitrary workbooks, and multi-line request models are outside this example.
