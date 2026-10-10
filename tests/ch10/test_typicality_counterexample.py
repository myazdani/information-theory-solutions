import unittest
from information_theory.ch10.typicality_counterexample import run
class Typicality(unittest.TestCase):
    def test_counterexample(self):self.assertTrue(all(run(None)['checks'].values()))
