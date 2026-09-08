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


def _index_records(records: list[dict[str, Any]], side: str) -> dict[Any, dict[str, Any]]:
    indexed: dict[Any, dict[str, Any]] = {}
    for record in records:
        record_id = record.get("id")
        if record_id is None:
            raise ValueError(f"Every {side} comparison record must have an id.")
        if record_id in indexed:
            raise ValueError(f"Duplicate {side} comparison id: {record_id}")
        indexed[record_id] = record
    return indexed


def compare_records(
    left_records: list[dict[str, Any]],
    right_records: list[dict[str, Any]],
    rubric: dict[str, Any],
    *,
    left_name: str = "left",
    right_name: str = "right",
) -> dict[str, Any]:
    """Compare two response sets by shared record id under one rubric.

    A winner is based only on weighted rubric score. Per-criterion differences
    are preserved so an equal total does not hide different strengths or
    failures. Missing or duplicate ids are rejected rather than guessed.
    """

    left_index = _index_records(left_records, left_name)
    right_index = _index_records(right_records, right_name)
    left_ids = set(left_index)
    right_ids = set(right_index)
    if left_ids != right_ids:
        missing_left = sorted(right_ids - left_ids, key=str)
        missing_right = sorted(left_ids - right_ids, key=str)
        raise ValueError(
            "Comparison sets must contain the same ids; "
            f"missing from {left_name}={missing_left}, missing from {right_name}={missing_right}."
        )

    wins = {left_name: 0, right_name: 0, "tie": 0}
    criterion_wins: dict[str, dict[str, int]] = {}
    pairs: list[dict[str, Any]] = []

    for record_id in sorted(left_ids, key=str):
        left_result = evaluate_response(left_index[record_id], rubric)
        right_result = evaluate_response(right_index[record_id], rubric)

        if left_result["score"] > right_result["score"]:
            winner = left_name
        elif right_result["score"] > left_result["score"]:
            winner = right_name
        else:
            winner = "tie"
        wins[winner] += 1

        left_trace = {item["criterion_id"]: item for item in left_result["trace"]}
        right_trace = {item["criterion_id"]: item for item in right_result["trace"]}
        deltas = []
        for criterion in rubric["criteria"]:
            cid = criterion["id"]
            left_item = left_trace[cid]
            right_item = right_trace[cid]
            if left_item["score"] > right_item["score"]:
                criterion_winner = left_name
            elif right_item["score"] > left_item["score"]:
                criterion_winner = right_name
            else:
                criterion_winner = "tie"
            counts = criterion_wins.setdefault(cid, {left_name: 0, right_name: 0, "tie": 0})
            counts[criterion_winner] += 1
            deltas.append(
                {
                    "criterion_id": cid,
                    "winner": criterion_winner,
                    left_name: {
                        "passed": left_item["passed"],
                        "score": left_item["score"],
                        "evidence": left_item["evidence"],
                    },
                    right_name: {
                        "passed": right_item["passed"],
                        "score": right_item["score"],
                        "evidence": right_item["evidence"],
                    },
                }
            )

        pairs.append(
            {
                "id": record_id,
                "winner": winner,
                "score_delta": round(left_result["score"] - right_result["score"], 6),
                left_name: left_result,
                right_name: right_result,
                "criterion_deltas": deltas,
            }
        )

    pair_count = len(pairs)
    return {
        "rubric": rubric.get("name", "unnamed"),
        "left": left_name,
        "right": right_name,
        "pairs": pair_count,
        "wins": wins,
        "win_rates": {
            left_name: round((wins[left_name] / pair_count * 100.0) if pair_count else 0.0, 2),
            right_name: round((wins[right_name] / pair_count * 100.0) if pair_count else 0.0, 2),
            "tie": round((wins["tie"] / pair_count * 100.0) if pair_count else 0.0, 2),
        },
        "criterion_wins": criterion_wins,
        "results": pairs,
    }
