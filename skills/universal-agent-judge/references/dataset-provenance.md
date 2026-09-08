# Named dataset provenance

Establish whether a specifically named dataset/source in the locked
contract is actually the data used by the candidate.

## Strong identity evidence
One or more of the following, preferably corroborating:
- source/download/API metadata tied to the named dataset;
- loader configuration resolving to that source;
- schema/content/domain fields characteristic of the dataset;
- dataset manifest/version/hash or trusted metadata;
- notebook/code references plus actual configured path/content.

## Weak evidence
A filename, variable name, README claim, or folder name alone is not dataset identity.
Use `WEAK_DATASET_PROVENANCE` when identity is inferred mainly from such claims.

## Synthetic stand-ins
If a mandatory clause requires a named real dataset and the candidate instead uses
synthetic/generated stand-in data without permission, record `SYNTHETIC_STANDIN` and
fail that explicit dataset clause.

If the rubric only asks for a generic CSV/input loader, do not invent a named-dataset
provenance requirement.
