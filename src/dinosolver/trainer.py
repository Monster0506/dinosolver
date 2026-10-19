import itertools
import threading
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Protocol

import numpy as np

from dinosolver.evolve import next_gen
from dinosolver.policy import random_params
from dinosolver.rollout import Result


@dataclass(frozen=True)
class Config:
    pop: int = 64
    elites: int = 8
    sigma: float = 0.3
    seed: int = 0
    generations: int | None = None


@dataclass(frozen=True)
class GenStats:
    gen: int
    best: float
    mean: float
    score: int
    params: np.ndarray


class Evaluates(Protocol):
    def evaluate(self, pop: np.ndarray, seed: int) -> Sequence[Result]: ...


def train(
    evaluator: Evaluates,
    cfg: Config,
    on_gen: Callable[[GenStats], None],
    stop: threading.Event,
) -> None:
    rng = np.random.default_rng(cfg.seed)
    pop = np.stack([random_params(rng) for _ in range(cfg.pop)])
    gens = range(cfg.generations) if cfg.generations is not None else itertools.count()

    for gen in gens:
        if stop.is_set():
            return

        results = evaluator.evaluate(pop, cfg.seed + gen)
        fitness = [r.fitness for r in results]
        top = int(np.argmax(fitness))
        on_gen(
            GenStats(
                gen=gen,
                best=fitness[top],
                mean=float(np.mean(fitness)),
                score=max(r.score for r in results),
                params=pop[top],
            )
        )
        pop = next_gen(pop, fitness, cfg.elites, cfg.sigma, rng)
