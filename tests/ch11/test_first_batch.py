import unittest
from information_theory.ch11.first_batch import run
class FirstBatch(unittest.TestCase):
    def test_checks(self):self.assertTrue(all(run(None)['checks'].values()))
