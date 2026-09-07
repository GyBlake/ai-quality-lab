# Contributing

This is a small demonstration lab. A focused correction or useful counterexample is more valuable than additional scaffolding.

For a defect, include the file or cell, reproduction command, expected result, actual result, and why the difference matters. For a rubric disagreement, identify the disputed criterion and quote the candidate text. A different preference without supporting evidence is difficult to review.

Keep inputs synthetic. Do not submit private prompts, employer or client records, personal data, credentials, or excerpts from restricted evaluations. Label constructed responses as constructed; if proposing a live-model experiment, first discuss its provenance and reproducibility requirements in an issue.

## Before a pull request

1. Make a focused change and explain the observable behavior it changes.
2. Add or update a test when a checking rule changes. Preserve examples for valid zero and missing input.
3. Run `python3 -m unittest discover -s tests -v`.
4. If fixtures or audit behavior changed intentionally, run `python3 scripts/audit_data.py --write`, inspect the report diff, and then run `python3 scripts/audit_data.py --check`.
5. Update nearby documentation if the contract or reported findings changed.

Do not refresh a snapshot merely to silence a failure. Explain why the new result is correct. Keep issues and commits tied to work that actually occurred; no activity targets or synthetic contribution history.
