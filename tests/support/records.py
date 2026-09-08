"""Record construction only. Expected labels and observed checks are separate callers."""
from copy import deepcopy
import hashlib
from pathlib import Path

from judgment import summarize


def policy(weighted=True):
    return {"mode": "WEIGHTED" if weighted else "BINARY_ONLY",
            "allocation_source": "RUBRIC" if weighted else "NONE",
            "policy_source": "rubric.json: explicit clause weights" if weighted else None,
            "rounding": {"decimal_places": 2, "mode": "ROUND_HALF_UP"},
            "content_cap": None, "penalty_cap": None,
            "not_evaluable_policy": "PRESERVE_NULL", "coercion_source": None,
            "earned_points": None, "max_points": None, "known_earned_points": None,
            "unresolved_max_points": None, "final_points": None}


def skeleton(rubric, snapshot=None):
    requirements = []
    for item in rubric["requirements"]:
        clauses = []
        for clause in item["clauses"]:
            clauses.append({"clause_id": clause["id"], "exact_text": clause["text"],
                            "evidence_obligation": "SUBMITTED_OUTPUT" if clause["check"] in {"submitted_run", "saved_outputs", "metric", "artifact", "eda"} else "CLEAN_EXECUTION" if clause["check"] == "clean_run" else "IMPLEMENTATION" if clause["check"] in {"implementation", "model", "pipeline", "search", "degree", "bias"} else "GENERIC",
                            "mandatory": True, "evaluability": "NOT_EVALUABLE",
                            "semantic_decision": None, "earned_points": None,
                            "max_points": clause["points"], "score_reason": "Not yet evaluated",
                            "evidence_ids": [], "failure_kind": None, "absence_proof": None})
        requirements.append({"requirement_id": item["id"], "parent_rubric_item": item["id"],
            "exact_text": item["text"], "mandatory": True, "prerequisites": [],
            "clauses": clauses, "evaluability": "NOT_EVALUABLE", "semantic_decision": None,
            "earned_points": None, "max_points": item["points"], "evidence": [],
            "confidence": "HIGH", "flags": [], "failed_clauses": [],
            "absence_proof_summary": None, "dependency_aware_status": None,
            "inspection_limitations": []})
    return {"schema_version": "1.0", "task_id": rubric["task_id"], "submission_id": "candidate-1",
        "mode": "NOTEBOOK_ML_MODE", "snapshot": {"identifier": "fixture-v1", "sha256": snapshot},
        "phase": "PRE_REFERENCE", "reference_accessed_before_lock": False,
        "overall_status": "NOT_EVALUABLE", "inputs": [], "requirements": requirements,
        "scoring": policy(), "penalties": [], "preference_scores": [], "runtime_runs": [],
        "flags": [], "inspection_limitations": [], "loaded_references": [], "access_log": [],
        "lock": None, "post_reference_audit": []}


def apply_observations(record, observations):
    result = deepcopy(record)
    for req in result["requirements"]:
        for clause in req["clauses"]:
            obs = observations[clause["clause_id"]]
            verdict = obs["decision"]
            clause["semantic_decision"] = verdict
            clause["evaluability"] = "NOT_EVALUABLE" if verdict is None else "EVALUABLE"
            clause["earned_points"] = (None if verdict is None else
                obs.get("points", clause["max_points"] if verdict == "SATISFIED" else 0))
            clause["score_reason"] = obs["description"]
            eid = clause["clause_id"] + "-evidence"
            clause["evidence_ids"] = [eid]
            cls = "DIRECT" if verdict == "SATISFIED" else "CONTRADICTORY" if verdict == "UNSATISFIED" else "SUPPORTING"
            kind = obs.get("failure_kind", "CONTRADICTION" if verdict == "UNSATISFIED" else None)
            clause["failure_kind"] = kind
            if kind == "ABSENCE":
                clause["absence_proof"] = {"scope": "candidate snapshot", "checks": obs["checks"], "result": obs["description"]}
                req["absence_proof_summary"] = "Recorded exact-path/cell and submission-scope search in failed clauses."
            req["evidence"].append({"evidence_id": eid, "location": obs["location"],
                "description": obs["description"], "evidence_class": cls,
                "provenance": obs.get("provenance", "SUBMITTED"),
                "dataset_strength": obs.get("dataset_strength")})
            for flag in obs.get("flags", []):
                if flag not in req["flags"]:
                    req["flags"].append(flag)
                if flag not in result["flags"]:
                    result["flags"].append(flag)
            if verdict is None:
                req["inspection_limitations"].append(obs["description"])
    return summarize(result)


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
