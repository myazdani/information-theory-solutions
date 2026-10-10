import unittest
from information_theory.ch08.compute import run as quantization
from information_theory.ch08.uniform_capacity import run as uniform_capacity
class Chapter8Numerics(unittest.TestCase):
    def test_quantization(self):self.assertTrue(all(quantization(None)['checks'].values()))
    def test_uniform_capacity(self):self.assertTrue(all(uniform_capacity(None)['checks'].values()))
