import pytest

from dinosolver import JUMP_SCALE_SPEED, JUMP_VELO, State, jump, jump_velo


@pytest.mark.parametrize("speed", [300, 500, JUMP_SCALE_SPEED])
def test_jump_unchanged_up_to_scale_speed(speed: int):
    State.speed = speed

    assert jump_velo() == JUMP_VELO


def test_jump_scales_with_speed_above_scale_speed():
    State.speed = JUMP_SCALE_SPEED * 2
    jump()

    assert State.dino_velo == JUMP_VELO * 2
