# Output contract

[judgment.schema.json](../schemas/judgment.schema.json) owns field names, shapes,
enums and nullability. Shared workflow owns semantics; scoring guide owns arithmetic.
Do not maintain a second schema in examples or adapters.

Record parent rubric, exact clauses, mandatory status, decisions/points, confidence,
flags, evidence IDs, failure kind, absence proof and limitations. Use `null` for
unknown/inapplicable values, not guessed numbers. Cite re-openable evidence locations
and actual provenance.

From the installed skill folder (requires `jsonschema`):

```bash
python scripts/judgment.py validate audit.json
python scripts/judgment.py render audit.json --detail standard
```

The [helper](../scripts/judgment.py) validates sums and evidence references beyond JSON Schema, renders the
record and offers `InputSession` for ordered access/immutable locking. It never
executes candidate code and is not a semantic grading engine.

| Detail | View |
|---|---|
| concise | Decisions, points, decisive evidence, unresolved items |
| standard | Plus clauses, failures, penalties, runtime and limitations |
| forensic | Plus expanded complete record |
| json | Canonical JSON only |

Every Markdown view includes full canonical JSON in a details block (visible for
forensic), so it round-trips without information loss. No decision/score exists only
in prose. Localize explanatory text if useful, but preserve machine enums.

Post-reference records keep the original requirements, link its immutable hash/path,
and put amendments in `post_reference_audit`. Agreement uses locked decisions.
Use `validate ... --predecessor pre-reference.json` to verify the actual predecessor
hash and frozen fields; a structurally valid hash string alone is not proof of a lock.

Install the optional helper dependency from the skill folder with
`python -m pip install -r requirements.txt`; see [requirements.txt](../requirements.txt).
