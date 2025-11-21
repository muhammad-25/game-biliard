
import sys
import pygame
from game_manager import GameManager

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

ASSET_DIR = "../assets"  


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Biliar - Starter")
    clock = pygame.time.Clock()

    gm = GameManager(screen, asset_dir=ASSET_DIR)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                gm.handle_event(event)

        gm.update(dt)
        gm.render()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

