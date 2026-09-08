"""Deterministic evaluation primitives for ai-quality-lab."""

from .evaluator import evaluate_records, evaluate_response, load_json

__all__ = ["evaluate_records", "evaluate_response", "load_json"]
__version__ = "0.1.0"
