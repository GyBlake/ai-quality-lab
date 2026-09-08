"""Small deterministic evaluation engine with evidence traces.

The engine is intentionally dependency-free. It does not call an LLM. Each
criterion produces a machine-readable decision containing the rule, observed
evidence, and weighted score contribution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _normalise(value: str) -> str:
    return " ".join(value.lower().split())


def _criterion_result(text: str, criterion: dict[str, Any]) -> dict[str, Any]:
    cid = criterion["id"]
    rule = criterion["rule"]
    weight = float(criterion.get("weight", 1.0))
    source = criterion.get("source")
    normalised = _normalise(text)
    values = criterion.get("values", [])
    matched: list[str] = []
    passed = False

    if rule == "contains_any":
        matched = [value for value in values if _normalise(value) in normalised]
        passed = bool(matched)
    elif rule == "contains_all":
        matched = [value for value in values if _normalise(value) in normalised]
        passed = len(matched) == len(values)
    elif rule == "excludes_any":
        matched = [value for value in values if _normalise(value) in normalised]
        passed = not matched
    elif rule == "max_chars":
        limit = int(criterion["value"])
        passed = len(text) <= limit
        matched = [f"chars={len(text)}", f"limit={limit}"]
    elif rule == "min_chars":
        limit = int(criterion["value"])
        passed = len(text) >= limit
        matched = [f"chars={len(text)}", f"limit={limit}"]
    else:
        raise ValueError(f"Unsupported rule: {rule}")

    return {
        "criterion_id": cid,
        "description": criterion.get("description", ""),
        "source": source,
        "rule": rule,
        "passed": passed,
        "weight": weight,
        "score": weight if passed else 0.0,
        "evidence": matched,
    }


def evaluate_response(record: dict[str, Any], rubric: dict[str, Any]) -> dict[str, Any]:
    text = str(record.get("response", ""))
    results = [_criterion_result(text, item) for item in rubric["criteria"]]
    earned = sum(item["score"] for item in results)
    possible = sum(item["weight"] for item in results)
    percent = round((earned / possible * 100.0) if possible else 0.0, 2)
    threshold = float(rubric.get("pass_threshold", 100.0))
    failed = [item["criterion_id"] for item in results if not item["passed"]]

    return {
        "id": record.get("id"),
        "score": earned,
        "possible": possible,
        "percent": percent,
        "pass_threshold": threshold,
        "passed": percent >= threshold,
        "failed_criteria": failed,
        "trace": results,
    }


def evaluate_records(records: list[dict[str, Any]], rubric: dict[str, Any]) -> dict[str, Any]:
    results = [evaluate_response(record, rubric) for record in records]
    passed = sum(1 for item in results if item["passed"])
    failure_counts: dict[str, int] = {}
    for item in results:
        for criterion_id in item["failed_criteria"]:
            failure_counts[criterion_id] = failure_counts.get(criterion_id, 0) + 1

    return {
        "rubric": rubric.get("name", "unnamed"),
        "records": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": round((passed / len(results) * 100.0) if results else 0.0, 2),
        "failure_counts": dict(sorted(failure_counts.items())),
        "results": results,
    }
