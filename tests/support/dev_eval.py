"""Development evaluator for the finite authored fixture language, not a universal judge.

Reads task/candidate through InputSession; writes immutable observations before gold.
AST checks and fresh-kernel evidence exercise the skill's decision boundaries.
Expected files are comparison-only. No LLM accuracy or independent blind claim.
"""
import argparse
import ast
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/universal-agent-judge/scripts"))
sys.path.insert(0, str(ROOT / "tests"))
from judgment import InputSession, render, validate_record
from support.records import skeleton, apply_observations, file_hash
from support.runtime import run_fixture

REFERENCES = ["input-roles.md", "mode-notebook-ml.md", "rubric-scoring.md",
              "safe-candidate-execution.md", "runtime-verification.md", "provenance.md",
              "notebook-execution.md", "dataset-provenance.md", "mode-artifact.md",
              "flags-full.md", "output-contract.md"]


def streams(cell):
    return "".join(o.get("text", "") if isinstance(o.get("text", ""), str) else "".join(o["text"])
                   for o in cell.get("outputs", []) if o.get("output_type") == "stream" and o.get("name") == "stdout").strip()


def inspect_clause(check, clause, nb, tree, candidate_files, runtime_nb, run, data_hash, rubric):
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    def named(name):
        return [n for n in calls if isinstance(n.func, ast.Name) and n.func.id == name]
    def kw(call, key):
        return next((ast.literal_eval(k.value) for k in call.keywords if k.arg == key), None)
    obs = {"decision": "SATISFIED", "location": "candidate/notebook.ipynb",
           "description": "Observed evidence supports: " + clause["text"]}
    def failed(message, flags=(), absence=False, location=None):
        obs.update(decision="UNSATISFIED", description=message, flags=list(flags),
                   failure_kind="ABSENCE" if absence else "CONTRADICTION")
        if location:obs["location"] = location
        if absence:obs["checks"] = ["Inspect exact locked cell/output/path", "Search all submitted notebook source/output arrays and candidate file inventory", "Follow relevant producer references; no matching required evidence found"]
    def unknown(message):
        obs.update(decision=None, description=message)
    code = [c for c in nb["cells"] if c["cell_type"] == "code" and c["source"].strip()]
    missing = [c["id"] for c in code if not c.get("outputs")]
    if check == "implementation":
        if not all(any(isinstance(c.func, ast.Attribute) and c.func.attr == name for c in calls) for name in ("fit", "predict")):
            failed("Required fit/predict call absent after full source inspection.", absence=True)
    elif check in {"submitted_run", "saved_outputs"}:
        if missing:
            failed("Required submitted outputs absent in " + ", ".join(missing) + "; counts are supporting only.",
                   ["NOTEBOOK_NOT_RUN_ALL"] if check == "submitted_run" else [], True,
                   "candidate/notebook.ipynb#" + ",".join(missing))
    elif check == "clean_run":
        obs["provenance"] = "JUDGE_RUNTIME";obs["location"] = "runtime-copy/executed.ipynb"
        if run["status"] == "FAIL":
            failed("Fresh kernel failed in cell " + str(run["failed_cell"]) + ": " + str(run["failure_stage"]),
                   ["HIDDEN_STATE_DEPENDENCY"] if "NameError" in run["stderr"] else [])
        elif run["status"] != "PASS":unknown("Clean execution inconclusive: " + str(run["failure_stage"]))
    elif check == "fresh_outputs":
        if missing or run["status"] != "PASS":unknown("No complete submitted/runtime output pair; freshness unresolved.")
        elif [streams(c) for c in nb["cells"]] != [streams(c) for c in runtime_nb["cells"]]:
            failed("Submitted semantic stdout differs from fresh run on identical source and data; stderr retained separately as diagnostics.",
                   ["SUBMITTED_RUNTIME_DIVERGENCE", "STALE_NOTEBOOK_OUTPUT"])
            obs["location"] = "candidate/notebook.ipynb#cell-4; runtime-copy/executed.ipynb#cell-4"
    elif check == "metric":
        if not any(re.search(r"RMSE\s+[-+0-9.eE]+", streams(c)) for c in code):
            failed("No submitted RMSE output after all cell outputs and files inspected.", absence=True)
        else:obs["location"] = "candidate/notebook.ipynb#cell-4"
    elif check == "protocol":
        bad = [c for c in calls if isinstance(c.func, ast.Attribute) and c.func.attr == "fit"
               and c.args and isinstance(c.args[0], ast.Name) and c.args[0].id in {"X", "X_test"}]
        if bad:failed("Preprocessing fit(X) includes held-out rows before evaluation.", ["DATA_LEAKAGE_RISK"])
        obs["location"] = "candidate/notebook.ipynb#cell-1,cell-3"
    elif check == "artifact":
        needed = re.findall(r"residual\d*\.svg", clause["text"])
        absent = [name for name in needed if name not in candidate_files or b"<svg" not in candidate_files[name]]
        if absent:failed("Required submitted SVG absent/invalid: " + ", ".join(absent), ["MISSING_ARTIFACT"], True,
                          "; ".join("candidate/"+name for name in absent))
        else:obs["location"] = "; ".join("candidate/"+name for name in needed)
    elif check == "dataset":
        rows = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "rows" for t in n.targets)]
        generated = any(isinstance(n.value, (ast.ListComp, ast.List)) for n in rows)
        if generated:failed("Actual rows are generated by a list comprehension rather than loaded from required source.", ["SYNTHETIC_STANDIN"])
        elif data_hash != rubric["dataset"]["sha256"]:failed("Actual loaded tiny.csv bytes differ from trusted task hash.")
        obs["dataset_strength"] = "IDENTITY_DIRECT"
        obs["location"] = "rubric.json#dataset.sha256; candidate/tiny.csv; candidate/notebook.ipynb#cell-1"
    elif check == "model":
        # Scope to the estimator actually constructed inside the assigned Pipeline.
        models = [n.value for n in ast.walk(tree) if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "model" for t in n.targets)]
        ridge = [n for model in models for n in ast.walk(model) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id == "Ridge"]
        if not ridge or not any(kw(n,"alpha") == 1.0 for n in ridge):
            failed("Active model Pipeline does not use required Ridge(alpha=1.0).", ["MODEL_CONFIG_MISMATCH"])
        obs["location"] = "candidate/notebook.ipynb#cell-3"
    elif check == "eda":
        if not any(streams(c).startswith("EDA") for c in code):failed("Required EDA output absent.", absence=True)
        obs["location"] = "candidate/notebook.ipynb#cell-2"
    elif check == "pipeline":
        if not named("Pipeline"):failed("No Pipeline constructor in submitted implementation.", absence=True)
        obs["location"] = "candidate/notebook.ipynb#cell-3"
    elif check == "search":
        if not named("GridSearchCV"):failed("No GridSearchCV call in any submitted cell; only fixed-alpha Lasso.fit.", absence=True)
        obs["location"] = "candidate/notebook.ipynb#cell-3"
    elif check in {"degree", "bias"}:
        name, expected = ("degree",2) if check == "degree" else ("include_bias",False)
        if not any(kw(c,name) == expected for c in named("PolynomialFeatures")):
            failed("PolynomialFeatures configuration contradicts " + clause["text"])
        obs["location"] = "candidate/notebook.ipynb#cell-3"
    else:
        raise ValueError("Unsupported dev-fixture check; no generic verdict inferred: " + check)
    return obs


def evaluate(fixture, work):
    fixture=Path(fixture);work=Path(work);work.mkdir(parents=True,exist_ok=False)
    roles=json.loads((fixture/'inputs.json').read_text(encoding='utf-8'))
    session=InputSession(fixture,roles)
    session.read('task.md')
    rubric=json.loads(session.read('rubric.json'))
    exposure=json.loads(session.read('exposure.json')) if 'exposure.json' in roles else None
    draft=skeleton(rubric)
    session.lock_requirements(draft['requirements'],draft['scoring'])
    session.advance()
    nb=json.loads(session.read('candidate/notebook.ipynb'))
    data=session.read('candidate/tiny.csv')
    files={p.split('/',1)[1]:session.read(p) for p,role in roles.items() if role=='CANDIDATE' and p not in {'candidate/notebook.ipynb','candidate/tiny.csv'}}
    source='\n'.join(c['source'] for c in nb['cells'] if c['cell_type']=='code')
    tree=ast.parse(source)
    # Actual routing reads, not invented telemetry; fixed finite fixture rubric needs these guides.
    (ROOT/'skills/universal-agent-judge/SKILL.md').read_text(encoding='utf-8')
    for name in REFERENCES:(ROOT/'skills/universal-agent-judge/references'/name).read_text(encoding='utf-8')
    run=run_fixture(fixture,work/'runtime-copy')
    executed=work/'runtime-copy/executed.ipynb'
    runtime_nb=json.loads(executed.read_text(encoding='utf-8')) if executed.exists() else None
    observations={c['id']:inspect_clause(c['check'],c,nb,tree,files,runtime_nb,run,
                  __import__('hashlib').sha256(data).hexdigest(),rubric)
                  for item in rubric['requirements'] for c in item['clauses']}
    record=apply_observations(draft,observations)
    record['snapshot']['sha256']=file_hash(fixture/'candidate/notebook.ipynb')
    record['runtime_runs']=[run]
    record['loaded_references']=['references/'+n for n in REFERENCES]
    record['access_log']=list(session.events)
    read_paths={e['path'] for e in session.events if e['action']=='READ'}
    record['inputs']=[{'path':p,'role':role,'classification_source':'inputs.json task manifest',
                      'access_phase':'PRE_REFERENCE' if p in read_paths else 'UNOPENED'} for p,role in roles.items()]
    record['inspection_limitations']=['Finite authored-fixture evaluator; not independent LLM evaluation or arbitrary-code sandbox.']
    if exposure is not None:
        if exposure['already_exposed']:
            record['reference_accessed_before_lock']=True;record['flags'].append('REFERENCE_LEAKAGE')
    session.advance()
    validate_record(record)
    locked=session.freeze(record,work/'pre-reference.json')
    (work/'judgment.md').write_text(render(record),encoding='utf-8')
    session.open_reference_phase()
    expected=json.loads(session.read('expected.judgment.json'))
    expected_flags=json.loads(session.read('expected-flags.json'))
    actual={c['clause_id']:c for r in record['requirements'] for c in r['clauses']}
    gold={c['clause_id']:c for r in expected['requirements'] for c in r['clauses']}
    fp=fn=tp=tn=0;mismatches=[]
    for cid,goal in gold.items():
        got=actual[cid]
        if goal['semantic_decision']=='SATISFIED':
            tp += got['semantic_decision']=='SATISFIED';fn += got['semantic_decision']=='UNSATISFIED'
        elif goal['semantic_decision']=='UNSATISFIED':
            tn += got['semantic_decision']=='UNSATISFIED';fp += got['semantic_decision']=='SATISFIED'
        for key in ['evaluability','semantic_decision','earned_points']:
            if got[key]!=goal[key]:mismatches.append(cid+': '+key)
    if set(record['flags'])!=set(expected_flags):mismatches.append('flags')
    if record['scoring']!=expected['scoring']:mismatches.append('scoring')
    summary={'case':fixture.name,'tp':tp,'tn':tn,'fp':fp,'fn':fn,'mismatches':mismatches,
             'earned_points':record['scoring']['earned_points'],'known_earned_points':record['scoring']['known_earned_points'],
             'max_points':record['scoring']['max_points'],'runtime':run['status'],'lock':locked,
             'reference_files_loaded':record['loaded_references'],
             'gated_file_reads':sum(e['action']=='READ' for e in session.events),
             'skill_reference_reads':len(REFERENCES)+1,'agent_tool_calls':None,
             'note':'File-access order is measured; fixture author knew expected cases. No strict-blind LLM accuracy claim.'}
    (work/'comparison.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (work/'post-access-log.json').write_text(json.dumps(session.events,indent=2),encoding='utf-8')
    return record,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',action='append')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    names=args.case or ['notebook_good','notebook_unexecuted_cells','notebook_wrong_dataset','advertising_partial']
    summaries=[]
    for name in names:
        _,summary=evaluate(ROOT/'tests/fixtures'/name,args.output/name)
        summaries.append(summary)
        print(json.dumps({k:summary[k] for k in ['case','runtime','earned_points','known_earned_points','fp','fn','mismatches']}),flush=True)
    (args.output/'summary.json').write_text(json.dumps(summaries,indent=2),encoding='utf-8')
    return int(any(s['mismatches'] for s in summaries))


if __name__=='__main__':raise SystemExit(main())
