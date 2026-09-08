# Universal Agent Judge

An agent skill for grading submitted work against explicit requirements, with
clause-level evidence and a blind boundary before reference answers.

Supports repositories, functions/classes, patches, tool-use traces, ML notebooks,
and final deliverables. Produces `SATISFIED` / `UNSATISFIED`, keeps `NOT_EVALUABLE`
separate, and adds weighted content points only when supplied by the rubric.
Administrative penalties and preference ratings remain separate from semantics.

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
the installer. The skill includes Markdown guides, a JSON Schema and an optional
Python record helper requiring Python 3.10+ and `jsonschema`.

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
  schemas/judgment.schema.json  Canonical audit record
  scripts/judgment.py           Validation, rendering and input-access helper
  requirements.txt             Optional Python helper dependency
```

Read [SKILL.md](skills/universal-agent-judge/SKILL.md) for the workflow and
[the example audit](skills/universal-agent-judge/references/output-example.md) for
the output. The agent loads only the guides needed for the current submission.

## Validate and render judgments

The Markdown skill works without Python. To use the optional record helper, install
its dependency from the repository root:

```bash
python -m pip install -r skills/universal-agent-judge/requirements.txt
python skills/universal-agent-judge/scripts/judgment.py validate audit.json
python skills/universal-agent-judge/scripts/judgment.py render audit.json --detail concise
```

See the [output contract](skills/universal-agent-judge/references/output-contract.md)
for record fields and validation rules. Markdown supports concise, standard and
forensic views with complete JSON included. The helper validates and renders records;
the agent performs the evidence-based grading.
