import pygame
from enum import Enum


class GameState(Enum):
    RUNNING = 0
    GAME_OVER = 1
    ENDED = 2



WIDTH = 800
HEIGHT= 300

DINO_WIDTH = WIDTH // 20
DINO_HEIGHT= HEIGHT // 5

def main() -> None:
    state = GameState.RUNNING
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    dino = pygame.Rect(0+DINO_WIDTH*2,HEIGHT-DINO_HEIGHT-100,DINO_WIDTH, DINO_HEIGHT)
    while state != GameState.ENDED:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = GameState.ENDED

        screen.fill("gray")
        pygame.draw.rect(screen, "red", dino)
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()
    print("Hello from dinosolver!")
