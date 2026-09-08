# v9 source patterns

Inspected 2026-09-08. Original judging content was rewritten for this repository;
no external skill body was copied.

| Source | Idea retained | Not adopted |
|---|---|---|
| [GitHub agentic-eval](https://github.com/github/awesome-copilot/blob/main/skills/agentic-eval/SKILL.md) | Explicit dimensions and structured records | Candidate refinement/evaluator-optimizer loop |
| [Google agents-cli eval](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-eval/SKILL.md) | Evaluation fixtures, recorded results, unchanged thresholds | Agent-fixing loops and service-specific dependencies |
| [ECC mle-workflow](https://github.com/affaan-m/ecc/blob/main/skills/mle-workflow/SKILL.md) | Trace data, experiment and artifact lineage; scope ML checks to task | Deployment/monitoring requirements absent from rubric |
| [Writing plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) | Concrete files and verifiable steps | Turning a judge run into an implementation task |

The requested sd0xdev test-review page and guessed source location could not be
retrieved during this session; no unverified content from that skill was incorporated.

Implementation API references: [nbclient execution](https://nbclient.readthedocs.io/en/latest/client.html)
for fresh-kernel execution, per-cell timeout and partial outputs;
[JSON Schema validation vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation)
for shape/nullability constraints. Arithmetic and reference equality are checked in
Python because schema validation alone cannot establish them.
