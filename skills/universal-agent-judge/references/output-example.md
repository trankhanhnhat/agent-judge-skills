# Output examples

Illustrative views only. [Output contract](output-contract.md) owns representation;
[rubric scoring](rubric-scoring.md) owns arithmetic. Real Markdown reports include
the full JSON record, with `phase`, `snapshot`, `requirements` and other schema fields.

## Concise binary-only view

Task: submit monthly CSV at exact `results/monthly.csv` and at least two plots under
`results/plots/`. Inspection finds the CSV and only one plot after absence search.

| requirement_id | evaluability | semantic_decision | Evidence |
|---|---|---|---|
| CSV | EVALUABLE | SATISFIED | Submitted results/monthly.csv has monthly rows |
| plots | EVALUABLE | UNSATISFIED | Exact folder, variants, producer and whole submission search find only one plot |

Met 1/2; content points null (no rubric weights); task NOT_SOLVED. Code for a second
plot is not the submitted plot. If the folder cannot be inspected, report an access
limitation and an ungradable clause instead of an absence conclusion.

## Weighted notebook view

Rubric provides these exact weights and partial credit by atomic clause. Candidate
has EDA and Pipeline, no GridSearchCV, PolynomialFeatures(2, include_bias=False) but
LinearRegression instead of Ridge, and final two cells without required saved output.

| Parent | Atomic outcome | earned_points / max_points |
|---|---|---|
| EDA | SATISFIED | 2/2 |
| Pipeline | SATISFIED | 2/2 |
| Lasso search | UNSATISFIED: GridSearchCV absence-proved | 0/2 |
| Polynomial/Ridge | degree SAT 0.5; bias SAT 0.5; Ridge UNSAT 0 | 1/2 |
| Submitted Run All evidence | UNSATISFIED: required output absent | 0/1 |
| Residual plots | UNSATISFIED: submitted files absent | 0/1 |

Content 5/10, penalties empty, final 5/10. Polynomial/Ridge remains UNSATISFIED
despite partial credit. Fresh-kernel runtime may PASS while required submitted
outputs remain absent. EDA/Pipeline decisions do not inherit model failure.

## Unresolved points

If one 1-point clause cannot be inspected and the other nine earn 7 points,
`earned_points: null`, `known_earned_points: 7`, `unresolved_max_points: 1`,
`max_points: 10`, `final_points: null`. Do not silently report 7/10 as a complete
score or 7/9 by dropping the unresolved clause. Only an explicit benchmark export
policy can coerce unknown points, without changing the semantic null.
