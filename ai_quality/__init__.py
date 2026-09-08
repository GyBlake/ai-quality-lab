"""Deterministic evaluation primitives for ai-quality-lab."""

from .evaluator import compare_records, evaluate_records, evaluate_response, load_json

__all__ = ["compare_records", "evaluate_records", "evaluate_response", "load_json"]
__version__ = "0.2.0"
