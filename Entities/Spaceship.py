from Entities.Entity import *
from EntityTags import *
from utils import expDecay
from Attacks import Gun
if __debug__:
    from EntityTags import ICanDamage

class Spaceship(Entity):
    hp:float
    hp_max:float
    controller:ControllerType
    __slots__ = 'hp','hp_max','alliance','guns','controller','engine_force'
    def __init__(self, pos:glm.vec2, vel:glm.vec2, rot:float,mass:float, _surf:Surface,tags:int,hp:int,alliance:str,guns:list[Gun],engine_force:float,controller:ControllerType):
        super().__init__(pos, vel, rot,mass, _surf,tags)
        self.hp = hp
        self.hp_max = hp
        self.alliance = alliance
        self.guns = guns
        self.engine_force = engine_force
        self.controller = controller
        self.controller.init(self)

    def move(self,dir:glm.vec2):
        if dir.x < -1: dir.x = -1
        elif dir.x > 1: dir.x = 1
        if dir.y < -1: dir.y = -1
        elif dir.y > 1: dir.y = 1
        if dir.x < 0:
            dir.x *= 0.1
        dir.y *= 0.1
        self.force += dir * self.engine_force

    

    def update(self, map, dt, game):
        self.controller.update(self,map,game)
        super().update(map, dt, game)
        self.vel *= glm.exp(-dt) #equivalent to vel = expDecay(vel,0,1,dt), inlined for speedup

    def onCollide(self, other:Entity,info:CollisionInfo,normal:glm.vec2):
        self.controller.onCollide(self,other,info,normal)
        if other.tags & E_CAN_DAMAGE:
            assert isinstance(other,ICanDamage)
            self.hp -= other.dmg
            if self.hp <= 0:
                self.dead = True
        super().onCollide(other,info,normal)
