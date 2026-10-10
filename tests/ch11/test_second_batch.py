import unittest
from information_theory.ch11.second_batch import run
class SecondBatch(unittest.TestCase):
    def test_checks(self):self.assertTrue(all(run(None)['checks'].values()))
