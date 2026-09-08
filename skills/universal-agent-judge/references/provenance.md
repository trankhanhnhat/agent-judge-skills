# Runtime and artifact provenance

Distinguish what the developer submitted from what execution or the judge
created/modified.

## Provenance categories
- `SUBMITTED`: present in the candidate snapshot before judge execution.
- `JUDGE_RUNTIME`: newly created by judge-triggered execution.
- `MODIFIED_BY_RUNTIME`: submitted file whose contents/state changed during execution.
- `EXTERNAL_ENVIRONMENT`: dependency/cache/system/resource not part of the submission.

Before runtime, snapshot/hash relevant files when practical. After runtime, diff the
relevant paths and tag provenance.

Before candidate execution, hash original inputs and copy only allowed files into
the isolated run root. Hash the originals again afterward. A changed file in the
runtime copy is `MODIFIED_BY_RUNTIME`; the original must remain unchanged. Runtime
records include before/after hashes, paths, writes, and containment limitations.

A `JUDGE_RUNTIME` artifact may prove reproducibility or capability, but never proves the
file was originally submitted.

## Environment intervention log
Record any:
- dependency installation;
- interpreter/runtime substitution;
- headless/display backend change;
- credential/network limitation or injected environment support.

Related flags: `RUNTIME_INTERVENTION`, `ENVIRONMENT_BLOCKED`,
`RUNTIME_PARTIAL_SUCCESS`, `NONDETERMINISTIC_RUNTIME`.
