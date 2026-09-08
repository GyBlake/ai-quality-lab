# ai-quality-lab

Evidence-trace evaluation and data-quality utilities for AI systems.

The project is built around one rule: **a quality judgment should be traceable from requirement → evidence → decision → disposition.** It combines a runnable deterministic response evaluator with source-grounded rubrics, pairwise comparison, prompt regression fixtures, and operational data audits.

This is an early-stage toolkit. It does not pretend deterministic string rules are a replacement for expert review or model-based judging. Instead, it provides a reproducible baseline that can be inspected, tested, extended, and compared.

## What works now

### 1. Deterministic response evaluation

Install locally and run the `aq` CLI against a JSON response set and rubric:

```bash
python -m pip install .
aq examples/eval/responses.json --rubric examples/eval/rubric.json
```

Each criterion emits an evidence trace containing the rule, source statement, matched evidence, weighted score, and pass/fail decision. Batch output includes pass rate and clustered failure counts.

Supported rules:

- `contains_any`
- `contains_all`
- `excludes_any`
- `max_chars`
- `min_chars`

The engine is dependency-free and makes no network or model calls.

### 2. Pairwise model-output comparison

Compare two response sets that share the same case IDs:

```bash
aq compare examples/eval/model-a.json examples/eval/model-b.json \
  --rubric examples/eval/rubric.json \
  --left-name model_a \
  --right-name model_b
```

The report tells you who won each case, the score difference, which criteria caused the difference, and the evidence seen on both sides. Equal totals are kept as ties, while criterion-level differences remain visible. Missing or duplicate case IDs fail loudly instead of being silently paired.

The comparison output includes aggregate wins and win rates plus per-criterion win counts, so the tool can answer both **which model won?** and **where did it win?**

### 3. Spreadsheet / operational data QA

The existing synthetic Requests audit checks duplicate IDs, missing inputs, invalid numeric values, shifted formula references, row-total mismatches, and broken summary ranges.

```bash
python scripts/audit_data.py
python scripts/audit_data.py --check
```

A successful `--check` means the intentionally broken fixture reproduces the expected diagnostics. It does **not** mean the data is clean.

### 4. Prompt regression fixtures

The prompt-testing project demonstrates explicit routing rules, ambiguity handling, structured output contracts, and regression cases including embedded instruction attacks.

## Existing evaluation examples

| Example | Start here | What it covers |
| --- | --- | --- |
| Runnable evaluator | [Rubric](examples/eval/rubric.json) | Weighted deterministic checks, evidence traces, failure clustering |
| Pairwise comparison | [Model A](examples/eval/model-a.json) / [Model B](examples/eval/model-b.json) | Case-by-case winners, criterion deltas, evidence on both sides |
| AI response evaluation | [Completed comparison](projects/ai-evaluation/cases/01-policy-answer.md) | A/B scoring, unsupported claims, failure tags, and [when to accept neither answer](projects/ai-evaluation/cases/02-conflicting-versions.md) |
| Spreadsheet / data QA | [Audit findings](projects/data-quality/audit-findings.md) | Duplicate IDs, missing values, shifted references, and totals that do not reconcile |
| Prompt refinement | [Prompt test case](projects/prompt-testing/README.md) | Explicit label rules, structured output, ambiguity handling, and regression fixtures |

All data, policies, prompts, and candidate responses are synthetic unless a future dataset explicitly states otherwise. Candidate responses are constructed examples, not outputs attributed to real models. See [provenance](docs/provenance.md).

## Run the full test suite

Requires Python 3.10+.

```bash
python -m unittest discover -s tests -v
python scripts/audit_data.py --check
```

GitHub Actions runs the package, legacy audit, unit tests, evaluator CLI, and pairwise comparison CLI on Python 3.10, 3.11, and 3.12.

## Layout

```text
ai_quality/          Reusable evaluation engine and CLI
examples/eval/       Runnable rubric, response, and pairwise fixtures
projects/
  ai-evaluation/     Rubric, source passages, A/B evaluations
  data-quality/      CSV, formula snapshot, findings, sample report
  prompt-testing/    Prompt versions, contract, regression cases
scripts/             Operational data audit
tests/               Evaluation, data, and prompt regression tests
docs/                Scope, reproduction notes, provenance, publishing
```

## Design principles

Define the acceptance rule before scoring. Preserve source records. Separate an observed defect from its possible cause. Keep unknown values distinct from valid zeroes. Every automated decision should expose enough evidence for a human to challenge it.

The deterministic evaluator is deliberately narrow. Keyword presence alone cannot establish truth, semantic equivalence, or instruction compliance in general. That boundary is part of the design, not hidden behind a confidence score.

## Roadmap

The next competitive layers are:

1. versioned rubric schemas and validation
2. baseline-vs-candidate regression reports
3. evaluator disagreement and uncertainty representation
4. pluggable deterministic and model-based judges
5. HTML/JSON audit reports with stable evidence IDs
6. benchmark datasets with explicit provenance and contamination notes

Contributions should make a judgment more reproducible, falsifiable, or useful. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and [TODO.md](TODO.md).

## Maintainer

Maintained by [PrimeÆClyptic (@GyBlake)](https://github.com/GyBlake).

I work across AI evaluation, data quality, prompt testing, and technical operations. Additional projects and R&D work are maintained privately.

## License

[MIT](LICENSE). Applies to the code, documentation, and synthetic fixtures in this repository.
