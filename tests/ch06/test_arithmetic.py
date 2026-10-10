import math
import unittest
from information_theory.ch06.compute import run

class Chapter6Arithmetic(unittest.TestCase):
    def test_all_invariants(self):
        result=run(None)
        self.assertTrue(all(result['checks'].values()))
    def test_finite_and_reproducible(self):
        a=run(None);b=run(None)
        self.assertEqual(a,b)
        self.assertTrue(all(math.isfinite(v) for v in a['results'].values()))
