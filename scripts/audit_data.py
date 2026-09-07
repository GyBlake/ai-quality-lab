#!/usr/bin/env python3
"""Audit the fixed synthetic Requests fixture. No formula execution or repairs."""

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "data-quality"
FIELDS = ["request_id", "queue", "units", "minutes_per_unit", "reported_minutes"]


def integer(value):
    """Return a canonical nonnegative integer, or None for missing/invalid input."""
    if isinstance(value, str) and re.fullmatch(r"0|[1-9][0-9]*", value):
        return int(value)
    return None


def audit(rows, snapshot):
    """Check the documented column layout; return findings without modifying rows."""
    findings = []
    first_seen = {}
    raw_total = 0
    reported_values_valid = True
    computable_subtotal = 0
    uncomputable_rows = []

    def flag(code, cell, detail):
        findings.append({"code": code, "cell": cell, "detail": detail})

    for row_number, row in enumerate(rows, start=2):
        for column, field in zip("ABCDE", FIELDS):
            if not row[field]:
                flag("MISSING_VALUE", f"{column}{row_number}", f"Required field {field} is blank.")

        key = row["request_id"]
        if key:
            if key in first_seen:
                flag("DUPLICATE_ID", f"A{row_number}", f"{key} also appears at A{first_seen[key]}; reconcile before deduplication.")
            else:
                first_seen[key] = row_number
        if row["queue"] and row["queue"] not in {"standard", "priority"}:
            flag("INVALID_CATEGORY", f"B{row_number}", "Expected standard or priority.")

        values = {}
        for column, field in zip("CDE", FIELDS[2:]):
            value = integer(row[field])
            if field == "minutes_per_unit" and value == 0:
                value = None
            values[field] = value
            if row[field] and value is None:
                flag("INVALID_NUMBER", f"{column}{row_number}", f"{field} violates the integer domain in the source contract.")

        units = values["units"]
        rate = values["minutes_per_unit"]
        reported = values["reported_minutes"]
        if reported is None:
            reported_values_valid = False
        else:
            raw_total += reported

        cell = f"E{row_number}"
        expected_formula = f"=C{row_number}*D{row_number}"
        actual_formula = snapshot["formulas"].get(cell)
        if actual_formula != expected_formula:
            flag("FORMULA_REFERENCE", cell, f"Captured {actual_formula!r}; expected fixed-layout pattern {expected_formula}.")

        if units is None or rate is None:
            uncomputable_rows.append(row_number)
            if actual_formula == expected_formula:
                flag("MISSING_INPUT_GUARD", cell, "Captured multiplication has no explicit unavailable state for invalid or missing inputs.")
        else:
            expected = units * rate
            computable_subtotal += expected
            if reported is not None and reported != expected:
                flag("BAD_ROW_TOTAL", cell, f"Reported {reported}; same-row inputs imply {expected} minutes.")

    last_row = len(rows) + 1
    summary = snapshot["summary"]
    expected_summary_cell = f"E{last_row + 1}"
    if summary["cell"] != expected_summary_cell:
        flag("SUMMARY_LOCATION", summary["cell"], f"Expected summary at {expected_summary_cell} for this layout.")
    expected_range = f"=SUM(E2:E{last_row})"
    if summary["formula"] != expected_range:
        flag("SUMMARY_RANGE", summary["cell"], f"Captured {summary['formula']}; full raw detail requires {expected_range}.")
    captured_total = summary["reported_minutes"]
    if type(captured_total) is not int or captured_total < 0:
        flag("INVALID_SUMMARY_VALUE", summary["cell"], "Expected a nonnegative integer summary value.")
    elif reported_values_valid and captured_total != raw_total:
        flag("BAD_SUMMARY_TOTAL", summary["cell"], f"Reported {captured_total}; full raw detail sums to {raw_total} minutes.")

    return {
        "scope": "Synthetic fixed-layout request audit; no workbook engine execution.",
        "rows_reviewed": len(rows),
        "diagnostic_count": len(findings),
        "disposition": "hold_for_review" if findings else "no_detected_defects_within_scope",
        "reported_detail_minutes": raw_total if reported_values_valid else None,
        "computable_input_subtotal_minutes": computable_subtotal,
        "uncomputable_input_rows": uncomputable_rows,
        "accepted_unique_request_total_minutes": None if findings else computable_subtotal,
        "findings": findings,
    }


def load_fixture():
    with (PROJECT / "data" / "requests.csv").open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != FIELDS:
            raise ValueError("CSV columns do not match the documented source contract.")
        rows = list(reader)
        if not rows or any(set(row) != set(FIELDS) or None in row.values() for row in rows):
            raise ValueError("Expected nonempty rows with exactly the documented columns.")
    snapshot = json.loads((PROJECT / "data" / "formula-snapshot.json").read_text(encoding="utf-8"))
    return rows, snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Compare with the saved demonstration report.")
    mode.add_argument("--write", action="store_true", help="Regenerate the saved report after a deliberate fixture change.")
    args = parser.parse_args()
    report = audit(*load_fixture())
    output = json.dumps(report, indent=2) + "\n"
    saved = PROJECT / "sample-output" / "audit-report.json"
    if args.check:
        if not saved.exists() or json.loads(saved.read_text(encoding="utf-8")) != report:
            print("Mismatch: inspect the findings before regenerating the sample report.")
            return 1
        print(f"Sample report matches: {report['diagnostic_count']} expected diagnostics; disposition={report['disposition']}.")
    elif args.write:
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_text(output, encoding="utf-8")
        print("Updated projects/data-quality/sample-output/audit-report.json")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
