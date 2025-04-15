from Entities.TimedEntity import *
import math

class Bullet(TemporaryEntity):
    type = 'Bullet'
    dir:glm.vec2
    dmg = 1
    __slots__ = 'dir',
    def __init__(self,pos:glm.vec2,vel:glm.vec2,rot:float):
        s = Surface((10,5))
        s.set_colorkey('black')
        s.fill('red')
        s.set_at((0,0),'black')
        self.dir = glm.vec2(math.cos(rot),math.sin(-rot))
        super().__init__(pos,vel,rot,s,5)
        self.vel += self.dir * 300

    def onCollide(self, other:"Entity"):
        self.dead = True
