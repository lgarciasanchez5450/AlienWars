from Entities.Spaceship import Spaceship
from gametypes import *
from Controllers.States.core import *
from ChunkManager import TWO_PI, pi,PI_OVER_TWO
import math

from gametypes import GameType, MapType

class Pursue(BaseAttack):
    __slots__ = 'parent',
    def __init__(self):
        super().__init__()
        self.max_dist_from_parent = 3000
        self.shoot_threshold = 0.9

    def start(self,parent:Spaceship,target:EntityType):
        super().start(target)
        self.parent = parent

    def think(self, controller: 'StateController', entity: Spaceship, map: MapType, game: GameType):
        if self.target.dead:
            controller.setState(Idle())

      
class Idle(State):
    pass
 
class Orbit(State):
    class State:
        GET_CLOSE = 0
        SPINNIN = 1

    __slots__ = 'target','radius','_state'
    def start(self,entity:Spaceship,target:EntityType,radius:float):
        self.target = target
        self.radius = radius

    def update(self, controller: 'StateController', entity: Spaceship, map: MapType, game: GameType):
        fdt = 1
        d = self.target.pos-entity.pos
        fd = self.target.pos - (entity.pos+entity.vel * fdt)
        dist = glm.length(d)
        t_rot = math.atan2(fd.y,-fd.x) - PI_OVER_TWO
        t_rot -= max(-PI_OVER_TWO,min(PI_OVER_TWO,(dist - self.radius)/self.radius))
        d_rot = (t_rot - entity.rot) % TWO_PI
        if d_rot > pi:
            d_rot -= TWO_PI
        movement = glm.vec2(max(0.2,abs(dist-self.radius)*0.001),0)
        if d_rot:
            entity.rot += max(-1,min(d_rot,1)) * game.dt*game.dt * entity.engine_force / entity.mass 
            entity.dirty = True
        entity.move(movement)