import math
import unittest

from information_theory.ch12_markov import (
    binary_entropy, cycle_grid, elementary_cycles, flow_statistics,
    lumped_flow, match_information, separated_flow, symmetric_flow,
    total_variation, two_step_flow,
)


class MarkovEntropyTests(unittest.TestCase):
    def test_cycles_are_stationary(self):
        self.assertEqual(len(elementary_cycles()), 8)
        for q in elementary_cycles():
            self.assertAlmostEqual(sum(map(sum, q)), 1)
            for i in range(3):
                self.assertAlmostEqual(sum(q[i]), sum(row[i] for row in q))

    def test_grid_size(self):
        self.assertEqual(sum(1 for _ in cycle_grid(3)), math.comb(10, 7))

    def test_endpoints_and_absent_states(self):
        self.assertAlmostEqual(flow_statistics(symmetric_flow(0))[0], math.log2(3))
        self.assertAlmostEqual(flow_statistics(symmetric_flow(0))[1], 0)
        self.assertAlmostEqual(flow_statistics(symmetric_flow(1))[0], 0)
        self.assertAlmostEqual(flow_statistics(symmetric_flow(1))[1], math.log2(3))
        self.assertEqual(flow_statistics(separated_flow(1, 0)), (0, 0))
        h, a = flow_statistics(separated_flow(0, 0))
        self.assertAlmostEqual(h, 1)
        self.assertAlmostEqual(a, 0)

    def test_special_equality(self):
        h, a = flow_statistics(lumped_flow(1 / 3, 1))
        self.assertAlmostEqual(h, 2 / 3)
        self.assertAlmostEqual(a, binary_entropy(1 / 3))
        self.assertAlmostEqual(h + a, math.log2(3))

    def test_lumped_squaring(self):
        for p in (0.2, 1 / 3, 0.7):
            for t in (0.2, 0.7, 1):
                self.assertLess(total_variation(two_step_flow(lumped_flow(p, t)), lumped_flow(p, t * t)), 1e-14)

    def test_symmetric_not_optimal(self):
        a = 0.001
        symmetric = match_information(symmetric_flow, a)
        rank_one = match_information(lambda t: lumped_flow(1 / 3, t), a)
        self.assertGreater(rank_one['entropy_rate'], symmetric['entropy_rate'])
        self.assertAlmostEqual(rank_one['lag_two_information'], a, places=12)


if __name__ == '__main__':
    unittest.main()
