# FUNCTION_MODE

Use for function/class-level tasks such as HumanEval/MBPP/ClassEval-style candidates.

## Minimum identity
- `task_id`
- exact natural-language/API contract
- candidate code text
- target function/class/entrypoint

## Map
Usually inspect only:
- target signature and body;
- imported or local helpers actually used;
- edge-case branches;
- stated exceptions/side effects;
- visible tests/examples only when protocol permits them.

Do not invent a repository when the candidate is only a snippet.

## Clause checks
Match the locked contract against:
- signature/parameters;
- input domain;
- return value/type/shape;
- boundary conditions;
- ordering/stability and words such as `first`, `all`, `at most`, `exactly`;
- documented exceptions;
- mutation/side effects;
- complexity only when explicit.

## Static falsification before SATISFIED
Actively try: empty/singleton inputs, duplicates, zero/negative values, boundary indices,
tie/order cases, invalid inputs covered by the contract, missing exception branches,
accidental mutation, type mismatch, and silent default returns.

Passing visible examples cannot outweigh a code path that violates another
explicit clause.

## Oracle
Official/hidden tests are O1 and must follow [runtime verification](runtime-verification.md); never import a
hidden edge case or exact hidden exception type into the locked contract.
