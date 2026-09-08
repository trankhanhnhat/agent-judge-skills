# Diagnostic flags

Use these standardized diagnostic labels to explain evidence quality,
conflict, or protocol state; **a flag is not automatically a verdict**.

| Flag | Typical mode | Required condition |
|---|---|---|
| `MISSING_WORKSPACE` | WORKSPACE, NOTEBOOK_ML | Required filesystem candidate object is absent/inaccessible. |
| `MISSING_CANDIDATE_CODE` | FUNCTION | Candidate function/class code is absent. |
| `MISSING_PATCH` | PATCH | Candidate diff/patch is absent. |
| `MISSING_TRAJECTORY` | TRAJECTORY | Required trajectory record is absent. |
| `MISSING_ARTIFACT` | ARTIFACT, WORKSPACE, NOTEBOOK_ML | Explicit required submitted deliverable is absent after core Absence Proof. |
| `MISSING_SUBMISSION_EVIDENCE` | all | Candidate exists but judge-visible evidence for a clause cannot be inspected enough for a fair decision. |
| `SNAPSHOT_MISMATCH` | snapshot modes | Observed snapshot/hash does not match declared identity. |
| `REFERENCE_LEAKAGE` | blind evaluation | Reference/gold value was exposed before PRE_REFERENCE lock. |
| `PATH_MISMATCH` | artifact/workspace | Locked path semantics are violated. |
| `WEAK_DATASET_PROVENANCE` | workspace/notebook | Named dataset identity rests mainly on filename/name/claim. |
| `SYNTHETIC_STANDIN` | workspace/notebook | Required named dataset is replaced by an unallowed synthetic stand-in. |
| `DATA_LEAKAGE_RISK` | notebook | Evidence suggests forbidden train/val/test contamination. |
| `STALE_NOTEBOOK_OUTPUT` | notebook | Output cannot be mapped to current code/data/config. |
| `METRIC_PROVENANCE_WEAK` | notebook | Metric origin cannot be traced to a concrete run/config/data. |
| `CHECKPOINT_PROVENANCE_WEAK` | notebook | Checkpoint exists but training provenance is unclear. |
| `PRODUCER_CODE_MISMATCH` | artifact/composite | Valid artifact exists but current producer path/logic differs. |
| `POSSIBLE_STALE_ARTIFACT` | artifact/workspace | Artifact may not correspond to current source/run. |
| `TRAJECTORY_EVIDENCE_TRUNCATED` | trajectory | Submitted/visible trace is cut off. |
| `UNSUPPORTED_CLAIM` | trajectory/claim evidence | A claim lacks direct supporting observation. |
| `RUNTIME_PARTIAL_SUCCESS` | runtime | Execution completes only part of the relevant workflow. |
| `RUNTIME_INTERVENTION` | runtime | Judge changed environment to make diagnosis/execution possible. |
| `ENVIRONMENT_BLOCKED` | runtime | Credentials/network/environment prevents relevant execution. |
| `NONDETERMINISTIC_RUNTIME` | runtime | Repeated executions materially disagree. |
| `UNDERSPECIFIED_REQUIREMENT` | all | Allowed task sources leave verdict-changing ambiguity unresolved. |
| `UNDERSPECIFIED_ORACLE_DETAIL` | function/patch/O1 | Oracle demands a detail absent from the locked contract. |
| `ORACLE_MISMATCH` | function/patch/O1 | Oracle result conflicts with locked semantic judgment for an unstated detail. |
| `JUDGE_ACCESS_LIMITATION` | all | Tool/permission limitation prevents direct inspection. |
