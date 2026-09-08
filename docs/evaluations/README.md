# Developer evaluation results

These are measured executions of finite authored fixtures, not independent LLM
accuracy estimates. Expected files were opened only after immutable JSON lock.
The fixture author knew the intended cases; no strict-blind LLM claim is made.

Command:

```bash
python tests/support/dev_eval.py --output .eval-work/dev-eval-final
```

Fresh kernels, 20 seconds/cell, 90 seconds/notebook; source hashes unchanged.
No OS-level network/memory/disk isolation: only reviewed hash-allowlisted fixtures
were executed, with no inherited secrets. Semantic stdout comparisons are exact
at the precision printed by the candidate (RMSE rounded to eight decimal places);
stderr remains diagnostic evidence. An authoring-time font-cache warning in the
good submitted notebook is retained, not erased or treated as stale semantic output.

| Case | Runtime | Content | Known / unresolved max | TP | TN | FP | FN | Mismatches |
|---|---|---|---|---|---|---|---|---|
| [notebook_good](notebook_good/judgment.md) | PASS | 10.0/10.0 | 10.0 / 0.0 | 10 | 0 | 0 | 0 | 0 |
| [notebook_unexecuted_cells](notebook_unexecuted_cells/judgment.md) | PASS | unresolved / 10.0 | 5.0 / 1.0 | 5 | 4 | 0 | 0 | 0 |
| [notebook_wrong_dataset](notebook_wrong_dataset/judgment.md) | PASS | 9.0/10.0 | 9.0 / 0.0 | 9 | 1 | 0 | 0 | 0 |
| [advertising_partial](advertising_partial/judgment.md) | PASS | 5.0/10.0 | 5.0 / 0.0 | 4 | 4 | 0 | 0 | 0 |

The unexecuted-output case earns 5 known points, fails four submitted-evidence
clauses, and has one unresolved freshness point; its complete score stays null.
Clean-run PASS does not retroactively satisfy saved-output requirements.

The advertising case keeps EDA and Pipeline satisfied. Missing GridSearchCV, wrong
Ridge estimator and missing submitted execution/plots fail independently; correct
polynomial degree and bias earn 1/2, giving transparent content 5/10.

Each case directory includes the lossless [Markdown/JSON format](../../skills/universal-agent-judge/references/output-contract.md),
comparison counts, post-lock access log, executed notebook and stdout/stderr.
`comparison.json` records the exact reference guide list, gated file-read count,
and reference-read count. Agent tool-call count is null because the harness does
not measure model/tool telemetry. Counts describe only instrumented reads.

Runtime versions are recorded in [environment.json](environment.json). Full-suite
commands and final counts are documented in [validation](../validation.md).
