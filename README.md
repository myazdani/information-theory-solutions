# Elements of Information Theory: worked solutions

Original solutions to Thomas M. Cover and Joy A. Thomas, *Elements of Information Theory*, second edition (Wiley, 2006).

**378 / 378 exercises independently accepted; 0 drafts; 0 pending.**

All inventoried exercises have independently reviewed solutions. The exercise index distinguishes independently reviewed solutions from drafts and work not yet submitted. A numbered exercise counts as accepted only when every inventoried subpart has been checked and the review still matches the exact solution and numerical evidence. Automated checks verify evidence integrity; they do not certify a proof.

## Browse

- [Exercise-by-exercise index](solutions/README.md)
- [Source inventory and edition notes](inventory/README.md)
- [Review and contribution guide](docs/CONTRIBUTING.md)
- [Reproducibility guide](docs/REPRODUCIBILITY.md)
- [Machine-readable coverage](coverage/status.json)

| Chapter | Topic | Accepted | Draft | Pending | Total |
| --- | --- | ---: | ---: | ---: | ---: |
| 2 | [Entropy, Relative Entropy, and Mutual Information](solutions/README.md#chapter-2) | 48 | 0 | 0 | 48 |
| 3 | [Asymptotic Equipartition Property](solutions/README.md#chapter-3) | 13 | 0 | 0 | 13 |
| 4 | [Entropy Rates of a Stochastic Process](solutions/README.md#chapter-4) | 35 | 0 | 0 | 35 |
| 5 | [Data Compression](solutions/README.md#chapter-5) | 45 | 0 | 0 | 45 |
| 6 | [Gambling and Data Compression](solutions/README.md#chapter-6) | 18 | 0 | 0 | 18 |
| 7 | [Channel Capacity](solutions/README.md#chapter-7) | 37 | 0 | 0 | 37 |
| 8 | [Differential Entropy](solutions/README.md#chapter-8) | 11 | 0 | 0 | 11 |
| 9 | [Gaussian Channel](solutions/README.md#chapter-9) | 22 | 0 | 0 | 22 |
| 10 | [Rate Distortion Theory](solutions/README.md#chapter-10) | 20 | 0 | 0 | 20 |
| 11 | [Information Theory and Statistics](solutions/README.md#chapter-11) | 29 | 0 | 0 | 29 |
| 12 | [Maximum Entropy](solutions/README.md#chapter-12) | 22 | 0 | 0 | 22 |
| 13 | [Universal Source Coding](solutions/README.md#chapter-13) | 11 | 0 | 0 | 11 |
| 14 | [Kolmogorov Complexity](solutions/README.md#chapter-14) | 14 | 0 | 0 | 14 |
| 15 | [Network Information Theory](solutions/README.md#chapter-15) | 36 | 0 | 0 | 36 |
| 16 | [Information Theory and Portfolio Theory](solutions/README.md#chapter-16) | 12 | 0 | 0 | 12 |
| 17 | [Inequalities in Information Theory](solutions/README.md#chapter-17) | 5 | 0 | 0 | 5 |

## Reproduce and check

The finite-alphabet library and integrity tests require only Python 3.11 or newer. Numerical experiments list any optional packages they use.

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/validate.py
python scripts/build_index.py --check
```

For an experiment's exact command, dependencies, seed, and input/output hashes, follow its recorded `artifacts/.../results.json`. Solutions include their useful numerical findings, not just code links.

## Reading conventions

All logarithms are base 2 unless stated otherwise. Entropies are measured in bits; differential-entropy units are stated where needed. Each solution identifies its textbook exercise and printed page, states only the scope needed to follow the derivation, and develops an original argument. Fenced `math` blocks and GitHub-compatible inline math are used throughout.

## Source qualifications

Some printed problems have missing assumptions, ambiguous diagrams, or false boundary claims. Those solutions state the issue explicitly and give a justified interpretation or counterexample rather than assert an invalid proof. Examples include [7.34](solutions/ch07/ex-7-34.md), [9.4](solutions/ch09/ex-9-4.md), [10.16](solutions/ch10/ex-10-16.md), and [11.4](solutions/ch11/ex-11-4.md). The general solution to [12.11](solutions/ch12/ex-12-11.md) is a proved convergent finite-enumeration limit, not a closed-form classification or a finite two-sided optimality-gap certificate.

## Scope and rights

The goal is complete coverage of all 378 numbered exercises in Chapters 2–17. Chapter 1 has no numbered exercise section. Full textbook pages, full problem statements, and instructor solutions are not redistributed. Consult a lawful copy of the textbook for the exact questions. This independent project is not affiliated with the authors or publisher. Public availability alone does not grant an additional reuse license.
