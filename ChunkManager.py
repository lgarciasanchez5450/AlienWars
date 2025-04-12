import glm
import typing
import pygame
import math
from math import pi
RAD_TO_DEG = 180 / pi
DEG_TO_RAD = pi / 180

type MapType = dict[tuple[int,int],list['Entity']]
NULL_SURF = pygame.Surface((0,0))
class Entity:
    pos:glm.vec2 # current position 
    vel:glm.vec2 # current velocity
    rot:float
    surf:pygame.Surface # surface to draw each frame
    dirty:bool
    dead:bool = False
    # The Following are for physics
    rect:pygame.Rect # bounding Rect of the surface
    mask:pygame.Mask # mask from surface
    def __init__(self,pos:glm.vec2,rot:float):
        self.pos = pos
        self.rot = rot
        self.vel = glm.vec2()
        self._surf = NULL_SURF
        self.dirty = True
    
    def update(self,map:MapType,dt:float): ...
    
    def regenerate_physics(self):
        self.surf = pygame.transform.rotate(self._surf,self.rot*RAD_TO_DEG)
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
    
    def onCollide(self,other:"Entity"): ...

class Bullet(Entity):
    dir:glm.vec2
    dmg = 1
    def __init__(self,pos:glm.vec2,bvel:glm.vec2,rot:float):
        super().__init__(pos,rot)
        self.dir = glm.vec2(math.cos(rot),math.sin(-rot))
        self._surf = pygame.Surface((10,5))
        self._surf.set_colorkey('black')
        self._surf.fill('red')
        self._surf.set_at((0,0),'black')
        self.t = 5
        self.vel = bvel + self.dir *  200

    
    def regenerate_physics(self):
        super().regenerate_physics()

    def update(self,map:MapType,dt:float):
        self.pos += self.vel * dt
        self.t -= dt
        if self.t < 0: self.dead = True

    def onCollide(self, other):
        if isinstance(other,Spaceship):
            self.dead = True


class Attack:
    reload_time:float
    next_atk_time:float
    bullet_power:float
    def makeBullet(self) -> Bullet: ...

class Spaceship(Entity):
    rot:float
    hp:float
    hp_max:float
    atk_1:Attack
    atk_2:Attack

    def __init__(self,pos,rot,hp,img:pygame.Surface):
        super().__init__(pos,rot)
        self.hp = hp
        self._surf = img

    def onCollide(self, other):
        if isinstance(other,Bullet):
            self.hp -= other.dmg
            if self.hp <= 0:
                self.dead = True

CHUNK_SIZE = 100

def build_map(ships:list[Entity]):
    #first hash everything
    map:MapType = {}
    for ship in ships:
        cpos = glm.ivec2(ship.pos // CHUNK_SIZE).to_tuple()
        if cpos not in map:
            map[cpos] = [ship]
        else:
            map[cpos].append(ship)
    return map
        
    
    

