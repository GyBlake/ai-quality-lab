# Case EVAL-002: Neither answer has enough evidence

**Final judgment: accept neither; request the applicable policy version.** There is no evidence that either passage is current.

Provenance: constructed synthetic source, prompt, and candidate responses. Rubric: [v1.0](../rubric.md). No real model was tested.

## Prompt

```text
Two undated policy extracts were supplied:
Extract X: “Requests received after 16:00 are processed the next business day.”
Extract Y: “Requests received after 17:00 are processed the next business day.”
Neither extract identifies its effective date, version, or applicable team.

A request arrived at 16:30. Based only on these extracts, does the policy
require next-business-day processing? Explain in no more than three sentences.
If the evidence conflicts, identify the missing information instead of choosing.
```

## Model response A — synthetic candidate

> Yes. The 16:00 cutoff applies, so the request must be processed the next business day.

## Model response B — synthetic candidate

> No. The 17:00 cutoff applies, so the policy does not require next-business-day processing.

## Scoring

| Dimension | A | B | Evidence and rationale |
| --- | ---: | ---: | --- |
| Grounding | 0 | 0 | Each asserts that one cutoff applies without version or team evidence. |
| Instruction compliance | 0 | 0 | Both choose despite the explicit instruction to identify missing information. |
| Completeness | 1 | 1 | Both answer the surface question but omit the conflict and clarification needed. |
| Clarity | 2 | 2 | Both are readable; neither is justified. |
| **Total** | **3/8** | **3/8** | Neither meets the grounding or instruction gates. |

## Failure tags and rationale

Both: `AMBIGUITY_IGNORED`, `UNSUPPORTED_CLAIM`, `INSTRUCTION_MISS`, `OMISSION`. The decisive critical defect is unsupported selection of the applicable policy. These tags overlap and are not four independent incidents.

A follows X and B follows Y, so picking the more fluent answer would hide the actual defect: the evidence cannot establish which policy controls. Request the current approved version and applicable team from the policy owner, then reassess.

**Preference:** neither. **Review confidence:** high that neither is acceptable; applicability remains unresolved.

## Acceptable reference answer — constructed

> The extracts conflict, so they do not establish whether next-business-day processing is required for the 16:30 request. Confirm the applicable team and current approved policy version before deciding.
