import os
import pygame


class Renderer:
    def __init__(self, screen, asset_dir="../assets"):
        self.screen = screen
        self.asset_dir = asset_dir
        self.width, self.height = self.screen.get_size()

    def clear(self):

        self.screen.fill((30, 110, 40))

    def draw_table(self):

        pad = 40
        pygame.draw.rect(self.screen, (12, 80, 30), (pad, pad, self.width - pad * 2, self.height - pad * 2))

    def draw_hud(self, score_obj):
        font = pygame.font.SysFont(None, 24)
        txt = font.render(f"Score: {score_obj.points}  |  Drag behind the ball to pull the cue; release to shoot", True, (255, 255, 255))
        self.screen.blit(txt, (10, 10))
