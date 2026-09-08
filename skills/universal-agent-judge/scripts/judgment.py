"""Validate/render audit records and mediate input access. Never executes candidates."""
from __future__ import annotations

import argparse
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = SKILL_ROOT / "schemas" / "judgment.schema.json"
REFERENCE_ROLES = {"REFERENCE_SOLUTION", "GOLD_LABEL", "ORACLE_TEST"}
STATES = ["INPUT_CLASSIFICATION", "REQUIREMENT_LOCK", "PRE_REFERENCE_EVIDENCE",
          "PRE_REFERENCE_DECISION", "IMMUTABLE_LOCK", "OPTIONAL_REFERENCE_ACCESS",
          "POST_REFERENCE_AUDIT"]


def canonical(record):
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def digest(record):
    return hashlib.sha256(canonical(record)).hexdigest()


def decimal(value):
    return Decimal(str(value))


def number(value):
    return None if value is None else float(value)


def semantic(clauses):
    required = [c for c in clauses if c["mandatory"]]
    if not required:
        return "EVALUABLE", "SATISFIED"
    if any(c["semantic_decision"] == "UNSATISFIED" for c in required):
        return "EVALUABLE", "UNSATISFIED"
    if any(c["evaluability"] == "NOT_EVALUABLE" for c in required):
        return "NOT_EVALUABLE", None
    return "EVALUABLE", "SATISFIED"


def summarize(record):
    """Derive totals from judged clauses. Does not decide clause semantics."""
    result = deepcopy(record)
    weighted = result["scoring"]["mode"] == "WEIGHTED"
    known = Decimal(0)
    unresolved = Decimal(0)
    maximum = Decimal(0)
    unknown = False
    for req in result["requirements"]:
        req["evaluability"], req["semantic_decision"] = semantic(req["clauses"])
        req["failed_clauses"] = [c["clause_id"] for c in req["clauses"]
                                 if c["semantic_decision"] == "UNSATISFIED"]
        if weighted:
            local = Decimal(0)
            local_unknown = False
            for clause in req["clauses"]:
                if clause["max_points"] is None:
                    raise ValueError("Weighted clause needs a known maximum")
                weight = decimal(clause["max_points"])
                maximum += weight
                if clause["earned_points"] is None:
                    unknown = local_unknown = True
                    unresolved += weight
                else:
                    earned = decimal(clause["earned_points"])
                    known += earned
                    local += earned
            req["earned_points"] = None if local_unknown else number(local)
        else:
            req["earned_points"] = None
    by_id = {r["requirement_id"]: r for r in result["requirements"]}
    for req in result["requirements"]:
        req["dependency_aware_status"] = req["semantic_decision"]
        if req["semantic_decision"] == "SATISFIED" and any(
            by_id[p]["semantic_decision"] == "UNSATISFIED" for p in req["prerequisites"]
        ):
            req["dependency_aware_status"] = "BLOCKED"
    required = [r for r in result["requirements"] if r["mandatory"]]
    if not required:
        result["overall_status"] = "NOT_EVALUABLE"
    elif any(r["semantic_decision"] == "UNSATISFIED" for r in required):
        result["overall_status"] = "NOT_SOLVED"
    elif any(r["semantic_decision"] is None for r in required):
        result["overall_status"] = "NOT_EVALUABLE"
    else:
        result["overall_status"] = "SOLVED"
    scoring = result["scoring"]
    if not weighted:
        for key in ("earned_points", "max_points", "known_earned_points",
                    "unresolved_max_points", "final_points"):
            scoring[key] = None
        return result
    scoring["earned_points"] = None if unknown else number(known)
    scoring["max_points"] = number(maximum)
    scoring["known_earned_points"] = number(known)
    scoring["unresolved_max_points"] = number(unresolved)
    if unknown and scoring["not_evaluable_policy"] != "BENCHMARK_ZERO":
        scoring["final_points"] = None
    else:
        content = known
        if scoring["content_cap"] is not None:
            content = min(content, decimal(scoring["content_cap"]))
        penalty = sum((decimal(p["points"]) for p in result["penalties"]), Decimal(0))
        if scoring["penalty_cap"] is not None:
            penalty = min(penalty, decimal(scoring["penalty_cap"]))
        unit = Decimal(1).scaleb(-scoring["rounding"]["decimal_places"])
        scoring["final_points"] = number(max(Decimal(0), content-penalty).quantize(
            unit, rounding=ROUND_HALF_UP))
    return result


def validate_record(record):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(record)
    canonical(record)  # Reject NaN/infinity rather than accepting non-JSON numbers.
    errors = []
    requirements = record["requirements"]
    ids = [r["requirement_id"] for r in requirements]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate requirement ID")
    clause_ids = [c["clause_id"] for r in requirements for c in r["clauses"]]
    if len(clause_ids) != len(set(clause_ids)):
        errors.append("Duplicate clause ID")
    all_evidence = [e["evidence_id"] for r in requirements for e in r["evidence"]]
    if len(all_evidence) != len(set(all_evidence)):
        errors.append("Duplicate evidence ID")
    weighted = record["scoring"]["mode"] == "WEIGHTED"
    for req in requirements:
        evidence = {e["evidence_id"]: e for e in req["evidence"]}
        if not set(req["prerequisites"]).issubset(ids) or req["requirement_id"] in req["prerequisites"]:
            errors.append("Unknown/self prerequisite")
        if weighted:
            weights = [c["max_points"] for c in req["clauses"]]
            if req["max_points"] is None or any(w is None for w in weights):
                errors.append("Weighted rubric requires maxima")
            elif sum(map(decimal, weights), Decimal(0)) != decimal(req["max_points"]):
                errors.append("RUBRIC_WEIGHT_MISMATCH")
        elif req["max_points"] is not None:
            errors.append("Binary-only parent must not invent points")
        for clause in req["clauses"]:
            if not set(clause["evidence_ids"]).issubset(evidence):
                errors.append("Unknown evidence reference")
                continue
            entries = [evidence[e] for e in clause["evidence_ids"]]
            classes = {e["evidence_class"] for e in entries}
            verdict = clause["semantic_decision"]
            if verdict == "SATISFIED" and ("DIRECT" not in classes or "CONTRADICTORY" in classes):
                errors.append("SATISFIED needs direct proof without decisive contradiction")
            if verdict == "SATISFIED" and clause["evidence_obligation"] == "SUBMITTED_OUTPUT":
                if not any(e["provenance"] == "SUBMITTED" and e["evidence_class"] == "DIRECT" for e in entries):
                    errors.append("Runtime output cannot prove submitted output")
            if verdict == "SATISFIED" and clause["evidence_obligation"] == "CLEAN_EXECUTION":
                if not any(e["provenance"] == "JUDGE_RUNTIME" and e["evidence_class"] == "DIRECT" for e in entries):
                    errors.append("Code presence cannot prove clean execution")
            if verdict == "UNSATISFIED":
                kind = clause["failure_kind"]
                if kind == "ABSENCE":
                    if not clause["absence_proof"] or not req["absence_proof_summary"]:
                        errors.append("Negative absence requires Absence Proof")
                    if not entries:
                        errors.append("Absence proof needs recorded search evidence")
                elif kind != "CONTRADICTION" or "CONTRADICTORY" not in classes:
                    errors.append("UNSATISFIED needs contradiction or absence proof")
            elif clause["failure_kind"] is not None:
                errors.append("Failure kind only applies to a failed clause")
            earned, maximum = clause["earned_points"], clause["max_points"]
            if not weighted and (earned is not None or maximum is not None):
                errors.append("Binary-only clause must not invent points")
            if earned is not None and (maximum is None or decimal(earned) > decimal(maximum)):
                errors.append("Earned points exceed maximum")
            if weighted and clause["evaluability"] == "EVALUABLE" and earned is None:
                errors.append("Evaluable weighted clause requires points")
    # Detect dependency cycles without recursively loading policy documents.
    graph = {r["requirement_id"]: r["prerequisites"] for r in requirements}
    def visit(node, active, done):
        if node in active:
            raise ValueError("Circular requirement prerequisites")
        if node in done or node not in graph:
            return
        for parent in graph[node]:
            visit(parent, active | {node}, done)
        done.add(node)
    for node in graph:
        visit(node, set(), set())
    scoring = record["scoring"]
    if weighted and (scoring["allocation_source"] == "NONE" or not scoring["policy_source"]):
        errors.append("Weighted score requires allocation/policy source")
    if not weighted and scoring["allocation_source"] != "NONE":
        errors.append("Binary-only allocation must be NONE")
    if scoring["allocation_source"] == "JUDGE_DERIVED_ALLOCATION" and "JUDGE_DERIVED_ALLOCATION" not in record["flags"]:
        errors.append("Derived allocation must be disclosed")
    if scoring["not_evaluable_policy"] == "BENCHMARK_ZERO" and not scoring["coercion_source"]:
        errors.append("Benchmark coercion requires exact source")
    for penalty in record["penalties"]:
        if not set(penalty["evidence_ids"]).issubset(all_evidence):
            errors.append("Penalty evidence missing")
    for preference in record["preference_scores"]:
        if preference["value"] is not None and preference["value"] > preference["max_value"]:
            errors.append("Preference outside scale")
        if not set(preference["evidence_ids"]).issubset(all_evidence):
            errors.append("Preference evidence missing")
        if preference["content_clause_id"] is not None and preference["content_clause_id"] not in clause_ids:
            errors.append("Preference content clause missing")
    leaked = record["reference_accessed_before_lock"]
    if leaked and "REFERENCE_LEAKAGE" not in record["flags"]:
        errors.append("Reference leakage must be disclosed")
    for item in record["inputs"]:
        if item["role"] is None and item["access_phase"] != "UNOPENED":
            errors.append("Ambiguous role must remain unopened")
        if item["role"] in REFERENCE_ROLES and item["access_phase"] == "PRE_REFERENCE" and not leaked:
            errors.append("Undisclosed reference leakage")
    for event in record["access_log"]:
        if event["action"] == "READ" and event["role"] in REFERENCE_ROLES:
            if STATES.index(event["state"]) < STATES.index("OPTIONAL_REFERENCE_ACCESS") and not leaked:
                errors.append("Reference access before lock")
    for run in record["runtime_runs"]:
        hashes = run["file_hashes"]
        if run["source_unchanged"] is True and hashes["source_before"] != hashes["source_after"]:
            errors.append("Source preservation claim contradicts hashes")
        for delta in run["file_delta"]:
            existed = delta["path"] in hashes["source_before"]
            if delta["provenance"] != ("MODIFIED_BY_RUNTIME" if existed else "JUDGE_RUNTIME"):
                errors.append("File delta provenance contradicts original snapshot")
            if delta["sha256_before"] != hashes["source_before"].get(delta["path"]):
                errors.append("File delta original hash mismatch")
            if delta["sha256_after"] != hashes["runtime_after"].get(delta["path"]):
                errors.append("File delta runtime hash mismatch")
    if record["phase"] == "PRE_REFERENCE" and record["post_reference_audit"]:
        errors.append("PRE_REFERENCE cannot include reference findings")
    if record["phase"] == "POST_REFERENCE" and record["lock"] is None:
        errors.append("POST_REFERENCE requires predecessor lock")
    if not requirements and not record["inspection_limitations"]:
        errors.append("Missing requirements must be explained")
    if errors:
        raise ValueError("; ".join(errors))
    derived = summarize(record)
    for key in ("overall_status", "scoring"):
        if record[key] != derived[key]:
            raise ValueError("Inconsistent derived field: " + key)
    for old, new in zip(requirements, derived["requirements"]):
        for key in ("evaluability", "semantic_decision", "earned_points", "failed_clauses", "dependency_aware_status"):
            if old[key] != new[key]:
                raise ValueError("Inconsistent requirement " + old["requirement_id"] + ": " + key)
    return record


def render(record, detail="standard"):
    validate_record(record)
    raw = json.dumps(record, ensure_ascii=False, indent=2, allow_nan=False)
    if detail == "json":
        return raw + "\n"
    if detail not in {"concise", "standard", "forensic"}:
        raise ValueError("Unknown detail")
    def cell(value):
        return str(value if value is not None else "unresolved").replace("|", "\\|").replace("\n", " ")
    lines = ["# Judgment: " + record["task_id"], "", "Status: " + record["overall_status"], "",
             "| ID | Evaluability | Decision | Content points | Evidence |",
             "|---|---|---|---|---|"]
    for req in record["requirements"]:
        points = "binary only" if record["scoring"]["mode"] == "BINARY_ONLY" else f'{req["earned_points"]}/{req["max_points"]}'
        values = [req["requirement_id"], req["evaluability"], req["semantic_decision"], points,
                  "; ".join(e["location"] + ": " + e["description"] for e in req["evidence"])]
        lines.append("| " + " | ".join(map(cell, values)) + " |")
    s = record["scoring"]
    lines += ["", f'Content: {s["earned_points"]}/{s["max_points"]}; known: {s["known_earned_points"]}; unresolved maximum: {s["unresolved_max_points"]}; final: {s["final_points"]}.',
              "", "Penalties: " + json.dumps(record["penalties"], ensure_ascii=False),
              "", "Limitations: " + ("; ".join(record["inspection_limitations"]) or "none")]
    if detail != "concise":
        for req in record["requirements"]:
            lines += ["", "## " + req["requirement_id"]]
            lines += [f'- {c["clause_id"]}: {c["exact_text"]} — {c["semantic_decision"]}; {c["score_reason"]}' for c in req["clauses"]]
            lines += ["", "Flags: " + (", ".join(req["flags"]) or "none")]
        lines += ["", "Runtime: " + ("; ".join(r["run_id"] + " " + r["status"] for r in record["runtime_runs"]) or "not run")]
    lines += ["", "<details>" if detail != "forensic" else "", "<summary>Canonical judgment JSON</summary>" if detail != "forensic" else "## Canonical judgment JSON", "", "```json", raw, "```", "", "</details>" if detail != "forensic" else ""]
    return "\n".join(lines) + "\n"


def contract_projection(requirements):
    return [{k: r[k] for k in ("requirement_id", "parent_rubric_item", "exact_text", "mandatory", "prerequisites", "max_points")} |
            {"clauses": [{k: c[k] for k in ("clause_id", "exact_text", "mandatory", "max_points", "evidence_obligation")} for c in r["clauses"]]} for r in requirements]


class InputSession:
    """Optional access gate. Manifest metadata must come from the user/task protocol."""
    def __init__(self, root, roles):
        self.root = Path(root).resolve()
        valid_roles = REFERENCE_ROLES | {"TASK_SOURCE", "RUBRIC", "CANDIDATE", "CONTEXT_ONLY", None}
        if any(role not in valid_roles for role in roles.values()):
            raise ValueError("Unknown input role")
        self.roles = dict(roles)
        self.state = "INPUT_CLASSIFICATION"
        self.events = []
        self._contract = None
        self._scoring_policy = None
        self._locked = None

    def read(self, path):
        role = self.roles.get(path)
        allowed = role is not None
        if role in REFERENCE_ROLES:
            allowed = self.state in {"OPTIONAL_REFERENCE_ACCESS", "POST_REFERENCE_AUDIT"}
        if role == "CANDIDATE":
            allowed = self.state != "INPUT_CLASSIFICATION"
        resolved = (self.root / path).resolve()
        allowed = allowed and resolved.is_relative_to(self.root)
        self.events.append({"path": path, "role": role, "state": self.state,
                            "action": "READ" if allowed else "DENIED"})
        if not allowed:
            raise PermissionError("Input role or phase denies access: " + path)
        return resolved.read_bytes()

    def lock_requirements(self, requirements, scoring_policy):
        if self.state != "INPUT_CLASSIFICATION" or not requirements:
            raise ValueError("Explicit nonempty requirements must precede candidate semantics")
        if not any(e["action"] == "READ" and e["role"] in {"TASK_SOURCE", "RUBRIC"} for e in self.events):
            raise ValueError("Read an authorized requirement source first")
        self._contract = canonical(contract_projection(requirements))
        self._scoring_policy = canonical({k: scoring_policy[k] for k in ("mode", "allocation_source", "policy_source", "rounding", "content_cap", "penalty_cap", "not_evaluable_policy", "coercion_source")})
        self.state = "REQUIREMENT_LOCK"

    def advance(self):
        index = STATES.index(self.state)
        if self.state in {"INPUT_CLASSIFICATION", "PRE_REFERENCE_DECISION", "IMMUTABLE_LOCK"}:
            raise ValueError("Use the explicit lock/access operation")
        if index == len(STATES)-1:
            raise ValueError("Terminal state")
        self.state = STATES[index+1]

    def freeze(self, record, destination):
        if self.state != "PRE_REFERENCE_DECISION":
            raise ValueError("Decision must precede immutable lock")
        validate_record(record)
        if record["phase"] != "PRE_REFERENCE":
            raise ValueError("Only initial judgment can be frozen")
        if canonical(contract_projection(record["requirements"])) != self._contract:
            raise ValueError("Locked requirements/thresholds/weights changed")
        policy = {k: record["scoring"][k] for k in ("mode", "allocation_source", "policy_source", "rounding", "content_cap", "penalty_cap", "not_evaluable_policy", "coercion_source")}
        if canonical(policy) != self._scoring_policy:
            raise ValueError("Locked scoring policy changed")
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as handle:
            handle.write(canonical(record))
        self._locked = {"path": str(destination), "sha256": digest(record)}
        self.state = "IMMUTABLE_LOCK"
        return deepcopy(self._locked)

    def open_reference_phase(self):
        if self.state != "IMMUTABLE_LOCK" or self._locked is None:
            raise ValueError("Immutable record required before reference access")
        if hashlib.sha256(Path(self._locked["path"]).read_bytes()).hexdigest() != self._locked["sha256"]:
            raise ValueError("Immutable record was modified")
        self.state = "OPTIONAL_REFERENCE_ACCESS"


def validate_post_reference(record, predecessor):
    """Verify linkage and preservation, in addition to structural validation."""
    validate_record(predecessor)
    validate_record(record)
    if record["phase"] != "POST_REFERENCE" or predecessor["phase"] != "PRE_REFERENCE":
        raise ValueError("Expected PRE_REFERENCE predecessor and POST_REFERENCE audit")
    if record["lock"]["sha256"] != digest(predecessor):
        raise ValueError("Predecessor hash mismatch")
    for field in ("task_id", "submission_id", "mode", "snapshot", "requirements", "scoring", "penalties", "preference_scores", "reference_accessed_before_lock"):
        if record[field] != predecessor[field]:
            raise ValueError("Post-reference audit rewrote frozen field: " + field)
    if record["runtime_runs"][:len(predecessor["runtime_runs"])] != predecessor["runtime_runs"]:
        raise ValueError("Post-reference audit rewrote initial runtime evidence")
    ids = {r["requirement_id"]: {c["clause_id"] for c in r["clauses"]} for r in predecessor["requirements"]}
    for item in record["post_reference_audit"]:
        if item["requirement_id"] not in ids or not set(item["locked_clause_ids"]).issubset(ids[item["requirement_id"]]):
            raise ValueError("Amendment must reference locked clauses")
        if item["amended_decision"] is not None and not item["locked_clause_ids"]:
            raise ValueError("Amendment needs an explicit locked clause")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["validate", "render"])
    parser.add_argument("record", type=Path)
    parser.add_argument("--detail", choices=["concise", "standard", "forensic", "json"], default="standard")
    parser.add_argument("--predecessor", type=Path, help="Required for POST_REFERENCE integrity validation")
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    validate_record(record)
    if record["phase"] == "POST_REFERENCE":
        if args.predecessor is None:
            parser.error("POST_REFERENCE validation requires --predecessor")
        validate_post_reference(record, json.loads(args.predecessor.read_text(encoding="utf-8")))
    print("Valid judgment" if args.operation == "validate" else render(record, args.detail))


if __name__ == "__main__":
    main()
