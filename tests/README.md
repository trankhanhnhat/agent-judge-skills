# Validation

Run `python -m pytest -q` from the repository root after installing
`requirements-dev.txt` in your Python environment.

The automated suite checks metadata, relative documentation links, and discovery
of the packaged references. It deliberately does not infer grading quality from
the presence of a particular phrase in the instructions.

## Manual cases

Use [regression-cases.md](regression-cases.md) to review verdict boundaries. For each
case, supply its task and candidate to the skill without exposing the Expected
section; record the actual output before comparing with the expected result.
For reference/oracle cases, reveal those values only after the independent lock.

The cases are text scenarios, not complete executable fixtures. No automated agent
runner or current behavioral pass rate is provided. Extend them with real artifacts
before making measured accuracy claims.
