from collections.abc import Sequence

import numpy as np


def next_gen(
    pop: np.ndarray,
    fitness: Sequence[float],
    elites: int,
    sigma: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Keep the top `elites` unchanged (best first); refill with mutated copies."""
    order = np.argsort(fitness)[::-1]
    best = pop[order[:elites]]

    parents = best[rng.integers(0, elites, len(pop) - elites)]
    children = parents + rng.normal(0.0, sigma, parents.shape)

    return np.concatenate([best, children])
