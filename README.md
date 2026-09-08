# Universal Agent Judge

An agent skill for grading submitted work against explicit requirements, with
clause-level evidence and a blind boundary before reference answers.

Supports repositories, functions/classes, patches, tool-use traces, ML notebooks,
and final deliverables. Produces `SATISFIED` / `UNSATISFIED` decisions and reports
`NOT_EVALUABLE` separately when the evidence cannot support a fair judgment.

## Install

From GitHub:

```bash
npx skills add Nhatdangdihoc/agent-judge-skills --skill universal-agent-judge
```

From a local checkout:

```bash
npx skills add . --skill universal-agent-judge
```

The [Skills CLI](https://github.com/vercel-labs/skills) also accepts GitHub repository
URLs with the same `--skill universal-agent-judge` option. Node.js/npm is needed for
the installer; the skill itself consists of Markdown instructions.

## Use

Give your agent the task/rubric and the exact candidate snapshot or artifact:

```text
Use universal-agent-judge to grade ./submission against ./rubric.md.
Report each requirement with decisive evidence. Do not repair the submission.
Keep ./gold.json unopened until the independent judgment is locked.
```

Vietnamese example:

```text
Dùng universal-agent-judge chấm bài trong ./submission theo ./rubric.md.
Chỉ rõ từng yêu cầu đạt/chưa đạt và bằng chứng. Không sửa bài.
Chấm độc lập trước, sau đó mới mở ./gold.json để đối chiếu.
```

If your tool exposes all input files at once, keep reference answers out of the
initial context. Mentioning a denylist cannot undo an answer already revealed.

## What it checks

| Submission | Main checks |
|---|---|
| Workspace | Requirement evidence and reachable integrated behavior |
| Function / class | API contract, return semantics, boundaries, side effects |
| Patch | Issue behavior, active call paths, affected regressions |
| Tool trace | Observed evidence supporting the final answer |
| Notebook / ML | Dataset identity, experiment execution, evaluation, saved results |
| Artifact | Actual submitted file, required content, format, and path |

For example, if the task requires a submitted PDF, an export script alone does not
satisfy it. If the task only requires an error, a hidden test demanding one unstated
exception type cannot silently become part of the rubric.

## Repository layout

```text
skills/universal-agent-judge/
  SKILL.md                     Entry point and shared judging rules
  references/                  Six mode guides and conditional procedures
tests/                         Package checks and manual regression cases
docs/                          Design sources and migration notes
```

Read [SKILL.md](skills/universal-agent-judge/SKILL.md) for the workflow and
[the example audit](skills/universal-agent-judge/references/output-example.md) for
the output. The agent loads only the guides needed for the current submission.

## Validation

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Package tests validate metadata and resource links. Manual judgment cases live in
[tests/regression-cases.md](tests/regression-cases.md); they are not automated LLM
evaluations. This repository provides instructions, not a grading server or an
executable benchmark runner. It makes no measured accuracy claim.

## Design

The v8 rewrite follows the concise entry points and conditional detail seen in
popular skills from Vercel and Anthropic. The judging policy comes from the supplied
Universal Agent Judge v7. See [design notes](docs/design-notes.md) for source links,
the packaging changes, and validation limits.
