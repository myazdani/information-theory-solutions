"""CLI for reproducible, content-bound numerical runs."""
import argparse
from pathlib import Path
from .evidence import run_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="run a deterministic experiment module")
    run.add_argument("module")
    run.add_argument("--output", required=True)
    run.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    if args.command == "run":
        print(run_experiment(args.root, args.module, args.output))


if __name__ == "__main__":
    main()
