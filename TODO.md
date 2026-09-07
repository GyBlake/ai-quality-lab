# Open work

These are proposed improvements, not active assignments or completed results.

- [ ] **Native spreadsheet verification.** Import the fixture into Excel and Google Sheets, record application versions, and verify the documented formulas with blank, zero, and appended-row cases. Acceptance: recorded expected/actual cells and any engine differences; preserve the original CSV.
- [ ] **Conflicting duplicate fixture.** Add two rows sharing an ID with different quantities. Acceptance: the audit reports the conflicting identity without silently selecting or deleting a row.
- [ ] **Rubric disagreement example.** Add a synthetic case where two reasoned reviews disagree on a specific anchor. Acceptance: both rationales, adjudication, and any versioned rubric change are visible.
- [ ] **Live prompt experiment protocol.** Define model/version recording, repeated runs, and output capture before generating real responses. Acceptance: separate hand-authored expectations from observed runs; do not present the current fixtures as benchmark results.

Open a focused issue before adding dependencies or expanding into a general workbook or model-evaluation framework.
