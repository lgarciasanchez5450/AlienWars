import utils
import typing
from pyglm import glm
from gametypes import *
from Entities.Bullet import Bullet
from Entities.Spaceship import Spaceship
from physics import CollisionInfo

if typing.TYPE_CHECKING:
    from Controllers.StateController import StateController


class State:
    def __init_subclass__(cls): pass
    def start(self): ...

    def update(self,controller:'StateController',entity:Spaceship,map:MapType,game:GameType): ...

    def think(self,controller:'StateController',entity:Spaceship,map:MapType,game:GameType): ...

    def onCollide(self,controller:'StateController',entity:'Spaceship',other:EntityType,collision:CollisionInfo,normal:Vec2): ...

    def copy(self):
        return type(self)()


class BaseAttack(State):
    __slots__ = 'target','optimal_distance','sight'
    def __init__(self):
        self.optimal_distance = 300
        self.sight = 900
        
    def start(self,target:EntityType):
        self.target = target

    def update(self,controller:'StateController',entity:Spaceship,map:MapType,game:GameType): 
        if self.target.dead:
            return self.think(controller,entity,map,game)
        dpos = self.target.pos - entity.pos
        dist = glm.length(dpos)
        d_rot = -utils.cross2d(entity.dir,dpos) / dist # type: ignore
        dot = glm.dot(entity.dir,dpos) / dist
        if abs(d_rot) > 0.05:
            entity.rot += max(-1,min(d_rot,1)) * game.dt*game.dt * entity.engine_force / entity.mass 
            entity.dirty = True
        if dot > 0.8:
            for gun in entity.guns:
                if gun.tryFire(game.time):
                    pos = entity.pos + entity.vel * game.dt + \
                        glm.rotate(gun.pos,-entity.rot)
                    bullet=Bullet.makeDefault(
                        pos,
                        glm.vec2(entity.vel),
                        entity.rot + gun.rot,
                        entity
                    )
                    game.spawnEntity(bullet)

        entity.move(glm.vec2(.1,0)*(dist-self.optimal_distance)) 
