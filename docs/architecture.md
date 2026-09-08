# Architecture: Universal Agent Judge v9

The skill is a judging protocol, with optional deterministic record tooling. It does
not generate/fix candidates. The developer evaluator handles only the finite authored
fixture language; it is not a universal automatic grading engine.

## Before and after

| v8 | v9 |
|---|---|
| Prose workflow and denylist | Explicit role classification and access state machine |
| Binary per requirement | Binary + evaluability + weighted content + separate penalties/preferences |
| Five ML obligations | Eight obligations and fresh-kernel protocol |
| Weak data identity lacks outcome boundary | Direct/corroborating/claim classes and explicit SAT/UNSAT/NE boundary |
| Markdown example only | Canonical schema, arithmetic validation, lossless Markdown views |
| 22 package checks, manual scenarios | Package checks retained; invariant tests, 11 real notebook fixtures, dev reports |

The historical [pre-upgrade inventory](pre-upgrade-audit.md) covers every original
file, caller, authority, overlap, risk and test coverage at b918d79.

## State and provenance

```mermaid
flowchart LR
  A[INPUT_CLASSIFICATION] --> B[REQUIREMENT_LOCK]
  B --> C[PRE_REFERENCE_EVIDENCE]
  C --> D[PRE_REFERENCE_DECISION]
  D --> E[IMMUTABLE_LOCK]
  E --> F[OPTIONAL_REFERENCE_ACCESS]
  F --> G[POST_REFERENCE_AUDIT]
```

The initial record is write-once and SHA-256 identified. Amendments reference it and
cannot rewrite clauses, weights, evidence or independent decisions. File-origin labels
distinguish SUBMITTED, JUDGE_RUNTIME, MODIFIED_BY_RUNTIME and EXTERNAL_ENVIRONMENT.
A runtime copy is provenance protection, not security containment.

## Authority and routing map

Paths below are relative to `skills/universal-agent-judge/`. The entry links every
reference directly; mode guides contain only conditional specialist pointers.
Shared-policy backlinks are documentation, not recursive load instructions.

| File | Authority | Load condition / caller |
|---|---|---|
| SKILL.md | State order, requirement lock, semantic model | Every judgment |
| references/input-roles.md | Input roles and reference access | Entry gate |
| references/rubric-scoring.md | Allocation, points, rounding, caps, penalties, preference | Entry when rubric scores; notebook when scored |
| references/mode-workspace.md | Workspace evidence | Entry for filesystem snapshot |
| references/mode-function.md | API/function checks | Entry for function/class |
| references/mode-patch.md | Changed active behavior | Entry for diff/issue |
| references/mode-trajectory.md | Observation/answer support | Entry for trace |
| references/mode-notebook-ml.md | Eight ML obligations | Entry for experiment |
| references/mode-artifact.md | Actual submitted deliverable | Entry or workspace/notebook for saved artifact |
| references/notebook-execution.md | Fresh kernel and output comparison | Notebook or runtime guide when freshness/execution matters |
| references/safe-candidate-execution.md | Execution gate | Before imports/tests/cells/commands |
| references/runtime-verification.md | E0–E3/O1 levels, failure classification | Execution or oracle requested |
| references/provenance.md | File origins and deltas | Runtime may write |
| references/dataset-provenance.md | Identity-to-use chain and outcomes | Named dataset in contract |
| references/flags-full.md | Flag definitions, exclusions, effects | A diagnostic condition occurs |
| references/benchmark-adapters.md | Packaging only | Unfamiliar benchmark input/output |
| references/output-contract.md | Record/render mapping | Every final output |
| references/output-example.md | Illustrations only | First/weighted report |
| references/post-reference-metrics.md | Agreement definitions | Multiple locked/reference samples |
| references/disagreement-audit.md | Mismatch categories | Post-lock disagreement |
| schemas/judgment.schema.json | Machine shape/enums/nullability | Output contract/validator |
| scripts/judgment.py | Invariant enforcement, rendering, access helper | Optional deterministic record handling |

Additional repository files:

| Area | Purpose |
|---|---|
| tests/test_package.py | Existing metadata/link/discovery checks |
| tests/test_judgment.py | Schema, scoring, nulls, evidence, lock and role invariants |
| tests/test_dev_evaluation.py | Executes all 11 reviewed notebook fixtures |
| tests/support/records.py | Record construction; no verdict inference |
| tests/support/build_fixtures.py | One-time explicit fixture/gold authoring, never grading |
| tests/support/notebook_worker.py | Fresh-kernel execution of reviewed fixture copy |
| tests/support/runtime.py | Hash allowlist, environment, timeout and original preservation |
| tests/support/dev_eval.py | Finite-fixture observations, freeze, then gold comparison |
| tests/fixtures/ | Task, rubric, candidate, withheld expected JSON/flags and case README |
| docs/evaluations/ | Saved dev records and execution evidence |
| requirements-dev.txt | Test/notebook dependencies, not candidate-requested installation |
| README.md, tests/README.md | User install/use and maintainer validation instructions |
| docs/design-notes.md | Historical v8 design, not current quality claims |

## Verdict and scoring model

A requirement passes only when every mandatory clause passes; a decisive failed
clause makes it UNSATISFIED. With no decisive failure and an ungradable mandatory
clause, decision is null/NOT_EVALUABLE. Required items determine whole-task status.
Optional scored clauses can affect points without inventing mandatory semantics.

Without weights, scores are null. With weights, decimal clause sums must equal each
parent maximum. Unknown points remain null, with known subtotal/unresolved maximum.
Partial points never turn failed semantics into satisfaction. Content, administrative
penalties and preference ratings are separate. The final score applies declared caps,
penalties and end-of-calculation rounding. Flags/confidence are not score factors.

## Extension points and limits

Add a mode-specific check by extending its guide; do not copy shared rules. A new
reference needs an explicit conditional route and must retain single authority.
Schema changes need compatibility/version consideration plus fixtures and rejection
tests. Prefer adding new external evaluation cases with independently withheld labels
over teaching the developer fixture checker to recognize arbitrary application code.

The local development harness lacks OS-level network/memory/disk containment and
refuses unknown candidate bytes. Production judging must use an adequate external
sandbox or remain static/ungradable. The record helper does not mediate tools outside
its InputSession or prove truthfulness of supplied evidence. No independent LLM
accuracy claim follows from these developer tests.
