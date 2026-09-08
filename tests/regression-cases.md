# Universal Agent Judge — behavioral regression cases

These manual scenarios were carried forward from v7 for review of the v8 skill.
They contain expected outcomes, not measured results from a new agent run. Each mode has a
clear SATISFIED case, clear UNSATISFIED case, and an edge/ambiguous case.

## WORKSPACE_MODE

### W-S — reachable implementation + submitted artifact
Requirement: app exports `results/out.csv` at that exact path when run.
Candidate: entrypoint calls exporter; submitted `results/out.csv` exists, readable and
non-empty.
Expected: `EVALUABLE`, `SATISFIED`, HIGH.

### W-U — producer exists, required artifact missing
Requirement: submit `results/report.pdf`.
Candidate: `make_report.py` contains PDF export code, but `results/report.pdf` is absent;
search exact path, filenames, producer references, and workspace finds no PDF.
Expected: `EVALUABLE`, `UNSATISFIED`, `MISSING_ARTIFACT`. Producer code must not rescue it.

### W-A — verdict-changing path ambiguity
Requirement: “save the result in the output folder, e.g. `output/result.csv`”; rubric does
not clarify whether the example is literal. Candidate saves `output/final.csv`.
Expected: lock path as `ILLUSTRATIVE` if grammar clearly marks “e.g.”; SATISFIED if content
is valid. If surrounding task text conflicts and makes exactness genuinely unresolved,
`NOT_EVALUABLE` + `UNDERSPECIFIED_REQUIREMENT`; never silently enforce exact path.

## FUNCTION_MODE

### F-S — first occurrence semantics
Requirement: return the index of the first matching value, or -1 if absent.
Candidate: linear scan returns on first match and -1 after loop.
Expected: `EVALUABLE`, `SATISFIED`, HIGH.

### F-U — wrong duplicate semantics
Requirement: return first matching index.
Candidate: scans all items and returns the last matching index.
Expected: `EVALUABLE`, `UNSATISFIED`; failed clause = first-occurrence semantics.

### F-A — hidden oracle over-specifies exception type
Requirement: for invalid input, “raise an error”. Candidate raises `ValueError`.
After PRE_REFERENCE lock, hidden oracle expects `RuntimeError` and fails.
Expected: locked semantic `SATISFIED`; oracle `FAIL` classified
`UNDERSPECIFIED_ORACLE_DETAIL`; optionally `ORACLE_MISMATCH`; do not rewrite semantic verdict.

## PATCH_MODE

### P-S — behavior fixed through reachable changed path
Issue: parser must accept quoted commas in one named field.
Patch changes the active parser branch; relevant visible test and code semantics confirm it.
Expected: `EVALUABLE`, `SATISFIED`.

### P-U — code changed but unreachable
Issue: fix timeout handling in active request path.
Patch adds correct logic to helper `new_timeout_handler`, but no caller invokes it; active
request path remains unchanged.
Expected: `EVALUABLE`, `UNSATISFIED`; reachability/integration clause fails.

### P-A — issue wording genuinely underspecified
Issue: “improve handling of malformed headers” with no examples or accepted behavior.
Two incompatible interpretations change whether the patch passes, and no allowed task
source resolves them.
Expected: `NOT_EVALUABLE` + `UNDERSPECIFIED_REQUIREMENT`; do not invent hidden malformed cases.

## TRAJECTORY_MODE

### T-S — directly grounded answer
Requirement: report account balance and source document name.
Trajectory opens the account page and source document; final answer exactly reflects both
observations.
Expected: `EVALUABLE`, `SATISFIED` on answer/evidence clauses.

### T-U — unsupported and contradicted claim
Requirement: report whether booking is confirmed.
Observation says “pending”; final answer says “confirmed”.
Expected: `EVALUABLE`, `UNSATISFIED`, `UNSUPPORTED_CLAIM` and decisive contradiction.

### T-A — trace truncation blocks one mandatory clause
Requirement: provide price and cancellation deadline.
Visible trace proves price; trace ends before the purported deadline observation.
Expected: if the missing trace cannot be inspected, `NOT_EVALUABLE` for the combined
requirement + `TRAJECTORY_EVIDENCE_TRUNCATED` / `MISSING_SUBMISSION_EVIDENCE`; do not call
missing visibility candidate failure.

## NOTEBOOK_ML_MODE

### N-S — current held-out metric with valid provenance
Requirement: train requested model on named dataset, evaluate on held-out test, save metric.
Candidate proves dataset identity, split before fit, reachable training/eval, current metric
file submitted and traceable to run/config.
Expected: `EVALUABLE`, `SATISFIED`.

### N-U — explicit held-out evaluation violated by leakage
Requirement: evaluate on an untouched held-out test set.
Candidate fits scaler on full data before split and reports test accuracy.
Expected: `EVALUABLE`, `UNSATISFIED`; explicit held-out clause violated; `DATA_LEAKAGE_RISK`.

### N-A — named dataset only asserted by filename
Requirement explicitly requires Sentiment140.
Candidate loads `sentiment140.csv`; no source/schema/metadata/content evidence establishes
identity.
Expected: `NOT_EVALUABLE` for identity if only weak evidence remains and no wrong
source is established; `WEAK_DATASET_PROVENANCE`. Proven wrong data is UNSATISFIED.
An explicitly required provenance document can separately fail after absence proof.

## ARTIFACT_MODE

### A-S — exact final PDF satisfies content
Requirement: submit `report/final.pdf` with Methods and Results sections.
Candidate PDF exists at exact path, readable, and contains both required sections.
Expected: `EVALUABLE`, `SATISFIED`.

### A-U — source exists but final deliverable absent
Requirement: submit `slides/final.pdf`.
Candidate has `slides.md` and export script; no PDF exists after Absence Proof.
Expected: `EVALUABLE`, `UNSATISFIED`, `MISSING_ARTIFACT`.

### A-A — valid artifact, producer currently writes elsewhere
Requirement only asks to submit `plots/roc.png`.
Candidate includes valid `plots/roc.png`, but producer code now writes `outputs/roc.png`.
Expected: `EVALUABLE`, `SATISFIED` for pure deliverable clause + `PRODUCER_CODE_MISMATCH`;
do not fail an unstated producer-code requirement.

## Cross-cutting blind-boundary regression

### X-BLIND — gold field exists in payload but is not opened before lock
Task bundle stores candidate and `gold_label` as separate addressable fields. Protocol lets
the judge inspect fields selectively. Judge can identify that a gold field exists without
reading its value.
Expected: denylist `gold_label`; perform candidate judgment and immutable PRE_REFERENCE lock
first; only then open value. `reference_accessed_before_lock=false` and no leakage. If the
gold value itself was already displayed in prompt/context, expected instead:
`REFERENCE_LEAKAGE=true` and run excluded from strict-blind metrics.
