# Validation record

Initial local validation: September 7, 2026.

Environment: macOS, Python 3.13.3. The examples target Python 3.10+, but other Python versions and operating systems have not been tested in this build.

## Commands and results

```bash
python3 scripts/audit_data.py --check
python3 -m unittest discover -s tests -v
```

The saved audit report reproduces **8 diagnostics** and `hold_for_review`. The **15 tests** pass. Counts describe this fixture and test suite only.

The audit’s raw reported detail is 127 minutes; its computable input subtotal is 142 minutes, including the repeated R002 row and excluding the missing R003 quantity. The accepted unique-request total remains null.

## Coverage

The data tests exercise a clean input, a valid zero, a missing quantity, a repeated ID, a shifted reference even when its reported number happens to match, a bad reported value with a correct formula, invalid numeric domains, an unknown queue, and the full fixture's reconciliation. A copy comparison confirms the audit preserves its input records.

The prompt tests check the four saved candidates, missing/extra keys, unsupported evidence, mismatched routes, an unjustified label on an ambiguous request, and invalid value types. They do not assess model behavior.

The local package check also parses all JSON files and resolves repository-local Markdown links. The Python audit executes no supplied formulas and makes no network calls.

## Limits

No live model calls, independent second-reviewer calibration, native Excel/Google Sheets recalculation, cloud CI run, or production-data trial was performed. The spreadsheet instructions are a text guide with expected results; native-engine verification is an open TODO.

This record describes the initial local build. Update it when the documented validation scope changes; use test output and actual commits as evidence for later changes.
