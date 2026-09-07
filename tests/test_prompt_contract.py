"""Validate saved synthetic responses; these tests do not run an AI model."""

import copy
import json
from pathlib import Path
import unittest


CASES_PATH = Path(__file__).resolve().parents[1] / "projects" / "prompt-testing" / "cases.json"
ROUTES = {"access": "route_access_review", "data_fix": "route_data_review", "needs_review": "ask_clarification"}


def validate_candidate(case, candidate):
    if not isinstance(candidate, dict) or set(candidate) != {"label", "evidence", "next_step"}:
        return False
    if not all(isinstance(value, str) for value in candidate.values()):
        return False
    label = candidate["label"]
    evidence = candidate["evidence"]
    return (
        label in ROUTES
        and label == case["expected_label"]
        and candidate["next_step"] == ROUTES[label]
        and 0 < len(evidence) <= 120
        and evidence in case["request"]
    )


class PromptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))["cases"]

    def test_saved_candidates_match_contract_and_expected_labels(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(validate_candidate(case, case["candidate"]))

    def test_missing_or_extra_keys_are_rejected(self):
        case = self.cases[0]
        candidate = copy.deepcopy(case["candidate"])
        candidate.pop("evidence")
        self.assertFalse(validate_candidate(case, candidate))
        candidate = dict(case["candidate"], confidence="high")
        self.assertFalse(validate_candidate(case, candidate))

    def test_unsupported_evidence_is_rejected(self):
        case = self.cases[0]
        for evidence in ["", "Reset the password", "x" * 121]:
            self.assertFalse(validate_candidate(case, dict(case["candidate"], evidence=evidence)))

    def test_wrong_route_is_rejected(self):
        case = self.cases[0]
        self.assertFalse(validate_candidate(case, dict(case["candidate"], next_step="route_data_review")))

    def test_forced_ambiguous_label_is_rejected(self):
        case = self.cases[2]
        candidate = dict(case["candidate"], label="access", next_step="route_access_review")
        self.assertFalse(validate_candidate(case, candidate))

    def test_invalid_types_are_rejected(self):
        case = self.cases[0]
        self.assertFalse(validate_candidate(case, None))
        self.assertFalse(validate_candidate(case, dict(case["candidate"], label=[])))


if __name__ == "__main__":
    unittest.main()
