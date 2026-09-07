# AI response evaluation

**Question:** Which response meets the task, and when should neither be accepted?

The first case separates fluency from factual support. The second shows why a preference ranking cannot replace an acceptability decision.

| Case | Outcome | Key evidence |
| --- | --- | --- |
| [Policy answer](cases/01-policy-answer.md) | Accept B; reject A | A invents a deadline despite a source-only instruction. |
| [Conflicting versions](cases/02-conflicting-versions.md) | Accept neither; request clarification | Both candidates choose a policy without evidence of which version applies. |

Use the [rubric](rubric.md) to inspect the scores. The [blank evaluation template](evaluation-template.md) shows the record format for another case.

## Method

Read the task and synthetic source before reading the candidate responses. Establish the expected answer, score each dimension separately, quote the decisive evidence, and apply the acceptance rule. Record a preference only after deciding whether either response is acceptable.

All prompts, source passages, and A/B responses were constructed for this portfolio with AI assistance. A and B do not identify real models. Scores are illustrative applications of a local rubric, not measured model performance, hiring-test results, or evidence of reviewer agreement. A live evaluation would also record model versions, generation settings, timestamps, prompt versions, and independent reviewer disagreements.
