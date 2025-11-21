import pygame
import math

class Bola:
    """Simple ball class used for demonstration."""

    def __init__(self, x=0, y=0, radius=10, vx=0, vy=0, color=(200, 200, 255), mass=1.0):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.mass = mass

        # store initial state for reset
        self._initial = (x, y, vx, vy)

        # physics tuning
        self._friction_per_second = 0.98  # per-frame-style multiplier baseline
        self._min_stop_speed = 5.0  # px/s under this we snap to zero

    def update(self, dt):
        # Simple Euler integration
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Apply damping to simulate friction (frame-rate independent-ish)
        # Using an exponential decay: multiplier^(dt*60) so tuning is easier
        damping = self._friction_per_second ** (dt * 60.0)
        self.vx *= damping
        self.vy *= damping

        # If speed is very small, stop (snap to 0) to avoid drifting
        speed = math.hypot(self.vx, self.vy)
        if speed < self._min_stop_speed:
            self.vx = 0.0
            self.vy = 0.0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def reset(self):
        x, y, vx, vy = self._initial
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)

    # helper to set velocity (used by cue)
    def set_velocity(self, vx, vy):
        self.vx = float(vx)
        self.vy = float(vy)

    # convenience check if ball is moving
    def is_moving(self):
        return math.hypot(self.vx, self.vy) > 1e-3
