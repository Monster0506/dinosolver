import pygame
from enum import Enum


class GameState(Enum):
    RUNNING = 0
    GAME_OVER = 1
    ENDED = 2


def main() -> None:
    state = GameState.RUNNING
    pygame.init()
    pygame.display.set_mode((60, 60))
    clock = pygame.time.Clock()
    while state != GameState.ENDED:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = GameState.ENDED
        clock.tick(60)
    pygame.quit()
    print("Hello from dinosolver!")
