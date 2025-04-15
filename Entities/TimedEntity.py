from Entities.Entity import *

class TemporaryEntity(Entity):
    __slots__ = 't',
    def __init__(self, pos:glm.vec2, vel:glm.vec2, rot:float, _surf:Surface,t:float):
        super().__init__(pos, vel, rot, _surf)
        self.t = t

    def update(self, map, dt, game):
        self.t -= dt
        if self.t <= 0:
            self.dead = True
        super().update(map, dt, game)
