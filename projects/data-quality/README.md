# Spreadsheet and data-quality audit

**Decision: hold the total for review.** The source contains a duplicate ID and a missing quantity; correcting arithmetic alone cannot establish a reliable unique-request total.

This synthetic operations example reviews planned handling minutes. It is a text representation of a small worksheet, with CSV inputs and formula strings. No binary XLSX is required and no native Excel or Google Sheets execution is claimed.

## Inspect the evidence

- [Source CSV](data/requests.csv): eight rows with deliberately seeded defects and one valid zero.
- [Formula snapshot](data/formula-snapshot.json): intended worksheet locations and captured formula text.
- [Data dictionary](data-dictionary.md): row meaning, types, and acceptance rules.
- [Audit findings](audit-findings.md): locations, effects, and corrective actions.
- [Spreadsheet checks](spreadsheet-checks.md): formulas and import instructions for a review copy.
- [Generated report](sample-output/audit-report.json): deterministic output from the [Python checker](../../scripts/audit_data.py).

## Reproduce

From the repository root, using Python 3.10+ with no external packages:

```bash
python3 scripts/audit_data.py
python3 scripts/audit_data.py --check
python3 -m unittest discover -s tests -v
```

The first command prints JSON without changing files. `--check` compares that result with the committed sample report. Exit 0 means the expected demonstration report matches, even though it intentionally contains defects. Exit 1 means the snapshot differs; malformed inputs produce an error. To regenerate the report after an intentional fixture change:

```bash
python3 scripts/audit_data.py --write
```

## What the script establishes

It independently checks integer inputs, duplicate keys, row arithmetic, a narrow expected formula pattern, and the summary range/value. It preserves the raw rows. It does not evaluate Excel formulas, inspect a real workbook, approve deletions, infer missing units, or certify the source as complete. A production checker would need a broader schema, controlled input handling, and workbook-engine validation appropriate to the actual workflow.
