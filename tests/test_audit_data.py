"""Behavior tests for the synthetic source contract and audit decisions."""

import copy
import unittest

from scripts.audit_data import audit, load_fixture


def clean_fixture():
    rows = [{"request_id": "R001", "queue": "standard", "units": "2",
             "minutes_per_unit": "5", "reported_minutes": "10"}]
    snapshot = {"formulas": {"E2": "=C2*D2"},
                "summary": {"cell": "E3", "formula": "=SUM(E2:E2)", "reported_minutes": 10}}
    return rows, snapshot


class AuditTests(unittest.TestCase):
    def test_clean_input(self):
        result = audit(*clean_fixture())
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["accepted_unique_request_total_minutes"], 10)

    def test_valid_zero_is_not_missing(self):
        rows, snapshot = clean_fixture()
        rows[0].update(units="0", reported_minutes="0")
        snapshot["summary"]["reported_minutes"] = 0
        result = audit(rows, snapshot)
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["accepted_unique_request_total_minutes"], 0)

    def test_missing_units_do_not_become_zero(self):
        rows, snapshot = clean_fixture()
        rows[0].update(units="", reported_minutes="0")
        snapshot["summary"]["reported_minutes"] = 0
        result = audit(rows, snapshot)
        self.assertIn("MISSING_VALUE", {f["code"] for f in result["findings"]})
        self.assertEqual(result["uncomputable_input_rows"], [2])
        self.assertIsNone(result["accepted_unique_request_total_minutes"])

    def test_duplicate_does_not_silently_deduplicate(self):
        rows, snapshot = clean_fixture()
        rows.append(copy.deepcopy(rows[0]))
        snapshot["formulas"]["E3"] = "=C3*D3"
        snapshot["summary"] = {"cell": "E4", "formula": "=SUM(E2:E3)", "reported_minutes": 20}
        result = audit(rows, snapshot)
        self.assertEqual([f["code"] for f in result["findings"]], ["DUPLICATE_ID"])
        self.assertEqual(result["reported_detail_minutes"], 20)
        self.assertIsNone(result["accepted_unique_request_total_minutes"])
        self.assertEqual(len(rows), 2)

    def test_shifted_reference_is_flagged_even_if_value_matches(self):
        rows, snapshot = clean_fixture()
        snapshot["formulas"]["E2"] = "=C2*D1"
        result = audit(rows, snapshot)
        self.assertEqual([f["code"] for f in result["findings"]], ["FORMULA_REFERENCE"])

    def test_wrong_value_with_right_formula(self):
        rows, snapshot = clean_fixture()
        rows[0]["reported_minutes"] = "11"
        snapshot["summary"]["reported_minutes"] = 11
        result = audit(rows, snapshot)
        self.assertEqual([f["code"] for f in result["findings"]], ["BAD_ROW_TOTAL"])

    def test_invalid_numbers_cannot_produce_an_accepted_total(self):
        for field, value in [("units", "-1"), ("units", "1.5"), ("units", "NaN"),
                             ("minutes_per_unit", "0"), ("reported_minutes", "oops")]:
            with self.subTest(field=field, value=value):
                rows, snapshot = clean_fixture()
                rows[0][field] = value
                result = audit(rows, snapshot)
                self.assertIn("INVALID_NUMBER", {f["code"] for f in result["findings"]})
                self.assertIsNone(result["accepted_unique_request_total_minutes"])
                if field == "reported_minutes":
                    self.assertIsNone(result["reported_detail_minutes"])

    def test_unknown_queue_is_flagged(self):
        rows, snapshot = clean_fixture()
        rows[0]["queue"] = "urgent"
        self.assertIn("INVALID_CATEGORY", {f["code"] for f in audit(rows, snapshot)["findings"]})

    def test_complete_fixture_reconciles_and_preserves_evidence(self):
        rows, snapshot = load_fixture()
        original = copy.deepcopy((rows, snapshot))
        result = audit(rows, snapshot)
        self.assertEqual(result["reported_detail_minutes"], 127)
        self.assertEqual(result["computable_input_subtotal_minutes"], 142)
        self.assertEqual(result["diagnostic_count"], 8)
        self.assertEqual(result["uncomputable_input_rows"], [5])
        self.assertIn(("SUMMARY_RANGE", "E10"), {(f["code"], f["cell"]) for f in result["findings"]})
        self.assertIn(("BAD_SUMMARY_TOTAL", "E10"), {(f["code"], f["cell"]) for f in result["findings"]})
        self.assertEqual((rows, snapshot), original)


if __name__ == "__main__":
    unittest.main()
