import unittest
from information_theory.ch07.second_batch import run
class SecondBatch(unittest.TestCase):
    def test_checks(self):self.assertTrue(all(run(None)['checks'].values()))
    def test_reproducible(self):self.assertEqual(run(None),run(None))
