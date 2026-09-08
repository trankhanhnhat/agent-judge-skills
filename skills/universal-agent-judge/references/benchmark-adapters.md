# Benchmark input/output adapters

Map common benchmark packaging to the universal modes. Core judging logic
must not change by benchmark name.

| Benchmark family | Usual mode | Packaging note |
|---|---|---|
| DevAI / requirement workspace | WORKSPACE or NOTEBOOK_ML | requirement-level verdicts; exact candidate snapshot required |
| Workspace-Bench | WORKSPACE / ARTIFACT | output-directory deliverables may use ARTIFACT as secondary/primary mode |
| WorkSurface / tool-use | TRAJECTORY | judge the submitted trace/final answer, not an invented filesystem |
| SWE-bench | PATCH | issue text is contract; candidate diff is submission |
| HumanEval / MBPP / ClassEval | FUNCTION | natural-language/API spec + candidate body |
| Notebook/ML benchmark | NOTEBOOK_ML | keep implementation/execution/metric/artifact obligations separate |

Keep gold, human labels, and official resolved status unopened until the
PRE_REFERENCE record is locked. See [the shared workflow](../SKILL.md).
