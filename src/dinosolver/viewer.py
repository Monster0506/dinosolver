import math
import queue
import threading
from multiprocessing.queues import Queue
from queue import Empty

import pygame

from dinosolver import FPS, HEIGHT, WIDTH
from dinosolver.pool import Frame
from dinosolver.render import Renderer
from dinosolver.trainer import GenStats

WINDOW = (1280, 720)
HEADER_H = 36
GAP = 4
BG = "gray15"
TEXT = "white"
FONT_SIZE = 22
LABEL_SIZE = 18
DRAIN_LIMIT = 512


def layout(workers: int, window: tuple[int, int]) -> tuple[int, int, int]:
    """Return (cols, tile_w, tile_h) so every tile fits under the header."""
    cols = math.ceil(math.sqrt(workers))
    rows = math.ceil(workers / cols)
    win_w, win_h = window

    tile_w = min(
        (win_w - GAP) // cols - GAP,
        ((win_h - HEADER_H - GAP) // rows - GAP) * WIDTH // HEIGHT,
    )
    return cols, tile_w, tile_w * HEIGHT // WIDTH


class Viewer:
    def __init__(self, workers: int) -> None:
        pygame.init()
        pygame.display.set_caption("dinosolver")
        self._workers: int = workers
        self._screen: pygame.Surface = pygame.display.set_mode(WINDOW)
        self._renderer: Renderer = Renderer()
        self._font: pygame.Font = pygame.font.Font(None, FONT_SIZE)
        self._label: pygame.Font = pygame.font.Font(None, LABEL_SIZE)
        self._latest: dict[int, Frame] = {}
        self._stats: GenStats | None = None

    def run(
        self,
        frames: Queue[Frame],
        stats: queue.Queue[GenStats],
        stop: threading.Event,
    ) -> None:
        clock = pygame.time.Clock()

        while not stop.is_set():
            clock.tick(FPS)
            if self._quit_requested():
                stop.set()
                break

            self._drain(frames, stats)
            self._paint()
            pygame.display.flip()

        pygame.quit()

    @staticmethod
    def _quit_requested() -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return True
        return False

    def _drain(self, frames: Queue[Frame], stats: queue.Queue[GenStats]) -> None:
        for _ in range(DRAIN_LIMIT):
            try:
                frame = frames.get_nowait()
            except Empty:
                break
            self._latest[frame.worker] = frame

        while True:
            try:
                self._stats = stats.get_nowait()
            except Empty:
                break

    def _paint(self) -> None:
        self._screen.fill(BG)
        self._paint_header()

        cols, tile_w, tile_h = layout(self._workers, WINDOW)
        for worker, frame in self._latest.items():
            col, row = worker % cols, worker // cols
            pos = (GAP + col * (tile_w + GAP), HEADER_H + GAP + row * (tile_h + GAP))
            self._screen.blit(
                self._renderer.draw(frame.snapshot, (tile_w, tile_h)), pos
            )
            tag = self._label.render(
                f"#{frame.agent}  {frame.snapshot.score}", True, "black"
            )
            self._screen.blit(tag, (pos[0] + GAP, pos[1] + GAP))

    def _paint_header(self) -> None:
        s = self._stats
        text = (
            "waiting for first generation..."
            if s is None
            else f"gen {s.gen}   best {s.best:.2f}   mean {s.mean:.2f}   top score {s.score}"
        )
        self._screen.blit(self._font.render(text, True, TEXT), (GAP * 2, GAP * 2))
