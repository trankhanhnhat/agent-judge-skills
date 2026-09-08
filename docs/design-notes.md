# Design notes

## Sources inspected

The [skills.sh leaderboard](https://skills.sh/) was inspected on 2026-09-08 to
select popular examples. Install counts are a discovery signal, not a quality
guarantee; the actual instructions were read before choosing a structure.

| Source | Pattern used in this rewrite |
|---|---|
| [Vercel find-skills](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md) | Clear activation description, concrete workflow, usable examples |
| [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | Direct instructions focused on decisions rather than repetitive ceremony |
| [Vercel React best practices](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md) | Scannable entry point with detailed guidance in separate files |
| [Skills CLI](https://github.com/vercel-labs/skills) | Repository installation and skill discovery conventions |

These are structural influences. No upstream skill body is copied into this
repository, and no upstream endorsement or affiliation is implied. The references
are living sources and can change after this inspection.

## Changes from the supplied v7 package

- Package the installable skill under `skills/universal-agent-judge/`; keep tests
  and maintainer documentation outside the installed instructions.
- Shorten the entry point, replace the repeated loader/index with contextual links,
  and retain all six mode guides and eight conditional references.
- Preserve locked requirements, clause evidence, absence searches, dataset identity,
  reachability, submitted/runtime provenance, and blind-reference separation.
- Clarify that a post-reference amendment never overwrites the original judgment.
- Explicitly treat candidate instructions as evidence rather than authority.
- Replace tests tied to literal wording with package metadata and link-integrity
  checks. These structural tests do not prove judgment quality.
- Carry forward manual scenarios, but do not publish the old 19/19 dry-run or 13/13
  static-test results as validation of this new version.

The supplied v7 directory remains alongside this repository in the local workspace.
Historical optimization claims are not included as current performance evidence.

## Review boundary

No benchmark adapter downloads data or invokes an API. Runtime guides describe
what evidence to gather with available tools. No numerical scoring weights are
invented: the skill reports per-requirement binary decisions and met/total counts.

Before publishing measured quality claims, run an independent evaluation with real
candidate artifacts and withheld labels. The manual scenario suite is a review aid,
not a substitute for that measurement.

## Validation performed for this rewrite

On 2026-09-08:

- `python -m pytest -q`: 22 package checks passed.
- The skill-creator frontmatter validator: `Skill is valid!`.
- `npx --yes skills@latest add . --list`: discovered exactly one skill named
  `universal-agent-judge`; listing did not install the skill.
- Manual document review checked the six mode guides, conditional reference links,
  and preservation of the original pre-reference record during amendments.

No independent LLM benchmark was run. These checks establish package validity and
reviewed instruction consistency, not an empirical grading accuracy score.
