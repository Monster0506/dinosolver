import pygame

from dinosolver import HEIGHT, WIDTH, State, draw
from dinosolver.env import Snapshot


class Renderer:
    """Draws snapshots through the game's own draw()."""

    def __init__(self) -> None:
        pygame.font.init()
        self._canvas: pygame.Surface = pygame.Surface((WIDTH, HEIGHT))

    def draw(self, snap: Snapshot, size: tuple[int, int]) -> pygame.Surface:
        State.obstacles[:] = [pygame.FRect(*r) for r in snap.obstacles]
        State.score = snap.score
        draw(self._canvas, pygame.FRect(*snap.dino))
        return pygame.transform.smoothscale(self._canvas, size)
