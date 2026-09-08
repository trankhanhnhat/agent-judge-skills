# TRAJECTORY_MODE

Use for immutable tool-use/web/office/agent traces where actions and observations are
the submitted evidence.

## Minimum identity
- `task_id`
- agent/model/run ID
- immutable trajectory record
- final answer when the task requires one

## Map
Track only decisive steps:
- step/turn;
- tool/surface + arguments/query;
- observation/result;
- relation of observation to final answer;
- observation → next-action dependency;
- errors/retries/loops when relevant.

## Trajectory ledger classes
`DIRECT_OBSERVATION`, `SUPPORTING_OBSERVATION`, `CONTRADICTORY_OBSERVATION`,
`UNSUPPORTED_CLAIM`, `TOOL_ERROR`, `IRRELEVANT_STEP`.

## Judge four separate axes when the rubric covers them
1. `ANSWER_SUPPORT`
2. `EVIDENCE_SUFFICIENCY`
3. `ROUTE_JUSTIFICATION`
4. `EFFICIENCY_SANITY`

Do not call a claim “absolutely factually correct” from trajectory support alone unless a
permitted canonical/reference source has been opened in the proper phase.

If the trace is truncated, record `TRAJECTORY_EVIDENCE_TRUNCATED`. Do not invent missing
observations. If truncation prevents a fair binary decision for a mandatory clause, use
core `NOT_EVALUABLE`; do not convert missing visibility into candidate failure.

## Falsification before SATISFIED
- Does any observed step contradict the final answer?
- Is each required answer clause directly grounded in a visible observation?
- Did an inappropriate route accidentally return a plausible answer?
- Are loops/retries merely efficiency issues, or do they actually break an explicit clause?
