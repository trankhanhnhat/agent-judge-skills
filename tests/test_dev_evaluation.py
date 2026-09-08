from pathlib import Path
import json

import pytest

from support.dev_eval import evaluate
from support.records import file_hash

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("fixture", sorted((ROOT/"tests/fixtures").glob("*/candidate")), ids=lambda p:p.parent.name)
def test_reviewed_notebook_behavior(fixture,tmp_path):
    before={p.name:file_hash(p) for p in fixture.iterdir() if p.is_file()}
    record,result=evaluate(fixture.parent,tmp_path/fixture.parent.name)
    assert not result["mismatches"], result
    assert result["fp"]==result["fn"]==0
    assert record["runtime_runs"][0]["source_unchanged"] is True
    assert before=={p.name:file_hash(p) for p in fixture.iterdir() if p.is_file()}
    events=json.loads((tmp_path/fixture.parent.name/"post-access-log.json").read_text())
    gold_reads=[e for e in events if e["role"]=="GOLD_LABEL" and e["action"]=="READ"]
    assert gold_reads and all(e["state"]=="OPTIONAL_REFERENCE_ACCESS" for e in gold_reads)
