import unittest
from information_theory.ch11.third_batch import run
class ThirdBatch(unittest.TestCase):
    def test_count_and_seeded_moment_checks(self):self.assertTrue(all(run(None)['checks'].values()))
