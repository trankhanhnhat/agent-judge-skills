# WORKSPACE_MODE

Use when the judged object is a repository/project/app/package filesystem snapshot.

## Minimum identity
- `task_id`
- `submission_id`
- `workspace_root`
- `snapshot_id` / commit / tree hash when available

## Map
Map only enough to locate relevant evidence:
- directory tree around likely entrypoints;
- source/notebook/config/data files tied to the criterion;
- tests relevant to the clause;
- submitted artifacts/metrics/plots/reports/checkpoints/logs;
- import/call relations when reachability matters;
- producer → artifact relation only when required.

## Workspace-specific checks

### Integrated implementation
Static code may be sufficient when semantics are direct. If the criterion requires an
integrated feature, verify the relevant path is reachable from the actual entrypoint;
an isolated unused helper cannot establish integrated behavior.

### Named dataset
If the criterion names a specific dataset, load [dataset provenance](dataset-provenance.md). Do not infer
identity from filename alone.

### Saved/final deliverable
Load [mode artifact](mode-artifact.md) as a secondary adapter. Inspect the submitted artifact before
producer source whenever the deliverable itself is the clause.

## Falsification before SATISFIED
- Is the relevant implementation reachable from the real entrypoint when integration is required?
- For named data, is identity directly evidenced rather than guessed from a filename?
- For saved output, was the actual submitted file inspected and validated?
- Is any README/comment/docstring being used as sole proof? If yes, it is `CLAIM_ONLY`.
