class ObjekGame:
    """Base class that other in-game objects can inherit from."""

    def update(self, dt):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError