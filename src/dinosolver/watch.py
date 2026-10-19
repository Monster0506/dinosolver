import argparse
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pygame

from dinosolver import FPS, HEIGHT, WIDTH
from dinosolver.env import DinoEnv
from dinosolver.policy import Net

DEFAULT_MODEL = Path("best.npy")
RESTART_DELAY_MS = 1000
SEED_RANGE = 2**31


@dataclass(frozen=True)
class Outcome:
    score: int
    quit: bool


def _quit_requested() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            return True
    return False


def _episode(
    net: Net, seed: int, screen: pygame.Surface, clock: pygame.Clock
) -> Outcome:
    env = DinoEnv(seed)

    while not env.over:
        clock.tick(FPS)
        if _quit_requested():
            return Outcome(env.score, quit=True)

        env.step(net.act(env.observe()))
        env.render(screen)
        pygame.display.flip()

    return Outcome(env.score, quit=False)


def main() -> None:
    ap = argparse.ArgumentParser(prog="dinosolver")
    ap.add_argument("model", type=Path, nargs="?", default=DEFAULT_MODEL)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    net = Net(np.load(args.model))
    rng = random.Random(args.seed)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        seed = rng.randrange(SEED_RANGE)
        outcome = _episode(net, seed, screen, clock)
        print(f"seed {seed}  score {outcome.score}")
        if outcome.quit:
            break
        pygame.time.wait(RESTART_DELAY_MS)

    pygame.quit()


if __name__ == "__main__":
    main()
