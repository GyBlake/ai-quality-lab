import unittest

from ai_quality.evaluator import compare_records, evaluate_records, evaluate_response


RUBRIC = {
    "name": "test-rubric",
    "pass_threshold": 75,
    "criteria": [
        {"id": "grounded", "rule": "contains_any", "values": ["source"], "weight": 2},
        {"id": "no_promise", "rule": "excludes_any", "values": ["guaranteed"], "weight": 2},
    ],
}


class EvaluatorTests(unittest.TestCase):
    def test_passes_when_all_weighted_rules_pass(self):
        result = evaluate_response({"id": "a", "response": "According to the source, this is supported."}, RUBRIC)
        self.assertTrue(result["passed"])
        self.assertEqual(result["percent"], 100.0)
        self.assertEqual(result["failed_criteria"], [])

    def test_trace_exposes_failed_rule_and_evidence(self):
        result = evaluate_response({"id": "b", "response": "This is guaranteed."}, RUBRIC)
        self.assertFalse(result["passed"])
        self.assertEqual(set(result["failed_criteria"]), {"grounded", "no_promise"})
        no_promise = next(item for item in result["trace"] if item["criterion_id"] == "no_promise")
        self.assertEqual(no_promise["evidence"], ["guaranteed"])

    def test_batch_reports_failure_clusters(self):
        result = evaluate_records(
            [
                {"id": "a", "response": "source"},
                {"id": "b", "response": "guaranteed"},
            ],
            RUBRIC,
        )
        self.assertEqual(result["records"], 2)
        self.assertEqual(result["passed"], 1)
        self.assertEqual(result["failure_counts"], {"grounded": 1, "no_promise": 1})

    def test_compare_picks_winner_and_preserves_criterion_deltas(self):
        result = compare_records(
            [{"id": "case-1", "response": "According to the source."}],
            [{"id": "case-1", "response": "This is guaranteed."}],
            RUBRIC,
            left_name="model_a",
            right_name="model_b",
        )
        self.assertEqual(result["wins"], {"model_a": 1, "model_b": 0, "tie": 0})
        pair = result["results"][0]
        self.assertEqual(pair["winner"], "model_a")
        self.assertGreater(pair["score_delta"], 0)
        deltas = {item["criterion_id"]: item for item in pair["criterion_deltas"]}
        self.assertEqual(deltas["grounded"]["winner"], "model_a")
        self.assertEqual(deltas["no_promise"]["winner"], "model_a")

    def test_compare_rejects_mismatched_ids(self):
        with self.assertRaisesRegex(ValueError, "same ids"):
            compare_records(
                [{"id": "case-1", "response": "source"}],
                [{"id": "case-2", "response": "source"}],
                RUBRIC,
            )

    def test_compare_rejects_duplicate_ids(self):
        with self.assertRaisesRegex(ValueError, "Duplicate left comparison id"):
            compare_records(
                [
                    {"id": "case-1", "response": "source"},
                    {"id": "case-1", "response": "source"},
                ],
                [{"id": "case-1", "response": "source"}],
                RUBRIC,
            )

    def test_unknown_rule_is_rejected(self):
        bad = {"name": "bad", "criteria": [{"id": "x", "rule": "magic", "weight": 1}]}
        with self.assertRaises(ValueError):
            evaluate_response({"id": "x", "response": "text"}, bad)


if __name__ == "__main__":
    unittest.main()
