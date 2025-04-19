from pyglm import glm
from Controllers.States.core import *
from ChunkManager import MAP,TWO_PI,pi


class Attack(BaseAttack):
    __slots__ = 'target',

    def think(self,controller:'StateController[None]',entity:Spaceship,map:MapType,game:GameType): 
        if self.target.dead:
            controller.setState(Wander(),entity.pos)
            #check if needs to retreat (low on health)
            #see if there are other enemies nearby (attack)
            #wander
            return
        else:
            t_dist = glm.distance2(self.target.pos,entity.pos)
            if t_dist > 900*900:
                controller.setState(Wander(),entity.pos)

    def copy(self):
        return type(self)()
    
class Wander(State):
    __slots__  = 'target',
    def start(self,target:glm.vec2):
        self.target = glm.vec2(target)

    def makeTarget(self,around:glm.vec2):
        t = glm.vec2(-1,-1)
        while not MAP.collidepoint(t):
            t = glm.circularRand(glm.linearRand(1000,10000)) + around
        return t
    
    def think(self,controller:'StateController[None]',entity:Spaceship,map:MapType,game:GameType): 
        if not hasattr(self,'target'):
            self.target = self.makeTarget(entity.pos)
        elif glm.distance(self.target,entity.pos) < 100:
            self.target = self.makeTarget(entity.pos)
        else:
            self.target = entity.pos

    def update(self, controller: 'StateController[None]', entity: Spaceship, map:MapType, game: GameType):
        dpos = self.target - entity.pos
        trot = glm.atan(-dpos.y,dpos.x)
        d_rot = (trot - entity.rot) % TWO_PI
        if d_rot > pi:
            d_rot -= TWO_PI
        if abs(d_rot) > 0.1:
            entity.rot += max(-1,min(d_rot,1))  * game.dt
            entity.dirty = True
        m = -abs(d_rot) + pi/2
        entity.move(glm.vec2(.4,0) * m *  1000 / entity.engine_force) 