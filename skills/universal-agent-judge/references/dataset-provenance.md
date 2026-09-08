# Dataset identity and use

Authority for named-source decisions. Check only contract-required version/split/
subset constraints or those needed to trace evidence; a generic loader has no
invented named-dataset requirement.

| Strength | Examples | Sufficiency |
|---|---|---|
| IDENTITY_DIRECT | Trusted manifest/hash matches actual loaded bytes; verified source/version/content | Sufficient when linked to required actual use |
| IDENTITY_CORROBORATING | Characteristic schema/content, loader URL/config, independent metadata | Supports identity; self-asserted metadata alone is insufficient |
| CLAIM_ONLY | Filename, variable, folder, README | Insufficient alone |

Trace identity -> version -> split -> subset -> transformations -> loader config
-> actual train/eval use -> metric/artifact. An unused correct download cannot prove
actual use. A candidate's own hash proves consistency, not authenticity, unless
matched against a trusted source.

## Outcomes

- `SATISFIED`: direct identity or independently corroborated provenance/content
  resolves identity, with actual use and all explicit constraints supported.
- `UNSATISFIED`: decisive wrong source/version/subset/use or unallowed synthetic
  substitution. Also fail a separate explicit provenance-document submission clause
  when absence-proved missing.
- `NOT_EVALUABLE`: names/claims only, inaccessible evidence, or unresolved identity
  without contradiction. Lack of proof is not automatically proof of wrong data.
- `WEAK_DATASET_PROVENANCE`: mainly weak claimed identity; diagnostic only.
- `SYNTHETIC_STANDIN`: observed generation replacing a required source without
  permission; cite the code/content, not the flag, as failure evidence. Permitted
  synthetic data does not trigger it.

The right dataset with contaminated evaluation may pass identity and fail protocol
independently.
