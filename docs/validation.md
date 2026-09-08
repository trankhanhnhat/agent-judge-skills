# v9 validation log

Baseline b918d79: 22 package tests passed before editing. Full commands/results for
the final revision are recorded below; no unrun check counts as PASS.

## Final results (2026-09-08)

| Check | Result |
|---|---|
| Full pytest command below | **109 passed, 0 failed, 0 skipped in 36.46s** |
| Skill-creator frontmatter validator | `Skill is valid!` |
| Skills CLI `add . --list` | Exactly one skill: universal-agent-judge |
| Schema / all expected records | All 11 fixtures validated inside the suite |
| All notebook behavioral fixtures | 11 fresh-kernel cases match expected decisions/points/flags |
| Four saved dev audits | 28 TP, 9 TN, 0 FP, 0 FN; one matching NOT_EVALUABLE clause reported separately |
| Reference routing | 19/19 guides directly discoverable; no orphan references |
| Local Markdown links | Validated across repository documents by retained package tests |
| Whitespace diff check | `git diff --check` clean |

The dev-case null is not counted as binary failure. The counts above describe the
authored fixture evaluator, not measured independent LLM accuracy.

Generated Matplotlib SVGs contain trailing spaces in path data. `.gitattributes`
disables whitespace lint only for SVG and preserves fixture/report bytes with
`-text`; candidates are not edited to satisfy lint. This also prevents Git newline
conversion from invalidating SHA-256 on Windows/Linux checkout.

## Commands

On this Windows workspace, the default pytest temp folder belongs to another
execution identity. Use a new test directory inside the repository:

```powershell
New-Item -ItemType Directory -Force .eval-work | Out-Null
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=.eval-work/pytest-final-02 --tb=short
.\.venv\Scripts\python.exe -X utf8 C:/Users/admin/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/universal-agent-judge
npx --yes skills@latest add . --list
```

For other machines, `python -m pip install -r requirements-dev.txt` followed by
`python -m pytest -q` is sufficient if local kernel sockets and temp files work.
The skill-creator validator is an external development tool; it is not required
to install or use this repository.

## Earlier failures and resolution

- Initial runtime-test command failed at setup: 11 errors, `PermissionError:
  [WinError 5]` on `C:/Users/admin/AppData/Local/Temp/pytest-of-admin`. No notebooks
  ran, and this was not counted as a candidate or judge PASS/FAIL.
- The first custom basetemp attempt failed because its parent did not exist:
  11 setup errors, `[WinError 3] ... .eval-work/pytest-runtime-01`.
- Creating the parent and running
  `python -m pytest -q tests/test_dev_evaluation.py -p no:cacheprovider --basetemp=.eval-work/pytest-runtime-02 --tb=short`
  completed: 11 passed in 33.80 seconds, no skips.
- Docker executable was present but its daemon was unavailable. No claim of Docker
  isolation is made; external untrusted candidates remain blocked/static unless
  adequate isolation is supplied. Only authored hash-allowlisted fixtures ran locally.

## What is verified

- Original package tests retained, all local Markdown links and direct reference routes.
- Frontmatter and discoverability; schema itself and all 11 expected judgments.
- Semantic/null/points separation, partial credit, penalties/caps/rounding, preference,
  fixed weights/thresholds, mandatory Absence Proof and evidence provenance.
- Reference input ordering, unknown-role denial, lock tamper detection and separate
  post-reference amendment integrity.
- Eleven actual notebook runs from fresh kernels; original candidates unchanged.
- Four saved developer audits, both Markdown and JSON, including measured FP/FN and
  instrumented file reads: [results](evaluations/README.md).

The finite-fixture evaluator and fixture author are not an independent blind LLM
evaluation. Schema checks do not prove truthfulness of externally supplied evidence.
