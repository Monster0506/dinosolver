import pygame
from enum import Enum


class GameState(Enum):
    RUNNING = 0
    GAME_OVER = 1
    QUIT = 2



WIDTH = 800
HEIGHT= 300

DINO_WIDTH = WIDTH // 20
DINO_HEIGHT= HEIGHT // 5

GROUND_Y = 200

GRAVITY = 2000

def main() -> None:
    state = GameState.RUNNING
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    dino = pygame.Rect(0+DINO_WIDTH*2,10, DINO_WIDTH, DINO_HEIGHT)
    dino.bottom = GROUND_Y - 100
    
    vel_y = 0.0
    y = float(dino.y)
    dt = 0
    while state != GameState.QUIT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = GameState.QUIT
                
        if dino.bottom >= GROUND_Y:
            dino.bottom = GROUND_Y
            y = dino.y
            vel_y = 0
            

        screen.fill("gray")
        pygame.draw.line(screen, "black", (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        pygame.draw.rect(screen, "red", dino)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        
        vel_y += GRAVITY * dt
        y += vel_y * dt
        dino.y = round(y)

    pygame.quit()
    print("Hello from dinosolver!")
