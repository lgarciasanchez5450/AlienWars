import math
import physics
from glm import vec2
from Entities.Entity import Entity
from Entities.TimedEntity import *
from EntityTags import GameType, MapType
import ResourceManager
from ChunkManager import TWO_PI,PI_OVER_TWO,pi
from gametypes import GameType, MapType
from physics import CollisionInfo

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

    def onCollide(self, other:"Entity",info:CollisionInfo,normal:glm.vec2):
        self.dead = True


class Missile(TemporaryEntity):
    __slots__ = 'dmg','max_speed','shooter','target','c_info'
    @staticmethod
    def makeDefault(pos:glm.vec2,vel:glm.vec2,rot:float,target:EntityType,shooter:EntityType|None=None):
        return Missile(pos,vel,rot,3,ResourceManager.loadColorKey('./Images/Bullets/missile_red.png',(0,0,1)),5,5,target,shooter)  
    def __init__(self,pos:glm.vec2,vel:glm.vec2,rot:float,mass:float,img:Surface,dmg:int,t:float,target:EntityType,shooter:EntityType|None):
        super().__init__(pos,vel,rot,mass,img,E_CAN_DAMAGE,t)
        self.cache_every=None
        self.dmg = dmg
        self.max_speed = 0
        self.shooter = shooter
        self.target = target
        self.c_info = None

    def update(self, map, dt, game):
        fdt =0.2
        d = self.target.pos-self.pos
        fd = (self.target.pos + self.target.vel * fdt) - (self.pos+self.vel * fdt)
        t_rot = math.atan2(-fd.y,fd.x)
        d_rot = (t_rot - self.rot) % TWO_PI
        if d_rot > pi:
            d_rot -= TWO_PI
        self.rot += max(-1,min(d_rot,1)) * dt*dt * 2000 / self.mass 
        self.dirty = True
        self.addRelForce(glm.vec2(1,0) * 2000) #type: ignore
        super().update(map,dt,game)

    def onCollide(self, other: Entity, info: CollisionInfo, normal: vec2):
        self.dead = True
        self.c_info = info
        other.vel -= normal*self.dmg 


    def onDeath(self, map: MapType, dt: float, game: GameType):
        if self.c_info:
            explosion_pos = self.c_info.center_of_collision
        else:
            explosion_pos = self.pos
        game.explosion_sfx.play()
        game.spawnEntity(
            Explosion(
                explosion_pos,
                self.vel,
            )
        )

class Explosion(Entity):
    __slots__ = 'animation','fps','frame','t'
    def __init__(self,pos:Vec2,vel:Vec2):
        self.animation = ResourceManager.loadDir('./Images/Explosion',Surface.convert,lambda s:s.set_colorkey((0,0,0)))
        self.fps = 24
        self.t = 0
        self.frame = 0
        super().__init__(pos,vel,0,0,self.animation[0],0)
        self.cache_every = 50
        
    
    def update(self, map: MapType, dt: float, game: GameType):
        self.t += dt * self.fps
        new_frame = int(self.t)
        if new_frame != self.frame:
            if new_frame == len(self.animation):
                self.dead = True
                return
            self.frame = new_frame
            self._surf = self.animation[new_frame]
            self.dirty = True 