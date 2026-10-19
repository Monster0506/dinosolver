# dinosolver

Dino game (`src/dinosolver/__init__.py`) plus a neuroevolution trainer that learns to play it.

    uv run dinosolver      # play by hand
    uv run dinotrain       # train, live tile grid
    uv run dinotrain --display none --generations 100

Options: `--workers` (processes, one tile each), `--pop`, `--elites`, `--sigma`, `--seed`, `--generations`, `--out`.
The best genome of each generation is saved to `--out` (`best.npy`). Press `q` in the window to stop.

## Layout

| Module | Role |
|---|---|
| `env.py` | Headless fixed-timestep driver over the game's own functions |
| `policy.py` | numpy MLP, flat parameter vector |
| `rollout.py` | One episode. Fitness = score + tiny survival tie-breaker |
| `evolve.py` | Elitism + gaussian mutation |
| `pool.py` | Worker processes (game state is process-global); stream snapshots |
| `trainer.py` | Generation loop |
| `render.py`, `viewer.py` | Draw snapshots with the game's `draw()` into one window |

Episodes are capped at 300 s of game time. Workers run unthrottled, so tiles are a sampled fast-forward, not real time.
