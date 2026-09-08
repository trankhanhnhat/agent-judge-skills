"""Package validation; this does not measure an LLM's grading accuracy."""

from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "universal-agent-judge"
DOCUMENTS = sorted(p for p in ROOT.rglob("*.md") if not any(
    part.startswith(".") or part == "node_modules" for part in p.relative_to(ROOT).parts
))


def test_skill_is_discoverable():
    candidates = sorted((ROOT / "skills").glob("*/SKILL.md"))
    assert candidates == [SKILL / "SKILL.md"]
    text = candidates[0].read_text(encoding="utf-8")
    assert text.startswith("---\n")
    metadata = yaml.safe_load(text.split("---", 2)[1])
    assert metadata["name"] == SKILL.name
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata["name"])
    assert len(metadata["name"]) <= 64
    assert isinstance(metadata["description"], str)
    assert 0 < len(metadata["description"]) <= 1024
    assert isinstance(metadata["metadata"]["version"], str)


@pytest.mark.parametrize("document", DOCUMENTS, ids=lambda p: str(p.relative_to(ROOT)))
def test_local_markdown_links_resolve(document):
    text = document.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        destination = (document.parent / unquote(parsed.path)).resolve()
        assert destination.is_relative_to(ROOT), (document, target)
        assert destination.exists(), (document, target)


def test_all_reference_guides_are_discoverable():
    entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    linked = {
        (SKILL / target).resolve()
        for target in re.findall(r"\[[^\]]*\]\((references/[^)]+\.md)\)", entry)
    }
    assert linked == {p.resolve() for p in (SKILL / "references").glob("*.md")}


def test_six_submission_adapters_are_packaged():
    actual = {p.stem for p in (SKILL / "references").glob("mode-*.md")}
    assert actual == {
        "mode-workspace", "mode-function", "mode-patch", "mode-trajectory",
        "mode-notebook-ml", "mode-artifact",
    }
