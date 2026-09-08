# Judge/reference disagreement audit

Explain why a locked PRE_REFERENCE verdict differs from the reference.
Never rewrite the locked verdict retroactively.

For each mismatch inspect:
- locked wording and atomic clauses;
- decisive candidate evidence;
- any clause added/omitted by either side;
- static vs runtime conflict;
- oracle hidden-detail mismatch;
- environment failure;
- possible reference error.

Useful error categories:
`LOCATE_ERROR`, `READ_ERROR`, `MISSING_EVIDENCE`, `INCORRECT_REASONING`,
`TOO_LENIENT`, `TOO_STRICT`, `AMBIGUOUS_RUBRIC`, `ARTIFACT_NOT_CHECKED`,
`RUNTIME_NOT_CHECKED`, `ORACLE_DETAIL_OVERFIT`, `POSSIBLE_REFERENCE_ERROR`.

Record the finding in the POST_REFERENCE audit column; preserve the immutable locked
judge field for honest agreement measurement.
