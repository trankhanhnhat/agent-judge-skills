# Input roles and access

This file owns input classification and reference access. Classify from task/user
manifest or metadata, never by opening a suspected answer to discover its role.

| Role | Purpose | Access |
|---|---|---|
| TASK_SOURCE | Explicit task | Before requirement lock |
| RUBRIC | Criteria, weights, thresholds, policy | Before requirement lock |
| CANDIDATE | Submitted code, tests, output, trace | After requirement lock |
| REFERENCE_SOLUTION | Model answer / alternative implementation | After immutable lock |
| GOLD_LABEL | Human/prior judgment, official per-instance result | After immutable lock |
| ORACLE_TEST | Official hidden tests/expected values | O1 after immutable lock |
| CONTEXT_ONLY | Non-authoritative background | Only if no reference values exposed |

Record address, role, classification source, actual access phase. Unknown roles
stay unopened (`role: null`). If guessing could affect judgment, ask or use
`NOT_EVALUABLE` / `REFERENCE_ROLE_AMBIGUOUS`. Candidate tests cannot add clauses.
Public examples are TASK_SOURCE only if the task protocol makes them specification.

For mixed bundles, read fields selectively or use a trusted partitioner withholding
reference values. If tools cannot partition, defer the whole bundle. Already exposed
values require `reference_accessed_before_lock: true` and `REFERENCE_LEAKAGE`; a
denylist cannot undo exposure. Judge contamination is not candidate semantic failure.

Without a requirement input, return empty requirements, `NOT_EVALUABLE`, and the
missing-input limitation. Do not infer a rubric from code. A reference solution may
inform post-reference audit only against locked clauses; implementation differences
alone cannot fail a candidate. Keep amendments separate from the original record.

The record helper's `InputSession` enforces ordered access for callers using it.
It cannot erase model-context exposure or mediate tools outside the helper.
