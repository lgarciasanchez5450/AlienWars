from gametypes import EntityType
import utils
import physics
from math import pi
from pyglm import glm
from pygame import Rect
from Attacks import Gun
from Entities.Bullet import Bullet,Missile
from EntityTags import *

from Controllers.States import WarshipFighterState
from Controllers.States.core import *

class SharedState:
    def __init__(self):
        self.max_spawns = 20
        self.spawns:list[Spaceship] = []
        self.anger_levels:dict[EntityType,int] = {}

    def copy(self):
        new = type(self)()
        new.spawns = self.spawns.copy()
        return new
#actions that the warship can take

class SpawnFighterAction:
    def __init__(self):
        self.switch = 1
        self.next_time = 0
        self.reload_time = 5

    def isAvailable(self,shared_state:SharedState,game:GameType) -> bool:
        if game.time < self.next_time: return False
        if len(shared_state.spawns) < shared_state.max_spawns: return True
        for i,spawn in enumerate(shared_state.spawns):
            if spawn.dead:
                break
        else:
            return False
        shared_state.spawns.pop(i)
        return True
    
    def run(self,controller:'StateController[SharedState]', entity: Spaceship, map: MapType, game: GameType):
        builder = game.builder
        new = builder.buildEnemy(
            glm.vec2(entity.pos) +  entity.vel * game.dt +glm.rotate(glm.vec2(-80,self.switch*80),-entity.rot),
            glm.vec2(),
            entity.rot + self.switch * -pi/2,entity.alliance,
            **builder.fighter
        )

        self.switch = -self.switch
        controller.shared_state.spawns.append(new)
        game.spawnEntity(new)
        self.next_time = game.time + self.reload_time
        return new

class Idle(State):
    def __init__(self):
        self.action_spawn_fighter = SpawnFighterAction()

    def think(self,controller:'StateController[SharedState]',entity:Spaceship,map:MapType,game:GameType):
        around = list(physics.get_colliding(entity.rect.inflate(entity.rect.size),map))
        for other in around:    
            if other is entity: continue
            if type(other) is Spaceship:
                if other.alliance is not entity.alliance:
                    controller.shared_state.anger_levels[other] = 3
                    controller.setState(Attack(),controller,entity,other)
            
    def onCollide(self,controller:'StateController[SharedState]',entity:'Spaceship',other,collision:CollisionInfo,normal:Vec2):
        if other.tags & E_CAN_DAMAGE:
            assert isinstance(other,ICanDamage)
            if other.dmg >= 5:
                shooter = other.shooter
                anger_levels = controller.shared_state.anger_levels
                if shooter in anger_levels:
                    anger_levels[shooter] += other.dmg
                else:
                    anger_levels[shooter] = other.dmg
                if anger_levels[shooter] > 10:
                    controller.setState(Attack(),controller,entity,shooter)
    
    def update(self,controller:'StateController[SharedState]',entity:'Spaceship',map:MapType,game:GameType):
        if self.action_spawn_fighter.isAvailable(controller.shared_state,game):
            new = self.action_spawn_fighter.run(controller,entity,map,game)
            new.controller.setState(WarshipFighterState.Orbit(),new,entity,200) #type: ignore

class Attack(BaseAttack):
    __slots__ = 'action_spawn_fighter',
    def __init__(self):
        super().__init__()
        self.action_spawn_fighter = SpawnFighterAction()

    def start(self,controller:'StateController[SharedState]',entity:Spaceship, target: EntityType):
        super().start(target)
        s_state = controller.shared_state
        angers = s_state.anger_levels.copy()
        if angers:
            for ship in s_state.spawns:
                if typing.TYPE_CHECKING and __debug__:
                    assert isinstance(ship.controller,StateController)
                state = ship.controller.state#type: ignore
                if type(state) is WarshipFighterState.Orbit: 
                    max_anger = max(angers.keys(),key=angers.__getitem__)
                    if angers[max_anger] > 0:
                        angers[max_anger] -= 1
                        ship.controller.setState(WarshipFighterState.Pursue(),entity,max_anger) #type: ignore    
                

    def think(self, controller: 'StateController[SharedState]', entity: Spaceship, map: MapType, game: GameType):
        #define the circumstances when the warship should go out of Attack State
        if self.target.dead:
            around = list(physics.get_colliding(entity.rect.inflate(entity.rect.size),map))
            for other in around:
                if other is entity: continue
                if type(other) is Spaceship:
                    if other.alliance is not entity.alliance:
                        self.start(controller,entity,other)
        #manage the anger levels
        s_state = controller.shared_state
        anger = s_state.anger_levels
        for key in list(anger.keys()):
            if key.dead:
                del anger[key]
            else:
                sqrDst = glm.distance2(key.pos,entity.pos)
                if sqrDst > self.sight * self.sight:
                    if anger[key] <= controller.think_dt//2:
                        del anger[key]
                    else:
                        anger[key] -= controller.think_dt//2

        if not anger:
            #the warship isnt angry at anything -> Go back to idle
            controller.setState(Idle())
            #make every current ship go back to orbit
            for spawn in s_state.spawns:
                spawn_state = spawn.controller.state #type: ignore
                if type(spawn_state) is not WarshipFighterState.Orbit:
                    spawn.controller.setState(WarshipFighterState.Orbit(),spawn,entity,200) #type: ignore

    def update(self,controller:'StateController[SharedState]',entity:Spaceship,map:MapType,game:GameType): 
        if self.action_spawn_fighter.isAvailable(controller.shared_state,game):
            #determine what action
            new = self.action_spawn_fighter.run(controller,entity,map,game)
            if typing.TYPE_CHECKING and __debug__:
                assert isinstance(new.controller,StateController)
            s_state = controller.shared_state
            angers = s_state.anger_levels.copy()
            for ship in s_state.spawns:
                if typing.TYPE_CHECKING and __debug__:
                    assert isinstance(ship.controller,StateController)
                state = ship.controller.state#type: ignore
                if type(state) is WarshipFighterState.Pursue: 
                    if state.target in angers:
                        angers[state.target] -= 1
            max_anger_ship = max(angers.keys(),key=angers.__getitem__)
            
            if angers[max_anger_ship] > 0: 
                new.controller.setState(WarshipFighterState.Pursue(),entity,max_anger_ship) #type: ignore    
            else:
                new.controller.setState(WarshipFighterState.Orbit(),new,entity,200) #type: ignore

        if self.target.dead:
            return self.think(controller,entity,map,game)
        dpos = self.target.pos - entity.pos
        dist = glm.length(dpos)
        d_rot = -utils.cross2d(entity.dir,dpos) / dist # type: ignore
        dot = glm.dot(entity.dir,dpos) / dist
        if abs(d_rot) > 0.05:
            entity.rot += max(-1,min(d_rot,1)) * game.dt*game.dt * entity.engine_force / entity.mass 
            entity.dirty = True
        if dot > self.shoot_threshold:
            for gun in entity.guns:
                if gun.tryFire(game.time):
                    pos = entity.pos + entity.vel * game.dt + \
                        glm.rotate(gun.pos,-entity.rot)
                    bullet=Missile.makeDefault(
                        pos,
                        glm.vec2(entity.vel),
                        entity.rot + gun.rot,
                        self.target,
                        entity
                    )
                    game.spawnEntity(bullet)

        entity.move(glm.vec2(.1,0)*(dist-self.optimal_distance)) 

    def onCollide(self, controller: 'StateController[SharedState]', entity: Spaceship, other: EntityType, collision: CollisionInfo, normal: Vec2):
        s_state = controller.shared_state
        if type(other) is Spaceship:
            if other.alliance is entity.alliance: return

        if other not in s_state.anger_levels:
            s_state.anger_levels[other] = 1
        else:
            s_state.anger_levels[other] += 1