import unittest
from fractions import Fraction as F
from information_theory.experiments.ch13_coding import interval, common_bits, lz78, decode, run
class Chapter13Checks(unittest.TestCase):
    def test_arithmetic_13_3(self):
        self.assertEqual(interval('10',F(3,4)),(F(1,2),F(5,8)))
        self.assertEqual(common_bits(*interval('1010111',F(3,4)))[:3],'100')
    def test_arithmetic_13_4(self):
        self.assertEqual(interval('01110',F(1,3)),(F(25,54),F(79,162)))
        self.assertEqual(common_bits(*interval('01110',F(1,3))),'0111')
    def test_lz_roundtrip(self):
        for text in ('00000011010100000110101','00000100000011010111','111111111111','0','01'):
            self.assertEqual(decode(lz78(text)[1]),text)
    def test_all_recorded_invariants(self):
        self.assertTrue(all(run(None)['checks'].values()))
