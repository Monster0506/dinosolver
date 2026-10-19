import numpy as np

from dinosolver.env import OBS_SIZE, Action

HIDDEN = 8

_W1 = OBS_SIZE * HIDDEN
_B1 = _W1 + HIDDEN
_W2 = _B1 + HIDDEN
PARAM_COUNT = _W2 + 1


def random_params(rng: np.random.Generator) -> np.ndarray:
    return rng.normal(0.0, 1.0, PARAM_COUNT)


class Net:
    def __init__(self, params: np.ndarray) -> None:
        self._w1: np.ndarray = params[:_W1].reshape(OBS_SIZE, HIDDEN)
        self._b1: np.ndarray = params[_W1:_B1]
        self._w2: np.ndarray = params[_B1:_W2]
        self._b2: float = params[_W2]

    def act(self, obs: np.ndarray) -> Action:
        hidden = np.tanh(obs @ self._w1 + self._b1)
        return Action.JUMP if hidden @ self._w2 + self._b2 > 0 else Action.STAY
