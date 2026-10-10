"""Finite, globally convergent characterization for Exercise 12.11.

Floating-point functions here validate constructions. They do not implement
outward-rounded interval arithmetic and must not be called certified bounds.
"""
from __future__ import annotations

from itertools import combinations
from math import fsum, log2

Matrix = tuple[tuple[float, ...], ...]


def entropy(probabilities):
    return -fsum(x * log2(x) for x in probabilities if x > 0)


def binary_entropy(p):
    return entropy((p, 1 - p))


def elementary_cycles() -> tuple[Matrix, ...]:
    cycles = []
    for i in range(3):
        q = [[0.0] * 3 for _ in range(3)]
        q[i][i] = 1.0
        cycles.append(tuple(map(tuple, q)))
    for i, j in combinations(range(3), 2):
        q = [[0.0] * 3 for _ in range(3)]
        q[i][j] = q[j][i] = 0.5
        cycles.append(tuple(map(tuple, q)))
    for order in ((0, 1, 2), (0, 2, 1)):
        q = [[0.0] * 3 for _ in range(3)]
        for i, j in zip(order, order[1:] + order[:1]):
            q[i][j] = 1 / 3
        cycles.append(tuple(map(tuple, q)))
    return tuple(cycles)


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, parts - 1):
                yield (first,) + rest


def cycle_mixture(weights):
    cycles = elementary_cycles()
    return tuple(tuple(fsum(weights[k] * cycles[k][i][j] for k in range(8))
                       for j in range(3)) for i in range(3))


def cycle_grid(n):
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    for counts in compositions(n, 8):
        yield cycle_mixture(tuple(m / n for m in counts))


def quantize_weights(weights, n):
    """Largest-remainder quantization; every coordinate changes by <= 1/n."""
    counts = [int(n * w) for w in weights]
    remainder = n - sum(counts)
    order = sorted(range(len(weights)), key=lambda i: n * weights[i] - counts[i], reverse=True)
    for i in order[:remainder]:
        counts[i] += 1
    return tuple(m / n for m in counts)


def marginal(q):
    return tuple(fsum(row) for row in q)


def two_step_flow(q):
    pi = marginal(q)
    return tuple(tuple(fsum(q[i][k] * q[k][j] / pi[k]
                                  for k in range(3) if pi[k] > 0)
                       for j in range(3)) for i in range(3))


def flow_statistics(q):
    pi = marginal(q)
    r = two_step_flow(q)
    h = entropy(x for row in q for x in row) - entropy(pi)
    alpha = 2 * entropy(pi) - entropy(x for row in r for x in row)
    return h, alpha


def total_variation(q, r):
    return 0.5 * fsum(abs(x - y) for rowq, rowr in zip(q, r) for x, y in zip(rowq, rowr))


def entropy_modulus(d, t):
    if t < 0 or d < 2:
        raise ValueError("d >= 2 and t >= 0 are required")
    if t >= 1 - 1 / d:
        return log2(d)
    return binary_entropy(t) + t * log2(d - 1)


def grid_moduli(n):
    delta = 4 / n
    eta = entropy_modulus(9, delta) + entropy_modulus(3, delta)
    rho = 2 * entropy_modulus(3, delta) + entropy_modulus(9, 3 * delta)
    return eta, rho


def grid_envelope_float(alpha, n):
    """Floating verification of the formula, NOT a certified numerical bound."""
    eta, rho = grid_moduli(n)
    candidates = ((flow_statistics(q), q) for q in cycle_grid(n))
    best = max(((h, a, q) for (h, a), q in candidates if abs(a - alpha) <= rho),
               key=lambda item: item[0])
    return {"rate": best[0], "lag_two_information": best[1], "flow": best[2],
            "rate_modulus": eta, "information_modulus": rho,
            "upper_formula_float": best[0] + eta}


def flow_from_transition(pi, p):
    return tuple(tuple(pi[i] * p[i][j] for j in range(3)) for i in range(3))


def symmetric_flow(t):
    p = tuple(tuple((1 - t) / 3 + (t if i == j else 0) for j in range(3)) for i in range(3))
    return flow_from_transition((1 / 3,) * 3, p)


def lumped_flow(p, t):
    """Binary Markov class label, with independent uniform emission in class 2."""
    a, b = p + (1 - p) * t, p * (1 - t)
    transition = ((a, (1 - a) / 2, (1 - a) / 2),
                  (b, (1 - b) / 2, (1 - b) / 2),
                  (b, (1 - b) / 2, (1 - b) / 2))
    return flow_from_transition((p, (1 - p) / 2, (1 - p) / 2), transition)


def separated_flow(p, t):
    """An absorbing singleton and a binary symmetric recurrent class."""
    a = (1 + t) / 2
    transition = ((1, 0, 0), (0, a, 1 - a), (0, 1 - a, a))
    return flow_from_transition((p, (1 - p) / 2, (1 - p) / 2), transition)


def match_information(flow_at_t, alpha, iterations=60):
    low, high = 0.0, 1.0
    a_low = flow_statistics(flow_at_t(low))[1]
    a_high = flow_statistics(flow_at_t(high))[1]
    if not a_low - 1e-12 <= alpha <= a_high + 1e-12:
        raise ValueError("alpha is outside this family's range")
    for _ in range(iterations):
        middle = (low + high) / 2
        if flow_statistics(flow_at_t(middle))[1] < alpha:
            low = middle
        else:
            high = middle
    t = (low + high) / 2
    q = flow_at_t(t)
    h, a = flow_statistics(q)
    return {"t": t, "entropy_rate": h, "lag_two_information": a, "flow": q}
