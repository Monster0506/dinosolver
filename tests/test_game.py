import random

import pytest

from dinosolver import SPAWN_SCALE_SPEED, WIDTH, State, initalize, reset_cactus

MIN_GAP = 300
MAX_GAP = 600


def _gaps(speed: int, factor: int) -> list[float]:
    random.seed(0)
    initalize()
    State.speed = speed
    gaps = []

    for _ in range(50):
        prev = max(WIDTH * factor, max(o.x for o in State.obstacles))
        reset_cactus(State.obstacles[0], 0)
        gaps.append(State.obstacles[0].x - prev)

    return gaps


@pytest.mark.parametrize("factor", [1, 2, 5])
def test_gap_scales_with_speed_above_scale_speed(factor: int):
    gaps = _gaps(SPAWN_SCALE_SPEED * factor, factor)

    assert min(gaps) >= MIN_GAP * factor
    assert max(gaps) <= MAX_GAP * factor


def test_gap_unscaled_below_scale_speed():
    gaps = _gaps(SPAWN_SCALE_SPEED // 2, 1)

    assert MIN_GAP <= min(gaps)
    assert max(gaps) <= MAX_GAP


def test_spawn_distance_scales_with_speed():
    factor = 3
    initalize()
    State.speed = SPAWN_SCALE_SPEED * factor
    reset_cactus(State.obstacles[0], 0)

    assert State.obstacles[0].x >= (WIDTH + MIN_GAP) * factor
