import numpy as np

from dinosolver.evolve import next_gen


def test_elites_survive_best_first_and_size_holds():
    rng = np.random.default_rng(0)
    pop = rng.normal(size=(10, 4))
    fitness = [3.0, 9.0, 1.0, 7.0, 0.0, 5.0, 2.0, 4.0, 6.0, 8.0]

    out = next_gen(pop, fitness, elites=3, sigma=0.1, rng=rng)

    assert out.shape == pop.shape
    assert np.array_equal(out[:3], pop[[1, 9, 3]])


def test_children_mutate_from_elites():
    rng = np.random.default_rng(0)
    pop = np.zeros((6, 3))
    pop[0] = 1.0
    fitness = [1.0, 0, 0, 0, 0, 0]

    out = next_gen(pop, fitness, elites=1, sigma=0.01, rng=rng)

    assert not np.array_equal(out[1], out[0])
    assert np.allclose(out[1:], 1.0, atol=0.1)
