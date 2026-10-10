"""Validate source alignment, deterministic evidence, and hash-bound reviews."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from information_theory.coverage import coverage_report

if __name__ == "__main__":
    report = coverage_report(ROOT)
    print(f"{report['accepted']}/{report['total']} accepted; {report['draft']} drafts; {report['pending']} pending")
