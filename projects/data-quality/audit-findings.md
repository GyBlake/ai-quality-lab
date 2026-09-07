# Audit findings: request workload

**Disposition: hold for review.** Do not use the reported summary for capacity planning. Duplicate identity and missing units remain unresolved.

Scope: eight synthetic rows, `Requests!A2:E9`, plus the E10 summary. Method: source-contract checks, formula-reference inspection, independent integer arithmetic, and raw-detail reconciliation. [Machine-readable report](sample-output/audit-report.json).

## Findings

| Location | Finding | Impact | Next action |
| --- | --- | --- | --- |
| A3 / A4 | R002 appears twice with identical fields. | Possible double counting of 30 minutes. | Ask the source owner whether this is a repeated export or separate request requiring a corrected ID. Preserve both rows until resolved. |
| C5 / E5 | Units are blank; E5 reports 0 and uses unguarded `=C5*D5`. | Missing workload can appear as a valid zero. | Obtain the missing quantity; use an explicit unavailable state while it is unknown. |
| E6 | `=C6*D5` uses the preceding row's rate: 2 × 5 = 10. Same-row inputs imply 2 × 15 = 30. | Understates this row by 20 minutes. | In a review copy, correct the reference to D6 and recheck the copied range. |
| E7 | Captured value is 25; `=C7*D7` and inputs imply 5 × 4 = 20. | Overstates this row by 5 minutes. | Compare the native cell and export; recalculate and recapture. The fixture alone does not identify the cause. |
| E10 | `=SUM(E2:E8)` omits E9. Reported 115 differs from full raw detail 127. | Omits 12 reported minutes before other defects are resolved. | Extend to E9 for the raw-detail tie-out; do not treat that as final operational approval. |

These are five grouped findings. The checker emits eight diagnostic records because some findings have separate input, formula, or total checks. Diagnostic count is not a count of independent root causes.

## Reconciliation

| Measure | Minutes | Interpretation |
| --- | ---: | --- |
| Captured summary | 115 | Deliberately incomplete SUM range. |
| Sum of all reported row values | 127 | Includes the duplicate and incorrect row values. |
| Sum of computable C × D values | 142 | Includes both R002 rows; excludes R003 because units are unknown. This is a partial subtotal. |
| Conditional subtotal if one identical R002 row is confirmed redundant | 112 | 142 − 30. Still excludes R003; not a corrected final total. |
| Approved unique-request total | Unavailable | Requires duplicate resolution and the missing R003 quantity. |

R006 has zero units and zero reported minutes. It passes the numeric checks. Treating it as missing would create a false positive.

## Handoff

The source owner must resolve R002 and supply R003 units. The spreadsheet maintainer should correct E6 and the E10 range, then investigate E7's formula/value mismatch. The reviewer should rerun the checks on a separate corrected copy, confirm the raw-to-final row reconciliation, and record the owner responses before accepting a total. These are proposed workflow roles, not claims that a real team performed the actions.
