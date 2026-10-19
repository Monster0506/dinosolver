import multiprocessing as mp
import queue
import time
from collections.abc import Callable
from dataclasses import dataclass
from multiprocessing.pool import Pool
from multiprocessing.queues import Queue
from multiprocessing.sharedctypes import Synchronized

import numpy as np

from dinosolver.env import DinoEnv, Snapshot
from dinosolver.rollout import Result, rollout

SNAPSHOT_INTERVAL = 1 / 30
QUEUE_SIZE = 256

Task = tuple[int, np.ndarray, int]


@dataclass(frozen=True)
class Frame:
    worker: int
    agent: int
    snapshot: Snapshot


_frames: Queue[Frame] | None = None
_worker: int = 0


def _init(counter: Synchronized[int], frames: Queue[Frame] | None) -> None:
    global _frames, _worker
    _frames = frames
    with counter.get_lock():
        _worker = counter.value
        counter.value += 1


def _publisher(agent: int) -> Callable[[DinoEnv], None] | None:
    if _frames is None:
        return None

    frames = _frames
    worker = _worker
    last = 0.0

    def publish(env: DinoEnv) -> None:
        nonlocal last
        now = time.perf_counter()
        if now - last < SNAPSHOT_INTERVAL:
            return

        last = now
        try:
            frames.put_nowait(Frame(worker, agent, env.snapshot()))
        except queue.Full:
            pass

    return publish


def _evaluate(task: Task) -> Result:
    agent, params, seed = task
    return rollout(params, seed, _publisher(agent))


class Evaluator:
    def __init__(self, workers: int, frames: Queue[Frame] | None = None) -> None:
        ctx = mp.get_context("spawn")
        counter = ctx.Value("i", 0)
        self._pool: Pool = ctx.Pool(workers, _init, (counter, frames))

    def evaluate(self, pop: np.ndarray, seed: int) -> list[Result]:
        tasks = [(i, params, seed) for i, params in enumerate(pop)]
        return self._pool.map(_evaluate, tasks, chunksize=1)

    def close(self) -> None:
        self._pool.terminate()
        self._pool.join()


def make_queue() -> Queue[Frame]:
    return mp.get_context("spawn").Queue(QUEUE_SIZE)
