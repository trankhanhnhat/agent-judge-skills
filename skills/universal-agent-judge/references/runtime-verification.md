# Runtime verification ladder

Choose the execution check that resolves the uncertain clause, then classify any
oracle failure. Track file origins using [provenance](provenance.md).

Before every level that executes code (including imports), apply
[safe execution](safe-candidate-execution.md). Work in an isolated runtime copy.
For notebook clean runs use [notebook execution](notebook-execution.md).

## E0 — Non-invasive preflight
Syntax/import/discovery checks. Useful for viability; not end-to-end proof.

## E1 — As-shipped end-to-end
Run the documented/default entrypoint in the runtime copy without patching source/config.
Record cwd, command, environment, exit code, decisive stdout/stderr, failure stage, and
artifact delta. E1 is the strongest evidence for explicit end-to-end behavior.

## E2 — Component invocation
Invoke a reusable submitted component with valid existing input without modifying source.
E2 pass does not erase a relevant E1 failure.

## E3 — Repository-provided tests
Useful developer-facing evidence; never assume the suite is complete for the rubric.

## O1 — Official benchmark/oracle tests
Run only after the immutable PRE_REFERENCE lock.

Classify each failure:
1. `EXPLICIT_REQUIREMENT_VIOLATION`
2. `UNDERSPECIFIED_ORACLE_DETAIL`
3. `ENVIRONMENT_FAILURE`
4. `INCONCLUSIVE`

Only class 1 can justify a separately recorded POST_REFERENCE semantic amendment,
because it maps directly to a locked clause. Never overwrite the PRE_REFERENCE
decision. Classes 2–4 are recorded separately without changing the semantic decision.

## Selection guide
| Need | Level |
|---|---|
| parse/import viability only | E0 |
| explicit end-to-end behavior | E1 |
| isolated function/component behavior | E2 |
| candidate-provided test suite | E3 |
| official hidden benchmark behavior | O1 after PRE_REFERENCE lock |

Environment intervention used only to diagnose must be logged; never present an
intervened run as pure as-shipped behavior.
