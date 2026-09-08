# Validation

Run `python -m pytest -q` from the repository root after installing
`requirements-dev.txt` in your Python environment.

The full suite includes existing package checks, machine-record invariants and 11
fresh-kernel notebook fixture evaluations. Notebook tests need local kernel sockets.
They never run arbitrary submitted code. Use a writable fresh temporary directory
if your platform account cannot access pytest's default temp location.

For deterministic developer evidence and saved Markdown/JSON reports:

```bash
python tests/support/dev_eval.py --output .eval-work/my-new-run
```

This runs complete, unexecuted-output, wrong-dataset and advertising cases. Use a
new output directory for every invocation: prior locked reports are not overwritten.
`--case notebook_synthetic_standin` selects another fixture. All 11 cases are exercised
by the full pytest suite. No fixture/gold is regenerated as part of these commands.

The fixture author knew the expected cases. The evaluator is a finite AST/observation
harness, not an independent LLM judge. Gold files are opened only after record lock;
this verifies file-access order, not absence of all possible contextual bias.

## Manual cases

Use [regression-cases.md](regression-cases.md) to review verdict boundaries. For each
case, supply its task and candidate to the skill without exposing the Expected
section; record the actual output before comparing with the expected result.
For reference/oracle cases, reveal those values only after the independent lock.

The legacy cases above are text scenarios. Executable inputs are under `fixtures/`:
each case has task/rubric, candidate, expected JSON, expected flags and README.
`support/build_fixtures.py` is an explicit authoring utility; do not run it to fix a
failing evaluation. Review any changed candidate and expected labels separately.
