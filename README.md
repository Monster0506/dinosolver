# dinosolver

Dino game (`src/dinosolver/__init__.py`) plus a neuroevolution trainer that learns to play it.

    uv run dinoplay                  # play by hand
    uv run dinosolver [model.npy]    # watch a saved agent at 60 FPS (default best.npy)
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
| `watch.py` | Real-time playback of a saved agent |

Episodes are capped at 300 s of game time. Workers run unthrottled, so tiles are a sampled fast-forward, not real time.

Speed ramps 10 px/s per cactus up to `MAX_SPEED` (4000, below the 4800 where a cactus can skip past the dino in one frame). Above `SPAWN_SCALE_SPEED` (800), cactus spawn distance and gap scale with speed, so obstacle timing in seconds stays constant and a perfect player survives at any speed. Observations are time to contact for the same reason.
