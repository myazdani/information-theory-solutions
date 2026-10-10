# Reproduction

## Core checks

From the repository root, with Python 3.11 or newer:

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/validate.py
python scripts/build_index.py --check
```

The core library and tests use only Python's standard library. Optional scientific dependencies can be installed with `python -m pip install -e '.[numerical]'`. Each numerical run record identifies the exact versions actually used; the optional dependency ranges are compatibility bounds, not a claim that all versions were tested.

## Experiment contract

Put each experiment in `src/information_theory/experiments/`. Export `run(output_dir)`, returning:

- `results`: concise finite JSON values, such as optimal values, entropies, error bounds, or selected summaries
- `checks`: a nonempty mapping of descriptive invariant names to booleans, all true
- `source_files`: every repository-relative computational dependency, including shared helper modules
- `seed`: the actual fixed integer seed, or null for an entirely deterministic calculation
- `dependencies`: installed distribution names such as `numpy` and `scipy`; standard-library-only work uses an empty list
- `artifacts`: optional paths of figures or compact generated data

Run an experiment with the common wrapper:

```sh
PYTHONPATH=src python -m information_theory run information_theory.experiments.MODULE --output artifacts/CHAPTER/EXERCISE
```

The wrapper executes the calculation, verifies its boolean checks, rejects nonfinite JSON output, and writes `results.json` with the command, Python/package versions, seed declaration, and source/figure hashes. It hashes the experiment module and wrapper automatically. Authors must declare other dependencies accurately. The wrapper cannot detect an undeclared import or prove a result mathematically.

Solutions should show the useful numerical values and link relevant plots, explain tolerances and any approximations, and distinguish a finite experiment from an analytic proof. Do not store huge trial-by-trial dumps or environment caches. A compact summary with a deterministic generator is preferred.

If using Matplotlib on a read-only home directory, set `MPLCONFIGDIR` to a writable temporary location. Prefer deterministic metadata for exported figures. Different library versions may produce tiny floating-point or rendering differences; rerun checks against stated tolerances and re-review any content change before changing an accepted hash.
