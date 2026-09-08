# NOTEBOOK_ML_MODE

Use when correctness depends on an ML/notebook experiment rather than code syntax alone.

## Minimum identity
- `task_id`
- notebook/code snapshot
- data/config identity when required
- submitted metrics/plots/checkpoints/report when present

## Map the experiment graph
- data load/preprocessing;
- split/validation logic;
- model definition;
- train/eval calls;
- metrics;
- plots/checkpoints/results;
- report references;
- seeds/config/environment only when explicit or needed for provenance.

## Keep obligations separate
Do not collapse these into one proof:
1. implementation exists;
2. experiment actually ran;
3. a metric was produced;
4. the metric follows the required evaluation protocol;
5. required artifacts/report were submitted.

## ML-specific checks
Apply only when relevant to the locked rubric:
- dataset identity: use [dataset provenance](dataset-provenance.md);
- train/validation/test separation and leakage;
- split method/seed;
- preprocessing fit only on permitted training data;
- requested model/loss/optimizer/config;
- reachable training loop;
- correct metric/CV folds;
- submitted metric/plot/checkpoint/report;
- synthetic/placeholder shortcuts.

Notebook output cells are not automatically current evidence. If outputs cannot be mapped
to the current code/data, record `STALE_NOTEBOOK_OUTPUT` and lower their evidence value.

## Falsification before SATISFIED
- Is the reported metric traceable to the current code/data/config?
- Does an explicit held-out/CV clause suffer leakage?
- Is a named dataset proven by identity rather than filename?
- If a saved artifact is required, was the submitted artifact itself inspected via [mode artifact](mode-artifact.md)?
