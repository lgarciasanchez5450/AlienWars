from Entities.Entity import *
from EntityTags import *
from EntityTags import ICanDamage

class Spaceship(Entity):
    type = 'Spaceship'
    hp:float
    hp_max:float
    atk_1:AttackType|None
    atk_2:AttackType|None
    controller:ControllerType
    __slots__ = 'hp','hp_max','alliance','atk_1','atk_2','controller'
    def __init__(self, pos:glm.vec2, vel:glm.vec2, rot:float,mass:float, _surf:Surface,tags:int,hp:int,alliance:str,controller:ControllerType):
        super().__init__(pos, vel, rot,mass, _surf,tags)
        self.hp = hp
        self.hp_max = hp
        self.alliance = alliance
        self.atk_1 = None
        self.atk_2 = None
        self.controller = controller
        self.controller.init(self)

    def update(self, map, dt, game):
        self.controller.update(self,map,game)
        super().update(map, dt, game)

    def onCollide(self, other:Entity):
        if other.tags & E_CAN_DAMAGE:
            assert isinstance(other,ICanDamage)
            self.hp -= other.dmg
            if self.hp <= 0:
                self.dead = True