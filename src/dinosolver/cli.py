import argparse
import threading
from pathlib import Path

import numpy as np

from dinosolver.pool import Evaluator
from dinosolver.trainer import Config, GenStats, train

DEFAULT_WORKERS = 8


def _parse() -> tuple[argparse.Namespace, Config]:
    defaults = Config()
    ap = argparse.ArgumentParser(prog="dinotrain")
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    ap.add_argument("--pop", type=int, default=defaults.pop)
    ap.add_argument("--elites", type=int, default=defaults.elites)
    ap.add_argument("--sigma", type=float, default=defaults.sigma)
    ap.add_argument("--seed", type=int, default=defaults.seed)
    ap.add_argument("--generations", type=int, default=defaults.generations)
    ap.add_argument("--out", type=Path, default=Path("best.npy"))
    args = ap.parse_args()

    cfg = Config(args.pop, args.elites, args.sigma, args.seed, args.generations)
    return args, cfg


def main() -> None:
    args, cfg = _parse()

    def on_gen(s: GenStats) -> None:
        np.save(args.out, s.params)
        print(f"gen {s.gen:4d}  best {s.best:8.2f}  mean {s.mean:7.2f}  score {s.score}")

    evaluator = Evaluator(args.workers)
    try:
        train(evaluator, cfg, on_gen, threading.Event())
    except KeyboardInterrupt:
        pass
    finally:
        evaluator.close()


if __name__ == "__main__":
    main()
