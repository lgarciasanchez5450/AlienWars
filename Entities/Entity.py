from pyglm import glm
from pygame import Surface
from pygame import Mask
from pygame import Rect

from pygame import transform
from pygame import mask
from EntityTags import *

from physics import CollisionInfo


from gametypes import *

class Entity:
    _global_physics_cache:dict[tuple[Surface,int],tuple[Surface,Mask]] = {}

    pos:glm.vec2 # current position 
    vel:glm.vec2 # current velocity
    n_vel:glm.vec2 # next_velocity 
    mass:float
    rot:float
    surf:Surface # surface to draw each frame
    dirty:bool
    # The Following are for physics
    rect:Rect # bounding Rect of the surface
    mask:Mask # mask from surface
    tags:int

    __slots__ = 'pos','vel','n_vel','rot','dir','mass','surf','_surf','dirty','dead','rect','mask','tags','force','cache_every'


    def __init__(self,pos:glm.vec2,vel:glm.vec2,rot:float,mass:float,_surf:Surface,tags:int):
        self.cache_every = 0
        self.pos = pos
        self.n_vel = self.vel = vel
        self.rot = rot
        self.dir:Vec2 = glm.rotate(glm.vec2(1,0),-rot) #type: ignore
        self.mass = mass
        self._surf = _surf
        self.tags = tags
        self.force = glm.vec2()
        self.dirty = True
        self.dead = False
    
    def update(self,map:MapType,dt:float,game:GameType):
        self.vel = self.n_vel
        self.vel += glm.rotate(self.force,-self.rot) * (dt / self.mass)
        self.force *= 0 #clear force
        self.pos += self.vel * dt
        
        self.rect.center = self.pos
    
    def regenerate_physics(self):
        if not self.cache_every:
            self.surf = transform.rotate(self._surf,self.rot*(180/3.141592653589793)) #Convert Radians to Degrees
            self.mask = mask.from_surface(self.surf,0)
        else:
            degrees = self.rot*(180/3.141592653589793)
            rot_hash = int(degrees) % 360 // self.cache_every
            cache = Entity._global_physics_cache
            key = (self._surf,rot_hash)
            if key not in cache:
                surf = transform.rotate(self._surf,degrees)
                mask_ = mask.from_surface(surf,0)
                if len(cache) < 1000:
                    cache[key] = surf,mask_
            else:
                surf,mask_ = cache[key]
            self.surf = surf
            self.mask = mask_
        self.rect = self.surf.get_rect()
        self.dir = glm.rotate(glm.vec2(1,0),-self.rot) #type: ignore
        self.rect.center = self.pos

    
    def onCollide(self,other:"Entity",info:CollisionInfo,normal:glm.vec2):
        if other.tags & self.tags & E_CAN_BOUNCE:
            rel_vel = self.vel - other.vel
            d = glm.vec2(normal)
            dot = glm.dot(d,rel_vel)
            if dot < 0:
                d *= dot * 2/glm.length2(d) #type: ignore
                self.n_vel = self.vel -  d * (other.mass / (self.mass+other.mass))
            else:
                self.n_vel += d * 0.01 * (other.mass / (self.mass+other.mass))
 
    def addRelForce(self,force:glm.vec2):
        self.force += force
