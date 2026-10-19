import numpy as np

from dinosolver.policy import random_params
from dinosolver.pool import Evaluator, Frame, make_queue
from dinosolver.rollout import rollout


def _pop(n: int) -> np.ndarray:
    rng = np.random.default_rng(3)
    return np.stack([random_params(rng) for _ in range(n)])


def test_workers_match_serial_rollouts():
    pop = _pop(6)
    evaluator = Evaluator(workers=2)
    try:
        parallel = evaluator.evaluate(pop, seed=5)
    finally:
        evaluator.close()

    assert parallel == [rollout(p, 5) for p in pop]


def test_workers_publish_frames_with_distinct_ids():
    frames = make_queue()
    evaluator = Evaluator(workers=2, frames=frames)
    try:
        evaluator.evaluate(_pop(8), seed=1)
        got: list[Frame] = [frames.get(timeout=5)]
        while not frames.empty():
            got.append(frames.get())
    finally:
        evaluator.close()

    assert {f.worker for f in got} <= {0, 1}
