# NOTEBOOK_ML_MODE

Identify task, notebook/code snapshot, required data/config, and submitted outputs.
Trace loader -> preprocessing -> split -> model -> train -> evaluate -> artifacts.

## Eight separate obligations

Apply only obligations the rubric requires; do not impose all eight on code-only work.

| Obligation | Evidence |
|---|---|
| Implementation exists | Reachable source with required semantics |
| Cell ran | Submitted output/run record attributable to that cell |
| Clean Run All succeeds | Fresh kernel, unchanged runtime-copy source, document order |
| Output saved | Output entries/files in submitted snapshot |
| Output matches current code | Source/data/config traceability and clean-run comparison |
| Metric produced | Observed value tied to a concrete run |
| Metric protocol correct | Actual eval data/split/transforms and metric definition |
| Artifact submitted | Direct inspection via [artifact mode](mode-artifact.md) |

For execution/order/freshness use [notebook execution](notebook-execution.md).
For named data use [dataset provenance](dataset-provenance.md). For points use
[rubric scoring](rubric-scoring.md); notebook warning counts are not scores.

## ML checks and falsification

- Trace version, subset, actual train/eval rows, split method and seed as required.
- Detect forbidden leakage: preprocessing fit on full/test data, overlap, or wrong
  validation protocol. A correct metric formula cannot rescue contaminated inputs.
- Verify requested model/config, search/CV, loss/optimizer and reachable fit calls.
- Inspect actual metric/plot/checkpoint outputs; captions and model names are claims.
- Check synthetic substitution, placeholders, contradictory claims and stale metrics.
- Keep EDA/Pipeline decisions independent of a downstream wrong model.
- Ask whether clean execution needs deleted state, current outputs match source,
  and judge-created files are being mistaken for submitted artifacts.
