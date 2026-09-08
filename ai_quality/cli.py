"""Command-line entry point for deterministic response evaluation."""

from __future__ import annotations

import argparse
import json
import sys

from .evaluator import compare_records, evaluate_records, load_json


def _validate_rubric(rubric: object) -> dict:
    if not isinstance(rubric, dict) or not isinstance(rubric.get("criteria"), list):
        raise SystemExit("Rubric must be a JSON object containing a criteria list.")
    return rubric


def _print_result(result: dict, compact: bool) -> None:
    if compact:
        print(json.dumps(result, separators=(",", ":")))
    else:
        print(json.dumps(result, indent=2))


def _run_compare(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="aq compare", description="Compare two response sets against the same rubric.")
    parser.add_argument("left", help="JSON file containing the left response set")
    parser.add_argument("right", help="JSON file containing the right response set")
    parser.add_argument("--rubric", required=True, help="JSON rubric file")
    parser.add_argument("--left-name", default="left", help="Label used for the left response set")
    parser.add_argument("--right-name", default="right", help="Label used for the right response set")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    args = parser.parse_args(argv)

    if args.left_name == args.right_name or "tie" in {args.left_name, args.right_name}:
        raise SystemExit("Comparison labels must be distinct and cannot be 'tie'.")

    left = load_json(args.left)
    right = load_json(args.right)
    rubric = _validate_rubric(load_json(args.rubric))
    if not isinstance(left, list) or not isinstance(right, list):
        raise SystemExit("Both comparison files must contain JSON lists.")

    try:
        result = compare_records(left, right, rubric, left_name=args.left_name, right_name=args.right_name)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    _print_result(result, args.compact)
    return 0


def _run_evaluate(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="aq", description="Evaluate response records against a deterministic JSON rubric.")
    parser.add_argument("responses", help="JSON file containing a list of records with id and response fields")
    parser.add_argument("--rubric", required=True, help="JSON rubric file")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    args = parser.parse_args(argv)

    records = load_json(args.responses)
    rubric = _validate_rubric(load_json(args.rubric))
    if not isinstance(records, list):
        raise SystemExit("Responses file must contain a JSON list.")

    _print_result(evaluate_records(records, rubric), args.compact)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "compare":
        return _run_compare(args[1:])
    return _run_evaluate(args)


if __name__ == "__main__":
    raise SystemExit(main())
