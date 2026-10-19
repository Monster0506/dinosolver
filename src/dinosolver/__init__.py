import pygame
from enum import Enum
from random import randint


class GameState(Enum):
    RUNNING = 0
    GAME_OVER = 1
    QUIT = 2


class DinoState(Enum):
    ON_GROUND = 0
    IN_AIR = 1


FPS = 60


WIDTH = 800
HEIGHT = 300

DINO_WIDTH = WIDTH // 20
DINO_HEIGHT = HEIGHT // 5

CACTUS_HEIGHT = HEIGHT // 6

GROUND_Y = 200

GRAVITY = 2000
JUMP_VELO = -700

SPEED_STEP = 10
MAX_SPEED = 4000
JUMP_SCALE_SPEED = 800


class State:
    game_state: GameState = GameState.RUNNING
    dino_pos: DinoState = DinoState.ON_GROUND
    dino_y: float = 0.0
    dino_velo: float = 0.0
    obstacles: list[pygame.FRect] = []
    speed: int = 300
    score: int = 0


def reset_dino(dino: pygame.FRect):
    dino.bottom = GROUND_Y
    State.dino_y = dino.y
    State.dino_velo = 0
    State.dino_pos = DinoState.ON_GROUND


def move_dino(dino: pygame.FRect, dt: float):
    State.dino_velo += GRAVITY * dt
    State.dino_y += State.dino_velo * dt
    dino.y = State.dino_y

    if dino.bottom >= GROUND_Y:
        reset_dino(dino)


def jump_velo() -> float:
    return JUMP_VELO * max(1, State.speed / JUMP_SCALE_SPEED)


def jump():
    State.dino_pos = DinoState.IN_AIR
    State.dino_velo = jump_velo()


def reset_cactus(cactus: pygame.FRect, i: int):
    rightmost = max(State.obstacles, key=lambda o: o.x)
    spawn_loc = max(WIDTH, rightmost.x) + randint(300, 600)
    cactus.x = spawn_loc
    State.obstacles[i].x = cactus.x


def move_cactus(i: int, cactus: pygame.FRect, dt: float):

    State.obstacles[i].x -= State.speed * dt
    cactus.x = State.obstacles[i].x

    if cactus.right <= 0:
        State.score += 1
        State.speed = min(State.speed + SPEED_STEP, MAX_SPEED)
        reset_cactus(cactus, i)


def draw(screen: pygame.Surface, dino: pygame.FRect):
    screen.fill("lightblue")
    score_font = pygame.font.Font(None, 15)
    score_text = score_font.render(f"{State.score}", True, "black")
    pygame.draw.line(screen, "black", (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
    pygame.draw.rect(screen, "red", dino)

    for i in range(len(State.obstacles)):
        pygame.draw.rect(screen, "green", State.obstacles[i])
    screen.blit(score_text, (15, 15))


def play(dino: pygame.FRect, screen: pygame.Surface, clock: pygame.Clock):
    while State.game_state == GameState.RUNNING:
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
                        jump()
                    elif event.key == pygame.K_q:
                        State.game_state = GameState.QUIT

                case _:
                    pass

        if any(dino.colliderect(o) for o in State.obstacles):
            State.game_state = GameState.GAME_OVER
            continue

        move_dino(dino, dt)

        for i in range(len(State.obstacles)):
            move_cactus(i, State.obstacles[i], dt)

        draw(screen, dino)
        pygame.display.flip()


def initalize():
    dino = pygame.FRect(DINO_WIDTH * 2, 0, DINO_WIDTH, DINO_HEIGHT)
    dino.bottom = GROUND_Y - 100

    cactus = pygame.FRect(WIDTH, 0, DINO_WIDTH, CACTUS_HEIGHT)
    cactus.bottom = GROUND_Y

    cactus2 = pygame.FRect(WIDTH + 300, 0, DINO_WIDTH, CACTUS_HEIGHT)
    cactus2.bottom = GROUND_Y
    State.dino_velo = 0
    State.dino_pos = DinoState.ON_GROUND
    State.obstacles.clear()
    State.obstacles.append(cactus)
    State.obstacles.append(cactus2)
    State.speed = 300
    State.score = 0
    return dino


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    dino = initalize()

    while True:
        if State.game_state == GameState.QUIT:
            break
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    State.game_state = GameState.QUIT
                case pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_SPACE
                        and State.game_state == GameState.GAME_OVER
                    ):
                        dino = initalize()
                        State.game_state = GameState.RUNNING
                        break
                    elif event.key == pygame.K_q:
                        State.game_state = GameState.QUIT

        play(dino, screen, clock)

    pygame.quit()
    print("Hello from dinosolver!")
