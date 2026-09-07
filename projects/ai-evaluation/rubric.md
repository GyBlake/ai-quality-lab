# Evaluation rubric v1.0

Scope: source-grounded answers to the synthetic operational-policy tasks in this folder.

Score each dimension from 0 to 2. Equal weights; total out of 8. Scores are ordinal judgments and should not be interpreted as probabilities.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Grounding | A material claim contradicts the source or lacks support. | Core answer is supported, but a minor qualification or source detail is inaccurate. | Every material claim is supported; source limits are preserved. |
| Instruction compliance | Breaks an explicit task constraint. | Follows the main task with a minor format or coverage miss. | Meets every explicit constraint. |
| Completeness | Misses the main question or gives an unusable answer. | Addresses the main question but omits a requested part or necessary next step. | Covers the requested parts, including an explicit unknown when needed. |
| Clarity | Confusing or internally contradictory. | Understandable, with avoidable ambiguity or excess. | Direct, readable, and unambiguous. |

## Acceptance and preference

Accept only when grounding = 2, instruction compliance = 2, total ≥ 7, and no critical failure is present. An unsupported material policy assertion is critical. A high total cannot override it.

Prefer an acceptable response over an unacceptable one. If both are acceptable, compare totals and decisive evidence; a tie is valid. If neither is acceptable, record **neither** and state the correction or clarification needed. Correctly explaining that the source cannot answer a question can be a complete response.

## Failure tags

| Tag | Meaning | Default severity |
| --- | --- | --- |
| `UNSUPPORTED_CLAIM` | Adds a material fact absent from the supplied source. | Critical |
| `SOURCE_CONTRADICTION` | Gives a materially different answer from the source. | Critical |
| `INSTRUCTION_MISS` | Breaks an explicit task requirement. | Major; critical if it invalidates the answer |
| `AMBIGUITY_IGNORED` | Resolves a material uncertainty without supporting evidence. | Critical |
| `OMISSION` | Leaves out a requested element or necessary next step. | Major |
| `UNCLEAR_WORDING` | Wording prevents a clear interpretation. | Minor or major, depending on impact |

Several tags may describe one defect. Do not add them together as independent error counts. Severity describes impact; the dimension scores describe response quality.

## Review confidence and disagreement

Use high confidence when explicit text settles the judgment; medium when a defined criterion requires interpretation; low when the rubric or evidence is insufficient. Confidence is about the evaluation, not confidence in the candidate’s answer.

For disagreement, preserve both rationales, identify the disputed criterion, and request adjudication. Version the rubric if its wording changes, then revisit affected cases. Do not average away a critical grounding disagreement.
