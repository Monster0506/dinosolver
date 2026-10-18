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
SPEED = 300


class State:
    game_state: GameState = GameState.RUNNING
    dino_pos: DinoState = DinoState.ON_GROUND
    dino_y: float = 0.0
    dino_velo: float = 0.0
    cactus_xs: list[float] = [0.0]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    dino = pygame.Rect(DINO_WIDTH * 2, 0, DINO_WIDTH, DINO_HEIGHT)
    dino.bottom = GROUND_Y - 100

    cactus = pygame.Rect(WIDTH, 0, DINO_WIDTH, CACTUS_HEIGHT)
    cactus.bottom = GROUND_Y
    
    obstacles = [cactus]
    
    while State.game_state != GameState.QUIT:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    State.game_state = GameState.QUIT
                case pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_SPACE
                        and State.dino_pos == DinoState.ON_GROUND
                    ):
                        State.dino_pos = DinoState.IN_AIR
                        State.dino_velo = JUMP_VELO

        State.dino_velo += GRAVITY * dt
        State.dino_y += State.dino_velo * dt
        dino.y = round(State.dino_y)

        if dino.bottom >= GROUND_Y:
            dino.bottom = GROUND_Y
            State.dino_y = dino.y
            State.dino_velo = 0
            State.dino_pos = DinoState.ON_GROUND

        for i in range(len(State.cactus_xs)):
            
            State.cactus_xs[i] -= SPEED * dt
            obstacles[i].x = round(State.cactus_xs[i])

            if cactus.right <= 0:
                cactus.x = WIDTH
                State.cactus_xs[i] = obstacles[i].x

        screen.fill("gray")

        pygame.draw.line(screen, "black", (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

        pygame.draw.rect(screen, "red", dino)

        pygame.draw.rect(screen, "green", cactus)

        pygame.display.flip()

    pygame.quit()
    print("Hello from dinosolver!")
