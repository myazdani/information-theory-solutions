import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from information_theory.evidence import run_experiment, sha256


class NumericalEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "src/information_theory/experiments/check.py"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("# Synthetic experiment source used only by this test.\n")
        wrapper = self.root / "src/information_theory/evidence.py"
        wrapper.write_text("# Synthetic wrapper identity used only by this test.\n")
        self.payload = {"results":{"entropy_bits":1.0},"checks":{"fair_bit_entropy":True},"seed":None,"dependencies":[]}
        self.name = "_synthetic_evidence_test"
        self.module = SimpleNamespace(__file__=str(self.source), run=lambda output: self.payload)
        sys.modules[self.name] = self.module
        self.addCleanup(lambda: sys.modules.pop(self.name, None))

    def test_execution_and_hashes(self):
        path = run_experiment(self.root, self.name, "artifacts/test")
        data = json.loads(path.read_text())
        self.assertEqual(data["results"]["entropy_bits"], 1)
        self.assertEqual(data["source_hashes"]["src/information_theory/experiments/check.py"], sha256(self.source))
        self.assertIn("python", data["environment"])
        self.assertIsNone(data["seed"])
        first = path.read_bytes()
        run_experiment(self.root, self.name, "artifacts/test")
        self.assertEqual(path.read_bytes(), first)

    def test_false_checks_stop_publication(self):
        self.payload["checks"]["fair_bit_entropy"] = False
        with self.assertRaisesRegex(ValueError, "all true"):
            run_experiment(self.root, self.name, "artifacts/test")
        self.assertFalse((self.root / "artifacts/test/results.json").exists())

    def test_nonfinite_results_rejected(self):
        self.payload["results"]["entropy_bits"] = float("nan")
        with self.assertRaises(ValueError):
            run_experiment(self.root, self.name, "artifacts/test")

    def test_non_boolean_checks_rejected(self):
        self.payload["checks"]["fair_bit_entropy"] = 1
        with self.assertRaises(ValueError):
            run_experiment(self.root, self.name, "artifacts/test")

    def test_artifact_hash_bound(self):
        artifact = self.root / "artifacts/plot.svg"
        artifact.parent.mkdir()
        artifact.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>\n')
        self.payload["artifacts"] = ["artifacts/plot.svg"]
        data = json.loads(run_experiment(self.root, self.name, "artifacts/test").read_text())
        self.assertEqual(data["artifact_hashes"], {"artifacts/plot.svg":sha256(artifact)})


if __name__ == "__main__":
    unittest.main()
