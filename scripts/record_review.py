"""Record an independently completed review, binding current content hashes.

Only the reviewer should run this after reading source, checking every subpart,
and reproducing numerical experiments. This command does not perform a review.
"""
import argparse
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from information_theory.coverage import make_review, load_json
from information_theory.evidence import write_json

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("exercise_id")
    p.add_argument("--reviewer", required=True)
    p.add_argument("--assessment", type=Path, required=True, help="JSON with summary and explicit checks")
    args = p.parse_args()
    assessment = load_json(args.assessment)
    review = make_review(ROOT, args.exercise_id, args.reviewer, assessment["summary"], assessment["checks"])
    path = ROOT / "reviews" / f"ex-{args.exercise_id.replace('.', '-')}.json"
    if path.exists():
        raise SystemExit("Review exists; inspect it and deliberately replace it only after a fresh review.")
    write_json(path, review)
    print(path)
