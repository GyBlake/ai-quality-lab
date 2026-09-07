# Repository guide

The root README is the entry point for someone inspecting or cloning the lab. Each example keeps its source, method, decision, and limitations close together.

## Public file structure

```text
ai-quality-lab/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── bug_report.md
│   └── pull_request_template.md
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── TODO.md
├── docs/
│   ├── provenance.md
│   ├── publishing.md
│   ├── repository-guide.md
│   └── validation.md
├── projects/
│   ├── ai-evaluation/
│   │   ├── README.md
│   │   ├── evaluation-template.md
│   │   ├── rubric.md
│   │   └── cases/
│   │       ├── 01-policy-answer.md
│   │       └── 02-conflicting-versions.md
│   ├── data-quality/
│   │   ├── README.md
│   │   ├── audit-findings.md
│   │   ├── data-dictionary.md
│   │   ├── spreadsheet-checks.md
│   │   ├── data/
│   │   │   ├── formula-snapshot.json
│   │   │   └── requests.csv
│   │   └── sample-output/
│   │       └── audit-report.json
│   └── prompt-testing/
│       ├── README.md
│       └── cases.json
├── scripts/
│   └── audit_data.py
└── tests/
    ├── test_audit_data.py
    └── test_prompt_contract.py
```

The ignored `.delivery/` folder, when present locally, contains publishing handoff material and a separate profile draft. It is excluded from the public project.

## Conventions

Use lowercase hyphenated names for Markdown and data files; Python modules use snake_case. Keep stable IDs such as `EVAL-001` and `PROMPT-001` in records, independent of display titles. Worksheet coordinates refer to the fixed layout documented in the data dictionary.

Raw fixtures live under `data/`. Generated output lives under `sample-output/` and should be changed through its script, then reviewed. Markdown decisions live beside their evidence.

The evaluation rubric is v1.0; the prompt document explicitly retains v1 and v2 to explain the rule change. If a rule changes, identify the version and revisit affected examples. Do not overwrite old candidate text to make a revised rule appear more successful.

## Review paths

For AI evaluation, read a completed case and then challenge its rubric anchors. For data quality, read the findings, inspect the CSV and formula snapshot, and run the checker. For prompt work, inspect the classification rules and test cases before extending the contract.

The technical scope stays intentionally small: no package install, model SDK, external service, or application deployment is needed. See [validation](validation.md) for the checks actually performed and [TODO](../TODO.md) for unverified extensions.
