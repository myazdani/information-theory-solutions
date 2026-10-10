import json
from pathlib import Path
import tempfile
import unittest
from information_theory.coverage import coverage_report, make_review, validate_submission
from information_theory.evidence import write_json, safe_path, sha256


class ReviewIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = {"id":"2.1","chapter":2,"number":1,"subparts":["a","b"],"source_verified":True,"kind":"proof"}
        write_json(self.root / "inventory/exercises.json", {"schema_version":1,"chapters":[{"number":2,"problem_count":1,"exercise_ids":["2.1"]}],"exercises":[self.source]})
        write_json(self.root / "coverage/source-lock.json", {"inventory_sha256": sha256(self.root / "inventory/exercises.json"), "exercise_count":1})
        self.entry = {"id":"2.1","path":"solutions/ch02/ex-2-1.md","author":"author-A","covered_subparts":["a","b"],"artifacts":[],"numerical":False}
        path = self.root / self.entry["path"]
        path.parent.mkdir(parents=True)
        path.write_text("# Exercise 2.1\n\n## Solution\n\nIndependent derivation.\n")
        write_json(self.root / "coverage/submissions/ch02.json", {"schema_version":1,"solutions":[self.entry]})
        self.checks = {k: True for k in ["source_alignment", "all_subparts", "derivation", "edge_cases"]}

    def accept(self):
        r = make_review(self.root, "2.1", "reviewer-B", "Verified all cases against the source.", self.checks)
        write_json(self.root / "reviews/ex-2-1.json", r)

    def test_draft_is_not_accepted(self):
        self.assertEqual(coverage_report(self.root)["accepted"], 0)
        self.assertEqual(coverage_report(self.root)["draft"], 1)
        self.accept()
        self.assertEqual(coverage_report(self.root)["accepted"], 1)

    def test_self_review_rejected(self):
        with self.assertRaises(ValueError):
            make_review(self.root, "2.1", "author-A", "Checked.", self.checks)

    def test_any_solution_mutation_invalidates_acceptance(self):
        self.accept()
        with (self.root / self.entry["path"]).open("a") as f:
            f.write("New unreviewed sentence.\n")
        with self.assertRaisesRegex(ValueError, "stale or incomplete"):
            coverage_report(self.root)

    def test_changed_scope_invalidates_acceptance(self):
        self.accept()
        data = json.loads((self.root / "inventory/exercises.json").read_text())
        data["exercises"][0]["printed_page"] = 24
        write_json(self.root / "inventory/exercises.json", data)
        with self.assertRaisesRegex(ValueError, "source inventory changed"):
            coverage_report(self.root)

    def test_visual_inspection_required_when_flagged(self):
        path = self.root / "inventory/exercises.json"
        data = json.loads(path.read_text())
        data["exercises"][0]["visual_check_required"] = True
        write_json(path, data)
        write_json(self.root / "coverage/source-lock.json", {"inventory_sha256":sha256(path),"exercise_count":1})
        with self.assertRaisesRegex(ValueError, "explicit successful checks"):
            self.accept()
        self.checks["visual_source_inspection"] = True
        self.accept()
        self.assertEqual(coverage_report(self.root)["accepted"], 1)

    def test_missing_subpart_rejected(self):
        self.entry["covered_subparts"] = ["a"]
        with self.assertRaisesRegex(ValueError, "subpart coverage"):
            validate_submission(self.root, self.source, self.entry)

    def test_numerical_claim_requires_evidence(self):
        self.entry["numerical"] = True
        with self.assertRaisesRegex(ValueError, "run evidence"):
            validate_submission(self.root, self.source, self.entry)

    def test_unchecked_review_rejected(self):
        self.checks["edge_cases"] = False
        with self.assertRaises(ValueError):
            make_review(self.root, "2.1", "reviewer-B", "Partial check.", self.checks)

    def test_path_traversal_rejected(self):
        for name in ("../private-source.pdf", "/etc/passwd", "x/../../private.txt"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                safe_path(self.root, name)


if __name__ == "__main__":
    unittest.main()
