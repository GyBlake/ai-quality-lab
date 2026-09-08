"""Command-line entry point for deterministic response evaluation."""

from __future__ import annotations

import argparse
import json

from .evaluator import evaluate_records, load_json


def main() -> int:
    parser = argparse.ArgumentParser(prog="aq", description="Evaluate response records against a deterministic JSON rubric.")
    parser.add_argument("responses", help="JSON file containing a list of records with id and response fields")
    parser.add_argument("--rubric", required=True, help="JSON rubric file")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    args = parser.parse_args()

    records = load_json(args.responses)
    rubric = load_json(args.rubric)
    if not isinstance(records, list):
        raise SystemExit("Responses file must contain a JSON list.")
    if not isinstance(rubric, dict) or not isinstance(rubric.get("criteria"), list):
        raise SystemExit("Rubric must be a JSON object containing a criteria list.")

    result = evaluate_records(records, rubric)
    if args.compact:
        print(json.dumps(result, separators=(",", ":")))
    else:
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
