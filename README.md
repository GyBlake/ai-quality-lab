# ai-quality-lab

Small, inspectable examples for evaluating AI responses and checking operational data. The lab combines source-grounded rubrics, prompt regression fixtures, and a dependency-free Python audit.

The focus is the review decision: what failed, which evidence supports that judgment, and what needs clarification before the result can be used.

## Examples

| Example | Start here | What it covers |
| --- | --- | --- |
| AI response evaluation | [Completed comparison](projects/ai-evaluation/cases/01-policy-answer.md) | A/B scoring, unsupported claims, failure tags, and [when to accept neither answer](projects/ai-evaluation/cases/02-conflicting-versions.md). |
| Spreadsheet / data QA | [Audit findings](projects/data-quality/audit-findings.md) | Duplicate IDs, missing values, shifted references, and totals that do not reconcile. |
| Prompt refinement | [Prompt test case](projects/prompt-testing/README.md) | Explicit label rules, structured output, ambiguity handling, and regression fixtures. |

All data, policies, prompts, and candidate responses are synthetic. Candidate responses are constructed examples, not outputs attributed to real models. This is a small demonstration lab, not a model benchmark. See [provenance](docs/provenance.md).

## Run locally

Requires Python 3.10+; no dependencies, API keys, or network calls.

```bash
python3 scripts/audit_data.py
python3 scripts/audit_data.py --check
python3 -m unittest discover -s tests -v
```

Run from the repository root. The audit prints a JSON report; `--check` verifies it against the saved sample. The fixture intentionally contains defects: a successful check means those expected findings reproduce, not that the data is clean.

The tests cover blank versus zero, duplicates, arithmetic and formula-reference defects, invalid numeric values, and prompt-output contracts. They do not call a model or execute a spreadsheet engine.

## Layout

```text
projects/
  ai-evaluation/    Rubric, source passages, A/B evaluations
  data-quality/     CSV, formula snapshot, findings, sample report
  prompt-testing/   Prompt versions, contract, regression cases
scripts/           Small standard-library audit script
tests/             Data checks and prompt-fixture validation
docs/              Scope, reproduction notes, and publishing
```

For the complete file map and naming conventions, see the [repository guide](docs/repository-guide.md).

## Review approach

Define the acceptance rule before scoring. Preserve source records. Separate an observed defect from its possible cause, and keep unknown values distinct from valid zeroes. Each review should leave enough evidence and a next action for someone else to continue asynchronously.

The spreadsheet example is supplied as CSV and formula text. The Python script checks a deliberately narrow contract; it is not a general workbook auditor. The prompt examples illustrate expected behavior; they do not establish live model reliability.

## Contributing and open work

Useful contributions include a counterexample, a clearer rubric anchor, or a test exposing a false positive. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and the concrete items in [TODO.md](TODO.md). Keep examples synthetic and include a reproducible expected result.

## Maintainer

Maintained by [PrimeÆClyptic (@GyBlake)](https://github.com/GyBlake).

I work across AI evaluation, data quality, prompt testing, and technical operations. Additional projects and R&D work are maintained privately.

## License

[MIT](LICENSE). Applies to the code, documentation, and synthetic fixtures in this repository.
