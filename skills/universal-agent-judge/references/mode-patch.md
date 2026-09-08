# PATCH_MODE

Use when the judged object is a candidate patch/diff for an issue or bug report.

## Minimum identity
- `task_id` / issue ID
- issue/problem statement
- base context or base commit when needed
- exact candidate patch/diff

## Map
- changed files and symbols;
- issue clauses → changed hunks;
- changed function → relevant callers/callees;
- tests touched/added;
- nearby unchanged context required to interpret behavior.

Patch size is never correctness evidence.

## Patch-specific evidence order
1. changed code semantics;
2. relevant unchanged context;
3. tests added/updated;
4. visible runtime/test behavior when allowed.

Check whether the patch actually changes the requested behavior, is reachable/integrated,
avoids a clear regression in the affected behavior, handles issue-stated edge cases, and
does not merely hard-code the provided example.

## Falsification before SATISFIED
- Does the changed path execute for the issue scenario?
- Is any explicit issue edge case still unhandled?
- Is there a directly visible regression in related behavior?
- Is the patch example-specific rather than satisfying the general stated clause?

Official resolved/unresolved status and hidden tests are POST_REFERENCE/O1 only.
