"""Regenerate honest book coverage and navigation; never invent acceptance."""
import argparse
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from information_theory.coverage import coverage_report, load_json
from information_theory.evidence import write_json


def outputs():
    report = coverage_report(ROOT)
    inventory = load_json(ROOT / "inventory/exercises.json")
    chapters = {c["number"]: c for c in inventory["chapters"]}
    summary = f"**{report['accepted']} / {report['total']} exercises independently accepted; {report['draft']} drafts; {report['pending']} pending.**"
    lines = ["# Elements of Information Theory: worked solutions", "", "Original solutions to Thomas M. Cover and Joy A. Thomas, *Elements of Information Theory*, second edition (Wiley, 2006).", "", summary, "", "This is an in-progress companion. The exercise index distinguishes independently reviewed solutions from drafts and work not yet submitted. A numbered exercise counts as accepted only when every inventoried subpart has been checked and the review still matches the exact solution and numerical evidence. Automated checks verify evidence integrity; they do not certify a proof.", "", "## Browse", "", "- [Exercise-by-exercise index](solutions/README.md)", "- [Source inventory and edition notes](inventory/README.md)", "- [Review and contribution guide](docs/CONTRIBUTING.md)", "- [Reproducibility guide](docs/REPRODUCIBILITY.md)", "- [Machine-readable coverage](coverage/status.json)", "", "| Chapter | Topic | Accepted | Draft | Pending | Total |", "| --- | --- | ---: | ---: | ---: | ---: |"]
    for row in report["chapters"]:
        number = row["chapter"]
        lines.append(f"| {number} | [{chapters[number]['title']}](solutions/README.md#chapter-{number}) | {row['accepted']} | {row['draft']} | {row['pending']} | {row['total']} |")
    lines += ["", "## Reproduce and check", "", "The finite-alphabet library and integrity tests require only Python 3.11 or newer. Numerical experiments list any optional packages they use.", "", "```sh", "PYTHONPATH=src python -m unittest discover -s tests -v", "python scripts/validate.py", "python scripts/build_index.py --check", "```", "", "For an experiment's exact command, dependencies, seed, and input/output hashes, follow its recorded `artifacts/.../results.json`. Solutions include their useful numerical findings, not just code links.", "", "## Reading conventions", "", "All logarithms are base 2 unless stated otherwise. Entropies are measured in bits; differential-entropy units are stated where needed. Each solution identifies its textbook exercise and printed page, states only the scope needed to follow the derivation, and develops an original argument. Fenced `math` blocks and GitHub-compatible inline math are used throughout.", "", "## Scope and rights", "", "The goal is complete coverage of all 378 numbered exercises in Chapters 2–17. Chapter 1 has no numbered exercise section. Full textbook pages, full problem statements, and instructor solutions are not redistributed. Consult a lawful copy of the textbook for the exact questions. This independent project is not affiliated with the authors or publisher. Public availability alone does not grant an additional reuse license.", ""]
    index = ["# Exercise index", "", summary, "", "Accepted means a separate reviewer checked every source subpart and the current files match the recorded hashes. Drafts are available for inspection but have not passed that acceptance gate. Pending entries have no submitted solution.", ""]
    for row in report["chapters"]:
        number = row["chapter"]
        index += [f"## Chapter {number}", "", chapters[number]["title"], "", "| Exercise | Printed page | Status |", "| --- | ---: | --- |"]
        for entry in [e for e in report["exercises"] if e["chapter"] == number]:
            source = next(e for e in inventory["exercises"] if e["id"] == entry["id"])
            identity = entry["id"]
            link = f"[{identity}]({entry['path'].removeprefix('solutions/')})" if entry["path"] else identity
            index.append(f"| {link} | {source.get('printed_page', '—')} | {entry['status']} |")
        index.append("")
    return report, "\n".join(lines), "\n".join(index)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report, readme, index = outputs()
    texts = {ROOT / "README.md": readme, ROOT / "solutions/README.md": index}
    if args.check:
        if load_json(ROOT / "coverage/status.json") != report:
            raise SystemExit("coverage/status.json is stale; run scripts/build_index.py")
        for path, text in texts.items():
            if path.read_text() != text:
                raise SystemExit(f"{path.relative_to(ROOT)} is stale; run scripts/build_index.py")
        print("Coverage and navigation match validated evidence.")
    else:
        write_json(ROOT / "coverage/status.json", report)
        for path, text in texts.items():
            path.write_text(text)
        print(f"Generated index: {report['accepted']}/{report['total']} accepted.")
