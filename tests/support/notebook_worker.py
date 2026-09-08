"""Fresh-kernel worker for reviewed repository fixtures; not an untrusted executor."""
import json
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient


def main():
    work = Path(sys.argv[1]).resolve()
    notebook = nbformat.read(work / "notebook.ipynb", as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    report = {"status": "PASS", "failed_cell": None, "failure_stage": None,
              "stdout": "", "stderr": ""}
    active = None
    def started(cell, cell_index, **kwargs):
        nonlocal active
        if cell.cell_type == "code":
            active = cell_index
    client = NotebookClient(notebook, timeout=20, startup_timeout=30,
                            kernel_name="fixture-python", allow_errors=False,
                            resources={"metadata": {"path": str(work)}},
                            on_cell_start=started)
    try:
        client.execute()
    except Exception as error:
        name = type(error).__name__
        report.update(status="FAIL" if name == "CellExecutionError" else "INCONCLUSIVE",
                      failed_cell=active, failure_stage=name, stderr=str(error))
    finally:
        nbformat.write(notebook, work / "executed.ipynb")
        streams = [(out.get("name"), out.get("text", "")) for cell in notebook.cells
                   for out in cell.get("outputs", []) if out.get("output_type") == "stream"]
        report["stdout"] = "".join(value for name, value in streams if name == "stdout")
        report["stderr"] += "".join(value for name, value in streams if name == "stderr")
        (work / "runtime.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
