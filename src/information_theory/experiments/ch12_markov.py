"""Reproduce feasible-chain and continuity checks for Exercise 12.11."""
from math import log, log2
from pathlib import Path
import random

from information_theory.ch12_markov import (
    binary_entropy, cycle_grid, cycle_mixture, elementary_cycles, flow_statistics,
    grid_envelope_float, lumped_flow, match_information, quantize_weights,
    separated_flow, symmetric_flow, total_variation, two_step_flow,
)


def run(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(1211)
    continuity_checks = []
    quantization_checks = []
    for _ in range(200):
        a = [rng.random() for _ in range(8)]
        b = [rng.random() for _ in range(8)]
        a = [x / sum(a) for x in a]
        b = [x / sum(b) for x in b]
        q, r = cycle_mixture(a), cycle_mixture(b)
        continuity_checks.append(total_variation(two_step_flow(q), two_step_flow(r))
                                 <= 3 * total_variation(q, r) + 1e-12)
        rounded = cycle_mixture(quantize_weights(a, 101))
        quantization_checks.append(total_variation(q, rounded) <= 4 / 101 + 1e-12)
    comparison = []
    for alpha in (0.001, 0.01, 0.1, 0.2, 0.5):
        isotropic = match_information(symmetric_flow, alpha)
        rank_one = match_information(lambda t: lumped_flow(1 / 3, t), alpha)
        # This explicit nonuniform choice is feasible, without an optimization claim.
        p = 0.29610602 if alpha == 0.2 else 1 / 3
        nonuniform = match_information(lambda t: lumped_flow(p, t), alpha)
        comparison.append({"alpha": alpha, "symmetric_rate": isotropic["entropy_rate"],
                           "rank_one_uniform_rate": rank_one["entropy_rate"],
                           "explicit_stationary_singleton_mass": p,
                           "explicit_candidate_rate": nonuniform["entropy_rate"],
                           "explicit_candidate_parameter": nonuniform["t"],
                           "constraint_residual": abs(nonuniform["lag_two_information"] - alpha)})
    asymptotic = []
    for t in (0.08, 0.04, 0.02, 0.01):
        h, alpha = flow_statistics(lumped_flow(1 / 3, t))
        asymptotic.append({"t": t, "alpha": alpha,
                           "deficit_over_asymptotic": (log2(3) - h) / (alpha / (2 * log(2))) ** 0.5})
    # The tiny grid checks the algorithm, not its asymptotic usefulness or tightness.
    grid = grid_envelope_float(0.2, 3)
    special_h, special_alpha = flow_statistics(lumped_flow(1 / 3, 1))
    curves = []
    for title, color, factory in (
        ("Ternary symmetric (feasible)", "#b85b34", symmetric_flow),
        ("Rank-one, uniform stationary (feasible)", "#2266a5", lambda t: lumped_flow(1 / 3, t)),
        ("Two recurrent classes, uniform within each (feasible)", "#158068", lambda p: separated_flow(p / 2, 0)),
    ):
        points = [flow_statistics(factory(k / 150)) for k in range(151)]
        curves.append((title, color, points))
    width, height = 820, 560
    left, top, pw, ph = 78, 54, 690, 360
    def xy(alpha, h):
        return left + pw * alpha / log2(3), top + ph * (1 - h / log2(3))
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="white"/>',
           '<g font-family="Arial,sans-serif" fill="#222">',
           '<text x="78" y="30" font-size="20">Exercise 12.11: achievable rates and universal upper bound</text>']
    for value in (0, .4, .8, 1.2, log2(3)):
        x, _ = xy(value, 0)
        _, y = xy(0, value)
        label = "log₂3" if value == log2(3) else f"{value:g}"
        svg += [f'<path d="M{x:.3f},{top} V{top+ph}" stroke="#e4e7eb"/>',
                f'<path d="M{left},{y:.3f} H{left+pw}" stroke="#e4e7eb"/>',
                f'<text x="{x:.3f}" y="{top+ph+24}" text-anchor="middle" font-size="13">{label}</text>',
                f'<text x="{left-12}" y="{y+4:.3f}" text-anchor="end" font-size="13">{label}</text>']
    svg.append(f'<path d="M{left},{top} V{top+ph} H{left+pw}" fill="none" stroke="#222"/>')
    svg.append(f'<path d="M{left},{top} L{left+pw},{top+ph}" stroke="#444" stroke-dasharray="7 5" fill="none"/>')
    for title, color, points in curves:
        coords = " ".join(f"{xy(a,h)[0]:.3f},{xy(a,h)[1]:.3f}" for h, a in points)
        svg.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2.4"/>')
    svg += ['<text x="423" y="462" text-anchor="middle" font-size="15">Lag-two mutual information α (bits)</text>',
            '<text x="20" y="238" text-anchor="middle" font-size="15" transform="rotate(-90 20 238)">Entropy rate (bits per symbol)</text>']
    legend = [("Universal upper bound log₂3 − α", "#444")] + [(t, c) for t,c,_ in curves]
    for i, (title, color) in enumerate(legend):
        x, y = (78 if i < 2 else 420), 492 + (i % 2) * 26
        svg += [f'<path d="M{x},{y-4} h25" stroke="{color}" stroke-width="2.4"/>',
                f'<text x="{x+33}" y="{y}" font-size="12">{title}</text>']
    svg.append('</g></svg>')
    figure = output_dir / 'achievable-curves.svg'
    figure.write_text('\n'.join(svg), encoding='utf-8')
    return {
        "results": {"scope": "Floating-point verification of constructions; no machine-certified global bounds.",
                    "comparison": comparison, "small_alpha_asymptotic": asymptotic,
                    "special_point": {"alpha": special_alpha, "entropy_rate": special_h},
                    "cycle_count": len(elementary_cycles()), "grid_n3_count": sum(1 for _ in cycle_grid(3)),
                    "grid_n3_verification": {k:v for k,v in grid.items() if k != "flow"}},
        "checks": {"cycle_count_is_eight": len(elementary_cycles()) == 8,
                   "lag_two_continuity_samples": all(continuity_checks),
                   "quantization_samples": all(quantization_checks),
                   "special_point": abs(special_h - 2 / 3) < 1e-12 and abs(special_alpha - binary_entropy(1 / 3)) < 1e-12,
                   "constructed_constraints": all(r["constraint_residual"] < 1e-12 for r in comparison),
                   "rank_one_beats_isotropic_at_small_alpha": comparison[0]["rank_one_uniform_rate"] > comparison[0]["symmetric_rate"],
                   "nonuniform_improves_uniform_at_point_two": comparison[3]["explicit_candidate_rate"] > comparison[3]["rank_one_uniform_rate"],
                   "asymptotic_ratio_approaches_one": abs(asymptotic[-1]["deficit_over_asymptotic"] - 1) < .005},
        "source_files": ["src/information_theory/ch12_markov.py"],
        "seed": 1211, "dependencies": [], "artifacts": [figure.relative_to(Path(__file__).resolve().parents[3]).as_posix()],
    }
