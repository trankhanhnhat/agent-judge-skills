# Judgment: notebook_good

Status: SOLVED

| ID | Evaluability | Decision | Content points | Evidence |
|---|---|---|---|---|
| implementation | EVALUABLE | SATISFIED | 1.0/1 | candidate/notebook.ipynb: Observed evidence supports: Implement a reachable fit and predict workflow. |
| submitted_run | EVALUABLE | SATISFIED | 1.0/1 | candidate/notebook.ipynb: Observed evidence supports: Submit completed output for every nonempty code cell as Run All evidence. |
| clean_run | EVALUABLE | SATISFIED | 1.0/1 | runtime-copy/executed.ipynb: Observed evidence supports: Notebook must run from a fresh kernel in document order. |
| saved_outputs | EVALUABLE | SATISFIED | 1.0/1 | candidate/notebook.ipynb: Observed evidence supports: Save all nonempty code-cell outputs in the submitted notebook. |
| fresh_outputs | EVALUABLE | SATISFIED | 1.0/1 | candidate/notebook.ipynb: Observed evidence supports: Saved semantic outputs must match current code and supplied data. |
| metric | EVALUABLE | SATISFIED | 1.0/1 | candidate/notebook.ipynb#cell-4: Observed evidence supports: Submit the RMSE produced by the evaluation cell. |
| protocol | EVALUABLE | SATISFIED | 1.0/1 | candidate/notebook.ipynb#cell-1,cell-3: Observed evidence supports: Fit preprocessing only on first four training rows; evaluate untouched last two rows. |
| artifact | EVALUABLE | SATISFIED | 1.0/1 | candidate/residual.svg: Observed evidence supports: Submit residual.svg containing the residual scatter plot. |
| dataset | EVALUABLE | SATISFIED | 1.0/1 | rubric.json#dataset.sha256; candidate/tiny.csv; candidate/notebook.ipynb#cell-1: Observed evidence supports: Train/evaluate using the supplied JudgeTiny v1 CSV bytes identified by trusted SHA-256. |
| model | EVALUABLE | SATISFIED | 1.0/1 | candidate/notebook.ipynb#cell-3: Observed evidence supports: Use sklearn Ridge(alpha=1.0) in the model Pipeline. |

Content: 10.0/10.0; known: 10.0; unresolved maximum: 0.0; final: 10.0.

Penalties: []

Limitations: Finite authored-fixture evaluator; not independent LLM evaluation or arbitrary-code sandbox.

## implementation
- implementation.1: Implement a reachable fit and predict workflow. — SATISFIED; Observed evidence supports: Implement a reachable fit and predict workflow.

Flags: none

## submitted_run
- submitted_run.1: Submit completed output for every nonempty code cell as Run All evidence. — SATISFIED; Observed evidence supports: Submit completed output for every nonempty code cell as Run All evidence.

Flags: none

## clean_run
- clean_run.1: Notebook must run from a fresh kernel in document order. — SATISFIED; Observed evidence supports: Notebook must run from a fresh kernel in document order.

Flags: none

## saved_outputs
- saved_outputs.1: Save all nonempty code-cell outputs in the submitted notebook. — SATISFIED; Observed evidence supports: Save all nonempty code-cell outputs in the submitted notebook.

Flags: none

## fresh_outputs
- fresh_outputs.1: Saved semantic outputs must match current code and supplied data. — SATISFIED; Observed evidence supports: Saved semantic outputs must match current code and supplied data.

Flags: none

## metric
- metric.1: Submit the RMSE produced by the evaluation cell. — SATISFIED; Observed evidence supports: Submit the RMSE produced by the evaluation cell.

Flags: none

## protocol
- protocol.1: Fit preprocessing only on first four training rows; evaluate untouched last two rows. — SATISFIED; Observed evidence supports: Fit preprocessing only on first four training rows; evaluate untouched last two rows.

Flags: none

## artifact
- artifact.1: Submit residual.svg containing the residual scatter plot. — SATISFIED; Observed evidence supports: Submit residual.svg containing the residual scatter plot.

Flags: none

## dataset
- dataset.1: Train/evaluate using the supplied JudgeTiny v1 CSV bytes identified by trusted SHA-256. — SATISFIED; Observed evidence supports: Train/evaluate using the supplied JudgeTiny v1 CSV bytes identified by trusted SHA-256.

Flags: none

## model
- model.1: Use sklearn Ridge(alpha=1.0) in the model Pipeline. — SATISFIED; Observed evidence supports: Use sklearn Ridge(alpha=1.0) in the model Pipeline.

Flags: none

Runtime: clean-1 PASS

<details>
<summary>Canonical judgment JSON</summary>

```json
{
  "access_log": [
    {
      "action": "READ",
      "path": "task.md",
      "role": "TASK_SOURCE",
      "state": "INPUT_CLASSIFICATION"
    },
    {
      "action": "READ",
      "path": "rubric.json",
      "role": "RUBRIC",
      "state": "INPUT_CLASSIFICATION"
    },
    {
      "action": "READ",
      "path": "candidate/notebook.ipynb",
      "role": "CANDIDATE",
      "state": "PRE_REFERENCE_EVIDENCE"
    },
    {
      "action": "READ",
      "path": "candidate/tiny.csv",
      "role": "CANDIDATE",
      "state": "PRE_REFERENCE_EVIDENCE"
    },
    {
      "action": "READ",
      "path": "candidate/residual.svg",
      "role": "CANDIDATE",
      "state": "PRE_REFERENCE_EVIDENCE"
    }
  ],
  "flags": [],
  "inputs": [
    {
      "access_phase": "PRE_REFERENCE",
      "classification_source": "inputs.json task manifest",
      "path": "task.md",
      "role": "TASK_SOURCE"
    },
    {
      "access_phase": "PRE_REFERENCE",
      "classification_source": "inputs.json task manifest",
      "path": "rubric.json",
      "role": "RUBRIC"
    },
    {
      "access_phase": "UNOPENED",
      "classification_source": "inputs.json task manifest",
      "path": "expected.judgment.json",
      "role": "GOLD_LABEL"
    },
    {
      "access_phase": "UNOPENED",
      "classification_source": "inputs.json task manifest",
      "path": "expected-flags.json",
      "role": "GOLD_LABEL"
    },
    {
      "access_phase": "UNOPENED",
      "classification_source": "inputs.json task manifest",
      "path": "README.md",
      "role": "CONTEXT_ONLY"
    },
    {
      "access_phase": "PRE_REFERENCE",
      "classification_source": "inputs.json task manifest",
      "path": "candidate/notebook.ipynb",
      "role": "CANDIDATE"
    },
    {
      "access_phase": "PRE_REFERENCE",
      "classification_source": "inputs.json task manifest",
      "path": "candidate/residual.svg",
      "role": "CANDIDATE"
    },
    {
      "access_phase": "PRE_REFERENCE",
      "classification_source": "inputs.json task manifest",
      "path": "candidate/tiny.csv",
      "role": "CANDIDATE"
    }
  ],
  "inspection_limitations": [
    "Finite authored-fixture evaluator; not independent LLM evaluation or arbitrary-code sandbox."
  ],
  "loaded_references": [
    "references/input-roles.md",
    "references/mode-notebook-ml.md",
    "references/rubric-scoring.md",
    "references/safe-candidate-execution.md",
    "references/runtime-verification.md",
    "references/provenance.md",
    "references/notebook-execution.md",
    "references/dataset-provenance.md",
    "references/mode-artifact.md",
    "references/flags-full.md",
    "references/output-contract.md"
  ],
  "lock": null,
  "mode": "NOTEBOOK_ML_MODE",
  "overall_status": "SOLVED",
  "penalties": [],
  "phase": "PRE_REFERENCE",
  "post_reference_audit": [],
  "preference_scores": [],
  "reference_accessed_before_lock": false,
  "requirements": [
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "implementation.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "implementation.1-evidence"
          ],
          "evidence_obligation": "IMPLEMENTATION",
          "exact_text": "Implement a reachable fit and predict workflow.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Implement a reachable fit and predict workflow.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": null,
          "description": "Observed evidence supports: Implement a reachable fit and predict workflow.",
          "evidence_class": "DIRECT",
          "evidence_id": "implementation.1-evidence",
          "location": "candidate/notebook.ipynb",
          "provenance": "SUBMITTED"
        }
      ],
      "exact_text": "Implement a reachable fit and predict workflow.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "implementation",
      "prerequisites": [],
      "requirement_id": "implementation",
      "semantic_decision": "SATISFIED"
    },
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "submitted_run.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "submitted_run.1-evidence"
          ],
          "evidence_obligation": "SUBMITTED_OUTPUT",
          "exact_text": "Submit completed output for every nonempty code cell as Run All evidence.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Submit completed output for every nonempty code cell as Run All evidence.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": null,
          "description": "Observed evidence supports: Submit completed output for every nonempty code cell as Run All evidence.",
          "evidence_class": "DIRECT",
          "evidence_id": "submitted_run.1-evidence",
          "location": "candidate/notebook.ipynb",
          "provenance": "SUBMITTED"
        }
      ],
      "exact_text": "Submit completed output for every nonempty code cell as Run All evidence.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "submitted_run",
      "prerequisites": [],
      "requirement_id": "submitted_run",
      "semantic_decision": "SATISFIED"
    },
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "clean_run.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "clean_run.1-evidence"
          ],
          "evidence_obligation": "CLEAN_EXECUTION",
          "exact_text": "Notebook must run from a fresh kernel in document order.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Notebook must run from a fresh kernel in document order.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": null,
          "description": "Observed evidence supports: Notebook must run from a fresh kernel in document order.",
          "evidence_class": "DIRECT",
          "evidence_id": "clean_run.1-evidence",
          "location": "runtime-copy/executed.ipynb",
          "provenance": "JUDGE_RUNTIME"
        }
      ],
      "exact_text": "Notebook must run from a fresh kernel in document order.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "clean_run",
      "prerequisites": [],
      "requirement_id": "clean_run",
      "semantic_decision": "SATISFIED"
    },
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "saved_outputs.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "saved_outputs.1-evidence"
          ],
          "evidence_obligation": "SUBMITTED_OUTPUT",
          "exact_text": "Save all nonempty code-cell outputs in the submitted notebook.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Save all nonempty code-cell outputs in the submitted notebook.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": null,
          "description": "Observed evidence supports: Save all nonempty code-cell outputs in the submitted notebook.",
          "evidence_class": "DIRECT",
          "evidence_id": "saved_outputs.1-evidence",
          "location": "candidate/notebook.ipynb",
          "provenance": "SUBMITTED"
        }
      ],
      "exact_text": "Save all nonempty code-cell outputs in the submitted notebook.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "saved_outputs",
      "prerequisites": [],
      "requirement_id": "saved_outputs",
      "semantic_decision": "SATISFIED"
    },
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "fresh_outputs.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "fresh_outputs.1-evidence"
          ],
          "evidence_obligation": "GENERIC",
          "exact_text": "Saved semantic outputs must match current code and supplied data.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Saved semantic outputs must match current code and supplied data.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": null,
          "description": "Observed evidence supports: Saved semantic outputs must match current code and supplied data.",
          "evidence_class": "DIRECT",
          "evidence_id": "fresh_outputs.1-evidence",
          "location": "candidate/notebook.ipynb",
          "provenance": "SUBMITTED"
        }
      ],
      "exact_text": "Saved semantic outputs must match current code and supplied data.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "fresh_outputs",
      "prerequisites": [],
      "requirement_id": "fresh_outputs",
      "semantic_decision": "SATISFIED"
    },
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "metric.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "metric.1-evidence"
          ],
          "evidence_obligation": "SUBMITTED_OUTPUT",
          "exact_text": "Submit the RMSE produced by the evaluation cell.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Submit the RMSE produced by the evaluation cell.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": null,
          "description": "Observed evidence supports: Submit the RMSE produced by the evaluation cell.",
          "evidence_class": "DIRECT",
          "evidence_id": "metric.1-evidence",
          "location": "candidate/notebook.ipynb#cell-4",
          "provenance": "SUBMITTED"
        }
      ],
      "exact_text": "Submit the RMSE produced by the evaluation cell.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "metric",
      "prerequisites": [],
      "requirement_id": "metric",
      "semantic_decision": "SATISFIED"
    },
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "protocol.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "protocol.1-evidence"
          ],
          "evidence_obligation": "GENERIC",
          "exact_text": "Fit preprocessing only on first four training rows; evaluate untouched last two rows.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Fit preprocessing only on first four training rows; evaluate untouched last two rows.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": null,
          "description": "Observed evidence supports: Fit preprocessing only on first four training rows; evaluate untouched last two rows.",
          "evidence_class": "DIRECT",
          "evidence_id": "protocol.1-evidence",
          "location": "candidate/notebook.ipynb#cell-1,cell-3",
          "provenance": "SUBMITTED"
        }
      ],
      "exact_text": "Fit preprocessing only on first four training rows; evaluate untouched last two rows.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "protocol",
      "prerequisites": [],
      "requirement_id": "protocol",
      "semantic_decision": "SATISFIED"
    },
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "artifact.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "artifact.1-evidence"
          ],
          "evidence_obligation": "SUBMITTED_OUTPUT",
          "exact_text": "Submit residual.svg containing the residual scatter plot.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Submit residual.svg containing the residual scatter plot.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": null,
          "description": "Observed evidence supports: Submit residual.svg containing the residual scatter plot.",
          "evidence_class": "DIRECT",
          "evidence_id": "artifact.1-evidence",
          "location": "candidate/residual.svg",
          "provenance": "SUBMITTED"
        }
      ],
      "exact_text": "Submit residual.svg containing the residual scatter plot.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "artifact",
      "prerequisites": [],
      "requirement_id": "artifact",
      "semantic_decision": "SATISFIED"
    },
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "dataset.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "dataset.1-evidence"
          ],
          "evidence_obligation": "GENERIC",
          "exact_text": "Train/evaluate using the supplied JudgeTiny v1 CSV bytes identified by trusted SHA-256.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Train/evaluate using the supplied JudgeTiny v1 CSV bytes identified by trusted SHA-256.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": "IDENTITY_DIRECT",
          "description": "Observed evidence supports: Train/evaluate using the supplied JudgeTiny v1 CSV bytes identified by trusted SHA-256.",
          "evidence_class": "DIRECT",
          "evidence_id": "dataset.1-evidence",
          "location": "rubric.json#dataset.sha256; candidate/tiny.csv; candidate/notebook.ipynb#cell-1",
          "provenance": "SUBMITTED"
        }
      ],
      "exact_text": "Train/evaluate using the supplied JudgeTiny v1 CSV bytes identified by trusted SHA-256.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "dataset",
      "prerequisites": [],
      "requirement_id": "dataset",
      "semantic_decision": "SATISFIED"
    },
    {
      "absence_proof_summary": null,
      "clauses": [
        {
          "absence_proof": null,
          "clause_id": "model.1",
          "earned_points": 1,
          "evaluability": "EVALUABLE",
          "evidence_ids": [
            "model.1-evidence"
          ],
          "evidence_obligation": "IMPLEMENTATION",
          "exact_text": "Use sklearn Ridge(alpha=1.0) in the model Pipeline.",
          "failure_kind": null,
          "mandatory": true,
          "max_points": 1,
          "score_reason": "Observed evidence supports: Use sklearn Ridge(alpha=1.0) in the model Pipeline.",
          "semantic_decision": "SATISFIED"
        }
      ],
      "confidence": "HIGH",
      "dependency_aware_status": "SATISFIED",
      "earned_points": 1.0,
      "evaluability": "EVALUABLE",
      "evidence": [
        {
          "dataset_strength": null,
          "description": "Observed evidence supports: Use sklearn Ridge(alpha=1.0) in the model Pipeline.",
          "evidence_class": "DIRECT",
          "evidence_id": "model.1-evidence",
          "location": "candidate/notebook.ipynb#cell-3",
          "provenance": "SUBMITTED"
        }
      ],
      "exact_text": "Use sklearn Ridge(alpha=1.0) in the model Pipeline.",
      "failed_clauses": [],
      "flags": [],
      "inspection_limitations": [],
      "mandatory": true,
      "max_points": 1,
      "parent_rubric_item": "model",
      "prerequisites": [],
      "requirement_id": "model",
      "semantic_decision": "SATISFIED"
    }
  ],
  "runtime_runs": [
    {
      "cell_timeout_seconds": 20,
      "failed_cell": null,
      "failure_stage": null,
      "file_delta": [
        {
          "path": "executed.ipynb",
          "provenance": "JUDGE_RUNTIME",
          "sha256_after": "f80bb6d0fa27fcbc1eed884bac4aedfbedbca02aa2c62993a5c7eaa570814008",
          "sha256_before": null
        },
        {
          "path": "residual.svg",
          "provenance": "MODIFIED_BY_RUNTIME",
          "sha256_after": "1733a91b331e69df9c962f63f21196c140a5d9f61d97e9420321a421bfa76902",
          "sha256_before": "6564d24837e9cf24d00f24b16b89e0d9e50da686155a35a765824079a421ffd9"
        },
        {
          "path": "runtime.json",
          "provenance": "JUDGE_RUNTIME",
          "sha256_after": "05c04b1a8ce47f458746ad4eef2837032f7b2b81c85e025d30b8a49a87b2e344",
          "sha256_before": null
        }
      ],
      "file_hashes": {
        "runtime_after": {
          "executed.ipynb": "f80bb6d0fa27fcbc1eed884bac4aedfbedbca02aa2c62993a5c7eaa570814008",
          "notebook.ipynb": "198b02730554df29dbb9b9ae1882e9dc427efdd73a3a8e8aa765c85c7f6e8013",
          "residual.svg": "1733a91b331e69df9c962f63f21196c140a5d9f61d97e9420321a421bfa76902",
          "runtime.json": "05c04b1a8ce47f458746ad4eef2837032f7b2b81c85e025d30b8a49a87b2e344",
          "tiny.csv": "6f3db621a1805e9c2664dd1b55f394a02e5234968b40f1391b62848e2475c175"
        },
        "source_after": {
          "notebook.ipynb": "198b02730554df29dbb9b9ae1882e9dc427efdd73a3a8e8aa765c85c7f6e8013",
          "residual.svg": "6564d24837e9cf24d00f24b16b89e0d9e50da686155a35a765824079a421ffd9",
          "tiny.csv": "6f3db621a1805e9c2664dd1b55f394a02e5234968b40f1391b62848e2475c175"
        },
        "source_before": {
          "notebook.ipynb": "198b02730554df29dbb9b9ae1882e9dc427efdd73a3a8e8aa765c85c7f6e8013",
          "residual.svg": "6564d24837e9cf24d00f24b16b89e0d9e50da686155a35a765824079a421ffd9",
          "tiny.csv": "6f3db621a1805e9c2664dd1b55f394a02e5234968b40f1391b62848e2475c175"
        }
      },
      "filesystem_writes": [
        "executed.ipynb",
        "residual.svg",
        "runtime.json"
      ],
      "inspection_limitations": [
        "Reviewed fixture execution only; not safe for arbitrary untrusted submissions."
      ],
      "interventions": [],
      "invocation": "reviewed fixture fresh-kernel worker",
      "isolation": "Hash-allowlisted authored fixture; runtime copy, sanitized environment; no OS sandbox",
      "level": "E1",
      "network_access": "No candidate network operations; localhost kernel transport; OS egress not enforced",
      "resource_limits": "20 seconds/cell, 90 seconds/notebook, one numerical thread; no OS memory/disk cap",
      "run_id": "clean-1",
      "source_unchanged": true,
      "status": "PASS",
      "stderr": "C:\\Users\\admin\\Desktop\\skill_for_chamdiem\\agent-judge-skills\\.venv\\Lib\\site-packages\\zmq\\_future.py:718: RuntimeWarning: Proactor event loop does not implement add_reader family of methods required for zmq. Registering an additional selector thread for add_reader support via tornado. Use `asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())` to avoid this warning.\n  self._get_loop()\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n",
      "stdout": "imports ready\ndataset rows 6\nEDA {'rows': 6, 'x_min': 0.0, 'x_max': 5.0}\nMODEL Ridge\nRMSE 1.21655251\nPLOT residual.svg\n",
      "subprocesses": [
        "Python worker",
        "fresh ipykernel"
      ],
      "total_timeout_seconds": 90,
      "working_directory": "runtime-copy/"
    }
  ],
  "schema_version": "1.0",
  "scoring": {
    "allocation_source": "RUBRIC",
    "coercion_source": null,
    "content_cap": null,
    "earned_points": 10.0,
    "final_points": 10.0,
    "known_earned_points": 10.0,
    "max_points": 10.0,
    "mode": "WEIGHTED",
    "not_evaluable_policy": "PRESERVE_NULL",
    "penalty_cap": null,
    "policy_source": "rubric.json: explicit clause weights",
    "rounding": {
      "decimal_places": 2,
      "mode": "ROUND_HALF_UP"
    },
    "unresolved_max_points": 0.0
  },
  "snapshot": {
    "identifier": "fixture-v1",
    "sha256": "198b02730554df29dbb9b9ae1882e9dc427efdd73a3a8e8aa765c85c7f6e8013"
  },
  "submission_id": "candidate-1",
  "task_id": "notebook_good"
}
```

</details>
