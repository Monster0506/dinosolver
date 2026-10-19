from dinosolver import GROUND_Y, State
from dinosolver.env import Action, DinoEnv


def _play(seed: int, frames: int) -> tuple[int, float]:
    env = DinoEnv(seed)
    for f in range(frames):
        env.step(Action.JUMP if f % 40 == 0 else Action.STAY)
    return env.score, State.obstacles[0].x


def test_start_ignores_previous_episode():
    env = DinoEnv(0)
    while not env.over:
        env.step(Action.JUMP)

    fresh = DinoEnv(1)

    _, y, _, h = fresh.snapshot().dino
    assert y + h == GROUND_Y
    assert fresh.frames == 0
    assert not fresh.over


def test_same_seed_same_run():
    assert _play(7, 600) == _play(7, 600)


def test_standing_still_dies_at_first_cactus():
    env = DinoEnv(0)
    while not env.over:
        env.step(Action.STAY)

    assert env.score == 0
    assert 100 < env.frames < 200
