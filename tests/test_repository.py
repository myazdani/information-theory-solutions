"""Repository-wide regressions: coverage integrity and GitHub math syntax."""
from pathlib import Path
import re
import unittest
from information_theory.coverage import coverage_report

ROOT = Path(__file__).resolve().parents[1]


class RepositoryChecks(unittest.TestCase):
    @unittest.skipUnless((ROOT / "inventory/exercises.json").exists(), "inventory preparation is still in progress")
    def test_coverage_integrity(self):
        report = coverage_report(ROOT)
        self.assertEqual(report["total"], report["accepted"] + report["draft"] + report["pending"])

    def test_github_math_delimiters(self):
        for path in sorted((ROOT / "solutions").glob("ch*/ex-*.md")):
            text = path.read_text()
            with self.subTest(path=path.name):
                self.assertNotRegex(text, r"\\[\[\]\(\)]", "use fenced math / GitHub dollar-backtick inline math")
                self.assertNotIn("$$", text, "use fenced math display blocks")
                self.assertNotIn(r"\operatorname", text, "GitHub rejects this macro; use mathrm for named operators")
                self.assertEqual(sum(line.startswith("```") for line in text.splitlines()) % 2, 0, "unbalanced fenced blocks")
                for block in re.findall(r"```math\n(.*?)```", text, re.S):
                    self.assertNotIn("<", block, "use \\lt with a separating space to avoid HTML truncation")
                for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
                    if "://" in link or link.startswith("#") or link.startswith("mailto:"):
                        continue
                    target = link.split("#", 1)[0]
                    self.assertTrue((path.parent / target).exists(), f"broken relative link: {target}")


if __name__ == "__main__":
    unittest.main()
