# Case EVAL-001: A fluent answer invents a deadline

**Final judgment: accept B; reject A.** A gives a specific turnaround time that the supplied policy never states.

Provenance: constructed synthetic source, prompt, and candidate responses. Rubric: [v1.0](../rubric.md). No real model was tested.

## Prompt

```text
Use only this policy:
“A request with a missing delivery address must be placed in Needs Review.
The reviewer must ask the requester for the address before dispatch.
The policy does not specify a turnaround time.”

A request has no delivery address. What should happen next, and how long
will it take? Answer in no more than three sentences. If a timing detail
is not stated, say so; do not invent it.
```

## Expected behavior

State Needs Review, request the address before dispatch, and explicitly say the turnaround time is unspecified. Do not infer a deadline from operational convention.

## Model response A — synthetic candidate

> Place the request in Needs Review and ask the requester for the delivery address before dispatch. The review will be completed within 24 hours.

## Model response B — synthetic candidate

> Place the request in Needs Review and ask the requester for the missing delivery address before dispatch. The policy does not specify a turnaround time.

## Scoring

| Dimension | A | B | Evidence and rationale |
| --- | ---: | ---: | --- |
| Grounding | 0 | 2 | A’s “within 24 hours” is unsupported; B preserves the source’s timing limit. |
| Instruction compliance | 0 | 2 | A breaks “do not invent it.” Both meet the sentence limit. |
| Completeness | 2 | 2 | Both address the next action and timing question. Accuracy is scored under grounding. |
| Clarity | 2 | 2 | Both are direct and readable. Fluency does not establish correctness. |
| **Total** | **4/8** | **8/8** | A fails the acceptance gates. B meets all gates. |

## Failure tags and judgment

- **A:** `UNSUPPORTED_CLAIM`, `INSTRUCTION_MISS`; one critical deadline defect with two tags. Reject.
- **B:** no observed failure in this case. Accept.
- **Preference:** B.
- **Review confidence:** high. The source and task explicitly exclude an invented turnaround time.

The issue with A is consequential: a recipient could plan around a commitment the policy never made. Removing the 24-hour claim and stating that timing is unspecified would address the defect. This case supports a judgment about these two texts only.
