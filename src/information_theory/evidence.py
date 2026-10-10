"""Content hashes and deterministic experiment evidence; no proof certification."""
from __future__ import annotations
import hashlib
import importlib
import importlib.metadata
import platform
import json
import math
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def safe_path(root: Path, relative: str) -> Path:
    path = root / relative
    if Path(relative).is_absolute() or ".." in Path(relative).parts or path.is_symlink():
        raise ValueError(f"unsafe repository path: {relative}")
    resolved = path.resolve()
    if root.resolve() not in resolved.parents:
        raise ValueError(f"path is not within repository: {relative}")
    return resolved


def run_experiment(root: Path, module_name: str, output: str) -> Path:
    """Run a module and record result plus hashes of its declared dependencies.

    Module exports run(output_dir), returning {results, checks, source_files}.
    Checks must be a nonempty mapping to booleans. Modules write any figures to
    output_dir, and list their repository-relative paths in optional artifacts.
    All numerical results must be JSON-serializable finite values.
    """
    output_dir = safe_path(root, output)
    output_dir.mkdir(parents=True, exist_ok=True)
    module = importlib.import_module(module_name)
    payload = module.run(output_dir)
    if not isinstance(payload, dict) or "results" not in payload:
        raise ValueError("experiment must return results")
    checks = payload.get("checks", {})
    if not checks or not all(type(v) is bool for v in checks.values()) or not all(checks.values()):
        raise ValueError(f"experiment checks must be nonempty and all true: {checks}")
    source_files = payload.get("source_files", [])
    module_file = Path(module.__file__).resolve().relative_to(root.resolve()).as_posix()
    source_files = sorted(set([module_file, "src/information_theory/evidence.py"] + source_files))
    source_hashes = {p: sha256(safe_path(root, p)) for p in source_files}
    artifacts = sorted(set(payload.get("artifacts", [])))
    artifact_hashes = {p: sha256(safe_path(root, p)) for p in artifacts}
    dependencies = {name: importlib.metadata.version(name) for name in payload.get("dependencies", [])}
    record = {"schema_version": 1, "module": module_name,
              "environment": {"python": platform.python_version(), "packages": dependencies},
              "seed": payload.get("seed"),
              "command": f"PYTHONPATH=src python -m information_theory run {module_name} --output {output}",
              "source_hashes": source_hashes, "artifact_hashes": artifact_hashes,
              "results": payload["results"], "checks": checks}
    path = output_dir / "results.json"
    write_json(path, record)
    return path
