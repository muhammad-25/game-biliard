import math


class Physics:
    """
    Minimal physics helper: currently only implements bounds collision with simple elastic reflection.
    """

    def __init__(self, screen_size):
        self.width, self.height = screen_size

        self.margin = 40

    def resolve_bounds(self, objects):
        left = self.margin
        right = self.width - self.margin
        top = self.margin
        bottom = self.height - self.margin

        for o in objects:
            if not hasattr(o, "x"):
                continue


            if o.x - o.radius < left:
                o.x = left + o.radius
                o.vx = -o.vx
            if o.x + o.radius > right:
                o.x = right - o.radius
                o.vx = -o.vx
            if o.y - o.radius < top:
                o.y = top + o.radius
                o.vy = -o.vy
            if o.y + o.radius > bottom:
                o.y = bottom - o.radius
                o.vy = -o.vy
