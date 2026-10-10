"""Small, dependency-free finite-alphabet information-theory primitives.

Logarithms use base 2 by default. Zero-mass terms use their continuous limits.
Inputs are validated, never silently renormalized.
"""
from __future__ import annotations
import heapq
import math
from collections.abc import Iterable


def probability_vector(values: Iterable[float], *, atol: float = 1e-12) -> tuple[float, ...]:
    p = tuple(float(v) for v in values)
    if not p or any(not math.isfinite(v) or v < 0 for v in p):
        raise ValueError("probabilities must be a nonempty finite nonnegative sequence")
    if not math.isclose(math.fsum(p), 1.0, abs_tol=atol, rel_tol=0):
        raise ValueError("probabilities must sum to one")
    return p


def _log_scale(base: float) -> float:
    base = float(base)
    if not math.isfinite(base) or base <= 1:
        raise ValueError("logarithm base must be finite and greater than one")
    return math.log(base)


def entropy(values: Iterable[float], *, base: float = 2) -> float:
    p = probability_vector(values)
    scale = _log_scale(base)
    return -math.fsum(v * math.log(v) for v in p if v) / scale


def binary_entropy(p: float) -> float:
    return entropy((p, 1 - p))


def relative_entropy(p: Iterable[float], q: Iterable[float], *, base: float = 2) -> float:
    p, q = probability_vector(p), probability_vector(q)
    scale = _log_scale(base)
    if len(p) != len(q):
        raise ValueError("the alphabets must have equal size")
    if any(a > 0 and b == 0 for a, b in zip(p, q)):
        return math.inf
    return math.fsum(a * (math.log(a) - math.log(b)) for a, b in zip(p, q) if a) / scale


def joint_distribution(rows: Iterable[Iterable[float]]) -> tuple[tuple[float, ...], ...]:
    rows = tuple(tuple(float(v) for v in row) for row in rows)
    if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("joint probability array must be nonempty and rectangular")
    probability_vector(v for row in rows for v in row)
    return rows


def marginals(rows: Iterable[Iterable[float]]) -> tuple[tuple[float, ...], tuple[float, ...]]:
    rows = joint_distribution(rows)
    return tuple(math.fsum(row) for row in rows), tuple(math.fsum(col) for col in zip(*rows))


def mutual_information(rows: Iterable[Iterable[float]], *, base: float = 2) -> float:
    rows = joint_distribution(rows)
    px, py = marginals(rows)
    # Direct summation avoids the cancellation in H(X) + H(Y) - H(X,Y).
    scale = _log_scale(base)
    return math.fsum(v * (math.log(v) - math.log(px[i]) - math.log(py[j]))
                     for i, row in enumerate(rows) for j, v in enumerate(row) if v) / scale


def conditional_entropy(rows: Iterable[Iterable[float]], *, base: float = 2) -> float:
    """H(Y|X), with rows indexed by X and columns by Y."""
    rows = joint_distribution(rows)
    px, _ = marginals(rows)
    return math.fsum(mass * entropy((v / mass for v in row), base=base)
                     for row, mass in zip(rows, px) if mass)


def channel_joint(inputs: Iterable[float], channel: Iterable[Iterable[float]]) -> tuple[tuple[float, ...], ...]:
    """Joint p(x,y) from p(x) and row-stochastic W(y|x)."""
    inputs = probability_vector(inputs)
    channel = tuple(probability_vector(row) for row in channel)
    if len(inputs) != len(channel) or any(len(row) != len(channel[0]) for row in channel):
        raise ValueError("channel dimensions must match the input and output alphabets")
    return tuple(tuple(p * w for w in row) for p, row in zip(inputs, channel))


def huffman_lengths(values: Iterable[float]) -> tuple[int, ...]:
    """Deterministic binary Huffman lengths (ties break by insertion order).

    All supplied symbols, including zero-probability symbols, receive a code.
    A singleton alphabet receives the empty codeword, of length zero.
    """
    p = probability_vector(values)
    heap = [(mass, i, (i,)) for i, mass in enumerate(p)]
    heapq.heapify(heap)
    lengths = [0] * len(p)
    serial = len(p)
    while len(heap) > 1:
        a, _, ia = heapq.heappop(heap)
        b, _, ib = heapq.heappop(heap)
        indices = ia + ib
        for i in indices:
            lengths[i] += 1
        heapq.heappush(heap, (a + b, serial, indices))
        serial += 1
    return tuple(lengths)
