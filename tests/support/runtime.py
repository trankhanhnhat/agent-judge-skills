"""Execute only exact reviewed fixture bytes. Runtime copy is not a security sandbox."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from support.records import file_hash

ROOT = Path(__file__).resolve().parents[2]


def run_fixture(fixture, destination):
    fixture = Path(fixture).resolve()
    approved_root = (ROOT / "tests/fixtures").resolve()
    if fixture.parent != approved_root:
        raise PermissionError("Only repository-owned fixtures can execute")
    catalog = json.loads((approved_root / "trusted-fixtures.json").read_text(encoding="utf-8"))
    candidate = fixture / "candidate"
    paths = list(candidate.rglob("*"))
    if any(p.is_symlink() for p in paths):
        raise PermissionError("Fixture symlinks are forbidden")
    before = {p.relative_to(candidate).as_posix(): file_hash(p) for p in paths if p.is_file()}
    if before != catalog.get(fixture.name):
        raise PermissionError("Unknown or modified fixture bytes; execution refused")
    destination = Path(destination).resolve()
    if destination == candidate or destination.is_relative_to(candidate) or candidate.is_relative_to(destination):
        raise ValueError("Runtime destination must be disjoint from submission")
    shutil.copytree(candidate, destination)  # Fails if destination exists; no overwrite.
    support = destination.parent / (destination.name + "-kernel")
    support.mkdir()
    kernel = support / "kernels/fixture-python"
    kernel.mkdir(parents=True)
    (kernel / "kernel.json").write_text(json.dumps({"argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "Reviewed fixture Python", "language": "python"}), encoding="utf-8")
    # Allowlist platform necessities only, not inherited API keys, credentials or config.
    env = {k: os.environ[k] for k in ("SYSTEMROOT", "WINDIR") if k in os.environ}
    env.update({"PATH": str(Path(sys.executable).parent) + os.pathsep + str(Path(os.environ.get("SYSTEMROOT", "/usr")) / "System32"),
        "HOME": str(support), "USERPROFILE": str(support), "TEMP": str(support), "TMP": str(support),
        "APPDATA": str(support), "LOCALAPPDATA": str(support), "JUPYTER_PATH": str(support),
        "JUPYTER_CONFIG_DIR": str(support), "JUPYTER_RUNTIME_DIR": str(support),
        "IPYTHONDIR": str(support / "ipython"), "MPLCONFIGDIR": str(support / "matplotlib"),
        "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", "MPLBACKEND": "Agg",
        "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"})
    args = [sys.executable, str(Path(__file__).with_name("notebook_worker.py")), str(destination)]
    process = subprocess.Popen(args, cwd=destination, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, encoding="utf-8")
    try:
        stdout, stderr = process.communicate(timeout=90)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            subprocess.run([str(Path(os.environ["SYSTEMROOT"]) / "System32/taskkill.exe"),
                            "/PID", str(process.pid), "/T", "/F"], capture_output=True)
        else:
            import psutil
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
        stdout, stderr = process.communicate(timeout=10)
        result = {"status": "INCONCLUSIVE", "failed_cell": None,
                  "failure_stage": "WholeNotebookTimeout", "stdout": stdout, "stderr": stderr}
    else:
        path = destination / "runtime.json"
        result = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {
            "status": "INCONCLUSIVE", "failed_cell": None, "failure_stage": "WorkerStartup",
            "stdout": stdout, "stderr": stderr}
        result["stderr"] += stderr
    after = {p.relative_to(candidate).as_posix(): file_hash(p) for p in candidate.rglob("*") if p.is_file()}
    if after != before:
        raise RuntimeError("Original fixture changed during runtime")
    writes = [p.relative_to(destination).as_posix() for p in destination.rglob("*")
              if p.is_file() and before.get(p.relative_to(destination).as_posix()) != file_hash(p)]
    runtime_hashes = {p.relative_to(destination).as_posix(): file_hash(p)
                      for p in destination.rglob("*") if p.is_file()}
    delta = [{"path": name, "provenance": "MODIFIED_BY_RUNTIME" if name in before else "JUDGE_RUNTIME",
              "sha256_before": before.get(name), "sha256_after": runtime_hashes[name]} for name in writes]
    record = {"run_id": "clean-1", "level": "E1", "status": result["status"],
        "invocation": "reviewed fixture fresh-kernel worker", "working_directory": "runtime-copy/",
        "isolation": "Hash-allowlisted authored fixture; runtime copy, sanitized environment; no OS sandbox",
        "network_access": "No candidate network operations; localhost kernel transport; OS egress not enforced",
        "resource_limits": "20 seconds/cell, 90 seconds/notebook, one numerical thread; no OS memory/disk cap",
        "cell_timeout_seconds": 20, "total_timeout_seconds": 90,
        "failed_cell": result["failed_cell"], "failure_stage": result["failure_stage"],
        "stdout": result["stdout"], "stderr": result["stderr"],
        "interventions": [], "subprocesses": ["Python worker", "fresh ipykernel"],
        "filesystem_writes": writes, "source_unchanged": True,
        "file_hashes": {"source_before": before, "source_after": after, "runtime_after": runtime_hashes},
        "file_delta": delta,
        "inspection_limitations": ["Reviewed fixture execution only; not safe for arbitrary untrusted submissions."]}
    (destination / "run-record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    (destination / "stdout.txt").write_text(result["stdout"], encoding="utf-8")
    (destination / "stderr.txt").write_text(result["stderr"], encoding="utf-8")
    return record
