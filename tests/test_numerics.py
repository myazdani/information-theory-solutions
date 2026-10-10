import math
import unittest
from information_theory.numerics import (entropy, binary_entropy, relative_entropy,
    marginals, mutual_information, conditional_entropy, channel_joint, huffman_lengths)


class FiniteAlphabetTests(unittest.TestCase):
    def test_entropy_limits(self):
        self.assertEqual(entropy([1, 0]), 0)
        self.assertEqual(binary_entropy(0.5), 1)
        self.assertAlmostEqual(entropy([0.25] * 4), 2)
        self.assertAlmostEqual(entropy([0.5, 0.5], base=math.e), math.log(2))

    def test_invalid_distributions(self):
        for p in ([], [0.3], [-0.1, 1.1], [math.nan, 0], [math.inf, 0]):
            with self.subTest(p=p), self.assertRaises(ValueError):
                entropy(p)
        for base in [0, 1, -2, math.inf]:
            with self.subTest(base=base), self.assertRaises(ValueError):
                entropy([0.5, 0.5], base=base)

    def test_divergence_support_and_values(self):
        self.assertEqual(relative_entropy([1, 0], [0, 1]), math.inf)
        self.assertEqual(relative_entropy([0, 1], [0, 1]), 0)
        self.assertAlmostEqual(relative_entropy([1, 0], [0.5, 0.5]), 1)
        with self.assertRaises(ValueError):
            relative_entropy([1], [0.5, 0.5])

    def test_joint_identities_and_zero_rows(self):
        rows = ((0.0, 0.0), (0.125, 0.375), (0.375, 0.125))
        px, py = marginals(rows)
        self.assertEqual(px, (0, 0.5, 0.5))
        self.assertEqual(py, (0.5, 0.5))
        self.assertAlmostEqual(conditional_entropy(rows), binary_entropy(0.25))
        self.assertAlmostEqual(mutual_information(rows), 1 - binary_entropy(0.25))
        self.assertAlmostEqual(entropy(v for row in rows for v in row), entropy(px) + conditional_entropy(rows))

    def test_independence_and_perfect_channel(self):
        self.assertAlmostEqual(mutual_information([[0.1, 0.15], [0.3, 0.45]]), 0)
        self.assertAlmostEqual(mutual_information(channel_joint([0.25, 0.75], [[1, 0], [0, 1]])), binary_entropy(0.25))
        for rows in ([], [[]], [[0.5], [0.2, 0.3]]):
            with self.assertRaises(ValueError):
                mutual_information(rows)
        with self.assertRaises(ValueError):
            channel_joint([1], [[0.5, 0.4]])

    def test_huffman(self):
        lengths = huffman_lengths([0.5, 0.25, 0.125, 0.125])
        self.assertEqual(lengths, (1, 2, 3, 3))
        self.assertAlmostEqual(sum(2 ** -l for l in lengths), 1)
        self.assertEqual(huffman_lengths([1]), (0,))
        self.assertEqual(huffman_lengths([0.5, 0.5]), (1, 1))


if __name__ == "__main__":
    unittest.main()
