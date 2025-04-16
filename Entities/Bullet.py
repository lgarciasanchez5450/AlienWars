from Entities.TimedEntity import *
import math
import ResourceManager

class Bullet(TemporaryEntity):
    dir:glm.vec2
    __slots__ = 'dmg',
    @staticmethod
    def makeDefault(pos:glm.vec2,vel:glm.vec2,rot:float):
        return Bullet(pos,vel,rot,1,ResourceManager.loadColorKey('./Images/Bullets/red.png',(0,0,0)),1,2)
    
    @staticmethod
    def makeDefaultBlue(pos:glm.vec2,vel:glm.vec2,rot:float):
        return Bullet(pos,vel,rot,1,ResourceManager.loadColorKey('./Images/Bullets/blue.png',(0,0,0)),1,2)
    def __init__(self,pos:glm.vec2,vel:glm.vec2,rot:float,mass:float,img:Surface,dmg:int,t:float):
        super().__init__(pos,vel,rot,mass,img,E_CAN_DAMAGE,t)
        self.vel += glm.rotate(glm.vec2(400,0),-rot)
        self.dmg = dmg

    def onCollide(self, other:"Entity",info:CollisionInfo):
        self.dead = True
