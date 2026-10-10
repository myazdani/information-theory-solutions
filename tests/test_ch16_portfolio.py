import unittest
from fractions import Fraction as F
from information_theory.experiments.ch16_portfolio import wealth, universality_factor
class Chapter16Checks(unittest.TestCase):
    def test_parabola_identity(self):
        for b in [F(i,40) for i in range(41)]:
            self.assertEqual(wealth(b),1+b/2-b*b/2)
            self.assertLessEqual(wealth(b),F(9,8))
    def test_universality_values(self):
        self.assertEqual([universality_factor(n) for n in [1,2,3]],[F(1,2),F(2,5),F(9,26)])
    def test_rebalancing(self):
        self.assertEqual(F(3,4)*(F(5,9)+2*F(4,9)),F(13,12))
        self.assertEqual(F(3,2)*(F(4,9)+F(5,9)/2),F(13,12))
