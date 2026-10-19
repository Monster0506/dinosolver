import argparse
import queue
import threading
from collections.abc import Callable
from enum import Enum
from pathlib import Path

import numpy as np

from dinosolver.pool import Evaluator, make_queue
from dinosolver.trainer import Config, GenStats, train
from dinosolver.viewer import Viewer

DEFAULT_WORKERS = 8


class Display(Enum):
    GRID = "grid"
    NONE = "none"


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
    ap.add_argument(
        "--display", type=Display, choices=list(Display), default=Display.GRID
    )
    args = ap.parse_args()

    cfg = Config(args.pop, args.elites, args.sigma, args.seed, args.generations)
    return args, cfg


def _headless(workers: int, cfg: Config, on_gen: Callable[[GenStats], None]) -> None:
    evaluator = Evaluator(workers)
    try:
        train(evaluator, cfg, on_gen, threading.Event())
    except KeyboardInterrupt:
        pass
    finally:
        evaluator.close()


def _grid(workers: int, cfg: Config, on_gen: Callable[[GenStats], None]) -> None:
    frames = make_queue()
    stats: queue.Queue[GenStats] = queue.Queue()
    stop = threading.Event()
    evaluator = Evaluator(workers, frames)

    def publish(s: GenStats) -> None:
        on_gen(s)
        stats.put(s)

    def work() -> None:
        try:
            train(evaluator, cfg, publish, stop)
        finally:
            stop.set()

    threading.Thread(target=work, daemon=True).start()
    try:
        Viewer(workers).run(frames, stats, stop)
    finally:
        evaluator.close()


def main() -> None:
    args, cfg = _parse()

    def on_gen(s: GenStats) -> None:
        np.save(args.out, s.params)
        print(
            f"gen {s.gen:4d}  best {s.best:8.2f}  mean {s.mean:7.2f}  score {s.score}"
        )

    if args.display == Display.NONE:
        _headless(args.workers, cfg, on_gen)
        return

    _grid(args.workers, cfg, on_gen)


if __name__ == "__main__":
    main()
