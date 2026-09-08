from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

import nbformat
import pytest
from jsonschema import ValidationError

from judgment import InputSession, canonical, render, summarize, validate_record
from support.records import skeleton

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures"


@pytest.fixture
def good():
    return json.loads((FIXTURES / "notebook_good/expected.judgment.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", sorted(FIXTURES.glob("*/expected.judgment.json")), ids=lambda p:p.parent.name)
def test_expected_schema_and_invariants(path):
    record=json.loads(path.read_text(encoding="utf-8"))
    validate_record(record)
    flags=json.loads(path.with_name("expected-flags.json").read_text(encoding="utf-8"))
    assert set(flags)==set(record["flags"])
    nbformat.validate(nbformat.read(path.parent/"candidate/notebook.ipynb",as_version=4))


@pytest.mark.parametrize("detail", ["concise","standard","forensic","json"])
def test_output_round_trip(good,detail):
    output=render(good,detail)
    raw=output if detail=="json" else re.search(r"```json\n(.*?)\n```",output,re.S).group(1)
    assert json.loads(raw)==good


def session_with_contract(tmp_path,good):
    (tmp_path/"rubric.txt").write_text("Explicit fixture rubric")
    (tmp_path/"code.py").write_text("assert True")
    (tmp_path/"gold.json").write_text('{"answer":true}')
    session=InputSession(tmp_path,{"rubric.txt":"RUBRIC","code.py":"CANDIDATE","gold.json":"GOLD_LABEL"})
    session.read("rubric.txt")
    session.lock_requirements(good["requirements"],good["scoring"])
    session.advance()
    return session


def test_no_requirement_does_not_invent_rubric(tmp_path):
    (tmp_path/"code.py").write_text("return 1")
    session=InputSession(tmp_path,{"code.py":"CANDIDATE"})
    with pytest.raises(PermissionError):session.read("code.py")
    with pytest.raises(ValueError):session.lock_requirements([], {})


def test_reference_requires_immutable_lock(tmp_path,good):
    session=session_with_contract(tmp_path,good)
    with pytest.raises(PermissionError):session.read("gold.json")
    with pytest.raises(ValueError):session.open_reference_phase()
    session.read("code.py")
    session.advance()
    lock=session.freeze(good,tmp_path/"locked.json")
    session.open_reference_phase()
    assert json.loads(session.read("gold.json"))["answer"] is True
    assert hashlib.sha256((tmp_path/"locked.json").read_bytes()).hexdigest()==lock["sha256"]
    with pytest.raises(ValueError):session.freeze(good,tmp_path/"locked.json")


def test_ambiguous_role_and_escape_stay_unopened(tmp_path):
    session=InputSession(tmp_path,{"maybe.json":None,"../outside":"CONTEXT_ONLY"})
    with pytest.raises(PermissionError):session.read("maybe.json")
    with pytest.raises(PermissionError):session.read("../outside")
    assert all(e["action"]=="DENIED" for e in session.events)


def test_lock_detects_tampering(tmp_path,good):
    session=session_with_contract(tmp_path,good);session.advance()
    session.freeze(good,tmp_path/"locked.json")
    (tmp_path/"locked.json").write_text("{}")
    with pytest.raises(ValueError,match="modified"):session.open_reference_phase()


def test_not_evaluable_cannot_be_false_or_zero(good):
    clause=good["requirements"][0]["clauses"][0]
    clause.update(evaluability="NOT_EVALUABLE",semantic_decision="UNSATISFIED",earned_points=0)
    with pytest.raises(ValidationError):validate_record(good)


def test_unknown_points_remain_unresolved(good):
    clause=good["requirements"][0]["clauses"][0]
    clause.update(evaluability="NOT_EVALUABLE",semantic_decision=None,earned_points=None)
    record=summarize(good);validate_record(record)
    assert record["scoring"]["earned_points"] is None
    assert record["scoring"]["known_earned_points"]==9
    assert record["scoring"]["unresolved_max_points"]==1
    assert record["scoring"]["final_points"] is None


def test_flags_and_confidence_do_not_change_scores_or_verdict(good):
    changed=deepcopy(good)
    changed["flags"]=["WEAK_DATASET_PROVENANCE"]
    for req in changed["requirements"]:
        req["confidence"]="LOW";req["flags"]=["WEAK_DATASET_PROVENANCE"]
    validate_record(changed)
    assert summarize(changed)["scoring"]==good["scoring"]
    assert [r["semantic_decision"] for r in changed["requirements"]]==[r["semantic_decision"] for r in good["requirements"]]


@pytest.mark.parametrize("field", ["exact_text","max_points"])
def test_candidate_tests_cannot_add_or_relax_contract(tmp_path,good,field):
    session=session_with_contract(tmp_path,good);session.read("code.py");session.advance()
    changed=deepcopy(good)
    if field=="exact_text":changed["requirements"][0]["clauses"][0][field]="Hidden test asks for a different exception."
    else:
        changed["requirements"][0]["clauses"][0][field]=0.5
        changed["requirements"][0]["clauses"][0]["earned_points"]=0.5
        changed["requirements"][0]["max_points"]=0.5
        changed=summarize(changed)
    with pytest.raises(ValueError,match="Locked requirements"):session.freeze(changed,tmp_path/"locked.json")


def test_runtime_artifact_cannot_be_submitted(good):
    req=next(r for r in good["requirements"] if r["requirement_id"]=="artifact")
    req["evidence"][0]["provenance"]="JUDGE_RUNTIME"
    with pytest.raises(ValueError,match="submitted output"):validate_record(good)


def test_code_presence_cannot_prove_execution(good):
    req=next(r for r in good["requirements"] if r["requirement_id"]=="clean_run")
    req["evidence"][0]["provenance"]="SUBMITTED"
    with pytest.raises(ValueError,match="clean execution"):validate_record(good)


def test_partial_credit_keeps_failed_semantics(good):
    req=good["requirements"][0];clause=req["clauses"][0]
    clause.update(semantic_decision="UNSATISFIED",earned_points=0.5,failure_kind="CONTRADICTION",score_reason="Rubric explicitly gives half for incomplete implementation.")
    req["evidence"][0]["evidence_class"]="CONTRADICTORY"
    result=summarize(good);validate_record(result)
    assert result["requirements"][0]["semantic_decision"]=="UNSATISFIED"
    assert result["scoring"]["earned_points"]==9.5


def test_parent_weights_must_equal_clause_weights(good):
    good["requirements"][0]["max_points"]=2
    with pytest.raises(ValueError,match="RUBRIC_WEIGHT_MISMATCH"):validate_record(good)


def test_negative_absence_requires_search(good):
    req=good["requirements"][0]
    req["clauses"][0].update(semantic_decision="UNSATISFIED",failure_kind="ABSENCE",earned_points=0)
    with pytest.raises((ValueError,ValidationError)):validate_record(summarize(good))


def test_binary_only_has_no_invented_points(good):
    from support.records import policy
    good["scoring"]=policy(False)
    for req in good["requirements"]:
        req["max_points"]=None
        for clause in req["clauses"]:clause.update(max_points=None,earned_points=None)
    result=summarize(good);validate_record(result)
    assert result["scoring"]["earned_points"] is None


def test_penalties_caps_rounding_are_separate(good):
    good["penalties"]=[{"penalty_id":"late","rule_source":"Rubric: late penalty 0.125","points":0.125,"evidence_ids":[good["requirements"][0]["evidence"][0]["evidence_id"]]}]
    good["scoring"]["content_cap"]=9
    record=summarize(good);validate_record(record)
    assert record["scoring"]["earned_points"]==10
    assert record["scoring"]["final_points"]==8.88


def test_derived_allocation_needs_flag(good):
    good["scoring"]["allocation_source"]="JUDGE_DERIVED_ALLOCATION"
    with pytest.raises(ValueError,match="disclosed"):validate_record(good)
    good["flags"].append("JUDGE_DERIVED_ALLOCATION")
    validate_record(good)


def test_tampered_fixture_refuses_execution(tmp_path):
    from support.runtime import run_fixture
    with pytest.raises(PermissionError):run_fixture(tmp_path,tmp_path/"runtime")


def test_post_reference_requires_lock(good):
    good["phase"]="POST_REFERENCE"
    with pytest.raises(ValueError,match="predecessor lock"):validate_record(good)


def test_post_reference_cannot_rewrite_locked_record(good):
    from judgment import digest, validate_post_reference
    post=deepcopy(good)
    post.update(phase="POST_REFERENCE",lock={"path":"pre-reference.json","sha256":digest(good)})
    validate_post_reference(post,good)
    post["requirements"][0]["exact_text"]="Relaxed requirement after seeing answer"
    with pytest.raises(ValueError,match="rewrote"):validate_post_reference(post,good)


def test_preference_rating_separate_from_content(good):
    good["preference_scores"]=[{"criterion_id":"clarity","rule_source":"Rubric separately requests clarity rating out of 5",
        "value":3,"max_value":5,"evidence_ids":[good["requirements"][0]["evidence"][0]["evidence_id"]],"content_clause_id":None}]
    result=summarize(good);validate_record(result)
    assert result["scoring"]["earned_points"]==10


def test_benchmark_zero_export_preserves_semantic_null(good):
    good["requirements"][0]["clauses"][0].update(evaluability="NOT_EVALUABLE",semantic_decision=None,earned_points=None)
    good["scoring"].update(not_evaluable_policy="BENCHMARK_ZERO",coercion_source="Benchmark export contract explicitly forces zero for missing evidence")
    record=summarize(good);validate_record(record)
    assert record["scoring"]["final_points"]==9
    assert record["scoring"]["earned_points"] is None
    assert record["requirements"][0]["semantic_decision"] is None


def test_missing_requirement_record_is_ungradable(good):
    from support.records import policy
    good.update(requirements=[],scoring=policy(False),inspection_limitations=["No requirement supplied; no rubric invented."])
    record=summarize(good);validate_record(record)
    assert record["overall_status"]=="NOT_EVALUABLE"
    assert record["requirements"]==[]


def test_filename_only_identity_is_not_a_failure(good):
    req=next(r for r in good["requirements"] if r["requirement_id"]=="dataset")
    req["clauses"][0].update(evaluability="NOT_EVALUABLE",semantic_decision=None,earned_points=None)
    req["evidence"][0].update(evidence_class="CLAIM_ONLY",dataset_strength="CLAIM_ONLY",description="Only filename claims identity; no contradiction available.")
    req["flags"]=["WEAK_DATASET_PROVENANCE"]
    record=summarize(good);validate_record(record)
    assert next(r for r in record["requirements"] if r["requirement_id"]=="dataset")["semantic_decision"] is None


def test_execution_counts_alone_do_not_prove_staleness():
    import ast
    from support.dev_eval import inspect_clause
    root=FIXTURES/"notebook_good"
    nb=json.loads((root/"candidate/notebook.ipynb").read_text())
    runtime=deepcopy(nb)
    for cell in nb["cells"]:cell["execution_count"]=None
    clause={"text":"Current output must match code"}
    tree=ast.parse("\n".join(c["source"] for c in nb["cells"]))
    obs=inspect_clause("fresh_outputs",clause,nb,tree,{},runtime,{"status":"PASS"},None,{})
    assert obs["decision"]=="SATISFIED"
