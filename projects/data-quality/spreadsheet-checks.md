# Spreadsheet review copy

This is an Excel / Google Sheets-style formula guide in text form. The delivered artifacts are CSV and JSON, not a recalculated workbook. Formulas below have been inspected for the fixed layout; native application behavior has not been tested.

## Import and preserve the source

Import `data/requests.csv` at `Requests!A1`, preserving column A as text and C:E as numbers. Keep E2:E9 as captured values so the evidence remains visible. The JSON snapshot records their original formula text separately; it must not be imported over the captured values during review.

Put the captured summary 115 in E10 and label A10 `Reported summary`. Its captured formula is `=SUM(E2:E8)`; record this as text in a note or separate evidence column. It intentionally excludes row 9.

## Add review columns

Enter headers F1:J1 as `Expected minutes`, `Duplicate count`, `Required fields`, `Total check`, and `Queue check`. Enter the row-2 formulas below and fill down through row 9 only.

| Cell | Formula | Purpose |
| --- | --- | --- |
| F2 | `=IF(OR(C2="",D2=""),"Unavailable",IF(AND(ISNUMBER(C2),ISNUMBER(D2)),IF(AND(C2>=0,D2>0,MOD(C2,1)=0,MOD(D2,1)=0),C2*D2,"Invalid input"),"Invalid input"))` | Compute only from present, numeric, valid inputs. Preserve zero units. |
| G2 | `=COUNTIFS($A$2:$A$9,A2)` | Values > 1 identify repeated IDs. Review alongside required-field checks. |
| H2 | `=IF(OR(A2="",B2="",C2="",D2="",E2=""),"Missing","Present")` | Detect blanks independently of numeric validity. |
| I2 | `=IF(ISNUMBER(F2),IF(E2="","Missing reported value",IF(ISNUMBER(E2),IF(E2=F2,"Match","Mismatch"),"Invalid reported value")),"Review inputs")` | Avoid comparing an unavailable result with zero. |
| J2 | `=IF(OR(B2="standard",B2="priority"),"Valid","Invalid")` | Restrict the category vocabulary. |

`COUNTIFS` in these spreadsheet engines is case-insensitive; the Python ID check follows the case-sensitive source contract. The supplied IDs are all uppercase, so this fixture has no discrepancy. For a real case-sensitive identifier system, use a matching check that preserves that requirement.

To compare full raw detail with the captured summary, place `=SUM(E2:E9)` in a review cell; expected result: **127**. This reconciles imported values only. `=SUM(F2:F9)` returns **142**, but SUM skips the unavailable text in F5: label it **partial computable subtotal**, never “final total.”

## Input validation and reference checking

For a corrected input copy, set C2:C9 to whole numbers ≥ 0, D2:D9 to whole numbers ≥ 1, E2:E9 to whole numbers ≥ 0, and B2:B9 to a list containing `standard,priority`. Treat blanks as invalid through the required-field checks. Validation controls alone do not replace an audit of imported data.

The expected captured row pattern is `=Cr*Dr`, with r equal to the worksheet row. E6 instead uses D5. A corrected calculation column should use relative row references; the duplicate-search range must remain absolute when filled down. If records are added, extend every bounded range and the summary deliberately. Do not sort only part of the table.

## Expected spot checks

| Location | Expected result |
| --- | --- |
| F2 / I2 | 20 / Match |
| G3 / G4 | 2 / 2 |
| F5 / H5 / I5 | Unavailable / Missing / Review inputs |
| F6 / I6 | 30 / Mismatch |
| F7 / I7 | 20 / Mismatch |
| F8 / I8 | 0 / Match |
| F9 / I9 | 12 / Match |

Before relying on a native workbook, recalculate, inspect these cells, and test blank versus zero and an appended row in a disposable copy. Record the application and version used. No native-workbook results are represented as completed in this portfolio.
