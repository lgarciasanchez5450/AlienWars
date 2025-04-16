from Entities.Entity import *
from EntityTags import *

class TemporaryEntity(Entity):
    __slots__ = 't',
    def __init__(self, pos:glm.vec2, vel:glm.vec2, rot:float,mass:float, _surf:Surface,tags:int,t:float):
        super().__init__(pos, vel, rot,mass, _surf,tags)
        self.t = t

    def update(self, map, dt, game):
        self.t -= dt
        if self.t <= 0:
            self.dead = True
        super().update(map, dt, game)
