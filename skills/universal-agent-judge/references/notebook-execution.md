# Notebook execution and freshness

Use for historical execution, clean reproducibility, saved output or freshness.
[Safe execution](safe-candidate-execution.md) is a prerequisite;
[provenance](provenance.md) owns origin labels.

## Clean-run protocol

1. Parse and validate without executing. Inventory cell IDs/source, outputs/errors,
   execution counts, kernel, dependencies and submitted artifact paths. Hash notebook
   and relevant inputs.
2. Check kernel/dependencies. Record substitutions/installations as interventions;
   do not silently fix the environment. Retain static findings if safe execution is
   unavailable.
3. Make an allowlisted runtime copy; clear its outputs/counts, start a fresh kernel,
   execute every nonempty code cell in document order and save the executed copy.
   Do not edit/reorder source, suppress errors, skip failures or overwrite submission.
4. Set per-cell and whole-notebook timeouts before running. Capture stdout/stderr,
   cell index/ID, exception, failure stage and interventions. Save partial output on
   failure and terminate kernel/process tree on timeout.
5. Compare submitted/runtime outputs by cell ID/source hash and actual data/config.
   Ignore only irrelevant timestamps/counts; disclose numerical tolerance from the
   task or comparison policy. Do not dismiss semantic divergence as nondeterminism
   without evidence. Check metrics and required plots, not only exit status.
6. Rehash original to prove no modification. Record file delta: new outputs are
   `JUDGE_RUNTIME`, changed originals in the copy `MODIFIED_BY_RUNTIME`. New clean
   outputs do not prove an output was originally submitted.

## Signals, not shortcuts

| Signal | Interpretation |
|---|---|
| Null count | Supporting only; inspect outputs and run record |
| Duplicate/out-of-order counts | Possible re-execution, not proof of hidden state |
| Required print/plot output absent | Saved-output clause may fail after absence proof; historical execution can remain unknown |
| Fresh-kernel undefined variable | Hidden state if data/environment availability is established |
| Attributable saved output differs from clean result | Runtime divergence; assess staleness from source/data traceability |
| Error removed without run evidence | Completion unproven; do not invent deletion history |
| Caption/claim without output | Claim-only; trace producer and submitted files |

Never use `execution_count` alone to conclude freshness/staleness. Use
`NOTEBOOK_NOT_RUN_ALL` for proven incomplete/failed submitted Run All or missing
explicit required run evidence. Fresh success proves capability, not prior execution.
