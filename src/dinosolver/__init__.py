import pygame
from enum import Enum


class GameState(Enum):
    RUNNING = 0
    GAME_OVER = 1
    QUIT = 2


class DinoState(Enum):
    ON_GROUND = 0
    IN_AIR = 1


FPS = 600


WIDTH = 800
HEIGHT = 300

DINO_WIDTH = WIDTH // 20
DINO_HEIGHT = HEIGHT // 5

CACTUS_HEIGHT = HEIGHT // 6

GROUND_Y = 200

GRAVITY = 2000
JUMP_VELO = -700
SPEED= 300


def main() -> None:
    state = GameState.RUNNING
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    dino = pygame.Rect(DINO_WIDTH * 2, 0, DINO_WIDTH, DINO_HEIGHT)
    dino.bottom = GROUND_Y - 100
    dino_pos = DinoState.ON_GROUND

    vel_y = 0.0
    y = float(dino.y)

    cactus = pygame.Rect(WIDTH, 0, DINO_WIDTH, CACTUS_HEIGHT)
    cactus.bottom = GROUND_Y

    x = float(cactus.x)

    while state != GameState.QUIT:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    state = GameState.QUIT
                case pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and dino_pos == DinoState.ON_GROUND:
                        print("test")
                        dino_pos = DinoState.IN_AIR
                        vel_y = JUMP_VELO

        vel_y += GRAVITY * dt
        y += vel_y * dt
        dino.y = round(y)

        if dino.bottom >= GROUND_Y:
            dino.bottom = GROUND_Y
            y = dino.y
            vel_y = 0
            dino_pos = DinoState.ON_GROUND

        x -= SPEED * dt
        cactus.x = round(x)

        if cactus.right <= 0:
            cactus.x = WIDTH
            x = cactus.x

        screen.fill("gray")

        pygame.draw.line(screen, "black", (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

        pygame.draw.rect(screen, "red", dino)

        pygame.draw.rect(screen, "green", cactus)

        pygame.display.flip()

    pygame.quit()
    print("Hello from dinosolver!")
