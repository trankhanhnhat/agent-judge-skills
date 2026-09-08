# ARTIFACT_MODE

Use when a final PDF/document/slide/image/table/export is itself the judged deliverable.
This adapter may also be loaded as a secondary adapter from other modes.

## Minimum identity
- `task_id`
- exact submitted artifact or locked expected path/type
- artifact path/name/type
- producer source only when traceability is itself relevant

## Map the artifact first
Inspect in this order:
1. exact submitted artifact existence and readability;
2. semantic content: required sections/pages/sheets/slides/tables/plots/metrics/text;
3. internal consistency;
4. locked path/type/format constraints;
5. producer/source relationship only if the requirement asks for generation behavior or provenance;
6. README claims last.

## Artifact-specific rules
- Source Markdown does not substitute for a required PDF.
- Plotting/export code does not substitute for a missing required output file.
- A judge-generated artifact is runtime provenance, not retroactive submission evidence.
- If a valid submitted artifact satisfies a pure deliverable clause but current producer
  code points elsewhere, keep the deliverable verdict based on the artifact and record
  `PRODUCER_CODE_MISMATCH`; fail producer behavior only if it is an explicit clause.

## Falsification before SATISFIED
- Does the artifact satisfy locked `EXACT`/`DIRECTORY`/`ILLUSTRATIVE` semantics?
- Is it non-empty/readable and semantically contains each required element?
- Is producer code being mistaken for the required submitted file?
- Is a producer mismatch actually part of the contract, or merely a diagnostic concern?
