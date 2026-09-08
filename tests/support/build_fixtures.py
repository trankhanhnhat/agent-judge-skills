"""Author deterministic fixture inputs and gold once; never run during dev grading.

This executes only the source literals below to author saved notebook outputs.
Changes to authored candidates require a deliberate regeneration and review.
"""
from contextlib import redirect_stdout, redirect_stderr
from copy import deepcopy
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/universal-agent-judge/scripts"))
sys.path.insert(0, str(ROOT / "tests"))
from support.records import skeleton, apply_observations, file_hash
from judgment import validate_record

DATA = "x,y\n0,1\n1,3\n2,5\n3,7\n4,9\n5,11\n"
WRONG = "x,y\n0,10\n1,11\n2,12\n3,13\n4,14\n5,15\n"
CELLS = [
'''import csv, json
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge, LinearRegression, Lasso
from sklearn.metrics import root_mean_squared_error
print("imports ready")''',
'''rows = list(csv.DictReader(Path("tiny.csv").open()))
X = [[float(r["x"])] for r in rows]
y = [float(r["y"]) for r in rows]
X_train, X_test = X[:4], X[4:]
y_train, y_test = y[:4], y[4:]
print("dataset rows", len(rows))''',
'''print("EDA", {"rows": len(rows), "x_min": min(r[0] for r in X), "x_max": max(r[0] for r in X)})''',
'''model = Pipeline([("scale", StandardScaler()), ("reg", Ridge(alpha=1.0))])
model.fit(X_train, y_train)
print("MODEL", type(model.named_steps["reg"]).__name__)''',
'''prediction = model.predict(X_test)
rmse = float(root_mean_squared_error(y_test, prediction))
print("RMSE", round(rmse, 8))''',
'''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.scatter(prediction, [a-b for a,b in zip(y_test, prediction)])
plt.axhline(0)
plt.savefig("residual.svg")
plt.close()
print("PLOT residual.svg")''']

CHECKS = [
("implementation", "Implement a reachable fit and predict workflow.", 1),
("submitted_run", "Submit completed output for every nonempty code cell as Run All evidence.", 1),
("clean_run", "Notebook must run from a fresh kernel in document order.", 1),
("saved_outputs", "Save all nonempty code-cell outputs in the submitted notebook.", 1),
("fresh_outputs", "Saved semantic outputs must match current code and supplied data.", 1),
("metric", "Submit the RMSE produced by the evaluation cell.", 1),
("protocol", "Fit preprocessing only on first four training rows; evaluate untouched last two rows.", 1),
("artifact", "Submit residual.svg containing the residual scatter plot.", 1),
("dataset", "Train/evaluate using the supplied JudgeTiny v1 CSV bytes identified by trusted SHA-256.", 1),
("model", "Use sklearn Ridge(alpha=1.0) in the model Pipeline.", 1)]


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")


def requirement(cid, text, points):
    return {"id": cid, "text": text, "points": points,
            "clauses": [{"id": cid+".1", "text": text, "points": points, "check": cid}]}


def author_notebook(sources, data, hidden=False):
    cells=[]
    with tempfile.TemporaryDirectory() as temporary:
        temp=Path(temporary)
        (temp/'tiny.csv').write_text(data,encoding='utf-8',newline='')
        previous=Path.cwd()
        namespace={"hidden_offset": 0} if hidden else {}
        try:
            os.chdir(temp)
            for i, source in enumerate(sources):
                stdout,stderr=io.StringIO(),io.StringIO()
                with redirect_stdout(stdout),redirect_stderr(stderr):
                    exec(compile(source, f'authored-cell-{i}', 'exec'), namespace)
                outputs=[]
                for name,value in [('stdout',stdout.getvalue()),('stderr',stderr.getvalue())]:
                    if value:outputs.append({'output_type':'stream','name':name,'text':value})
                cells.append({'id':f'cell-{i}','cell_type':'code','source':source,'metadata':{},'execution_count':i+1,'outputs':outputs})
            artifacts={p.name:p.read_bytes() for p in temp.glob('*.svg')}
        finally:
            os.chdir(previous)
    return {'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'}},'cells':cells},artifacts


def main():
    fixtures=ROOT/'tests/fixtures';fixtures.mkdir(exist_ok=True)
    names=['notebook_good','notebook_unexecuted_cells','notebook_stale_outputs',
           'notebook_hidden_state','notebook_data_leakage','notebook_wrong_dataset',
           'notebook_synthetic_standin','notebook_wrong_model_config',
           'reference_leakage','missing_required_artifact','advertising_partial']
    catalog={}
    for name in names:
        root=fixtures/name
        candidate=root/'candidate';candidate.mkdir(parents=True,exist_ok=True)
        sources=deepcopy(CELLS);data=DATA
        if name=='notebook_hidden_state':sources[4]=sources[4].replace('model.predict(X_test)','model.predict(X_test) + hidden_offset')
        if name=='notebook_data_leakage':
            sources[3]='leaky = StandardScaler()\nleaky.fit(X)\nX_train, X_test = leaky.transform(X)[:4], leaky.transform(X)[4:]\n'+sources[3]
        if name=='notebook_wrong_dataset':data=WRONG
        if name=='notebook_synthetic_standin':sources[1]=sources[1].replace('rows = list(csv.DictReader(Path("tiny.csv").open()))','rows = [{"x": i, "y": i+10} for i in range(6)] # generated stand-in')
        if name=='notebook_wrong_model_config':sources[3]=sources[3].replace('Ridge(alpha=1.0)','Ridge(alpha=9.0)')
        if name=='advertising_partial':
            sources[3]='model = Pipeline([("poly", PolynomialFeatures(degree=2, include_bias=False)), ("reg", LinearRegression())])\nmodel.fit(X_train, y_train)\nlasso = Lasso(alpha=0.1)\nlasso.fit(X_train, y_train)\nprint("MODEL", type(model.named_steps["reg"]).__name__)'
            sources[5]+='\nplt.scatter(y_test, prediction)\nplt.savefig("residual2.svg")\nplt.close()\nprint("PLOT residual2.svg")'
        nb,artifacts=author_notebook(sources,data,name=='notebook_hidden_state')
        if name in {'notebook_unexecuted_cells','advertising_partial'}:
            for cell in nb['cells'][-2:]:cell.update(execution_count=None,outputs=[])
            artifacts={}
        if name=='notebook_stale_outputs':nb['cells'][4]['outputs'][0]['text']='RMSE 999.0\n'
        if name=='missing_required_artifact':artifacts={}
        (candidate/'tiny.csv').write_text(data,encoding='utf-8',newline='')
        dump(candidate/'notebook.ipynb',nb)
        for filename,content in artifacts.items():(candidate/filename).write_bytes(content)
        reqs=[requirement(*c) for c in CHECKS]
        if name=='advertising_partial':
            reqs=[requirement('eda','Submit EDA summary output.',2),requirement('pipeline','Implement sklearn Pipeline.',2),
                  requirement('search','Use GridSearchCV for Lasso.',2),
                  {'id':'polynomial','text':'PolynomialFeatures degree=2, include_bias=False, Ridge(alpha=1.0).','points':2,
                   'clauses':[{'id':'degree.1','text':'Use PolynomialFeatures degree=2.','points':0.5,'check':'degree'},
                              {'id':'bias.1','text':'Use include_bias=False.','points':0.5,'check':'bias'},
                              {'id':'model.1','text':'Use Ridge(alpha=1.0).','points':1,'check':'model'}]},
                  requirement('submitted_run','Submit completed outputs for Run All, including final two cells.',1),
                  requirement('artifact','Submit both residual.svg and residual2.svg residual plots.',1)]
        rubric={'task_id':name,'dataset':{'name':'JudgeTiny','version':'1','sha256':hashlib.sha256(DATA.encode()).hexdigest()},
                'requirements':reqs,'scoring_policy':'Explicit clause weights; binary clause credit; parent partial credit by clause sum; no penalties; round final HALF_UP to two decimals.'}
        dump(root/'rubric.json',rubric)
        (root/'task.md').write_text('Grade candidate/notebook.ipynb and submitted files using rubric.json. JudgeTiny is an intentionally tiny local dataset; use its exact supplied bytes. Do not open expected files before lock.\n',encoding='utf-8')
        roles={'task.md':'TASK_SOURCE','rubric.json':'RUBRIC','expected.judgment.json':'GOLD_LABEL','expected-flags.json':'GOLD_LABEL','README.md':'CONTEXT_ONLY'}
        if name=='reference_leakage':roles['exposure.json']='CONTEXT_ONLY'
        for file in candidate.iterdir():roles['candidate/'+file.name]='CANDIDATE'
        dump(root/'inputs.json',roles)
        record=skeleton(rubric,file_hash(candidate/'notebook.ipynb'))
        observations={}
        for req in reqs:
            for clause in req['clauses']:
                observations[clause['id']]={'decision':'SATISFIED','description':'Expected direct evidence for '+clause['text'],'location':'candidate/notebook.ipynb','provenance':'JUDGE_RUNTIME' if clause['check']=='clean_run' else 'SUBMITTED'}
        def fail(key,flags=(),absence=False):
            observations[key+'.1'].update(decision='UNSATISFIED',flags=list(flags),failure_kind='ABSENCE' if absence else 'CONTRADICTION')
            if absence:observations[key+'.1']['checks']=['Inspect exact required cell/output/path','Inventory submitted candidate files and output arrays; inspect producer references']
        if name=='notebook_unexecuted_cells':
            for key in ['submitted_run','saved_outputs','metric','artifact']:fail(key,['NOTEBOOK_NOT_RUN_ALL'] if key=='submitted_run' else ['MISSING_ARTIFACT'] if key=='artifact' else [],True)
            observations['fresh_outputs.1'].update(decision=None,description='Required submitted outputs absent; freshness cannot be compared.')
        if name=='notebook_stale_outputs':fail('fresh_outputs',['SUBMITTED_RUNTIME_DIVERGENCE','STALE_NOTEBOOK_OUTPUT'])
        if name=='notebook_hidden_state':
            fail('clean_run',['HIDDEN_STATE_DEPENDENCY'])
            observations['fresh_outputs.1'].update(decision=None,description='Clean execution fails before all outputs; freshness unresolved.')
        if name=='notebook_data_leakage':fail('protocol',['DATA_LEAKAGE_RISK'])
        if name=='notebook_wrong_dataset':fail('dataset')
        if name=='notebook_synthetic_standin':fail('dataset',['SYNTHETIC_STANDIN'])
        if name=='notebook_wrong_model_config':fail('model',['MODEL_CONFIG_MISMATCH'])
        if name=='missing_required_artifact':fail('artifact',['MISSING_ARTIFACT'],True)
        if name=='advertising_partial':
            fail('search',[],True);fail('model',['MODEL_CONFIG_MISMATCH']);fail('submitted_run',['NOTEBOOK_NOT_RUN_ALL'],True);fail('artifact',['MISSING_ARTIFACT'],True)
        record=apply_observations(record,observations)
        if name=='reference_leakage':
            record['reference_accessed_before_lock']=True;record['flags'].append('REFERENCE_LEAKAGE')
            dump(root/'exposure.json',{'already_exposed':True,'description':'Protocol declares that a prior gold value was already shown to the judge.'})
        validate_record(record)
        dump(root/'expected.judgment.json',record);dump(root/'expected-flags.json',record['flags'])
        (root/'README.md').write_text('# '+name+'\n\nTask and rubric are judge inputs; candidate contains the minimal submission.\nExpected JSON/flags are withheld gold. This fixture tests '+name.replace('_',' ')+'.\nSource/output authoring is deliberate; do not regenerate while evaluating.\n',encoding='utf-8')
        catalog[name]={str(p.relative_to(candidate)).replace('\\','/'):file_hash(p) for p in candidate.iterdir()}
    dump(fixtures/'trusted-fixtures.json',catalog)
    print('Authored',len(names),'fixtures and expected records')


if __name__=='__main__':main()
