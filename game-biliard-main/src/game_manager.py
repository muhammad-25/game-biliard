import os
import pygame
from renderer import Renderer
from physics import Physics
from objects.bola import Bola
from objects.tongkat import Tongkat
from skor import Score


class GameManager:
    """Central manager that owns game objects and coordinates update & render."""

    def __init__(self, screen, asset_dir=None):
        self.screen = screen


        if asset_dir:
            base = os.path.dirname(__file__)  # src/
            candidate = os.path.normpath(os.path.join(base, asset_dir))
            if os.path.exists(candidate):
                self.asset_dir = candidate
            else:
                self.asset_dir = os.path.abspath(asset_dir)
        else:
            base = os.path.dirname(__file__)
            self.asset_dir = os.path.normpath(os.path.join(base, "..", "assets"))

        print("ASSET PATH =", self.asset_dir)  

        self.renderer = Renderer(screen, asset_dir=self.asset_dir)
        self.physics = Physics(self.screen.get_size())

        self.objects = []
        self.score = Score()


        self.cue = Tongkat(asset_dir=self.asset_dir)

        self._init_scene()


    def _init_scene(self):

        w, h = self.screen.get_size()
        ball = Bola(x=w // 2, y=h // 2, radius=16, vx=0, vy=0)
        self.objects.append(ball)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for o in self.objects:
                    if hasattr(o, "reset"):
                        o.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                pos = event.pos
                target = self._find_ball_near(pos, threshold=20)
                if target:
                    self.cue.start_aim(target, pos)
                else:

                    x, y = pos
                    self.objects.append(Bola(x=x, y=y, radius=12, vx=0, vy=0))
        elif event.type == pygame.MOUSEMOTION:
            if self.cue.aiming:
                self.cue.update_aim(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.cue.aiming:
                self.cue.release(event.pos)

    def _find_ball_near(self, pos, threshold=20):
        x, y = pos
        for o in self.objects:
            dx = o.x - x
            dy = o.y - y
            dist2 = dx * dx + dy * dy
            if dist2 <= (o.radius + threshold) ** 2:
                return o
        return None

    def update(self, dt):

        for obj in self.objects:
            obj.update(dt)


        self.physics.resolve_bounds(self.objects)



    def render(self):

        self.renderer.clear()

        self.renderer.draw_table()


        for obj in self.objects:
            obj.draw(self.screen)


        if self.cue.aiming and self.cue.target_ball:
            self.cue.draw(self.screen)


        self.renderer.draw_hud(self.score)
