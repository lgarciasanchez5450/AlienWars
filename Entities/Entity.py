from pyglm import glm
from pygame import Surface
from pygame import Mask
from pygame import Rect

from pygame import transform
from pygame import mask


from gametypes import *



class Entity:
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
    __slots__ = 'type','pos','vel','n_vel','rot','mass','surf','_surf','dirty','dead','rect','mask','tags'
    def __init__(self,pos:glm.vec2,vel:glm.vec2,rot:float,mass:float,_surf:Surface,tags:int):
        self.pos = pos
        self.n_vel = self.vel = vel
        self.rot = rot
        self.mass = mass
        self._surf = _surf
        self.dirty = True
        self.dead = False
        self.tags = tags
    
    def update(self,map:MapType,dt:float,game:GameType):
        self.vel = self.n_vel
        self.pos += self.vel * dt
        self.rect.center = self.pos
    
    def regenerate_physics(self):
        self.surf = transform.rotate(self._surf,self.rot*(180/3.141592653589793)) #Convert Radians to Degrees
        self.mask = mask.from_surface(self.surf)
        self.rect = self.surf.get_rect()
        self.rect.center = self.pos
    
    def onCollide(self,other:"Entity"): ...


class EntityCachedPhysics(Entity):
    _global_physics_cache:dict[tuple[Surface,int],tuple[Surface,Mask]] = {}

    def regenerate_physics(self):
        degrees = self.rot*(180/3.141592653589793)
        rot_hash = int(degrees) % 360
        cache = EntityCachedPhysics._global_physics_cache
        key = (self._surf,rot_hash)
        if key not in cache:
            surf = transform.rotate(self._surf,degrees)
            mask_ = mask.from_surface(surf)
            if len(cache) < 1000:
                cache[key] = surf,mask_
        else:
            surf,mask_ = cache[key]
        self.surf = surf
        self.mask = mask_
        self.rect = self.surf.get_rect()
        self.rect.center = self.pos
