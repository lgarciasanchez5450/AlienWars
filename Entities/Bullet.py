from Entities.TimedEntity import *
import math
import ResourceManager

class Bullet(TemporaryEntity):
    dir:glm.vec2
    __slots__ = 'dmg','shooter'
    @staticmethod
    def makeDefault(pos:glm.vec2,vel:glm.vec2,rot:float,shooter:EntityType|None=None):
        return Bullet(pos,vel,rot,1,ResourceManager.loadColorKey('./Images/Bullets/red.png',(0,0,0)),1,2,shooter)
    
    @staticmethod
    def makeDefaultBlue(pos:glm.vec2,vel:glm.vec2,rot:float,shooter:EntityType|None=None):
        return Bullet(pos,vel,rot,1,ResourceManager.loadColorKey('./Images/Bullets/blue.png',(0,0,0)),1,2,shooter)
        
    def __init__(self,pos:glm.vec2,vel:glm.vec2,rot:float,mass:float,img:Surface,dmg:int,t:float,shooter:EntityType|None):
        super().__init__(pos,vel,rot,mass,img,E_CAN_DAMAGE,t)
        self.vel += glm.rotate(glm.vec2(400,0),-rot)
        self.dmg = dmg
        self.shooter = shooter

    def regenerate_physics(self):
        return super().regenerate_physics()
    def update(self, map, dt, game):
        return super().update(map, dt, game)

    def onCollide(self, other:"Entity",info:CollisionInfo,normal:glm.vec2):
        self.dead = True
