"""Chapter-specific numerical regression checks."""
import importlib
from pathlib import Path
import tempfile
import unittest

class NumericalEvidence(unittest.TestCase):
    modules = ['ch04_batch01', 'ch04_batch02', 'ch04_batch03']

    def test_all_recorded_invariants(self):
        for name in self.modules:
            with self.subTest(module=name), tempfile.TemporaryDirectory() as directory:
                result=importlib.import_module('information_theory.'+name).run(Path(directory))
                self.assertTrue(result['checks'])
                self.assertTrue(all(v is True for v in result['checks'].values()),result['checks'])

    def test_deterministic_results(self):
        for name in self.modules:
            with self.subTest(module=name), tempfile.TemporaryDirectory() as directory:
                module=importlib.import_module('information_theory.'+name)
                first=module.run(Path(directory))
                second=module.run(Path(directory))
                self.assertEqual(first['results'],second['results'])
                self.assertEqual(first['checks'],second['checks'])

if __name__=='__main__':unittest.main()
