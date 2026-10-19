import random
from dataclasses import dataclass
from enum import IntEnum

import numpy as np
import pygame

from dinosolver import (
    FPS,
    GRAVITY,
    GROUND_Y,
    JUMP_SCALE_SPEED,
    WIDTH,
    DinoState,
    GameState,
    State,
    initalize,
    jump,
    jump_velo,
    move_cactus,
    move_dino,
    reset_dino,
)

DT = 1 / FPS
OBS_SIZE = 5
SPEED_REF = JUMP_SCALE_SPEED
NO_OBSTACLE = 2.0

Rect = tuple[float, float, float, float]


class Action(IntEnum):
    STAY = 0
    JUMP = 1


@dataclass(frozen=True)
class Snapshot:
    dino: Rect
    obstacles: tuple[Rect, ...]
    score: int


def _rect(r: pygame.FRect) -> Rect:
    return (r.x, r.y, r.w, r.h)


class DinoEnv:
    """Headless fixed-timestep driver for the game in dinosolver.

    Game state is process-global, so one instance per process.
    """

    def __init__(self, seed: int) -> None:
        self._frames: int = 0
        self._dino: pygame.FRect = self._start(seed)

    @staticmethod
    def _start(seed: int) -> pygame.FRect:
        random.seed(seed)
        State.game_state = GameState.RUNNING
        dino = initalize()
        reset_dino(dino)
        return dino

    @property
    def over(self) -> bool:
        return State.game_state != GameState.RUNNING

    @property
    def score(self) -> int:
        return State.score

    @property
    def frames(self) -> int:
        return self._frames

    def step(self, action: Action) -> None:
        if self.over:
            return

        if action == Action.JUMP and State.dino_pos == DinoState.ON_GROUND:
            jump()

        if any(self._dino.colliderect(o) for o in State.obstacles):
            State.game_state = GameState.GAME_OVER
            return

        move_dino(self._dino, DT)
        for i, cactus in enumerate(State.obstacles):
            move_cactus(i, cactus, DT)
        self._frames += 1

    def observe(self) -> np.ndarray:
        dino = self._dino
        v0 = abs(jump_velo())
        apex = v0**2 / (2 * GRAVITY)
        ahead = sorted(
            (o for o in State.obstacles if o.right > dino.left), key=lambda o: o.x
        )
        dx = [(o.left - dino.right) / WIDTH for o in ahead[:2]]
        dx += [NO_OBSTACLE] * (2 - len(dx))

        return np.array(
            [
                dx[0],
                dx[1],
                (GROUND_Y - dino.bottom) / apex,
                State.dino_velo / v0,
                State.speed / SPEED_REF,
            ]
        )

    def snapshot(self) -> Snapshot:
        return Snapshot(
            dino=_rect(self._dino),
            obstacles=tuple(_rect(o) for o in State.obstacles),
            score=State.score,
        )
