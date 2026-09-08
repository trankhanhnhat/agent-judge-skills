# Rubric scoring

Authority for points, allocation, rounding, caps, preferences, and penalties.
Lock scoring policy before candidate semantics; never relax thresholds after results.

## Mode and allocation

- No weights: `BINARY_ONLY`; numeric content totals are `null`. Report met/total,
  not invented equal weights or percentages.
- Weights supplied: `WEIGHTED`; preserve parent maxima and partial-credit policy.
  Cite the exact rubric scoring source.
- Parent points without clause weights: use parent all-or-nothing unless the task
  authorizes derived allocation. If needed, disclose allocation before grading,
  rationale and each weight, with `JUDGE_DERIVED_ALLOCATION`; do not pretend it was
  rubric text. A single aggregate scored clause can represent all-or-nothing points.
- Inconsistent supplied weights: `RUBRIC_WEIGHT_MISMATCH`; preserve binary findings,
  leave affected points unresolved, and ask for clarification. Do not normalize
  silently or publish an invalid clause allocation as a valid score.

## Arithmetic and unresolved points

Use decimal arithmetic. Clause maxima sum exactly to parent maximum; count scored
items only once. Earned points are in [0, maximum]. Fractional credit needs explicit
rubric/disclosed allocation support in `score_reason`. Partial credit cannot turn
an `UNSATISFIED` mandatory clause/requirement into `SATISFIED`.

Report content earned/max, known earned subtotal, unresolved maximum, administrative
penalties, and final points separately. Ungradable clauses have `earned_points: null`;
the complete content total stays null if any points are unresolved. Do not reduce
the denominator. Benchmark-forced zero export (`BENCHMARK_ZERO`) needs an exact
policy source and never rewrites semantic nulls.

When unstated, disclose these defaults: no content/penalty cap, nonnegative final
points, round only the final/display total to 2 decimals using `ROUND_HALF_UP`.
Preserve clause precision. Explicit rubric precision/caps override defaults.

```text
content = sum(earned clauses), or null if unresolved
bounded_content = min(content, content_cap) if supplied
deduction = min(sum(penalties), penalty_cap) if supplied
final = round(max(0, bounded_content - deduction), configured precision)
```

Penalty entries require rule, points and evidence. Do not double-penalize a content
failure administratively unless explicitly required. Confidence and flags are never
score multipliers, deductions, or sources of extra points.

## Preference criteria

Only rate rubric-requested dimensions/scales. Record criterion, scale, rating,
evidence and policy source in `preference_scores`. If explicitly weighted as content,
link `content_clause_id` to its scored clause; never add the separate rating twice.
Unrequested personal preference cannot create failure.

## Weighted notebook example

Parent 10 points: EDA 2, Pipeline 2, Lasso search 2, polynomial/Ridge 2, submitted
Run All 1, residual plots 1. Correct EDA/Pipeline plus correct degree/bias but wrong
estimator (1/2 under explicit partial credit), no search and missing submitted
outputs earn 5/10; semantic verdict remains `UNSATISFIED`. If the rubric explicitly
assigns a late penalty of 1, content stays 5/10 and final is 4/10.
