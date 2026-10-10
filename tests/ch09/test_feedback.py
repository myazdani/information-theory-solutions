import unittest
from information_theory.ch09.feedback import run, optimize
class Feedback(unittest.TestCase):
    def test_covariance_and_optimization(self):self.assertTrue(all(run(None)['checks'].values()))

    def test_singular_rejected(self):
        with self.assertRaises(ValueError):optimize(1,1)
    def test_zero_power(self):self.assertEqual(optimize(0,.5)["feedback_information"],0)
