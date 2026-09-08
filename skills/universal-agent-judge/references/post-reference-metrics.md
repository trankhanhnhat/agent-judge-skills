# Post-reference metrics

Aggregate locked binary judgments after reference access.

Match by stable requirement/sample ID.

Binary mapping:
- TP: judge `SATISFIED`, reference positive
- TN: judge `UNSATISFIED`, reference negative
- FP: judge `SATISFIED`, reference negative
- FN: judge `UNSATISFIED`, reference positive

Report at minimum:
- matches / compared;
- agreement/accuracy;
- positive precision/recall/F1;
- negative precision/recall/F1 when sample support is sufficient;
- macro-F1;
- confusion matrix;
- `NOT_EVALUABLE` count separately;
- `REFERENCE_LEAKAGE` exclusions separately for strict-blind metrics.

Agreement with another LLM judge is not “absolute accuracy”. If the reference is an
executable oracle, call the result oracle/test agreement or correctness agreement as
appropriate.
