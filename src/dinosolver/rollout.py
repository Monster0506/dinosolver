from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from dinosolver import FPS
from dinosolver.env import DinoEnv
from dinosolver.policy import Net

MAX_FRAMES = FPS * 300
# Keeps survival time a tie-breaker that can never outweigh a cactus.
SURVIVAL_WEIGHT = 1 / (MAX_FRAMES + 1)


@dataclass(frozen=True)
class Result:
    fitness: float
    score: int
    frames: int


def rollout(
    params: np.ndarray,
    seed: int,
    on_step: Callable[[DinoEnv], None] | None = None,
) -> Result:
    net = Net(params)
    env = DinoEnv(seed)

    while not env.over and env.frames < MAX_FRAMES:
        env.step(net.act(env.observe()))
        if on_step is not None:
            on_step(env)

    return Result(
        fitness=env.score + env.frames * SURVIVAL_WEIGHT,
        score=env.score,
        frames=env.frames,
    )
