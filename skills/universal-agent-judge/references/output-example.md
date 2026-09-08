# Output example — WORKSPACE_MODE

This is a formatting example only; authoritative rules live in [the shared workflow](../SKILL.md) and adapters.

Task: “Export monthly revenue CSV at `results/monthly_report.csv` and save at least two
plots under `results/plots/`.”

Locked clauses:
- R1: CSV exists at `EXACT results/monthly_report.csv` and contains monthly data.
- R2: at least two valid plot artifacts exist under `DIRECTORY results/plots/`.

## Audit header
- `task_id`: revenue-app-001
- `submission_id`: sub-042
- `mode`: WORKSPACE_MODE
- `submission_identity`: `/workspace/sub-042`
- `snapshot_id`: `a1b2c3d`
- `judgment_phase`: PRE_REFERENCE
- `reference_accessed_before_lock`: false

## Requirement table
| ID | Evaluability | Decision | Decisive Evidence | Clauses | Confidence | Flags |
|---|---|---|---|---|---|---|
| R1 | EVALUABLE | SATISFIED | submitted CSV exists at exact path, non-empty, monthly rows present | all pass | HIGH | — |
| R2 | EVALUABLE | UNSATISFIED | only one submitted plot found after path + filename + producer/call-site search | count fails (1 < 2) | HIGH | — |

The presence of unreachable code for a second plot is not substituted for the missing
submitted artifact; the negative conclusion is made only after Absence Proof.

## Optional tables

Include these only for checks actually performed; identify unrun checks explicitly
if their absence limits the judgment.

| Run | Scope | Invocation | Status | Intervention | Key evidence | Provenance |
|---|---|---|---|---|---|---|

| ID | Locked semantic verdict | Oracle | Failure class | Post-reference amendment / note |
|---|---|---|---|---|

| ID | Independent | Dependency-aware | Note |
|---|---|---|---|

| ID | Locked judge | Reference | Match | Audit |
|---|---|---|---|---|

For an inaccessible mandatory artifact, report `NOT_EVALUABLE` with an empty
decision and the inspection limitation. Keep it outside binary agreement counts.
