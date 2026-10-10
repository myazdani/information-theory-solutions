import unittest
from information_theory.experiments.ch14_counts import equal_area_count, ratio_count, run
class Chapter14Checks(unittest.TestCase):
    def test_exact_parameterization(self):
        for n in range(1,20): self.assertEqual(equal_area_count(n),ratio_count(n))
    def test_recorded_checks(self): self.assertTrue(all(run(None)['checks'].values()))
