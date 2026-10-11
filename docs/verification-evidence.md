# Verification Evidence

This page separates observed CI results from claims that still require a local demonstration.

## Verified in GitHub Actions

- Workflow: [AI Quality Lab CI](https://github.com/GyBlake/ai-quality-lab/actions/workflows/ci.yml)
- Run: [Run #11](https://github.com/GyBlake/ai-quality-lab/actions/runs/38169745505)
- Result: successful
- Matrix jobs: Python 3.10, 3.11, and 3.12
- Test step: `python -m unittest discover -s tests -p "test_*.py"`
- Failure handling: the test command is not followed by a fallback that masks its exit code.

This confirms the repository's configured unit-test discovery completed successfully in the three matrix environments for that run. It does not prove semantic correctness beyond the tests, model-level truthfulness, or performance on external datasets.

## Reproduce locally

Requires Python 3.10 or newer.

```bash
python -m pip install -e .
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/audit_data.py --check
python -m ai_quality.cli --help
```

If the installed package exposes a different CLI entry point in a future version, follow the current package metadata and README. Do not interpret the synthetic data audit's expected defect findings as a claim that the intentionally broken fixture is clean.

## Evidence boundary

The repository contains synthetic examples and deterministic checks. The evaluator's keyword/string rules are a reproducible baseline, not a general substitute for expert review or semantic evaluation. This page records the CI result above; it is not a claim that an independent local run was performed during this portfolio update.

## Visual demo status

No application screenshots are attached yet. Add genuine captures from a local run before using screenshots in a public portfolio. Do not use mockups as if they were live product evidence.
