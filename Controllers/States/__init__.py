import typing
import utils
from gametypes import *
from Entities.Spaceship import Spaceship
from pyglm import glm
from Attacks import Gun
from math import pi
import physics
from pygame import Rect
from Entities.Bullet import Bullet
if typing.TYPE_CHECKING:
    from Controllers.WarshipController import StateController

class State:
    __counter= 0
    id:int
    def __init_subclass__(cls):
        cls.id = State.__counter
        State.__counter +=1
    def start(self): ...

    def update(self,controller:'StateController',entity:Spaceship,map:MapType,game:GameType): ...

    def think(self,controller:'StateController',entity:Spaceship,map:MapType,game:GameType): ...

    def copy(self):
        return type(self)()
#actions that the warship can take
class Action:
    def isAvailable(self,state:State,entity:Spaceship,game:GameType) -> bool: ...
    def run(self,state:State,entity:Spaceship,map:MapType,game:GameType): ...

class SpawnFighterAction(Action):
    def __init__(self,max_spawns:int):
        self.max_spawns = max_spawns
        self.spawns:list[Spaceship] = []
        print('reseting')
        self.switch = 1
        self.next_time = 0
        self.reload_time = 5

    def isAvailable(self,state:'StateAttack',entity:Spaceship,game:GameType) -> bool:
        if game.time < self.next_time: return False
        if len(self.spawns) < self.max_spawns: return True
        for spawn in self.spawns.copy(): #TODO this function very slow, optimize later
            if spawn.dead:
                self.spawns.remove(spawn)
                return True
        return False
    def run(self, state:'StateAttack',entity: Spaceship, map: MapType, game: GameType):
        assert len(self.spawns) < self.max_spawns
        builder = game.builder
        new = builder.buildEnemy(
            glm.vec2(entity.pos) +  entity.vel * game.dt +glm.rotate(glm.vec2(-80,self.switch*80),-entity.rot),
            glm.vec2(),
            entity.rot + self.switch * -pi/2,entity.alliance,
            **builder.fighter
        )
        ctrler = new.controller
        if typing.TYPE_CHECKING:
            assert type(ctrler) is StateController
        ctrler.setState(StateAttack.id,state.target)
        self.switch = -self.switch
        self.spawns.append(new)
        print(len(self.spawns))
        game.spawnEntity(new)
        self.next_time = game.time + self.reload_time

class ShootAction(Action):
    def __init__(self,gun:Gun):
        self.gun = gun
    def isAvailable(self,entity:Spaceship,game:GameType) -> bool: 
        return self.gun.canFire(game.time)
    def run(self,entity:Spaceship,map:MapType,game:GameType):
        self.gun.fire(game.time)
        pos = entity.pos + entity.vel * game.dt + \
              glm.rotate(self.gun.pos,-entity.rot)
        bullet=Bullet.makeDefault(
            pos,
            glm.vec2(entity.vel),
            entity.rot + self.gun.rot
        )
        game.spawnEntity(bullet)

class StateIdle(State):

    def __init__(self):
        pass
    def start(self): ...

    def think(self,controller:'StateController',entity:Spaceship,map:MapType,game:GameType):
        around = list(physics.get_colliding(entity.rect.inflate(entity.rect.size),map))
        for other in around:
            if other is entity: continue
            if type(other) is Spaceship:
                if other.alliance is not entity.alliance:
                    controller.setState(StateAttack.id,other)


class StateAttack(State):
    
    def start(self,target:EntityType):
        self.target = target
        self.optimal_distance = 300
        self.sight = 900

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

    def think(self,controller:'StateController',entity:Spaceship,map:MapType,game:GameType):
        sqrDst = glm.distance2(self.target.pos,entity.pos)
        if sqrDst > self.sight * self.sight or self.target.dead:
            big_rect = Rect(0,0,self.sight*2,self.sight*2)
            big_rect.center = entity.pos
            for other in physics.get_colliding(big_rect,map):
                if other is entity: continue
                if type(other) is Spaceship:
                    if other.alliance is not entity.alliance:
                        self.start(other)
                        break
            else:
                controller.setState(StateIdle.id)

class StateAttackWithSpawn(StateAttack):
    def __init__(self):
        self.action_spawn_fighter = SpawnFighterAction(4)

    def update(self,controller:'StateController',entity:Spaceship,map:MapType,game:GameType): 
        if self.action_spawn_fighter.isAvailable(self,entity,game):
            print('running action')
            self.action_spawn_fighter.run(self,entity,map,game)
        super().update(controller,entity,map,game)

StateAttackWithSpawn.id = StateAttack.id