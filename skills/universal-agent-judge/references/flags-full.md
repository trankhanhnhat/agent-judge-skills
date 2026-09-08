# Diagnostic flags

This registry owns definitions and exclusions. Every flag is diagnostic: **no flag
automatically changes a semantic verdict or subtracts points**. Cite independent
clause evidence for any failure and explicit rubric policy for any score effect.
Reference leakage excludes a run from strict-blind metrics; weight mismatch blocks
affected numeric scoring until resolved. Neither makes candidate semantics fail.

| Flag | Modes | Trigger / definition | Do not trigger when | Verdict / score effect |
|---|---|---|---|---|
| `MISSING_WORKSPACE` | WORKSPACE, NOTEBOOK_ML | Required filesystem candidate object is absent/inaccessible. | An accessible workspace merely lacks one required file. | None automatically; apply clause evidence and rubric policy. |
| `MISSING_CANDIDATE_CODE` | FUNCTION | Candidate function/class code is absent. | Code exists but is wrong. | None automatically; apply clause evidence and rubric policy. |
| `MISSING_PATCH` | PATCH | Candidate diff/patch is absent. | Patch exists but is ineffective. | None automatically; apply clause evidence and rubric policy. |
| `MISSING_TRAJECTORY` | TRAJECTORY | Required trajectory record is absent. | Trace exists but one observation is unclear. | None automatically; apply clause evidence and rubric policy. |
| `MISSING_ARTIFACT` | ARTIFACT, WORKSPACE, NOTEBOOK_ML | Explicit required submitted deliverable is absent after core Absence Proof. | Judge access is blocked, or output was not required. | None automatically; apply clause evidence and rubric policy. |
| `MISSING_SUBMISSION_EVIDENCE` | all | Candidate exists but judge-visible evidence for a clause cannot be inspected enough for a fair decision. | Evidence proves a concrete violation. | None automatically; apply clause evidence and rubric policy. |
| `SNAPSHOT_MISMATCH` | snapshot modes | Observed snapshot/hash does not match declared identity. | No trusted identity was supplied for comparison. | None automatically; apply clause evidence and rubric policy. |
| `REFERENCE_LEAKAGE` | blind evaluation | Reference/gold value was exposed before PRE_REFERENCE lock. | Only a reference filename was seen, not its value. | Exclude strict-blind agreement; no content penalty. |
| `PATH_MISMATCH` | artifact/workspace | Locked path semantics are violated. | Path was illustrative or any descendant was permitted. | None automatically; apply clause evidence and rubric policy. |
| `WEAK_DATASET_PROVENANCE` | workspace/notebook | Named dataset identity rests mainly on filename/name/claim. | Trusted identity is established and linked to use. | None automatically; apply clause evidence and rubric policy. |
| `SYNTHETIC_STANDIN` | workspace/notebook | Required named dataset is replaced by an unallowed synthetic stand-in. | Synthetic data is explicitly permitted. | None automatically; apply clause evidence and rubric policy. |
| `DATA_LEAKAGE_RISK` | notebook | Evidence suggests forbidden train/val/test contamination. | No forbidden overlap/protocol violation is evidenced. | None automatically; apply clause evidence and rubric policy. |
| `STALE_NOTEBOOK_OUTPUT` | notebook | Output cannot be mapped to current code/data/config. | Only execution counts are unusual. | None automatically; apply clause evidence and rubric policy. |
| `METRIC_PROVENANCE_WEAK` | notebook | Metric origin cannot be traced to a concrete run/config/data. | Metric is traced to the current run/data/config. | None automatically; apply clause evidence and rubric policy. |
| `CHECKPOINT_PROVENANCE_WEAK` | notebook | Checkpoint exists but training provenance is unclear. | A traceable checkpoint merely has an unusual filename. | None automatically; apply clause evidence and rubric policy. |
| `PRODUCER_CODE_MISMATCH` | artifact/composite | Valid artifact exists but current producer path/logic differs. | No relevant submitted artifact/producer discrepancy exists. | None automatically; apply clause evidence and rubric policy. |
| `POSSIBLE_STALE_ARTIFACT` | artifact/workspace | Artifact may not correspond to current source/run. | Only file modification time differs. | None automatically; apply clause evidence and rubric policy. |
| `TRAJECTORY_EVIDENCE_TRUNCATED` | trajectory | Submitted/visible trace is cut off. | The complete trace omits a required action. | None automatically; apply clause evidence and rubric policy. |
| `UNSUPPORTED_CLAIM` | trajectory/claim evidence | A claim lacks direct supporting observation. | Visible direct evidence supports the claim. | None automatically; apply clause evidence and rubric policy. |
| `RUNTIME_PARTIAL_SUCCESS` | runtime | Execution completes only part of the relevant workflow. | All relevant required stages completed. | None automatically; apply clause evidence and rubric policy. |
| `RUNTIME_INTERVENTION` | runtime | Judge changed environment to make diagnosis/execution possible. | Only a byte-identical runtime copy was made. | None automatically; apply clause evidence and rubric policy. |
| `ENVIRONMENT_BLOCKED` | runtime | Credentials/network/environment prevents relevant execution. | A candidate logic error caused failure. | None automatically; apply clause evidence and rubric policy. |
| `NONDETERMINISTIC_RUNTIME` | runtime | Repeated executions materially disagree. | Only irrelevant timestamps/counts differ. | None automatically; apply clause evidence and rubric policy. |
| `UNDERSPECIFIED_REQUIREMENT` | all | Allowed task sources leave verdict-changing ambiguity unresolved. | All defensible readings yield the same decision. | None automatically; apply clause evidence and rubric policy. |
| `UNDERSPECIFIED_ORACLE_DETAIL` | function/patch/O1 | Oracle demands a detail absent from the locked contract. | The expected detail is explicit in the locked task. | None automatically; apply clause evidence and rubric policy. |
| `ORACLE_MISMATCH` | function/patch/O1 | Oracle result conflicts with locked semantic judgment for an unstated detail. | Oracle and locked semantic result agree. | None automatically; apply clause evidence and rubric policy. |
| `JUDGE_ACCESS_LIMITATION` | all | Tool/permission limitation prevents direct inspection. | Accessible evidence establishes candidate failure. | None automatically; apply clause evidence and rubric policy. |
| `JUDGE_DERIVED_ALLOCATION` | all weighted | Judge allocates supplied parent points using a disclosed authorized rule. | Rubric supplies all clause weights. | Disclose allocation; no bonus or penalty. |
| `NOTEBOOK_NOT_RUN_ALL` | notebook | Incomplete/failed submitted Run All or missing explicitly required saved execution evidence is established. | Execution counts alone are null/nonmonotone. | None automatically; apply clause evidence and rubric policy. |
| `HIDDEN_STATE_DEPENDENCY` | notebook | Fresh kernel fails on state absent from document order with required inputs available. | Missing external dependencies explain failure. | None automatically; apply clause evidence and rubric policy. |
| `SUBMITTED_RUNTIME_DIVERGENCE` | runtime/notebook | Attributable submitted and clean-run semantic outputs differ. | Only irrelevant metadata differs. | None automatically; apply clause evidence and rubric policy. |
| `MODEL_CONFIG_MISMATCH` | notebook | Actual estimator/config contradicts an explicit model clause. | Model choice was not specified. | None automatically; apply clause evidence and rubric policy. |
| `RUBRIC_WEIGHT_MISMATCH` | weighted | Supplied atomic weights do not sum to their parent or scoring inputs conflict. | A valid disclosed allocation sums exactly. | Affected score unresolved; preserve semantic findings. |
| `REFERENCE_ROLE_AMBIGUOUS` | all | Input may be reference and unresolved role can affect judgment. | Authoritative manifest resolves the role. | None automatically; apply clause evidence and rubric policy. |
| `UNSAFE_EXECUTION_BLOCKED` | runtime | Available isolation cannot safely execute this candidate. | Execution is safe but candidate logic fails. | None automatically; apply clause evidence and rubric policy. |
