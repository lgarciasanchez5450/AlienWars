from Controllers.Controller import Controller
from Entities.Spaceship import Spaceship
from Entities.Bullet import Bullet
from pyglm import glm
from gametypes import *
from ChunkManager import TWO_PI,pi,MAP
import utils


class State:
    def __init__(self,entity:Spaceship): ...

    def think(self,controller:'StateMachineController',entity:Spaceship,map:MapType,game:GameType): ...

    def update(self,controller:'StateMachineController',entity:Spaceship,map:MapType,game:GameType): ...

class StateAttack(State):
    def __init__(self, entity: Spaceship,target:EntityType):
        super().__init__(entity)
        self.target = target

    def think(self,controller:'StateMachineController',entity:Spaceship,map:MapType,game:GameType): 
        if self.target.dead:
            controller.setState(StateWander(entity))
            #check if needs to retreat (low on health)
            #see if there are other enemies nearby (attack)
            #wander
            return
        else:
            t_dist = glm.distance2(self.target.pos,entity.pos)
            if t_dist > 900*900:
                controller.setState(StateWander(entity))

    def update(self, controller: 'StateMachineController', entity: Spaceship, map:MapType, game: GameType):
        dpos = self.target.pos - entity.pos
        dist = glm.length(dpos)
        d_rot = -utils.cross2d(entity.dir,dpos) / dist # type: ignore
        if abs(d_rot) > 0.05:
            entity.rot += max(-1,min(d_rot,1)) * game.dt * game.dt * entity.engine_force/ entity.mass
            entity.dirty = True
        if entity.guns:
            gun = entity.guns[0]
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

        entity.move(glm.vec2(.1,0)*(glm.length(dpos)-200) * 1000 / entity.engine_force) 

class StateWander(State):
    __slots__  = 'target',
    def __init__(self, entity: Spaceship):
        super().__init__(entity)

    def makeTarget(self,around:glm.vec2):
        t = glm.vec2(-1,-1)
        while not MAP.collidepoint(t):
            t = glm.circularRand(glm.linearRand(1000,10000)) + around
        return t
    
    def think(self,controller:'StateMachineController',entity:Spaceship,map:MapType,game:GameType): 
        if not hasattr(self,'target'):
            self.target = self.makeTarget(entity.pos)
        elif glm.distance(self.target,entity.pos) < 100:
            self.target = self.makeTarget(entity.pos)

    def update(self, controller: 'StateMachineController', entity: Spaceship, map:MapType, game: GameType):
        dpos = self.target - entity.pos
        trot = glm.atan(-dpos.y,dpos.x)
        d_rot = (trot - entity.rot) % TWO_PI
        if d_rot > pi:
            d_rot -= TWO_PI
        if abs(d_rot) > 0.1:
            entity.rot += max(-1,min(d_rot,1))  * game.dt
            entity.dirty = True
        m = -abs(d_rot) + pi/2
        entity.move(glm.vec2(.4,0) * m*  1000 / entity.engine_force) 

class StateMachineController(Controller):
    counter = 0
    __slots__ = 'state','next_state','uid'
    def init(self,entity:Spaceship):
        self.uid = StateMachineController.counter
        StateMachineController.counter += 1

        self.next_state = None
        if not hasattr(self,'state'):
            self.setState(StateWander(entity))

    def update(self,entity:Spaceship,map:MapType,game:GameType):
        if game.frame % 100 == self.uid % 100:
            self.state.think(self,entity,map,game)
        if self.next_state:
            self.state = self.next_state
            self.state.think(self,entity,map,game)
            self.next_state = None
        else:
            self.state.update(self,entity,map,game)

    def onCollide(self, entity: Spaceship, other: EntityType, collision_normal: Vec2):
        if type(self.state) is not StateAttack:
            if type(other) is Bullet:
                if other.shooter:
                    return self.setState(StateAttack(entity,other.shooter))    
            else:
                self.setState(StateAttack(entity,other))

    def setState(self,state:State):
        self.next_state = state

    def copy(self):
        return type(self)()
