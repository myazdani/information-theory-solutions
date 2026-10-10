"""Derive coverage from the source inventory, submissions, and bound reviews.

This validates the review evidence's integrity, not mathematical truth. A review
is an independent reader's explicit attestation and remains fallible.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
from pathlib import Path
from .evidence import safe_path, sha256, write_json

REQUIRED_CHECKS = ("source_alignment", "all_subparts", "derivation", "edge_cases")


def load_json(path: Path):
    return json.loads(path.read_text())


def object_hash(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def inventory_entries(root: Path) -> dict:
    inventory_path = root / "inventory/exercises.json"
    lock = load_json(root / "coverage/source-lock.json")
    if lock.get("inventory_sha256") != sha256(inventory_path):
        raise ValueError("source inventory changed after independent inventory verification")
    inventory = load_json(inventory_path)
    if inventory.get("schema_version") != 1:
        raise ValueError("unsupported inventory schema")
    entries = inventory["exercises"]
    if len(entries) != lock.get("exercise_count"):
        raise ValueError("source inventory count does not match verified lock")
    ids = [e["id"] for e in entries]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate inventory exercise ID")
    for e in entries:
        if e["id"] != f'{e["chapter"]}.{e["number"]}':
            raise ValueError(f"inconsistent inventory identity: {e['id']}")
        if len(e["subparts"]) != len(set(e["subparts"])):
            raise ValueError(f"ambiguous subpart identifiers: {e['id']}")
        if not e.get("source_verified"):
            raise ValueError(f"unverified inventory exercise: {e['id']}")
    for chapter in inventory["chapters"]:
        actual = [e["id"] for e in entries if e["chapter"] == chapter["number"]]
        if set(actual) != set(chapter["exercise_ids"]) or len(actual) != chapter["problem_count"]:
            raise ValueError(f"inconsistent chapter inventory: {chapter['number']}")
    return {e["id"]: e for e in entries}


def submissions(root: Path) -> dict:
    result = {}
    for path in sorted((root / "coverage/submissions").glob("*.json")):
        batch = load_json(path)
        if batch.get("schema_version") != 1:
            raise ValueError(f"unsupported submission schema: {path}")
        for entry in batch["solutions"]:
            if entry["id"] in result:
                raise ValueError(f"duplicate submission: {entry['id']}")
            result[entry["id"]] = entry
    return result


def validate_submission(root: Path, source: dict, entry: dict) -> set[str]:
    if not entry.get("author") or type(entry.get("numerical")) is not bool:
        raise ValueError(f"missing author/numerical declaration: {entry['id']}")
    if sorted(entry["covered_subparts"]) != sorted(source["subparts"]):
        raise ValueError(f"subpart coverage mismatch: {entry['id']}")
    expected_path = f"solutions/ch{source['chapter']:02d}/ex-{source['chapter']}-{source['number']}.md"
    if entry["path"] != expected_path:
        raise ValueError(f"unexpected solution path: {entry['id']}")
    files = {entry["path"], *entry.get("artifacts", [])}
    for relative in files:
        path = safe_path(root, relative)
        if not path.is_file():
            raise ValueError(f"missing declared file: {relative}")
    text = safe_path(root, entry["path"]).read_text()
    if not text.startswith("# ") or "## Solution" not in text:
        raise ValueError(f"solution must have a title and Solution heading: {entry['id']}")
    if source.get("kind") in {"numerical", "mixed"} and not entry["numerical"]:
        raise ValueError(f"source requires numerical evidence: {entry['id']}")
    evidence_files = entry.get("numerical_evidence", [])
    if entry["numerical"] and not evidence_files:
        raise ValueError(f"numerical submission requires run evidence: {entry['id']}")
    for relative in evidence_files:
        evidence = load_json(safe_path(root, relative))
        if evidence.get("schema_version") != 1 or not evidence.get("command") or "results" not in evidence:
            raise ValueError(f"incomplete run evidence: {relative}")
        checks = evidence.get("checks", {})
        if not checks or not all(v is True for v in checks.values()):
            raise ValueError(f"failed or missing numerical checks: {relative}")
        if not evidence.get("environment", {}).get("python") or "seed" not in evidence:
            raise ValueError(f"missing runtime version or seed declaration: {relative}")
        if not evidence.get("source_hashes"):
            raise ValueError(f"missing executed source hashes: {relative}")
        files.add(relative)
        for mapping in ("source_hashes", "artifact_hashes"):
            for path, digest in evidence.get(mapping, {}).items():
                if sha256(safe_path(root, path)) != digest:
                    raise ValueError(f"stale numerical evidence: {path}")
                files.add(path)
        # Forbid JSON nonfinite constants, which Python's default decoder accepts.
        json.dumps(evidence["results"], allow_nan=False)
    return files


def make_review(root: Path, exercise_id: str, reviewer: str, summary: str, checks: dict) -> dict:
    source = inventory_entries(root)[exercise_id]
    entry = submissions(root)[exercise_id]
    files = validate_submission(root, source, entry)
    if reviewer == entry["author"] or not reviewer.strip():
        raise ValueError("reviewer must be identified and different from the solution author")
    required = (REQUIRED_CHECKS
                + (("numerical_reproduction",) if entry["numerical"] else ())
                + (("visual_source_inspection",) if source.get("visual_check_required") else ()))
    if not summary.strip() or not all(checks.get(c) is True for c in required):
        raise ValueError("review requires a summary and explicit successful checks")
    return {"schema_version": 1, "exercise_id": exercise_id, "reviewer": reviewer,
            "verdict": "accepted", "summary": summary, "checks": checks,
            "inventory_sha256": sha256(root / "inventory/exercises.json"),
            "inventory_lock_sha256": sha256(root / "coverage/source-lock.json"),
            "inventory_entry_sha256": object_hash(source), "submission_sha256": object_hash(entry),
            "file_sha256": {p: sha256(safe_path(root, p)) for p in sorted(files)}}


def validate_review(root: Path, source: dict, entry: dict, review: dict) -> None:
    if review.get("schema_version") != 1 or review.get("exercise_id") != entry["id"] or review.get("verdict") != "accepted":
        raise ValueError(f"invalid review record: {entry['id']}")
    expected = make_review(root, entry["id"], review.get("reviewer", ""), review.get("summary", ""), review.get("checks", {}))
    for key in ("inventory_sha256", "inventory_lock_sha256", "inventory_entry_sha256", "submission_sha256", "file_sha256"):
        if review.get(key) != expected[key]:
            raise ValueError(f"stale or incomplete review {key}: {entry['id']}")


def coverage_report(root: Path) -> dict:
    inventory = inventory_entries(root)
    work = submissions(root)
    if set(work) - set(inventory):
        raise ValueError(f"submissions absent from inventory: {set(work) - set(inventory)}")
    rows = []
    for identity, source in inventory.items():
        entry = work.get(identity)
        status = "pending"
        if entry:
            validate_submission(root, source, entry)
            status = "draft"
            review_path = root / "reviews" / f"ex-{identity.replace('.', '-')}.json"
            if review_path.exists():
                validate_review(root, source, entry, load_json(review_path))
                status = "accepted"
        rows.append({"id": identity, "chapter": source["chapter"], "status": status,
                     "path": entry["path"] if entry else None,
                     "subparts": len(source["subparts"]), "numerical": entry["numerical"] if entry else None})
    known_review_names = {f"ex-{i.replace('.', '-')}.json" for i in work}
    orphaned = {p.name for p in (root / "reviews").glob("ex-*.json")} - known_review_names
    if orphaned:
        raise ValueError(f"orphaned reviews: {orphaned}")
    counts = Counter(r["status"] for r in rows)
    chapters = []
    for number in sorted({r["chapter"] for r in rows}):
        selected = [r for r in rows if r["chapter"] == number]
        c = Counter(r["status"] for r in selected)
        chapters.append({"chapter": number, "total": len(selected), **{k:c[k] for k in ("accepted", "draft", "pending")}})
    return {"schema_version":1, "total":len(rows), **{k:counts[k] for k in ("accepted", "draft", "pending")},
            "chapters":chapters, "exercises":rows}
